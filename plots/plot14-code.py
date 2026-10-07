# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.colors as mcolors
# import os
# from datetime import datetime
# import cartopy.crs as ccrs
# import cartopy.feature as cfeature

# # ===================== 参数设置 =====================
# model_npz_path = "scripts/test_bylyx/train_save/scripts/compare_with_jason/jason_code_interp_diff.npz"

# # ===================== 读取数据函数 =====================
# def load_diff_data(npz_path):
#     data = np.load(npz_path)
#     times = pd.to_datetime(data['time'])
#     lats = data['lat']
#     lons = data['lon']
#     diffs = data['diff']
#     return times, lats, lons, diffs


# def build_dataframe(times, lats, lons, diffs):
#     return pd.DataFrame({'time': times, 'lat': lats, 'lon': lons, 'diff': diffs})


# def get_season(month):
#     if month in [3, 4, 5]:
#         return 'Spring'
#     elif month in [6, 7, 8]:
#         return 'Summer'
#     elif month in [9, 10, 11]:
#         return 'Autumn'
#     else:
#         return 'Winter'


# def get_local_period(row):
#     local_hour = (row['time'].hour + row['lon'] / 15) % 24
#     if 12 <= local_hour < 16:
#         return 'day'
#     elif 0 <= local_hour < 4:
#         return 'night'
#     else:
#         return None


# # ===================== 加载数据 =====================
# times_m, lats_m, lons_m, diffs_m = load_diff_data(model_npz_path)
# df_model = build_dataframe(times_m, lats_m, lons_m, diffs_m)

# df_model['season'] = df_model['time'].dt.month.apply(get_season)
# df_model['period'] = df_model.apply(get_local_period, axis=1)
# df_model = df_model[df_model['period'].notnull()]

# # 年平均误差
# annual_mean_error = df_model['diff'].mean()

# # ===================== 绘图 =====================
# season_order = ['Spring', 'Summer', 'Autumn', 'Winter']
# period_order = ['night', 'day']
# lt_labels = {'night': '00:00–04:00', 'day': '12:00–16:00'}

# cmap = plt.get_cmap('RdBu_r')
# norm = mcolors.Normalize(vmin=-20, vmax=20)

# fig, axes = plt.subplots(nrows=4, ncols=4, figsize=(22, 14),
#                          subplot_kw={'projection': ccrs.PlateCarree()})

# # ---- 最上方四列的统一标题 ----
# # top_titles = [
# #     "00:00UT–04:00UT\n(Error)",
# #     "12:00UT–16:00UT\n(Error)",
# #     "00:00UT–04:00UT\n(Error–Mean Error)",
# #     "12:00UT–16:00UT\n(Error–Mean Error)"
# # ]

# top_titles = [
#     "00:00UT–04:00UT\n(Error)",
#     "00:00UT–04:00UT\n(Error–Mean Error)",
#     "12:00UT–16:00UT\n(Error)",
#     "12:00UT–16:00UT\n(Error–Mean Error)"
# ]



# for j in range(4):
#     axes[0, j].set_title(top_titles[j], fontsize=13, pad=15)

# # ---- 绘制每个子图 ----
# for i, season in enumerate(season_order):
#     for j, period in enumerate(period_order):
#         sub_df = df_model[(df_model['season'] == season) & (df_model['period'] == period)]
#         for k in range(2):
#             col_idx = j * 2 + k
#             ax = axes[i, col_idx]

#             # 绘制 error 或 (error - mean)
#             if k == 0:
#                 plot_diff = sub_df['diff']
#             else:
#                 plot_diff = sub_df['diff'] - annual_mean_error

#             # 背景地图
#             ax.add_feature(cfeature.OCEAN, facecolor='white', alpha=0.3)
#             ax.add_feature(cfeature.LAND, facecolor='white', alpha=1.0)
#             ax.add_feature(cfeature.COASTLINE, edgecolor='black', linewidth=0.6, alpha=0.8)
#             ax.set_extent([-180, 180, -50, 50])

#             # 经纬度刻度线
#             ax.set_xticks(np.arange(-180, 181, 60), crs=ccrs.PlateCarree())
#             ax.set_yticks(np.arange(-45, 46, 15), crs=ccrs.PlateCarree())

#             # 只有最下行显示 x 轴刻度标签
#             if i == 3:
#                 ax.set_xticklabels(['-180°', '-120°', '-60°', '0°', '60°', '120°', '180°'], fontsize=9)
#             else:
#                 ax.set_xticklabels([])

#             # 只有最左列显示 y 轴刻度标签
#             if col_idx == 0:
#                 ax.set_yticklabels(['-45°', '-30°', '-15°', '0°', '15°', '30°', '45°'], fontsize=9)
#             else:
#                 ax.set_yticklabels([])

#             ax.gridlines(draw_labels=False, linewidth=0.5, color='gray', alpha=0.4, linestyle='--')

#             # 绘制散点
#             ax.scatter(sub_df['lon'], sub_df['lat'], c=plot_diff, cmap=cmap, norm=norm,
#                        s=5, alpha=0.7, transform=ccrs.PlateCarree())

#     # 每行左侧标注季节
#     axes[i, 0].text(-0.25, 0.5, season, va='center', ha='right', fontsize=13,
#                     rotation=90, transform=axes[i, 0].transAxes, fontweight='bold')

# # ---- 添加颜色条 ----
# cbar_ax = fig.add_axes([0.25, 0.05, 0.5, 0.02])
# cbar = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap),
#                     cax=cbar_ax, orientation='horizontal')
# cbar.set_label('VTEC Difference (TECU)', fontsize=12)
# cbar.ax.tick_params(labelsize=10)

# # ---- 调整布局并保存 ----
# plt.subplots_adjust(left=0.08, right=0.95, top=0.90, bottom=0.10, hspace=0.08, wspace=0.05)

# save_path =  "/home/yxlei/cosmic2gim/scripts/plots/figures/14-code-jason.png"
# plt.savefig(save_path, dpi=500)
# plt.show()
# print(f"✅ 图像已保存：{save_path}")









import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os
from datetime import datetime
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# 设置全局字体
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10

# ===================== 参数设置 =====================
model_npz_path = "scripts/test_bylyx/train_save/scripts/compare_with_jason/jason_code_interp_diff.npz"

# ===================== 读取数据函数 =====================
def load_diff_data(npz_path):
    data = np.load(npz_path)
    times = pd.to_datetime(data['time'])
    lats = data['lat']
    lons = data['lon']
    diffs = data['diff']
    return times, lats, lons, diffs


def build_dataframe(times, lats, lons, diffs):
    return pd.DataFrame({'time': times, 'lat': lats, 'lon': lons, 'diff': diffs})


def get_season(month):
    if month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    elif month in [9, 10, 11]:
        return 'Autumn'
    else:
        return 'Winter'


def get_local_period(row):
    local_hour = (row['time'].hour + row['lon'] / 15) % 24
    if 12 <= local_hour < 16:
        return 'day'
    elif 0 <= local_hour < 4:
        return 'night'
    else:
        return None


# ===================== 加载数据 =====================
times_m, lats_m, lons_m, diffs_m = load_diff_data(model_npz_path)
df_model = build_dataframe(times_m, lats_m, lons_m, diffs_m)

df_model['season'] = df_model['time'].dt.month.apply(get_season)
df_model['period'] = df_model.apply(get_local_period, axis=1)
df_model = df_model[df_model['period'].notnull()]

# 年平均误差
annual_mean_error = df_model['diff'].mean()

# ===================== 绘图 =====================
season_order = ['Spring', 'Summer', 'Autumn', 'Winter']
period_order = ['night', 'day']
lt_labels = {'night': '00:00–04:00', 'day': '12:00–16:00'}

cmap = plt.get_cmap('RdBu_r')
norm = mcolors.Normalize(vmin=-20, vmax=20)

fig, axes = plt.subplots(nrows=4, ncols=4, figsize=(22, 14),
                         subplot_kw={'projection': ccrs.PlateCarree()})

# ---- 最上方四列的统一标题 ----
top_titles = [
    "00:00UT–04:00UT\n(Error)",
    "00:00UT–04:00UT\n(Error–Mean Error)",
    "12:00UT–16:00UT\n(Error)",
    "12:00UT–16:00UT\n(Error–Mean Error)"
]


for j in range(4):
    axes[0, j].set_title(top_titles[j], fontsize=10, pad=15)  # 字体大小和全局保持一致

# ---- 绘制每个子图 ----
for i, season in enumerate(season_order):
    for j, period in enumerate(period_order):
        sub_df = df_model[(df_model['season'] == season) & (df_model['period'] == period)]
        for k in range(2):
            col_idx = j * 2 + k
            ax = axes[i, col_idx]

            # 绘制 error 或 (error - mean)
            if k == 0:
                plot_diff = sub_df['diff']
            else:
                plot_diff = sub_df['diff'] - annual_mean_error

            # 背景地图
            ax.add_feature(cfeature.OCEAN, facecolor='white', alpha=0.3)
            ax.add_feature(cfeature.LAND, facecolor='white', alpha=1.0)
            ax.add_feature(cfeature.COASTLINE, edgecolor='black', linewidth=0.6, alpha=0.8)
            ax.set_extent([-180, 180, -50, 50])

            # 经纬度刻度线
            ax.set_xticks(np.arange(-180, 181, 60), crs=ccrs.PlateCarree())
            ax.set_yticks(np.arange(-45, 46, 15), crs=ccrs.PlateCarree())

            # 只有最下行显示 x 轴刻度标签，且不显示-180°
            if i == 3:
                xticklabels = ['' if x == -180 else f'{x}°' for x in np.arange(-180, 181, 60)]
                ax.set_xticklabels(xticklabels, fontsize=10)
            else:
                ax.set_xticklabels([])

            # 只有最左列显示 y 轴刻度标签
            if col_idx == 0:
                ax.set_yticklabels(['-45°', '-30°', '-15°', '0°', '15°', '30°', '45°'], fontsize=10)
            else:
                ax.set_yticklabels([])

            ax.gridlines(draw_labels=False, linewidth=0.5, color='gray', alpha=0.4, linestyle='--')

            # 绘制散点
            ax.scatter(sub_df['lon'], sub_df['lat'], c=plot_diff, cmap=cmap, norm=norm,
                       s=5, alpha=0.7, transform=ccrs.PlateCarree())

    # 每行左侧标注季节
    axes[i, 0].text(-0.15, 0.5, season, va='center', ha='right',
                    fontsize=10, rotation=90,
                    transform=axes[i, 0].transAxes)

# ---- 添加颜色条 ----
# cbar_ax = fig.add_axes([0.22, 0.17, 0.6, 0.015])  # 根据你的要求设置colorbar位置和大小
cbar_ax = fig.add_axes([0.22, 0.28, 0.6, 0.015])


cbar = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap),
                    cax=cbar_ax, orientation='horizontal')
cbar.set_label('VTEC Difference (TECU)', fontsize=10)
cbar.ax.tick_params(labelsize=10)

# ---- 调整布局 ----
# plt.subplots_adjust(top=0.71,
#                     bottom=0.23,
#                     left=0.155,
#                     right=0.92,
#                     hspace=0.0,
#                     wspace=0.045)

# plt.subplots_adjust(top=0.73,
#                     bottom=0.29,
#                     left=0.155,
#                     right=0.92,
#                     hspace=0.0,
#                     wspace=0.045)


plt.subplots_adjust(top=0.73,
                    bottom=0.325,
                    left=0.155,
                    right=0.92,
                    hspace=0.0,
                    wspace=0.045)

# ---- 保存和显示 ----
save_path = r"F:\cosmic2gim\test1\14-code.png"
plt.savefig(save_path, dpi=900)
plt.show()
plt.close()  # 释放内存

print(f"✅ 图像已保存：{save_path}")
