import os
import pandas as pd
import numpy as np
import xarray as xr
from ppgnss import gnss_utils, gnss_geodesy

def load_coord(filename):
    data = pd.read_csv(filename, names=["name", "num", "x", "y", "z"], header=0, index_col="name")
    return data

def read_ppp_iono(iono_fn, elev_fn):
    # 1. 读取STEC数据
    df_iono = pd.read_csv(iono_fn, header=None, comment="$", sep="\s+")
    df_iono[df_iono==0.0] = np.nan
    df_iono[df_iono==100.0] = np.nan
    
    datetime_series = pd.to_datetime(
        df_iono.iloc[:, 0].astype(str) + ' ' + df_iono.iloc[:, 1].astype(str)
    )
    valid_columns = df_iono.iloc[:, 2::2]  # 直接间隔切片选取
    rms_columns = df_iono.iloc[:, 3::2]  # 直接间隔切片选取
    satellites = [f"G{i:02d}" for i in range(1, 33)]
    # print(valid_columns.shape)
    df_iono_new = pd.DataFrame(
        data=valid_columns.values,  # 数据值
        index=datetime_series,      # 时间索引
        columns=satellites  # 自定义列名（可选）
    )
    
    df_iono_rms = pd.DataFrame(
        data=rms_columns.values,  # 数据值
        index=datetime_series,      # 时间索引
        columns=satellites  # 自定义列名（可选）
    )
    valid_mask =df_iono_rms > 0.2

    df_iono_new[(df_iono_new==0.0) | valid_mask] = np.nan
    time_start = pd.to_datetime(str(df_iono.iloc[0, 0]))
    time_index = pd.date_range(start=time_start, periods=2880, freq='30s')
    df_iono_new.reindex(time_index)
    
    # 2. 读取高度角
    df_azel = pd.read_csv(elev_fn, header=None, comment="$", sep="\s+")
    datetime_series = pd.to_datetime(
        df_azel.iloc[:, 0].astype(str) + ' ' + df_azel.iloc[:, 1].astype(str)
    )
    params = ['azi', 'ele']
    fields = [f"{_1}_{_2}" for _1 in satellites for _2 in params]
    # print(fields)
    
    df_azel[df_azel==0.] = np.nan
    df_azel[df_azel==100.] = np.nan
    df_azel_new = pd.DataFrame(
        data=df_azel.iloc[:, 2:].values,  # 数据值
        index=datetime_series,  # 时间索引
        columns=fields  # 自定义列名（可选）
    )
    df_azel_new.reindex(time_index)
    df = df_iono_new.join(df_azel_new)
    return df

def df2xr(df):
    # 首先提取三种不同类型的数据列

    # STEC 数据 (G01 到 G32)
    stec_cols = [f'G{i:02d}' for i in range(1, 33)]  # ['G01', 'G02', ..., 'G32']
    stec_df = df[stec_cols].copy()

    # 高度角数据 (G01_ele 到 G32_ele)
    elev_cols = [f'G{i:02d}_ele' for i in range(1, 33)]
    elev_df = df[elev_cols].copy()

    # 方位角数据 (G01_azi 到 G32_azi)
    azim_cols = [f'G{i:02d}_azi' for i in range(1, 33)]
    azim_df = df[azim_cols].copy()

    # 重命名高度角列名，去除后缀
    elev_df.columns = [col.replace('_ele', '') for col in elev_df.columns]
    azim_df.columns = [col.replace('_azi', '') for col in azim_df.columns]

    # 准备多维数据数组
    # 维度顺序: time × satellite × parameter

    # 参数名称列表
    parameters = ['stec', 'elevation', 'azimuth']

    # 创建三维数组 (时间点数 × 卫星数 × 参数数)
    data = np.zeros((len(df), len(stec_cols), len(parameters)))

    # 填充数据
    for i, sat in enumerate(stec_cols):
        # stec 值
        data[:, i, 0] = stec_df[sat].values
        # 高度角
        data[:, i, 1] = elev_df[sat].values
        # 方位角
        data[:, i, 2] = azim_df[sat].values

    # 创建 xarray DataArray
    da = xr.DataArray(
        data,
        dims=['time', 'satellite', 'parameter'],
        coords={
            'time': df.index,  # 时间索引
            'satellite': stec_cols,  # 卫星编号列表
            'parameter': parameters  # 参数列表
        },
        name='gnss_observations'
    )

    # 添加属性元数据
    da.attrs = {
        'description': 'GNSS卫星观测数据',
        'units': {
            'stec': 'TECU',
            'elevation': 'degrees',
            'azimuth': 'degrees'
        }
    }
    return da


def ionippblhAzel(rcv_lat, rcv_lon, rcv_alt, azimuth, elevation):
    RE_WGS84 = 6378.137
    H_ion = 450
    # 将方位角和高度角转换为弧度
    azimuth_rad = np.radians(azimuth)
    elevation_rad = np.radians(elevation)

    # 计算地球半径和电离层高度的比值
    re_hion_ratio = RE_WGS84 / (RE_WGS84 + H_ion)

    # 计算rp: 投影比例系数
    rp = re_hion_ratio * np.cos(elevation_rad)

    # 计算ap: 穿刺点的天顶角
    ap = np.pi / 2.0 - elevation_rad - np.arcsin(rp)

    # 计算sin(ap) 和 tan(ap)
    sinap = np.sin(ap)
    tanap = np.tan(ap)

    # 计算穿刺点位置的纬度
    cos_azimuth = np.cos(azimuth_rad)
    # rcv_lat, rcv_lon, rcv_alt = ecef2geo(*rcv_pos)  # 假设 rcv_pos 是ECEF坐标，转换为地理坐标
    rcv_lat_rad = np.radians(rcv_lat)

    ipp_lat_rad = np.arcsin(np.sin(rcv_lat_rad) * np.cos(ap) + np.cos(rcv_lat_rad) * sinap * cos_azimuth)

    # 计算穿刺点的经度
    if (rcv_lat > 70.0 and tanap * cos_azimuth > np.tan(np.pi / 2.0 - rcv_lat_rad)) or \
            (rcv_lat < -70.0 and -tanap * cos_azimuth > np.tan(np.pi / 2.0 + rcv_lat_rad)):
        ipp_lon_rad = np.radians(rcv_lon) + np.pi - np.arcsin(sinap * np.sin(azimuth_rad) / np.cos(ipp_lat_rad))
    else:
        ipp_lon_rad = np.radians(rcv_lon) + np.arcsin(sinap * np.sin(azimuth_rad) / np.cos(ipp_lat_rad))

    # 将穿刺点的纬度和经度转换为度
    ipp_lat = np.degrees(ipp_lat_rad)
    ipp_lon = np.degrees(ipp_lon_rad)

    # 穿刺点的高度就是电离层高度
    ipp_alt = H_ion

    # 计算投影函数 mf
    mf = 1.0 / np.sqrt(1.0 - rp * rp)
    return ipp_lat, ipp_lon, ipp_alt, mf



def calculate_ipp_vectorized(stn_lon, stn_lat, stn_alt, az, el, H=450):
    """
    向量化计算电离层穿刺点(IPP)坐标
    
    参数:
    stn_lon: 测站经度(度)
    stn_lat: 测站纬度(度)
    stn_alt: 测站海拔高度(米)
    az: 方位角数组(度)
    el: 高度角数组(度)
    H: 电离层高度(km)
    
    返回:
    lons, lats: 穿刺点经纬度数组(度)
    """
    # 地球半径常数 (km)
    a = 6378.137  # WGS84地球赤道半径
    
    # 转换为弧度
    lat_r = np.deg2rad(stn_lat)
    lon_r = np.deg2rad(stn_lon)
    az_r = np.deg2rad(az)
    el_r = np.deg2rad(el)
    
    # 站点海拔转换为km
    h = stn_alt / 1000
    
    # 1. 计算测站位置的地球半径
    # 考虑地球扁率 (WGS84椭球模型)
    f = 1/298.257223563  # 扁率
    R = a * (1 - f * np.sin(lat_r)**2) ** 0.5
    
    # 2. 计算地球中心角(ψ)
    # 注意: 对高度角很小的卫星进行限制处理
    cos_el = np.cos(el_r)
    # 避免负数和零除
    cos_el = np.where(cos_el <= 0, 1e-10, cos_el)
    
    sin_psi = (R + h) / (R + H) * cos_el
    # 确保sin值在[-1,1]范围内
    sin_psi = np.clip(sin_psi, -1.0, 1.0)
    
    psi = (np.pi/2) - el_r - np.arcsin(sin_psi)
    
    # 3. 计算穿刺点纬度
    sin_phi_ip = (
        np.sin(lat_r) * np.cos(psi) + 
        np.cos(lat_r) * np.sin(psi) * np.cos(az_r)
    )
    sin_phi_ip = np.clip(sin_phi_ip, -1.0, 1.0)
    phi_ip = np.arcsin(sin_phi_ip)
    
    # 4. 计算穿刺点经度
    cos_delta_lon = (np.cos(psi) - np.sin(lat_r)*np.sin(phi_ip)) / (
        np.cos(lat_r) * np.cos(phi_ip)
    )
    cos_delta_lon = np.clip(cos_delta_lon, -1.0, 1.0)
    delta_lon = np.arccos(cos_delta_lon)
    # 根据方位角确定经度方向
    sign = np.sign(np.sin(az_r))
    sign = np.where(sign == 0, 1, sign)  # 处理边界情况
    
    lambda_ip = lon_r + sign * delta_lon
    
    # 转换为度
    ipp_lat = np.rad2deg(phi_ip)
    ipp_lon = np.rad2deg(lambda_ip)
    
    # 规范化经度到[-180,180]范围
    ipp_lon = np.where(ipp_lon > 180, ipp_lon - 360, ipp_lon)
    ipp_lon = np.where(ipp_lon < -180, ipp_lon + 360, ipp_lon)
    
    return ipp_lon, ipp_lat

def xr_stec2ipp(xr_stec, stn_lat, stn_lon, stn_alt):
    """
    根据卫星高度角、方位角、STEC计算穿刺点经纬度、投影函数
    """
    # 电离层高度设定为450km
    iono_height = 450  # 单位: km

    # 1. 提取方位角和高度角数据
    stecs = xr_stec.sel(parameter="stec").values
    azimuths = xr_stec.sel(parameter='azimuth').values  # 形状: (time, satellite)
    elevations = xr_stec.sel(parameter='elevation').values  # 形状: (time, satellite)
    # 3. 向量化计算所有IPP
    ipp_lats, ipp_lons, ipp_alts, mfs = ionippblhAzel(
        stn_lat, stn_lon, stn_alt, azimuths, elevations)
    mask = np.isnan(mfs)
    # print(mfs[~mask])
    # 4. 创建XArray数据结构
    # 创建包含经纬度的DataArray
    xr_ipp = xr.DataArray(
        np.stack([stecs, azimuths, elevations, ipp_lons, ipp_lats, mfs], axis=-1),  # 组合经纬度为最后一维
        dims=['time', 'satellite', 'data'],
        coords={
            'time': xr_stec.time,
            'satellite': xr_stec.satellite,
            'data': ["stec", "azi", "ele", 'lon', 'lat', "mf"]
        },
        name='ipp stec'
    )
    
    return xr_ipp
    

def show_stec(da, fig_fn):
    # 方法1: 使用时间切片 (推荐)
    start_time = da.time[0].values  # 获取第一个时间点
    end_time = start_time + np.timedelta64(30, 'm')  # 30分钟后
    # da = da.sel(time=slice(start_time, end_time))
    
    import matplotlib.pyplot as plt
    lons = da.sel(data="lon").values.flatten()
    lats = da.sel(data="lat").values.flatten()
    mfs = da.sel(data="mf").values.flatten()
    v = da.sel(data="stec").values.flatten()
    # eles = da.sel(data="ele").values.flatten()
    plt.scatter(lons, lats, s=1,c=v/mfs)
    os.makedirs(os.path.dirname(fig_fn), exist_ok=True)
    plt.savefig(fig_fn)
    plt.close()





if __name__ == "__main__":
    year = 2024
    doy = 285
    current_dir = os.path.dirname(os.path.abspath(__file__))
    coord_fn = "/mnt/public/igs-rinex-2024/stations.csv" # 1111
    # ppp_sol_dir = f"/mnt/public/igs-rinex-2024/2024/PPPG_UU_Stat"  # 1111
    # ppp_sol_dir = f"/mnt/public/igs-rinex-2024/{doy:03d}/PPPG_UU_Stat"  # 1111

    ppp_sol_dir = f"/home/yxlei/cosmic2gim/scripts/IONPPP/igs-rinex-2024/{doy:03d}/PPPG_UU_Stat"

    out_stec_dir = os.path.join(current_dir, "..", "data", "stec") # 11111
    
    coords = load_coord(coord_fn)

    sites = list()
    data_list = list()
    for fn in os.listdir(ppp_sol_dir):
        if not fn.endswith("iono"): continue
        if not f"{doy:03d}" in fn: continue
        print(os.path.join(ppp_sol_dir,fn))
        site = fn[:4]
        sites.append(site)
        x, y, z = coords.loc[site, ["x", "y", "z"]]
        lat, lon, hgt = gnss_geodesy.xyz2blh(x, y, z)
        
        iono_fn = os.path.join(ppp_sol_dir, fn)
        pos_fn = os.path.join(ppp_sol_dir, fn[:-5])
        elev_fn = os.path.join(ppp_sol_dir, fn[:-5]+".elev")
        df_stec = read_ppp_iono(iono_fn, elev_fn)
        xr_stec = df2xr(df_stec)
        xr_stec_ipp = xr_stec2ipp(xr_stec, lat, lon, hgt)

        fig_filename = os.path.join(out_stec_dir, fn+".png")
        show_stec(xr_stec_ipp, fig_filename)
        
        data_list.append(xr_stec_ipp)
    xr_doy = xr.concat(data_list, dim="site")
    xr_doy = xr_doy.assign_coords(site=sites)
    outfn = f"{year:04d}_{doy:03d}-29sites.obj"
    out_fullname = os.path.join(out_stec_dir, outfn)
    gnss_utils.saveobject(xr_doy, out_fullname)
    print(out_fullname + " saved.")





# if __name__ == "__main__":
#     year = 2024
#     doy = 1
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     coord_fn = "/mnt/public/igs-rinex-2024/stations.csv" # 1111
#     # ppp_sol_dir = f"/mnt/public/igs-rinex-2024/2024/PPPG_UU_Stat"  # 1111

#     ppp_sol_dir = f"/mnt/public/igs-rinex-2024/{doy:03d}/PPPG_UU_Stat"  # 1111
    
#     out_stec_dir = os.path.join(current_dir, "..", "data", "stec") # 11111
    
#     coords = load_coord(coord_fn)

#     sites = list()
#     data_list = list()
#     for fn in os.listdir(ppp_sol_dir):
#         if not fn.endswith("iono"): continue
#         if not f"{doy:03d}" in fn: continue
#         print(os.path.join(ppp_sol_dir,fn))
#         site = fn[:4]
#         sites.append(site)
#         x, y, z = coords.loc[site, ["x", "y", "z"]]
#         lat, lon, hgt = gnss_geodesy.xyz2blh(x, y, z)
        
#         iono_fn = os.path.join(ppp_sol_dir, fn)
#         pos_fn = os.path.join(ppp_sol_dir, fn[:-5])
#         elev_fn = os.path.join(ppp_sol_dir, fn[:-5]+".elev")
#         df_stec = read_ppp_iono(iono_fn, elev_fn)
#         xr_stec = df2xr(df_stec)
#         xr_stec_ipp = xr_stec2ipp(xr_stec, lat, lon, hgt)

#         fig_filename = os.path.join(out_stec_dir, fn+".png")
#         show_stec(xr_stec_ipp, fig_filename)
        
#         data_list.append(xr_stec_ipp)
#     xr_doy = xr.concat(data_list, dim="site")
#     xr_doy = xr_doy.assign_coords(site=sites)
#     outfn = f"{year:04d}_{doy:03d}.obj"
#     out_fullname = os.path.join(out_stec_dir, outfn)
#     gnss_utils.saveobject(xr_doy, out_fullname)
#     print(out_fullname + " saved.")
