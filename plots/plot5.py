import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from ppgnss import gnss_utils
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter 

# ==================== 1. 文件路径 ====================
data_file = "/home/yxlei/cosmic2gim/data/Jason/jason3_vtec_2024.obj"
output_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "5-year.png")

# ==================== 2. 读取保存的VTEC数据 ====================
df_all = gnss_utils.loadobject(data_file)
print("Loaded data:", df_all.shape)
print(df_all.head())

# ==================== 3. 基本设置 ====================
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10

# 经纬度与TEC数据
lons = df_all["lon"].values
lats = df_all["lat"].values
tecs = df_all["tec"].values

# 去掉无效值
mask = np.isfinite(tecs)
lons = lons[mask]
lats = lats[mask]
tecs = tecs[mask]

# ==================== 4. 创建地图 ====================
fig = plt.figure(figsize=(10, 4))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_global()

# 地理要素：陆地白色、海洋浅蓝、边界线清晰
ax.add_feature(cfeature.LAND, facecolor='white', edgecolor='black', linewidth=0.3)
ax.add_feature(cfeature.OCEAN, facecolor='white')  
# ax.add_feature(cfeature.BORDERS, linewidth=0.4)
ax.coastlines(linewidth=0.6)

# 经纬度范围（Jason轨道主要覆盖 ±80°）
ax.set_extent([-180, 180, -80, 80], crs=ccrs.PlateCarree())

# 添加经纬度刻度线
ax.set_xticks(np.arange(-180, 181, 60), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-60, 61, 30), crs=ccrs.PlateCarree())
lon_formatter = LongitudeFormatter()
lat_formatter = LatitudeFormatter()
ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)
ax.tick_params(labelsize=9)

# ==================== 5. 绘制VTEC分布 ====================
sc = ax.scatter(lons, lats, c=tecs, s=1, cmap='turbo',
                vmin=0, vmax=110, transform=ccrs.PlateCarree())

# ==================== 6. 添加颜色条 ====================
cb = plt.colorbar(sc, orientation='horizontal', pad=0.05, fraction=0.05)
cb.set_label('VTEC (TECU)', fontsize=10)
cb.ax.tick_params(labelsize=9)

# ==================== 7. 添加标题并保存 ====================
# plt.title("Jason-3 VTEC Distribution (2024)", fontsize=11, pad=10)
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()

print(f"✅ Saved figure to: {output_path}")









# import os
# import matplotlib.pyplot as plt
# import cartopy.crs as ccrs
# import cartopy.feature as cfeature
# import numpy as np
# from ppgnss import gnss_utils

# # ==================== 1. 文件路径 ====================
# data_file = "/home/yxlei/cosmic2gim/data/Jason/jason3_vtec_2024.obj"
# output_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
# os.makedirs(output_dir, exist_ok=True)
# output_path = os.path.join(output_dir, "iono.png")

# # ==================== 2. 读取保存的VTEC数据 ====================
# df_all = gnss_utils.loadobject(data_file)
# print("Loaded data:", df_all.shape)
# print(df_all.head())

# # ==================== 3. 基本设置 ====================
# plt.rcParams['font.family'] = 'Arial'
# plt.rcParams['font.size'] = 10

# # 经纬度数据
# lons = df_all["lon"].values
# lats = df_all["lat"].values
# tecs = df_all["tec"].values

# # 去掉无效值
# mask = np.isfinite(tecs)
# lons = lons[mask]
# lats = lats[mask]
# tecs = tecs[mask]

# # ==================== 4. 创建地图 ====================
# fig = plt.figure(figsize=(10, 4))
# ax = plt.axes(projection=ccrs.PlateCarree())
# ax.set_global()
# ax.coastlines(linewidth=0.6)
# ax.add_feature(cfeature.BORDERS, linewidth=0.3)
# ax.add_feature(cfeature.LAND, facecolor='lightgray')
# ax.add_feature(cfeature.OCEAN, facecolor='white')

# # ==================== 5. 绘制VTEC分布 ====================
# sc = ax.scatter(lons, lats, c=tecs, s=1, cmap='turbo', transform=ccrs.PlateCarree())

# # 设置经纬度范围（Jason 是近南北轨道，可以适当缩放）
# ax.set_xlim(-180, 180)
# ax.set_ylim(-80, 80)

# # ==================== 6. 添加色标 ====================
# cb = plt.colorbar(sc, orientation='horizontal', pad=0.04, fraction=0.05)
# cb.set_label('VTEC (TECU)')

# # ==================== 7. 保存结果 ====================
# plt.title("Jason-3 VTEC Distribution (2024)")
# plt.savefig(output_path, dpi=300, bbox_inches='tight')
# plt.close()

# print(f"Saved figure to {output_path}")
