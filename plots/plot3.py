import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib import ticker

# 1. 加载数据文件
data = pd.read_pickle(r"/home/yxlei/cosmic2gim/data/prof_2024YEAR_data.pkl")

# 2. 确保时间列是datetime类型
data['time'] = pd.to_datetime(data['time'])

# 3. 提取2024年1月3日的数据
data_feb_1 = data[data['time'].dt.date == pd.to_datetime('2024-01-03').date()]

# 4. 提取经纬度和电子密度（vtec）
latitudes_1 = data_feb_1['lat']
longitudes_1 = data_feb_1['lon']

# 5. 提取2024年1月3日00:00到01:00的数据
start_time = pd.to_datetime('2024-01-03 00:00')
end_time = pd.to_datetime('2024-01-03 01:00')
data_feb_1_01_to_02 = data[(data['time'] >= start_time) & (data['time'] < end_time)]

# 6. 提取经纬度
latitudes_2 = data_feb_1_01_to_02['lat']
longitudes_2 = data_feb_1_01_to_02['lon']

# 7. 创建一个画布，包含两个子图
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10
fig, axes = plt.subplots(1, 2, figsize=(8, 3), subplot_kw={'projection': ccrs.EqualEarth()})

# --- 子图 (a) 绘制2024年1月3日的数据 ---
ax1 = axes[0]
ax1.set_global()  # 设置为全球显示
# ax1.add_feature(cfeature.BORDERS, linestyle=':', edgecolor='gray')  # 添加国界
ax1.add_feature(cfeature.COASTLINE, edgecolor='gray', linewidth=0.2)  # 添加海岸线
ax1.add_feature(cfeature.LAND, facecolor='lightgray')  # 添加陆地
gl = ax1.gridlines(
    draw_labels=True,
    dms=True,
    linewidth=0.3,
    color='gray',
    alpha=0.5
)
gl.top_labels = False
gl.right_labels = False
gl.xlocator = ticker.FixedLocator([-180, -90, 0, 90, 180])
ax1.scatter(longitudes_1, latitudes_1, c='#1f78b4', s=2, transform=ccrs.PlateCarree())

ax1.set_xlabel('Longitude')
ax1.set_ylabel('Latitude')

# 添加子图标题 (a) 在子图的下方
ax1.text(0.5, -0.2, '(a)', ha='center', va='center', transform=ax1.transAxes, fontsize=12)

# --- 子图 (b) 绘制01:00-02:00的数据 ---
ax2 = axes[1]
ax2.set_global()  # 设置为全球显示
# ax2.add_feature(cfeature.BORDERS, linestyle=':', edgecolor='gray')  # 添加国界
ax2.add_feature(cfeature.COASTLINE, edgecolor='gray', linewidth=0.2)  # 添加海岸线
ax2.add_feature(cfeature.LAND, facecolor='lightgray')  # 添加陆地
gl = ax2.gridlines(
    draw_labels=True,
    dms=True,
    linewidth=0.3,
    color='gray',
    alpha=0.5
)
gl.top_labels = False
gl.right_labels = False
gl.xlocator = ticker.FixedLocator([-180, -90, 0, 90, 180])
ax2.scatter(longitudes_2, latitudes_2, c='#1f78b4', s=2, transform=ccrs.PlateCarree())

ax2.set_xlabel('Longitude')
ax2.set_ylabel('Latitude')

# 添加子图标题 (b) 在子图的下方
ax2.text(0.5, -0.2, '(b)', ha='center', va='center', transform=ax2.transAxes, fontsize=12)

# 8. 调整布局
plt.tight_layout()



# 9. 保存图像到本地文件夹
output_path = r"/home/yxlei/cosmic2gim/scripts/plots/figures/3.png"
plt.savefig(output_path, dpi=700, bbox_inches='tight')

# 9. 显示图像
plt.show()