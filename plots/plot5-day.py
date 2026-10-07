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
output_path = os.path.join(output_dir, "5-day.png")

# ==================== 2. 读取保存的VTEC数据 ====================
df_all = gnss_utils.loadobject(data_file)
print("✅ Loaded data:", df_all.shape)
print(df_all.head())

# ==================== 3. 选择特定日期（示例：2024-03-15） ====================
df_all["time"] = pd.to_datetime(df_all["time"])
day_sel = datetime(2024, 3, 15)  # 可改为你想看的日期
df_day = df_all[df_all["time"].dt.date == day_sel.date()]

if df_day.empty:
    raise ValueError(f"❌ 没有找到 {day_sel.date()} 的数据，请换一天再试。")

print(f"✅ Selected {len(df_day)} points for {day_sel.date()}")

# ==================== 4. 基本设置 ====================
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10

# 经纬度与TEC数据
lons = df_day["lon"].values
lats = df_day["lat"].values
tecs = df_day["tec"].values

# 去掉无效值
mask = np.isfinite(tecs)
lons = lons[mask]
lats = lats[mask]
tecs = tecs[mask]

# ==================== 5. 创建地图 ====================
fig = plt.figure(figsize=(10, 4))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_global()

# 地理要素
ax.add_feature(cfeature.LAND, facecolor='white', edgecolor='black', linewidth=0.3)
ax.add_feature(cfeature.OCEAN, facecolor='white')
# ax.add_feature(cfeature.BORDERS, linewidth=0.4)
ax.coastlines(linewidth=0.6)

# 经纬度范围（Jason轨道主要覆盖 ±80°）
ax.set_extent([-180, 180, -80, 80], crs=ccrs.PlateCarree())

# 经纬度刻度
ax.set_xticks(np.arange(-180, 181, 60), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(-60, 61, 30), crs=ccrs.PlateCarree())
ax.xaxis.set_major_formatter(LongitudeFormatter())
ax.yaxis.set_major_formatter(LatitudeFormatter())
ax.tick_params(labelsize=9)

# ==================== 6. 绘制VTEC分布 ====================
sc = ax.scatter(
    lons, lats, c=tecs, s=1,
    cmap='turbo', vmin=0, vmax=110,
    transform=ccrs.PlateCarree()
)

# ==================== 7. 添加颜色条 ====================
# 让 colorbar 贴近上图，但不重叠
cb_ax = fig.add_axes([0.155, 0.18, 0.765, 0.03])  # 手动精确控制位置
cb = plt.colorbar(sc, cax=cb_ax, orientation='horizontal')
cb.set_label('VTEC (TECU)', fontsize=10)
cb.ax.tick_params(labelsize=9)

# ==================== 8. 保存结果 ====================
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"✅ Saved figure to: {output_path}")
