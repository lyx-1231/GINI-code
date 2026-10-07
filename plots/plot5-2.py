import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import pandas as pd
from datetime import datetime
from ppgnss import gnss_utils
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

# ==================== 1. 文件路径 ====================
data_file = "/home/yxlei/cosmic2gim/data/Jason/jason3_vtec_2024.obj"
output_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "5.png")

# ==================== 2. 读取保存的VTEC数据 ====================
df_all = gnss_utils.loadobject(data_file)
print("✅ Loaded data:", df_all.shape)
print(df_all.head())

# ==================== 3. 选择特定日期（示例：2024-03-15） ====================
df_all["time"] = pd.to_datetime(df_all["time"])
day_sel = datetime(2024, 3, 15)
df_day = df_all[df_all["time"].dt.date == day_sel.date()]

if df_day.empty:
    raise ValueError(f"❌ 没有找到 {day_sel.date()} 的数据，请换一天再试。")
print(f"✅ Selected {len(df_day)} points for {day_sel.date()}")

# ==================== 4. 基本设置 ====================
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 15

extent = [-180, 180, -80, 80]  # Jason轨道主要范围

# ==================== 5. 创建画布（上下两幅） ====================
fig, axes = plt.subplots(
    2, 1, figsize=(10, 7),
    subplot_kw={'projection': ccrs.PlateCarree()},
    gridspec_kw={
        'hspace': 0.10,   # ↑ 间距略微增大（原 0.05 → 0.10）
        'top': 0.97,
        'bottom': 0.07,
        'left': 0.09,
        'right': 0.88    # ← 缩小左右空隙（原 0.87 → 0.88）
    }
)

# ==================== 6. 定义绘图函数 ====================
def plot_vtec(ax, lons, lats, tecs, title_label):
    mask = np.isfinite(tecs)
    lons, lats, tecs = lons[mask], lats[mask], tecs[mask]

    ax.set_extent(extent, crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND, facecolor='white', edgecolor='black', linewidth=0.3)
    ax.add_feature(cfeature.OCEAN, facecolor='white')
    ax.coastlines(linewidth=0.5)
    ax.set_xticks(np.arange(-180, 181, 60), crs=ccrs.PlateCarree())
    ax.set_yticks(np.arange(-60, 61, 30), crs=ccrs.PlateCarree())
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    ax.tick_params(labelsize=15)

    sc = ax.scatter(
        lons, lats, c=tecs, s=1,
        cmap='turbo', vmin=0, vmax=110,
        transform=ccrs.PlateCarree()
    )

    ax.text(-175, 72, title_label, fontsize=15, fontweight='normal')

    return sc

# ==================== 7. 绘制上图 (a)：单日轨迹 ====================
sc1 = plot_vtec(
    axes[0],
    df_day["lon"].values,
    df_day["lat"].values,
    df_day["tec"].values,
    "(a)"
)

# ==================== 8. 绘制下图 (b)：全年轨迹 ====================
sc2 = plot_vtec(
    axes[1],
    df_all["lon"].values,
    df_all["lat"].values,
    df_all["tec"].values,
    "(b)"
)

# ==================== 9. 共用竖直 colorbar ====================
# 调整 colorbar 更贴近图像（原 left=0.89 → 0.885）
cbar_ax = fig.add_axes([0.875, 0.18, 0.02, 0.63])
cb = fig.colorbar(sc2, cax=cbar_ax, orientation='vertical')
cb.set_label('VTEC (TECU)', fontsize=15)
cb.ax.tick_params(labelsize=15)

# ==================== 10. 保存结果 ====================
plt.savefig(output_path, dpi=800)
plt.close()
print(f"✅ Saved figure to: {output_path}")




# import os
# import matplotlib.pyplot as plt
# import cartopy.crs as ccrs
# import cartopy.feature as cfeature
# import numpy as np
# import pandas as pd
# from datetime import datetime
# from ppgnss import gnss_utils
# from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

# # ==================== 1. 文件路径 ====================
# data_file = "/home/yxlei/cosmic2gim/data/Jason/jason3_vtec_2024.obj"
# output_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
# os.makedirs(output_dir, exist_ok=True)
# output_path = os.path.join(output_dir, "5.png")

# # ==================== 2. 读取保存的VTEC数据 ====================
# df_all = gnss_utils.loadobject(data_file)
# print("✅ Loaded data:", df_all.shape)
# print(df_all.head())

# # ==================== 3. 选择特定日期（示例：2024-03-15） ====================
# df_all["time"] = pd.to_datetime(df_all["time"])
# day_sel = datetime(2024, 3, 15)
# df_day = df_all[df_all["time"].dt.date == day_sel.date()]

# if df_day.empty:
#     raise ValueError(f"❌ 没有找到 {day_sel.date()} 的数据，请换一天再试。")
# print(f"✅ Selected {len(df_day)} points for {day_sel.date()}")

# # ==================== 4. 基本设置 ====================
# plt.rcParams['font.family'] = 'Arial'
# plt.rcParams['font.size'] = 10

# extent = [-180, 180, -80, 80]  # Jason轨道主要范围

# # ==================== 5. 创建画布（上下两幅） ====================
# fig, axes = plt.subplots(
#     2, 1, figsize=(10, 7),
#     subplot_kw={'projection': ccrs.PlateCarree()},
#     gridspec_kw={
#         'hspace': 0.10,   # ↑ 间距略微增大（原 0.05 → 0.10）
#         'top': 0.97,
#         'bottom': 0.07,
#         'left': 0.09,
#         'right': 0.88    # ← 缩小左右空隙（原 0.87 → 0.88）
#     }
# )

# # ==================== 6. 定义绘图函数 ====================
# def plot_vtec(ax, lons, lats, tecs, title_label):
#     mask = np.isfinite(tecs)
#     lons, lats, tecs = lons[mask], lats[mask], tecs[mask]

#     ax.set_extent(extent, crs=ccrs.PlateCarree())
#     ax.add_feature(cfeature.LAND, facecolor='white', edgecolor='black', linewidth=0.3)
#     ax.add_feature(cfeature.OCEAN, facecolor='white')
#     ax.coastlines(linewidth=0.5)
#     ax.set_xticks(np.arange(-180, 181, 60), crs=ccrs.PlateCarree())
#     ax.set_yticks(np.arange(-60, 61, 30), crs=ccrs.PlateCarree())
#     ax.xaxis.set_major_formatter(LongitudeFormatter())
#     ax.yaxis.set_major_formatter(LatitudeFormatter())
#     ax.tick_params(labelsize=9)

#     sc = ax.scatter(
#         lons, lats, c=tecs, s=1,
#         cmap='turbo', vmin=0, vmax=110,
#         transform=ccrs.PlateCarree()
#     )

#     ax.text(-175, 72, title_label, fontsize=11, fontweight='normal')

#     return sc

# # ==================== 7. 绘制上图 (a)：单日轨迹 ====================
# sc1 = plot_vtec(
#     axes[0],
#     df_day["lon"].values,
#     df_day["lat"].values,
#     df_day["tec"].values,
#     "(a)"
# )

# # ==================== 8. 绘制下图 (b)：全年轨迹 ====================
# sc2 = plot_vtec(
#     axes[1],
#     df_all["lon"].values,
#     df_all["lat"].values,
#     df_all["tec"].values,
#     "(b)"
# )

# # ==================== 9. 共用竖直 colorbar ====================
# # 调整 colorbar 更贴近图像（原 left=0.89 → 0.885）
# cbar_ax = fig.add_axes([0.875, 0.18, 0.02, 0.63])
# cb = fig.colorbar(sc2, cax=cbar_ax, orientation='vertical')
# cb.set_label('VTEC (TECU)', fontsize=10)
# cb.ax.tick_params(labelsize=9)

# # ==================== 10. 保存结果 ====================
# plt.savefig(output_path, dpi=800)
# plt.close()
# print(f"✅ Saved figure to: {output_path}")









# import os
# import matplotlib.pyplot as plt
# import cartopy.crs as ccrs
# import cartopy.feature as cfeature
# import numpy as np
# import pandas as pd
# from datetime import datetime
# from ppgnss import gnss_utils
# from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

# # ==================== 1. 文件路径 ====================
# data_file = "/home/yxlei/cosmic2gim/data/Jason/jason3_vtec_2024.obj"
# output_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
# os.makedirs(output_dir, exist_ok=True)
# output_path = os.path.join(output_dir, "5.png")

# # ==================== 2. 读取保存的VTEC数据 ====================
# df_all = gnss_utils.loadobject(data_file)
# print("✅ Loaded data:", df_all.shape)
# print(df_all.head())

# # ==================== 3. 选择特定日期（示例：2024-03-15） ====================
# df_all["time"] = pd.to_datetime(df_all["time"])
# day_sel = datetime(2024, 3, 15)
# df_day = df_all[df_all["time"].dt.date == day_sel.date()]

# if df_day.empty:
#     raise ValueError(f"❌ 没有找到 {day_sel.date()} 的数据，请换一天再试。")
# print(f"✅ Selected {len(df_day)} points for {day_sel.date()}")

# # ==================== 4. 基本设置 ====================
# plt.rcParams['font.family'] = 'Arial'
# plt.rcParams['font.size'] = 10

# # 经纬度范围（Jason轨道主要覆盖 ±80°）
# extent = [-180, 180, -80, 80]

# # ==================== 5. 创建画布（上下两幅） ====================
# fig, axes = plt.subplots(
#     2, 1, figsize=(10, 7),
#     subplot_kw={'projection': ccrs.PlateCarree()},
#     gridspec_kw={'hspace': 0.05, 'top': 0.97, 'bottom': 0.07, 'left': 0.08, 'right': 0.87}
# )

# # ==================== 6. 定义绘图函数 ====================
# def plot_vtec(ax, lons, lats, tecs, title_label):
#     # 去除无效值
#     mask = np.isfinite(tecs)
#     lons, lats, tecs = lons[mask], lats[mask], tecs[mask]

#     # 绘制背景
#     ax.set_extent(extent, crs=ccrs.PlateCarree())
#     ax.add_feature(cfeature.LAND, facecolor='white', edgecolor='black', linewidth=0.3)
#     ax.add_feature(cfeature.OCEAN, facecolor='white')
#     ax.coastlines(linewidth=0.5)
#     ax.set_xticks(np.arange(-180, 181, 60), crs=ccrs.PlateCarree())
#     ax.set_yticks(np.arange(-60, 61, 30), crs=ccrs.PlateCarree())
#     ax.xaxis.set_major_formatter(LongitudeFormatter())
#     ax.yaxis.set_major_formatter(LatitudeFormatter())
#     ax.tick_params(labelsize=9)

#     # 绘制散点
#     sc = ax.scatter(
#         lons, lats, c=tecs, s=1,
#         cmap='turbo', vmin=0, vmax=150,
#         transform=ccrs.PlateCarree()
#     )

#     # 添加小标题 (a)、(b)
#     ax.text(-175, 72, title_label, fontsize=11, fontweight='normal')

#     return sc

# # ==================== 7. 绘制上图 (a)：单日轨迹 ====================
# sc1 = plot_vtec(axes[0],
#                 df_day["lon"].values,
#                 df_day["lat"].values,
#                 df_day["tec"].values,
#                 "(a) Jason-3 VTEC (2024-03-15)")

# # ==================== 8. 绘制下图 (b)：全年轨迹 ====================
# sc2 = plot_vtec(axes[1],
#                 df_all["lon"].values,
#                 df_all["lat"].values,
#                 df_all["tec"].values,
#                 "(b) Jason-3 VTEC (2024 All Year)")

# # ==================== 9. 共用竖直 colorbar ====================
# cbar_ax = fig.add_axes([0.89, 0.18, 0.02, 0.63])  # [left, bottom, width, height]
# cb = fig.colorbar(sc2, cax=cbar_ax, orientation='vertical')
# cb.set_label('VTEC (TECU)', fontsize=10)
# cb.ax.tick_params(labelsize=9)

# # ==================== 10. 保存结果 ====================
# plt.savefig(output_path, dpi=300)
# plt.close()
# print(f"✅ Saved figure to: {output_path}")
