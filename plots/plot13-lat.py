# # -------------- 分纬度带 -------------------
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import os

# # ========= 参数设置 =========
# model_npz_path = "scripts/test_bylyx/train_save/scripts/compare_with_jason/jason_cosmic_interp_diff.npz"
# code_npz_path  = "scripts/test_bylyx/train_save/scripts/compare_with_jason/jason_code_interp_diff.npz"
# save_dir       = "scripts/test_bylyx/train_save/scripts/compare_with_jason/figures"
# os.makedirs(save_dir, exist_ok=True)

# # ========== 可调参数：纬度带间隔 ==========
# lat_bin_size = 5  # 单位：度
# lat_range = (-50, 50)

# # ========= 辅助函数：按纬度带统计 =========
# def compute_lat_band_stats(npz_path, label):
#     data = np.load(npz_path)
#     lats = data['lat']
#     diffs = data['diff']

#     df = pd.DataFrame({
#         'lat': lats,
#         'diff': diffs
#     })

#     # 定义纬度带
#     bins = np.arange(lat_range[0], lat_range[1] + lat_bin_size, lat_bin_size)
#     df['lat_bin'] = pd.cut(df['lat'], bins=bins, include_lowest=True)

#     # 添加纬度中心点（作为x轴标签）
#     df['lat_center'] = df['lat_bin'].apply(lambda x: (x.left + x.right) / 2 if pd.notnull(x) else np.nan)

#     # 分组计算统计量
#     grouped = df.groupby('lat_center')['diff'].agg([
#         ('rmse', lambda x: np.sqrt(np.nanmean(x**2))),
#         ('std', lambda x: np.nanstd(x)),
#         ('count', 'count')
#     ]).reset_index()

#     grouped['source'] = label
#     return grouped

# # ========= 加载并处理 =========
# df_model = compute_lat_band_stats(model_npz_path, 'Model')
# df_code  = compute_lat_band_stats(code_npz_path,  'CODE')
# df_all = pd.concat([df_model, df_code], ignore_index=True)

# # ========== 绘图函数 ==========
# def plot_lat_band_metric(metric_name, ylabel):
#     fig, ax = plt.subplots(figsize=(12.9/2.54, 2.5))

#     # 分组数据提取
#     df_model = df_all[df_all['source'] == 'Model']  # 假设 Model对应GCIRI
#     df_code = df_all[df_all['source'] == 'CODE']  # CODE对应IRI-2020

#     # 绘制两条曲线，指定样式
#     ax.plot(df_model['lat_center'], df_model[metric_name],
#             label='Model TEC',
#             color='#3c7fb1',
#             linewidth=1.8,
#             marker='s',
#             markersize=4)

#     ax.plot(df_code['lat_center'],df_code[metric_name],
#             label='CODE TEC',
#             color='#b53289',
#             linewidth=1.8,
#             marker='s',
#             markersize=4)

#     ax.set_xlabel("Latitude (°)")
#     ax.set_ylabel(ylabel)
#     # ax.set_title(f"{ylabel} vs Latitude (Interval: {lat_bin_size}°)")
#     ax.set_xticks(np.arange(lat_range[0], lat_range[1] + 1, lat_bin_size))
#     ax.grid(axis='y', linewidth=0.8, alpha=0.8)
#     ax.legend()
#     plt.xticks(rotation=45)
#     plt.tight_layout()

#     save_path = "/home/yxlei/cosmic2gim/scripts/plots/figures/13-lat-rmse.png"
#     plt.savefig(save_path, dpi=500)
#     plt.close()
#     print(f"图已保存：{save_path}")


# # ========= 绘图输出 =========
# plot_lat_band_metric('rmse', 'RMSE (TECU)')
# # plot_lat_band_metric('std', 'STD [TECU]')












# -------------- 分纬度带 ------------------- 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# ========= 参数设置 =========
model_npz_path = "scripts/test_bylyx/train_save/scripts/compare_with_jason/jason_cosmic_interp_diff.npz"
code_npz_path  = "scripts/test_bylyx/train_save/scripts/compare_with_jason/jason_code_interp_diff.npz"
save_dir       = "scripts/test_bylyx/train_save/scripts/compare_with_jason/figures"
os.makedirs(save_dir, exist_ok=True)

# ========== 可调参数：纬度带间隔 ==========
lat_bin_size = 5  # 单位：度，仍用于统计时分组
lat_range = (-50, 50)

# ========= 辅助函数：按纬度带统计 =========
def compute_lat_band_stats(npz_path, label):
    data = np.load(npz_path)
    lats = data['lat']
    diffs = data['diff']

    df = pd.DataFrame({
        'lat': lats,
        'diff': diffs
    })

    # 定义纬度带
    bins = np.arange(lat_range[0], lat_range[1] + lat_bin_size, lat_bin_size)
    df['lat_bin'] = pd.cut(df['lat'], bins=bins, include_lowest=True)

    # 添加纬度中心点（作为x轴标签）
    df['lat_center'] = df['lat_bin'].apply(lambda x: (x.left + x.right) / 2 if pd.notnull(x) else np.nan)

    # 分组计算统计量
    grouped = df.groupby('lat_center')['diff'].agg([
        ('rmse', lambda x: np.sqrt(np.nanmean(x**2))),
        ('std', lambda x: np.nanstd(x)),
        ('count', 'count')
    ]).reset_index()

    grouped['source'] = label
    return grouped

# ========= 加载并处理 =========
df_model = compute_lat_band_stats(model_npz_path, 'Model')
df_code  = compute_lat_band_stats(code_npz_path,  'CODE')
df_all = pd.concat([df_model, df_code], ignore_index=True)

# ========== 绘图函数 =========
def plot_lat_band_metric(metric_name, ylabel):
    fig, ax = plt.subplots(figsize=(12.9/2.54, 2.5))

    # 分组数据提取
    df_model = df_all[df_all['source'] == 'Model']  # 假设 Model对应GCIRI
    df_code = df_all[df_all['source'] == 'CODE']  # CODE对应IRI-2020

    # 绘制两条曲线，指定样式
    ax.plot(df_code['lat_center'], df_code[metric_name],
            label='CODE TEC',
            color='#3c7fb1',
            linewidth=1.8,
            marker='s',
            markersize=4)
    
    ax.plot(df_model['lat_center'], df_model[metric_name],
            label='GINI TEC',
            color='#b53289',
            linewidth=1.8,
            marker='s',
            markersize=4)



    ax.set_xlabel("Latitude (°)")
    ax.set_ylabel(ylabel)
    # x轴标签改为10度间隔
    ax.set_xticks(np.arange(lat_range[0], lat_range[1] + 1, 10))
    
    xmin = df_all['lat_center'].min()
    xmax = df_all['lat_center'].max()
    ax.set_xlim(xmin, xmax)

    ax.grid(axis='y', linewidth=0.8, alpha=0.8)
    ax.legend()
    # plt.xticks(rotation=45)
    plt.tight_layout()

    save_path = "/home/yxlei/cosmic2gim/scripts/plots/figures/13-lat-rmse.png"
    plt.savefig(save_path, dpi=500)
    plt.close()
    print(f"图已保存：{save_path}")

# ========= 绘图输出 =========
plot_lat_band_metric('rmse', 'RMSE (TECU)')
# plot_lat_band_metric('std', 'STD [TECU]')
