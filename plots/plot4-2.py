# # import os
# # import matplotlib.pyplot as plt
# # import cartopy.crs as ccrs
# # import cartopy.feature as cfeature
# # import numpy as np
# # from ppgnss import gnss_utils

# # # ------------------------
# # # 1. 加载数据
# # # ------------------------
# # xr_code = gnss_utils.loadobject(f"/mnt/geodata/GIM/CODG_1ch/CODG2024.obj")

# # # 选择 2024-01-01 00:00 时刻
# # time_sel = np.datetime64("2024-01-01T00:00")
# # tec = xr_code.sel(time=time_sel)

# # # ------------------------
# # # 2. 绘图设置
# # # ------------------------
# # plt.figure(figsize=(12, 6))
# # ax = plt.axes(projection=ccrs.PlateCarree())
# # ax.set_global()

# # # 添加地理要素
# # ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
# # ax.add_feature(cfeature.BORDERS, linewidth=0.3)
# # ax.add_feature(cfeature.LAND, facecolor="lightgray", zorder=0)
# # ax.add_feature(cfeature.OCEAN, facecolor="white", zorder=0)

# # # 添加经纬网
# # gl = ax.gridlines(draw_labels=True, linewidth=0.3, linestyle="--", color="gray")
# # gl.top_labels = False
# # gl.right_labels = False

# # # ------------------------
# # # 3. 绘制全球TEC格网
# # # ------------------------
# # lon = tec.lon
# # lat = tec.lat
# # data = tec.values

# # # 绘制填色图
# # pcm = ax.pcolormesh(
# #     lon, lat, data,
# #     cmap="turbo", shading="auto", transform=ccrs.PlateCarree()
# # )

# # # 颜色条
# # cb = plt.colorbar(pcm, ax=ax, orientation="horizontal", pad=0.05, shrink=0.8)
# # cb.set_label("Total Electron Content (TECU)", fontsize=10)

# # # 标题
# # plt.title("Global Ionospheric TEC Map (CODG)\n2024-01-01 00:00 UTC", fontsize=14, pad=15)

# # # ------------------------
# # # 4. 保存图片
# # # ------------------------
# # out_fig = "/home/yxlei/cosmic2gim/scripts/plots/figures/tec_global_20240101_0000.png"
# # os.makedirs(os.path.dirname(out_fig), exist_ok=True)
# # plt.savefig(out_fig, dpi=300, bbox_inches="tight")
# # plt.close()

# # print(f"✅ 全球电离层TEC格网图已保存至：{out_fig}")



# import os
# import matplotlib.pyplot as plt
# import cartopy.crs as ccrs
# import cartopy.feature as cfeature
# import numpy as np
# from ppgnss import gnss_utils

# # ------------------------
# # 1. 加载数据
# # ------------------------
# xr_code = gnss_utils.loadobject(f"/mnt/geodata/GIM/CODG_1ch/CODG2024.obj")

# # 选择 2024-01-01 00:00 时刻
# time_sel = np.datetime64("2024-01-01T00:00")
# tec = xr_code.sel(time=time_sel)

# # ------------------------
# # 2. 绘图设置（椭圆形地图投影）
# # ------------------------
# plt.figure(figsize=(10, 6))
# # 使用 Robinson 投影（优雅的椭圆形全球投影）
# ax = plt.axes(projection=ccrs.Robinson())

# # 设置显示范围为全球
# ax.set_global()

# # 添加地理要素
# ax.add_feature(cfeature.LAND, facecolor="lightgray", zorder=0)
# ax.add_feature(cfeature.OCEAN, facecolor="white", zorder=0)
# ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
# ax.add_feature(cfeature.BORDERS, linewidth=0.3)

# # 添加经纬网
# gl = ax.gridlines(draw_labels=False, linewidth=0.3, linestyle="--", color="gray")
# gl.xlocator = plt.FixedLocator(np.arange(-180, 181, 60))
# gl.ylocator = plt.FixedLocator(np.arange(-90, 91, 30))

# # ------------------------
# # 3. 绘制全球TEC格网
# # ------------------------
# lon = tec.lon
# lat = tec.lat
# data = tec.values

# pcm = ax.pcolormesh(
#     lon, lat, data,
#     cmap="turbo", shading="auto", transform=ccrs.PlateCarree()
# )

# # ------------------------
# # 4. 颜色条放左边（垂直）
# # ------------------------
# cb = plt.colorbar(
#     pcm, ax=ax, orientation="vertical", pad=0.05, fraction=0.035, shrink=0.85
# )
# cb.set_label("Total Electron Content (TECU)", fontsize=10)

# # ------------------------
# # 5. 标题与保存
# # ------------------------
# plt.title("Global Ionospheric TEC Map (CODG)\n2024-01-01 00:00 UTC", fontsize=13, pad=15)

# out_fig = "/home/yxlei/cosmic2gim/scripts/plots/figures/tec_global_20240101_0000_robinson.png"
# os.makedirs(os.path.dirname(out_fig), exist_ok=True)
# plt.savefig(out_fig, dpi=300, bbox_inches="tight", transparent=False)
# plt.close()

# print(f"✅ 椭圆形全球电离层TEC格网图已保存至：{out_fig}")



import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import pandas as pd
from ppgnss import gnss_utils, gnss_geodesy
from adjustText import adjust_text

# ------------------------
# 1. 加载全球 TEC 数据
# ------------------------
xr_code = gnss_utils.loadobject("/mnt/geodata/GIM/CODG_1ch/CODG2024.obj")
time_sel = np.datetime64("2024-01-01T00:00")
tec = xr_code.sel(time=time_sel)

# ------------------------
# 2. 读取 GNSS 站点坐标
# ------------------------
coord_fn = "/mnt/public/igs-rinex-2024/stations.csv"
stations = [
    "abpo", "areq", "bogt", "cord", "cro1", "dgar", "glps", "gode", "godz", "gol2", "gold",
    "guam", "hlfx", "hrao", "iisc", "kokb", "madr", "mkea", "nlib", "pie1", "pimo",
    "pol2", "quin", "sant", "sthl", "suth", "tidb", "usn7", "usud", "ykro"
]

coord_df = pd.read_csv(coord_fn, names=["name", "num", "x", "y", "z"], header=0, index_col="name")
coord_df.index = coord_df.index.str.lower()

# 筛选站点并转换 ECEF -> BLH
selected = coord_df.loc[coord_df.index.isin([s.lower() for s in stations])]
blh_list = []
for name, row in selected.iterrows():
    lat, lon, hgt = gnss_geodesy.xyz2blh(row.x, row.y, row.z)
    blh_list.append((name, lat, lon, hgt))
blh_df = pd.DataFrame(blh_list, columns=["name", "lat", "lon", "hgt"]).set_index("name")

# ------------------------
# 3. 绘制全球 TEC 图 + 站点
# ------------------------
plt.figure(figsize=(12, 6))
ax = plt.axes(projection=ccrs.Robinson())
ax.set_global()

# 底图
ax.add_feature(cfeature.LAND, facecolor="lightgray", zorder=0)
ax.add_feature(cfeature.OCEAN, facecolor="white", zorder=0)
ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
ax.add_feature(cfeature.BORDERS, linewidth=0.3)

# 经纬网
gl = ax.gridlines(draw_labels=False, linewidth=0.2, linestyle="--", color="gray")
gl.xlocator = plt.FixedLocator(np.arange(-180, 181, 60))
gl.ylocator = plt.FixedLocator(np.arange(-90, 91, 30))

# 绘制 TEC 数据
pcm = ax.pcolormesh(
    tec.lon, tec.lat, tec.values,
    cmap="turbo", shading="auto", transform=ccrs.PlateCarree(),
)

# 颜色条放左边
cb = plt.colorbar(
    pcm, ax=ax, orientation="vertical", pad=0.05, fraction=0.035, shrink=0.85
)
cb.set_label("TEC (TECU)", fontsize=10)

# 绘制 GNSS 站点：灰色三角形
# ax.scatter(
#     blh_df["lon"], blh_df["lat"],
#     color="gray", s=40, marker="^",
#     transform=ccrs.PlateCarree(), zorder=5, label="GNSS Station"
# )

ax.scatter(
    blh_df["lon"], blh_df["lat"],
    color="red", s=40, marker="^",
    transform=ccrs.PlateCarree(), zorder=5, label="GNSS Station"
)

# # 添加站点名称（自动避免重叠）
# texts = []
# for name, row in blh_df.iterrows():
#     txt = ax.text(
#         row["lon"], row["lat"], name.upper(),
#         fontsize=8, color="black", transform=ccrs.PlateCarree()
#     )
#     texts.append(txt)

# adjust_text(
#     texts, 
#     ax=ax,
#     expand_points=(1.2, 1.2),
#     expand_text=(1.2, 1.4),
#     arrowprops=dict(arrowstyle="-", color='gray', lw=0.5)
# )

# 标题
plt.title("GNSS stations and TEC map", fontsize=13, pad=15)
plt.legend(loc="lower left")

# 保存图片
out_fig = "/home/yxlei/cosmic2gim/scripts/plots/figures/4-2.png"
os.makedirs(os.path.dirname(out_fig), exist_ok=True)
plt.savefig(out_fig, dpi=300, bbox_inches="tight")
plt.close()

print(f"✅ 全球 TEC + GNSS 站点分布图已保存至：{out_fig}")
