import sys
import os    

import datetime
from pandas.tseries.offsets import Hour
from ppgnss import gnss_io, gnss_time, gnss_utils
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt

def main():
    """主函数 - 遍历全年 DOY"""
    year = 2024
    current_dir = os.path.dirname(os.path.abspath(__file__))
    stec_dir = os.path.join(current_dir, "..", "data", "stec")
    os.makedirs(stec_dir, exist_ok=True)

    results_dir = "/home/yxlei/cosmic2gim/scripts/IONPPP/results"
    fig_dir = os.path.join(results_dir, "figures")
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(fig_dir, exist_ok=True)

    # 遍历全年 DOY = 1 ~ 366              236-255？？
    for doy in range(1, 367):
        print(f"===== Processing {year}-{doy:03d} =====")

        stec_filename = os.path.join(stec_dir, f"{year:04d}_{doy:03d}.obj")
        if not os.path.isfile(stec_filename):
            print(f"skip {stec_filename}, file missing")
            continue

        try:
            xr_obs = gnss_utils.loadobject(stec_filename)
        except Exception as e:
            print(f"Failed to load {stec_filename}: {e}")
            continue

        cosm_obj_fn = f"xr_cosm_{year:04d}_{doy:03d}.obj"
        code_obj_fn = f"xr_code_{year:04d}_{doy:03d}.obj"

        _, mo, dy = gnss_time.doy2ymd(year, doy)
        day_from = np.datetime64(datetime.datetime(year, mo, int(dy))) 
        day_to = day_from + np.timedelta64(24,"h")

        if os.path.isfile(cosm_obj_fn) and os.path.isfile(code_obj_fn):
            xr_cosm_sel = gnss_utils.loadobject(cosm_obj_fn)
            xr_code_sel = gnss_utils.loadobject(code_obj_fn)
        else:
            xr_code = gnss_utils.loadobject(f"/mnt/geodata/GIM/CODG_1ch/CODG{year:04d}.obj")
            xr_cosm = xr.open_dataset(
                "/home/yxlei/cosmic2gim/scripts/test_bylyx/train_save/cosmic_grid_data.obj",
                engine="netcdf4"
            ).tec
            xr_cosm_sel = xr_cosm.sel(time=slice(day_from, day_to), lon=slice(-180, 175))
            xr_code_sel = xr_code.sel(time=slice(day_from, day_to), lon=slice(-180, 175))
            # gnss_utils.saveobject(xr_cosm_sel, cosm_obj_fn)
            # gnss_utils.saveobject(xr_code_sel, code_obj_fn)

        xr_cosm_slon = gnss_utils.xr_gim2solar(xr_cosm_sel)
        xr_code_slon = gnss_utils.xr_gim2solar(xr_code_sel)

        sites = xr_obs.site.values
        print(sites, len(sites))

        xr_obs = xr_obs.sel(site=sites)
        pd_obs = gnss_utils.xr_obs2pd(xr_obs)
        pd_obs_slon = gnss_utils.pd_obs2slon(pd_obs)

        # pd_diff_obs_vs_cosm = gnss_utils.valid_obs_vs_gim(pd_obs_slon, xr_cosm_slon)
        # pd_diff_obs_vs_code = gnss_utils.valid_obs_vs_gim(pd_obs_slon, xr_code_slon)

        # rms_cosm = pd_diff_obs_vs_cosm.groupby(["site", "ref_time_pre"])["delta"].apply(lambda x: np.sqrt(np.nanmean(x**2)))
        # rms_code = pd_diff_obs_vs_code.groupby(["site", "ref_time_pre"])["delta"].apply(lambda x: np.sqrt(np.nanmean(x**2)))


        pd_diff_obs_vs_cosm = gnss_utils.valid_obs_vs_gim(pd_obs_slon, xr_cosm_slon)
        pd_diff_obs_vs_code = gnss_utils.valid_obs_vs_gim(pd_obs_slon, xr_code_slon)
        # 以 "site" 字段分组，统计 pd_diff_obs_vs_cosm 和 pd_diff_obs_vs_code 的 "delta" 列的RMS
        rms_cosm = pd_diff_obs_vs_cosm.groupby(["site", "ref_time_pre"])["delta"].apply(lambda x: np.sqrt(np.nanmean(x**2)))
        rms_cosm_site = pd_diff_obs_vs_cosm.groupby(["site"])["delta"].apply(lambda x: np.sqrt(np.nanmean(x**2)))
        rms_code = pd_diff_obs_vs_code.groupby(["site", "ref_time_pre"])["delta"].apply(lambda x: np.sqrt(np.nanmean(x**2)))
        rms_code_site = pd_diff_obs_vs_code.groupby(["site"])["delta"].apply(lambda x: np.sqrt(np.nanmean(x**2)))
    
        print("各站点 Obs-COSM RMS：")
        print(rms_cosm)
        print(rms_cosm_site)
        print("各站点 Obs-CODE RMS：")
        print(rms_code)
        print(rms_code_site)
 
        # 绘图
        plot_solar_diff(xr_code_slon, pd_diff_obs_vs_code, xr_cosm_slon, pd_diff_obs_vs_cosm, year, doy)
        
        # 保存结果
        gnss_utils.saveobject(xr_cosm_sel, os.path.join(results_dir, f"xr_cosm_{year:04d}_{doy:03d}.obj"))
        gnss_utils.saveobject(xr_code_sel, os.path.join(results_dir, f"xr_code_{year:04d}_{doy:03d}.obj"))
        pd_diff_obs_vs_cosm.to_pickle(os.path.join(results_dir, f"pd_diff_obs_vs_cosm_{year:04d}_{doy:03d}.pkl"))
        pd_diff_obs_vs_code.to_pickle(os.path.join(results_dir, f"pd_diff_obs_vs_code_{year:04d}_{doy:03d}.pkl"))
        rms_cosm.to_pickle(os.path.join(results_dir, f"rms_cosm_{year:04d}_{doy:03d}.pkl"))
        rms_code.to_pickle(os.path.join(results_dir, f"rms_code_{year:04d}_{doy:03d}.pkl"))






# def main():
#     """主函数 - 执行所有主要逻辑"""
#     # 1. 加载观测 VTEC 数据
#     year = 2024
#     doy = 1           #111
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     stec_dir = os.path.join(current_dir, "..", "data", "stec") # 11111
#     stec_filename = os.path.join(stec_dir, f"{year:04d}_{doy:03d}.obj")
#     xr_obs = gnss_utils.loadobject(stec_filename)
#     cosm_obj_fn = f"xr_cosm_{year:04d}_{doy:03d}.obj"
#     code_obj_fn = f"xr_code_{year:04d}_{doy:03d}.obj"

#     _, mo, dy = gnss_time.doy2ymd(year, doy)
#     day_from = np.datetime64(datetime.datetime(year, mo, int(dy))) 
#     day_to = day_from + np.timedelta64(24,"h")
    
#     if os.path.isfile(cosm_obj_fn) and os.path.isfile(code_obj_fn):
#         xr_cosm_sel = gnss_utils.loadobject(cosm_obj_fn)
#         xr_code_sel = gnss_utils.loadobject(code_obj_fn)

#     else:
#         # xr_code = gnss_io.read_ionex_file("/home/lzhang/source/cosmic2gim/data/COD0OPSFIN_20240010000_01D_01H_GIM.INX")
#         xr_code = gnss_utils.loadobject(f"/mnt/geodata/GIM/CODG_1ch/CODG{year:04d}.obj")
#         # print(xr_code)

#         # xr_cosm = xr.open_dataset("data/cosmic_grid_data.obj")

#         xr_cosm = xr.open_dataset("/home/yxlei/cosmic2gim/scripts/test_bylyx/train_save/cosmic_grid_data.obj", engine="netcdf4")
#         # print(xr_cosm)

#         xr_cosm = xr_cosm.tec
#         xr_cosm_sel = xr_cosm.sel(time=slice(day_from, day_to),
#                                   lon=slice(-180, 175))
#         xr_code_sel = xr_code.sel(time=slice(day_from, day_to),
#                                   lon=slice(-180, 175))
#         gnss_utils.saveobject(xr_cosm_sel, cosm_obj_fn)
#         gnss_utils.saveobject(xr_code_sel, code_obj_fn)
    
#     xr_cosm_slon = gnss_utils.xr_gim2solar(xr_cosm_sel)
#     xr_code_slon = gnss_utils.xr_gim2solar(xr_code_sel)
#     sites = xr_obs.site.values #[:10]
#     print(sites, len(sites))
#     xr_obs = xr_obs.sel(site=sites)
#     pd_obs = gnss_utils.xr_obs2pd(xr_obs)
#     pd_obs_slon = gnss_utils.pd_obs2slon(pd_obs)
    
#     # print(pd_obs_slon.shape)
#     # print(xr_cosm_slon.shape)
#     # pd_diff_obs_vs_cosm2 = gnss_utils.valid_obs_vs_gim(pd_obs_slon.iloc[:100], xr_cosm_slon)
#     # # print(pd_diff_obs_vs_cosm2)

#     pd_diff_obs_vs_cosm = gnss_utils.valid_obs_vs_gim(pd_obs_slon, xr_cosm_slon)
#     pd_diff_obs_vs_code = gnss_utils.valid_obs_vs_gim(pd_obs_slon, xr_code_slon)
#     # 以 "site" 字段分组，统计 pd_diff_obs_vs_cosm 和 pd_diff_obs_vs_code 的 "delta" 列的RMS
#     rms_cosm = pd_diff_obs_vs_cosm.groupby(["site", "ref_time_pre"])["delta"].apply(lambda x: np.sqrt(np.nanmean(x**2)))
#     rms_cosm_site = pd_diff_obs_vs_cosm.groupby(["site"])["delta"].apply(lambda x: np.sqrt(np.nanmean(x**2)))
#     rms_code = pd_diff_obs_vs_code.groupby(["site", "ref_time_pre"])["delta"].apply(lambda x: np.sqrt(np.nanmean(x**2)))
#     rms_code_site = pd_diff_obs_vs_code.groupby(["site"])["delta"].apply(lambda x: np.sqrt(np.nanmean(x**2)))
#     print("各站点 Obs-COSM RMS：")
#     print(rms_cosm)
#     print(rms_cosm_site)
#     print("各站点 Obs-CODE RMS：")
#     print(rms_code)
#     print(rms_code_site)

#     plot_solar_diff(xr_code_slon, pd_diff_obs_vs_code, xr_cosm_slon, pd_diff_obs_vs_cosm, year, doy)

#     # 保存结果
#     # os.makedirs("results", exist_ok=True)
#     gnss_utils.saveobject(xr_cosm_sel, f"/home/yxlei/cosmic2gim/scripts/IONPPP/results/xr_cosm_{year:04d}_{doy:03d}.obj")
#     gnss_utils.saveobject(xr_code_sel, f"/home/yxlei/cosmic2gim/scripts/IONPPP/results/xr_code_{year:04d}_{doy:03d}.obj")
#     pd_diff_obs_vs_cosm.to_pickle(f"/home/yxlei/cosmic2gim/scripts/IONPPP/results/pd_diff_obs_vs_cosm_{year:04d}_{doy:03d}.pkl")
#     pd_diff_obs_vs_code.to_pickle(f"/home/yxlei/cosmic2gim/scripts/IONPPP/results/pd_diff_obs_vs_code_{year:04d}_{doy:03d}.pkl")
#     rms_cosm.to_pickle(f"/home/yxlei/cosmic2gim/scripts/IONPPP/results/rms_cosm_{year:04d}_{doy:03d}.pkl")
#     rms_code.to_pickle( f"/home/yxlei/cosmic2gim/scripts/IONPPP/results/rms_code_{year:04d}_{doy:03d}.pkl")






def plot_solar_diff(xr_code_slon, pd_diff_obs_vs_code, xr_cosm_slon, pd_diff_obs_vs_cosm, year, doy):
    # 生成4行4列的绘图
    _, mo, dy = gnss_time.doy2ymd(year, doy)

    times = [0, 6, 12, 18]
    fig, axes = plt.subplots(4, 5, figsize=(40, 20))
    # 获取xr_gim_slon的时间坐标
    # time_coords = xr_cosm_slon.time.values
    # xr_raw, xr_solar = xr_code_sel, xr_code_slon
    # xr_cosm_sel, xr_cosm_slon = xr_cosm_sel, xr_cosm_slon
    for i, hour in enumerate(times):
        # 找到最接近hour的时间索引
        t_sel = np.datetime64(f'{year:04d}-{mo:02d}-{int(dy):02d}T{hour:02d}:00:00')
        # 0列：原始GIM VTEC
        try:
            code_solar_vtec = xr_code_slon.sel(time=t_sel, data="solar_vtec")
        except Exception:
            code_solar_vtec = xr_code_slon.isel(time=i, data="solar_vtec")
        im0 = axes[i, 0].pcolormesh(
            code_solar_vtec.lon, code_solar_vtec.lat, code_solar_vtec, shading='auto', cmap='jet'
        )
        axes[i, 0].set_xlim(-180, 180)
        axes[i, 0].set_ylim(-45, 45)
        axes[i, 0].set_title(f"GIM VTEC {hour:02d}:00")
        fig.colorbar(im0, ax=axes[i, 0], label="VTEC (TECu)")
        axes[i, 0].set_xlabel("经度")
        axes[i, 0].set_ylabel("纬度")
        # 1列：太阳坐标GIM VTEC
        try:
            cosm_solar_vtec = xr_cosm_slon.sel(time=t_sel, data="solar_vtec")
        except Exception:
            cosm_solar_vtec = xr_cosm_slon.isel(time=i).sel(data="solar_vtec")
        im1 = axes[i, 1].pcolormesh(
            cosm_solar_vtec.lon, cosm_solar_vtec.lat, cosm_solar_vtec, shading='auto', cmap='jet'
        )
        
        print(cosm_solar_vtec.shape)
        axes[i, 1].set_xlim(-180, 180)
        axes[i, 1].set_ylim(-45, 45)
        axes[i, 1].set_title(f"Solar GIM VTEC {hour:02d}:00")
        fig.colorbar(im1, ax=axes[i, 1], label="VTEC (TECu)")
        axes[i, 1].set_xlabel("经度")
        axes[i, 1].set_ylabel("纬度")
        # 2列：观测
        mask = np.abs(pd_diff_obs_vs_cosm['time'].dt.hour - hour) < 0.5
        sc2 = axes[i, 2].scatter(
            pd_diff_obs_vs_cosm.loc[mask, "slon"],
            pd_diff_obs_vs_cosm.loc[mask, "lat"],
            c=pd_diff_obs_vs_cosm.loc[mask, "vtec"],
            cmap='jet',
            s=10,
            vmin=0,
            vmax=100
        )
        axes[i, 2].set_xlim(-180, 180)
        axes[i, 2].set_ylim(-45, 45)
        axes[i, 2].set_title(f"Obs {hour:02d}:00")
        axes[i, 2].set_xlabel("太阳经度")
        axes[i, 2].set_ylabel("纬度")
        fig.colorbar(sc2, ax=axes[i, 2], label="VTEC (TECu)")
        # 3列：观测VTEC散点（太阳坐标）
        mask_obs = np.abs(pd_diff_obs_vs_cosm['time'].dt.hour - hour) < 0.5
        sc3 = axes[i, 3].scatter(
            pd_diff_obs_vs_cosm.loc[mask_obs, "slon"],
            pd_diff_obs_vs_cosm.loc[mask_obs, "lat"],
            c=pd_diff_obs_vs_cosm.loc[mask_obs, "delta"],
            cmap='bwr',
            s=10,
            vmin=-20,
            vmax=20
        )
        axes[i, 3].set_xlim(-180, 180)
        axes[i, 3].set_ylim(-45, 45)
        axes[i, 3].set_title(f"diff (Obs-COSM) {hour:02d}:00")
        axes[i, 3].set_xlabel("太阳经度")
        axes[i, 3].set_ylabel("纬度")
        fig.colorbar(sc3, ax=axes[i, 3], label="VTEC (TECu)")
        
        # 4列：COSM VTEC散点（太阳坐标）
        mask_cosm = np.abs(pd_diff_obs_vs_code['time'].dt.hour - hour) < 0.5
        sc4 = axes[i, 4].scatter(
            pd_diff_obs_vs_code.loc[mask_cosm, "slon"],
            pd_diff_obs_vs_code.loc[mask_cosm, "lat"],
            c=pd_diff_obs_vs_code.loc[mask_cosm, "delta"],
            cmap='bwr',
            s=10,
            vmin=-20,
            vmax=20
        )
        
        axes[i, 4].set_xlim(-180, 180)
        axes[i, 4].set_ylim(-45, 45)
        axes[i, 4].set_title(f"diff (Obs-CODE) {hour:02d}:00")
        axes[i, 4].set_xlabel("经度")
        axes[i, 4].set_ylabel("纬度")
        fig.colorbar(sc4, ax=axes[i, 4], label="VTEC (TECu)")   
        
    plt.tight_layout()
    plt.savefig(f"/home/yxlei/cosmic2gim/scripts/IONPPP/results/figures/compare_gim_obs_{year:04d}_{doy:03d}.png", dpi=100)

    print(pd_diff_obs_vs_cosm.head())
    print(pd_diff_obs_vs_cosm.tail())

if __name__ == "__main__":
    main()