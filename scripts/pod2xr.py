import pandas as pd
import numpy as np
import xarray as xr
from math import sin, cos
import os
from ppgnss import gnss_utils
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # pod_data = gnss_utils.loadobject(os.path.join(data_dir, "pod_dataset.pkl"))
    # df = gnss_utils.loadobject(os.path.join(current_dir, "..", "data", "pod_34day_data.pkl"))          # 6.15
    # df = gnss_utils.loadobject(os.path.join(current_dir, "..", "data", "pod_2019to2024_data.pkl")) 
    df = gnss_utils.loadobject(os.path.join(current_dir, "..", "data", "pod_data/pod_2019to2024_data_nonan.pkl")) 


    # 确保时间列是datetime类型
    df['time'] = pd.to_datetime(df['time'])

    # 定义网格参数
    LAT_MIN, LAT_MAX = -50, 50
    LON_MIN, LON_MAX = -180, 180
    LAT_STEP, LON_STEP = 2.5, 5
    GRID_ROWS = int((LAT_MAX - LAT_MIN) / LAT_STEP) + 1 # 41
    GRID_COLS = int((LON_MAX - LON_MIN) / LON_STEP)  + 1# 73
    print("GRID_ROWS:", GRID_ROWS, "GRID_COLS:", GRID_COLS)
    # print(df[2000:3000]["lat"].min(), df[2000:3000]["lat"].max())

    # 创建网格中心点坐标
    lat_centers = [LAT_MIN + (i) * LAT_STEP for i in range(GRID_ROWS)]
    lon_centers = [LON_MIN + (j ) * LON_STEP for j in range(GRID_COLS)]

    # 生成所有整点时间（从最小时间到最大时间，以小时为单位）
    start_time = df['time'].min().floor('H')
    end_time = df['time'].max().ceil('H')
    hourly_times = pd.date_range(start=start_time, end=end_time, freq='H')

    # 创建空的数据数组，形状为(时间, 纬度, 经度, 通道)
    data = np.zeros((len(hourly_times), GRID_ROWS, GRID_COLS, 5), dtype=np.float32)

    # 通道名称
    channels = ['occultation_flag', "delta_time", 'az_sin', 'az_cos', 'max_tec']

    # 处理每个整点时间段
    for t_idx, t0 in enumerate(hourly_times):
        if t_idx == 105: continue
        # 筛选当前整点前后30分钟的数据
        t_start = t0 - pd.Timedelta(minutes=30)
        t_end = t0 + pd.Timedelta(minutes=30)
        mask = (df['time'] >= t_start) & (df['time'] < t_end)
        hour_group = df.loc[mask].copy()
        
        # 记录已填充的网格位置
        filled_cells = set()
        
        # 处理每个掩星事件
        for _, row in hour_group.iterrows():
            lat, lon = row['lat'], row['lon']

            # 跳过 NaN 的经纬度  # 6.15  ValueError: cannot convert float NaN to integer
            if pd.isnull(lat) or pd.isnull(lon) or pd.isnull(row['az']) or pd.isnull(row['max_tec']):
                continue

            
            # 计算网格行列索引
            row_idx = int((lat - LAT_MIN) // LAT_STEP)
            col_idx = int((lon - LON_MIN) // LON_STEP) % GRID_COLS
            
            # 跳过无效索引
            if not (0 <= row_idx < GRID_ROWS):
                continue
            
            # 检查网格是否已占用
            if (row_idx, col_idx) in filled_cells:
                continue
            
            # 填充网格数据
            data[t_idx, row_idx, col_idx, 0] = 1  # 掩星发生标志
            data[t_idx, row_idx, col_idx, 1] = (row["time"] - t0)/pd.Timedelta(1, "h")  # 方位角
            data[t_idx, row_idx, col_idx, 2] = sin(row['az'])  # 方位角正弦
            data[t_idx, row_idx, col_idx, 3] = cos(row['az'])  # 方位角余弦
            data[t_idx, row_idx, col_idx, 4] = row['max_tec']  # TEC值
            # 标记该网格已占用
            filled_cells.add((row_idx, col_idx))
        print(t_idx, np.sum(np.isnan(data[t_idx])))
        
    idx_valid = np.isnan(data[:, :, :, 4])
    data[:, :, :, 0][idx_valid] = 0
    data[:, :, :, 1][idx_valid] = 0
    data[:, :, :, 2][idx_valid] = 0
    data[:, :, :, 3][idx_valid] = 0
    
    # print(np.sum(np.isnan(data)))
    # 计算纬、经度网格中心点
    # 创建xarray DataArray
    da = xr.DataArray(
        data,
        dims=['time', 'lat', 'lon', 'channel'],
        coords={
            'time': hourly_times,
            'lat': lat_centers,
            'lon': lon_centers,
            'channel': channels
        },
        name='occultation_data'
    )

    # 设置属性
    da.attrs['description'] = 'GNSS occultation data in grid format'
    da.attrs['latitude_units'] = 'degrees_north'
    da.attrs['longitude_units'] = 'degrees_east'
    da.attrs['max_tec_units'] = 'TECU'
    da.attrs['azimuth_units'] = 'radians'

    # 输出结果
    print("Created xarray DataArray:")
    print(da)
    # out_filename = os.path.join(current_dir, "..", "data", 'cosmic_grid_5ch_2022_034.obj')        # 6.15
    out_filename=os.path.join(current_dir,"..","data",'cosmic_grid_5ch_2019to2024.obj')

    gnss_utils.saveobject(da, out_filename)