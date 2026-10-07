
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.colors as mcolors
# import os
# from datetime import datetime
# import cartopy.crs as ccrs
# import cartopy.feature as cfeature

# # 参数设置
# model_npz_path = "scripts/test_bylyx/train_save/scripts/compare_with_jason/jason_cosmic_interp_diff.npz"
# code_npz_path = "scripts/test_bylyx/train_save/scripts/compare_with_jason/jason_code_interp_diff.npz"
# save_dir = "scripts/test_bylyx/train_save/scripts/compare_with_jason/figures"
# os.makedirs(save_dir, exist_ok=True)

# # 读取数据函数
# def load_diff_data(npz_path):
#     data = np.load(npz_path)
#     times = pd.to_datetime(data['time'])
#     lats = data['lat']
#     lons = data['lon']
#     diffs = data['diff']
#     return times, lats, lons, diffs

# # 构建DataFrame
# def build_dataframe(times, lats, lons, diffs):
#     return pd.DataFrame({'time': times, 'lat': lats, 'lon': lons, 'diff': diffs})

# # 获取季节
# def get_season(month):
#     if month in [3, 4, 5]:
#         return 'ME'
#     elif month in [6, 7, 8]:
#         return 'JS'
#     elif month in [9, 10, 11]:
#         return 'SE'
#     else:
#         return 'DS'

# # 获取地方时段
# def get_local_period(row):
#     local_hour = (row['time'].hour + row['lon'] / 15) % 24
#     if 12 <= local_hour < 16:
#         return 'day'
#     elif 0 <= local_hour < 4:
#         return 'night'
#     else:
#         return None

# # 加载两组数据
# times_m, lats_m, lons_m, diffs_m = load_diff_data(model_npz_path)
# times_c, lats_c, lons_c, diffs_c = load_diff_data(code_npz_path)

# # 构建DataFrame
# df_model = build_dataframe(times_m, lats_m, lons_m, diffs_m)
# df_code = build_dataframe(times_c, lats_c, lons_c, diffs_c)

# # 添加分类字段
# df_model['season'] = df_model['time'].dt.month.apply(get_season)
# df_model['period'] = df_model.apply(get_local_period, axis=1)
# df_code['season'] = df_code['time'].dt.month.apply(get_season)
# df_code['period'] = df_code.apply(get_local_period, axis=1)

# # 筛选有效时段
# df_model = df_model[df_model['period'].notnull()]
# df_code = df_code[df_code['period'].notnull()]

# # ======= 绘图设置 ========
# season_order = ['ME', 'JS', 'SE', 'DS']
# period_order = ['day', 'night']
# lt_labels = {'day': 'LT 12–16', 'night': 'LT 0–4'}

# cmap = plt.get_cmap('RdBu_r')
# norm = mcolors.Normalize(vmin=-30, vmax=30)  # 设置颜色条范围为 -30 到 30

# fig, axes = plt.subplots(nrows=4, ncols=4, figsize=(20, 16),
#                          subplot_kw={'projection': ccrs.PlateCarree()})
# fig.suptitle("Global VTEC Difference (Model/CODE - Jason)\nGrouped by Season and Local Time", fontsize=16)

# for i, season in enumerate(season_order):
#     for j, period in enumerate(period_order):
#         # ====== Model 子图 ======
#         ax_m = axes[i, j * 2]
#         sub_df_m = df_model[(df_model['season'] == season) & (df_model['period'] == period)]
#         ax_m.set_title(f"Model - Jason\n{season} / {lt_labels[period]}", fontsize=10)

#         ax_m.add_feature(cfeature.OCEAN, facecolor='white', alpha=0.3)
#         ax_m.add_feature(cfeature.LAND, facecolor='white', alpha=1.0)
#         ax_m.add_feature(cfeature.COASTLINE, edgecolor='black', linewidth=0.8, alpha=0.8)

#         ax_m.set_extent([-180, 180, -50, 50], crs=ccrs.PlateCarree())
#         ax_m.set_xticks(np.arange(-180, 181, 60), crs=ccrs.PlateCarree())
#         ax_m.set_yticks(np.arange(-45, 46, 15), crs=ccrs.PlateCarree())
#         ax_m.set_xticklabels(['-180°', '-120°', '-60°', '0°', '60°', '120°', '180°'], fontsize=8)
#         ax_m.set_yticklabels(['-45°', '-30°', '-15°', '0°', '15°', '30°', '45°'], fontsize=8)
#         ax_m.gridlines(draw_labels=False)

#         ax_m.scatter(sub_df_m['lon'], sub_df_m['lat'], c=sub_df_m['diff'], cmap=cmap, norm=norm,
#                      s=5, alpha=0.7, transform=ccrs.PlateCarree())

#         # ====== CODE 子图 ======
#         ax_c = axes[i, j * 2 + 1]
#         sub_df_c = df_code[(df_code['season'] == season) & (df_code['period'] == period)]
#         ax_c.set_title(f"CODE GIM - Jason\n{season} / {lt_labels[period]}", fontsize=10)

#         ax_c.add_feature(cfeature.OCEAN, facecolor='white', alpha=0.3)
#         ax_c.add_feature(cfeature.LAND, facecolor='white', alpha=1.0)
#         ax_c.add_feature(cfeature.COASTLINE, edgecolor='black', linewidth=0.8, alpha=0.8)

#         ax_c.set_extent([-180, 180, -50, 50], crs=ccrs.PlateCarree())
#         ax_c.set_xticks(np.arange(-180, 181, 60), crs=ccrs.PlateCarree())
#         ax_c.set_yticks(np.arange(-45, 46, 15), crs=ccrs.PlateCarree())
#         ax_c.set_xticklabels(['-180°', '-120°', '-60°', '0°', '60°', '120°', '180°'], fontsize=8)
#         ax_c.set_yticklabels([], fontsize=8)  # 右图不显示y轴标签
#         ax_c.gridlines(draw_labels=False)

#         ax_c.scatter(sub_df_c['lon'], sub_df_c['lat'], c=sub_df_c['diff'], cmap=cmap, norm=norm,
#                      s=5, alpha=0.7, transform=ccrs.PlateCarree())

# # 添加统一颜色条
# cbar_ax = fig.add_axes([0.25, 0.05, 0.5, 0.02])
# cbar = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap),
#                     cax=cbar_ax, orientation='horizontal')
# cbar.set_label('VTEC Difference (TECU)', fontsize=12)
# cbar.ax.tick_params(labelsize=10)

# # 手动调整布局
# plt.subplots_adjust(left=0.05, right=0.95, top=0.92, bottom=0.10, hspace=0.25, wspace=0.15)

# # 保存图像
# save_path = "/home/yxlei/cosmic2gim/scripts/plots/figures/14-gim.png"
# plt.savefig(save_path, dpi=500)
# plt.show()
# print(f"图像已保存：{save_path}")









import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os
from datetime import datetime
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# 参数设置
model_npz_path = "scripts/test_bylyx/train_save/scripts/compare_with_jason/jason_cosmic_interp_diff.npz"
save_dir = "scripts/test_bylyx/train_save/scripts/compare_with_jason/figures"
os.makedirs(save_dir, exist_ok=True)

# 读取数据函数
def load_diff_data(npz_path):
    data = np.load(npz_path)
    times = pd.to_datetime(data['time'])
    lats = data['lat']
    lons = data['lon']
    diffs = data['diff']
    return times, lats, lons, diffs

# 构建DataFrame
def build_dataframe(times, lats, lons, diffs):
    return pd.DataFrame({'time': times, 'lat': lats, 'lon': lons, 'diff': diffs})

# 获取季节
def get_season(month):
    if month in [3, 4, 5]:
        return 'ME'
    elif month in [6, 7, 8]:
        return 'JS'
    elif month in [9, 10, 11]:
        return 'SE'
    else:
        return 'DS'

# 获取地方时段
def get_local_period(row):
    local_hour = (row['time'].hour + row['lon'] / 15) % 24
    if 12 <= local_hour < 16:
        return 'day'
    elif 0 <= local_hour < 4:
        return 'night'
    else:
        return None

# 加载 Model 数据
times_m, lats_m, lons_m, diffs_m = load_diff_data(model_npz_path)

# 构建 DataFrame
df_model = build_dataframe(times_m, lats_m, lons_m, diffs_m)

# 添加季节和地方时段字段
df_model['season'] = df_model['time'].dt.month.apply(get_season)
df_model['period'] = df_model.apply(get_local_period, axis=1)

# 筛选有效时段数据
df_model = df_model[df_model['period'].notnull()]

# 计算年平均误差（所有数据的平均diff）
annual_mean_error = df_model['diff'].mean()

# ======= 绘图设置 ========
season_order = ['ME', 'JS', 'SE', 'DS']
period_order = ['night', 'day']  # night=0-4, day=12-16
lt_labels = {'day': 'LT 12–16', 'night': 'LT 0–4'}

cmap = plt.get_cmap('RdBu_r')
norm = mcolors.Normalize(vmin=-30, vmax=30)  # 颜色范围固定

fig, axes = plt.subplots(nrows=4, ncols=4, figsize=(24, 16),
                         subplot_kw={'projection': ccrs.PlateCarree()})
fig.suptitle("Model VTEC Difference and Anomaly (Model - Jason)\nGrouped by Season and Local Time", fontsize=16)

for i, season in enumerate(season_order):
    for j, period in enumerate(period_order):
        # 选取对应季节和时段数据
        sub_df = df_model[(df_model['season'] == season) & (df_model['period'] == period)]
        
        # 左两列: error，右两列: error - mean error
        # col 0: night error
        # col 1: day error
        # col 2: night anomaly (error - mean)
        # col 3: day anomaly (error - mean)
        for k in range(2):
            col_idx = j*2 + k  # j=0->col0&2; j=1->col1&3
            ax = axes[i, col_idx]
            
            # 区分是普通误差还是减去年平均误差的异常
            if k == 0:
                # 普通误差
                plot_diff = sub_df['diff']
                title_suffix = "Error"
            else:
                # 减去年平均误差的异常值
                plot_diff = sub_df['diff'] - annual_mean_error
                title_suffix = "Error - Mean Error"

            # 标题（含季节，地方时段，类型）
            ax.set_title(f"{season} / {lt_labels[period]}\n{title_suffix}", fontsize=10)

            # 地图基础设置
            ax.add_feature(cfeature.OCEAN, facecolor='white', alpha=0.3)
            ax.add_feature(cfeature.LAND, facecolor='white', alpha=1.0)
            ax.add_feature(cfeature.COASTLINE, edgecolor='black', linewidth=0.8, alpha=0.8)

            ax.set_extent([-180, 180, -50, 50], crs=ccrs.PlateCarree())
            ax.set_xticks(np.arange(-180, 181, 60), crs=ccrs.PlateCarree())
            ax.set_yticks(np.arange(-45, 46, 15), crs=ccrs.PlateCarree())
            ax.set_xticklabels(['-180°', '-120°', '-60°', '0°', '60°', '120°', '180°'], fontsize=8)
            # 仅第一列显示y轴标签，右边三列不显示
            if col_idx == 0:
                ax.set_yticklabels(['-45°', '-30°', '-15°', '0°', '15°', '30°', '45°'], fontsize=8)
            else:
                ax.set_yticklabels([])

            ax.gridlines(draw_labels=False)

            # 绘制散点
            ax.scatter(sub_df['lon'], sub_df['lat'], c=plot_diff, cmap=cmap, norm=norm,
                       s=5, alpha=0.7, transform=ccrs.PlateCarree())

# 添加统一颜色条
cbar_ax = fig.add_axes([0.25, 0.05, 0.5, 0.02])
cbar = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap),
                    cax=cbar_ax, orientation='horizontal')
cbar.set_label('VTEC Difference (TECU)', fontsize=12)
cbar.ax.tick_params(labelsize=10)

# 手动调整布局
plt.subplots_adjust(left=0.05, right=0.95, top=0.92, bottom=0.10, hspace=0.25, wspace=0.15)

# 保存图像
save_path = "/home/yxlei/cosmic2gim/scripts/plots/figures/14-gim-model-error-and-anomaly.png"
plt.savefig(save_path, dpi=500)
plt.show()
print(f"图像已保存：{save_path}")
