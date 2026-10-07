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

special_stations = ["mkea", "bogt", "ykro", "iisc", "guam"]

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
# gl = ax.gridlines(draw_labels=False, linewidth=0.2, linestyle="--", color="gray")

gl = ax.gridlines(
    draw_labels=False,
    linewidth=0.1,
    linestyle="--",
    color=(0.5, 0.5, 0.5),  # 浅灰
    alpha=0.35
)



gl.xlocator = plt.FixedLocator(np.arange(-180, 181, 60))
gl.ylocator = plt.FixedLocator(np.arange(-90, 91, 30))

# 绘制 TEC 数据
pcm = ax.pcolormesh(
    tec.lon, tec.lat, tec.values,
    cmap="turbo", shading="auto", transform=ccrs.PlateCarree(),
)

# 绘制 30 个站点（红色上三角形）
ax.scatter(
    blh_df["lon"], blh_df["lat"],
    color="red", s=60, marker="^",
    transform=ccrs.PlateCarree(), zorder=6,
    label="GNSS stations (quiet & storm periods)"
)

# 绘制 5 个特殊站点（黄色下三角形）
special_df = blh_df.loc[blh_df.index.isin(special_stations)]
ax.scatter(
    special_df["lon"], special_df["lat"],
    color="yellow",
    edgecolors="black",
    s=60, marker="v",
    transform=ccrs.PlateCarree(), zorder=6,
    label="GNSS stations (year-round)"
)

# ------------------------
# 图例：放到主图上方，不遮挡
# ------------------------
# plt.legend(
#     loc="upper center",
#     bbox_to_anchor=(0.5, 1.08),
#     ncol=2,
#     frameon=False,
#     fontsize=20
# )

plt.legend(
    loc="lower center",
    bbox_to_anchor=(0.5, 0.95),  # 图像正上方
    ncol=1,                      # 关键：一列 → 上下两行
    frameon=False,
    fontsize=18,
    handlelength=1.5,
    labelspacing=0.4
)

plt.subplots_adjust(top=0.86)



# 保存图片
out_fig = "/home/yxlei/cosmic2gim/scripts/plots/figures/4.png"
os.makedirs(os.path.dirname(out_fig), exist_ok=True)
plt.savefig(out_fig, dpi=600, bbox_inches="tight")
plt.close()

print(f"✅ 全球 TEC + GNSS 站点分布图已保存至：{out_fig}")









# import os 
# import matplotlib.pyplot as plt
# import cartopy.crs as ccrs
# import cartopy.feature as cfeature
# import numpy as np
# import pandas as pd
# from ppgnss import gnss_utils, gnss_geodesy
# from adjustText import adjust_text

# # ------------------------
# # 1. 加载全球 TEC 数据
# # ------------------------
# xr_code = gnss_utils.loadobject("/mnt/geodata/GIM/CODG_1ch/CODG2024.obj")
# time_sel = np.datetime64("2024-01-01T00:00")
# tec = xr_code.sel(time=time_sel)

# # ------------------------
# # 2. 读取 GNSS 站点坐标
# # ------------------------
# coord_fn = "/mnt/public/igs-rinex-2024/stations.csv"

# stations = [
#     "abpo", "areq", "bogt", "cord", "cro1", "dgar", "glps", "gode", "godz", "gol2", "gold",
#     "guam", "hlfx", "hrao", "iisc", "kokb", "madr", "mkea", "nlib", "pie1", "pimo",
#     "pol2", "quin", "sant", "sthl", "suth", "tidb", "usn7", "usud", "ykro"
# ]

# special_stations = ["mkea", "bogt", "ykro", "iisc", "guam"]

# coord_df = pd.read_csv(coord_fn, names=["name", "num", "x", "y", "z"], header=0, index_col="name")
# coord_df.index = coord_df.index.str.lower()

# # 筛选站点并转换 ECEF -> BLH
# selected = coord_df.loc[coord_df.index.isin([s.lower() for s in stations])]
# blh_list = []
# for name, row in selected.iterrows():
#     lat, lon, hgt = gnss_geodesy.xyz2blh(row.x, row.y, row.z)
#     blh_list.append((name, lat, lon, hgt))
# blh_df = pd.DataFrame(blh_list, columns=["name", "lat", "lon", "hgt"]).set_index("name")

# # ------------------------
# # 3. 绘制全球 TEC 图 + 站点
# # ------------------------
# plt.figure(figsize=(12, 6))
# ax = plt.axes(projection=ccrs.Robinson())
# ax.set_global()

# # 底图
# ax.add_feature(cfeature.LAND, facecolor="lightgray", zorder=0)
# ax.add_feature(cfeature.OCEAN, facecolor="white", zorder=0)
# ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
# ax.add_feature(cfeature.BORDERS, linewidth=0.3)

# # 经纬网
# gl = ax.gridlines(draw_labels=False, linewidth=0.2, linestyle="--", color="gray")
# gl.xlocator = plt.FixedLocator(np.arange(-180, 181, 60))
# gl.ylocator = plt.FixedLocator(np.arange(-90, 91, 30))

# # 绘制 TEC 数据
# pcm = ax.pcolormesh(
#     tec.lon, tec.lat, tec.values,
#     cmap="turbo", shading="auto", transform=ccrs.PlateCarree(),
# )

# # 颜色条
# # cb = plt.colorbar(
# #     pcm, ax=ax, orientation="vertical", pad=0.05, fraction=0.035, shrink=0.85
# # )
# # cb.set_label("TEC (TECU)", fontsize=10)

# # 绘制 30 个站点（红色上三角形）
# ax.scatter(
#     blh_df["lon"], blh_df["lat"],
#     color="red", s=60, marker="^",
#     transform=ccrs.PlateCarree(), zorder=5, label="GNSS stations (quiet & storm periods)"
# )

# # 绘制 5 个特殊站点（黄色下三角形）
# special_df = blh_df.loc[blh_df.index.isin(special_stations)]
# ax.scatter(
#     special_df["lon"], special_df["lat"],
#     color="yellow", 
#     edgecolors="black", 
#     s=60, marker="v",
#     transform=ccrs.PlateCarree(), zorder=6, label="GNSS stations (year-round)"
# )

# # 标题与图例
# plt.title("GNSS Stations", fontsize=11, pad=15)
# plt.legend(loc="lower right")

# # 保存图片
# out_fig = "/home/yxlei/cosmic2gim/scripts/plots/figures/4.png"
# os.makedirs(os.path.dirname(out_fig), exist_ok=True)
# plt.savefig(out_fig, dpi=500, bbox_inches="tight")
# plt.close()

# print(f"✅ 全球 TEC + GNSS 站点分布图已保存至：{out_fig}")
















# import os
# import matplotlib.pyplot as plt
# import cartopy.crs as ccrs
# import cartopy.feature as cfeature
# import numpy as np
# import pandas as pd
# from ppgnss import gnss_utils, gnss_geodesy
# from adjustText import adjust_text

# # ------------------------
# # 1. 加载全球 TEC 数据
# # ------------------------
# xr_code = gnss_utils.loadobject("/mnt/geodata/GIM/CODG_1ch/CODG2024.obj")
# time_sel = np.datetime64("2024-01-01T00:00")
# tec = xr_code.sel(time=time_sel)

# # ------------------------
# # 2. 读取 GNSS 站点坐标
# # ------------------------
# coord_fn = "/mnt/public/igs-rinex-2024/stations.csv"
# stations = [
#     "abpo", "areq", "bogt", "cord", "cro1", "dgar", "glps", "gode", "godz", "gol2", "gold",
#     "guam", "hlfx", "hrao", "iisc", "kokb", "madr", "mkea", "nlib", "pie1", "pimo",
#     "pol2", "quin", "sant", "sthl", "suth", "tidb", "usn7", "usud", "ykro"
# ]

# coord_df = pd.read_csv(coord_fn, names=["name", "num", "x", "y", "z"], header=0, index_col="name")
# coord_df.index = coord_df.index.str.lower()

# # 筛选站点并转换 ECEF -> BLH
# selected = coord_df.loc[coord_df.index.isin([s.lower() for s in stations])]
# blh_list = []
# for name, row in selected.iterrows():
#     lat, lon, hgt = gnss_geodesy.xyz2blh(row.x, row.y, row.z)
#     blh_list.append((name, lat, lon, hgt))
# blh_df = pd.DataFrame(blh_list, columns=["name", "lat", "lon", "hgt"]).set_index("name")

# # ------------------------
# # 3. 绘制全球 TEC 图 + 站点
# # ------------------------
# plt.figure(figsize=(12, 6))
# ax = plt.axes(projection=ccrs.Robinson())
# ax.set_global()

# # 底图
# ax.add_feature(cfeature.LAND, facecolor="lightgray", zorder=0)
# ax.add_feature(cfeature.OCEAN, facecolor="white", zorder=0)
# ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
# ax.add_feature(cfeature.BORDERS, linewidth=0.3)

# # 经纬网
# gl = ax.gridlines(draw_labels=False, linewidth=0.2, linestyle="--", color="gray")
# gl.xlocator = plt.FixedLocator(np.arange(-180, 181, 60))
# gl.ylocator = plt.FixedLocator(np.arange(-90, 91, 30))

# # 绘制 TEC 数据
# pcm = ax.pcolormesh(
#     tec.lon, tec.lat, tec.values,
#     cmap="turbo", shading="auto", transform=ccrs.PlateCarree(),
# )

# # 颜色条放左边
# cb = plt.colorbar(
#     pcm, ax=ax, orientation="vertical", pad=0.05, fraction=0.035, shrink=0.85
# )
# cb.set_label("TEC (TECU)", fontsize=10)

# # 绘制 GNSS 站点：灰色三角形
# # ax.scatter(
# #     blh_df["lon"], blh_df["lat"],
# #     color="gray", s=40, marker="^",
# #     transform=ccrs.PlateCarree(), zorder=5, label="GNSS Station"
# # )

# ax.scatter(
#     blh_df["lon"], blh_df["lat"],
#     color="red", s=40, marker="^",
#     transform=ccrs.PlateCarree(), zorder=5, label="GNSS Station"
# )

# # # 添加站点名称（自动避免重叠）
# # texts = []
# # for name, row in blh_df.iterrows():
# #     txt = ax.text(
# #         row["lon"], row["lat"], name.upper(),
# #         fontsize=8, color="black", transform=ccrs.PlateCarree()
# #     )
# #     texts.append(txt)

# # adjust_text(
# #     texts, 
# #     ax=ax,
# #     expand_points=(1.2, 1.2),
# #     expand_text=(1.2, 1.4),
# #     arrowprops=dict(arrowstyle="-", color='gray', lw=0.5)
# # )

# # 标题
# plt.title("GNSS stations", fontsize=13, pad=15)
# plt.legend(loc="lower left")

# # 保存图片
# out_fig = "/home/yxlei/cosmic2gim/scripts/plots/figures/4.png"
# os.makedirs(os.path.dirname(out_fig), exist_ok=True)
# plt.savefig(out_fig, dpi=300, bbox_inches="tight")
# plt.close()

# print(f"✅ 全球 TEC + GNSS 站点分布图已保存至：{out_fig}")









# # import os
# # import matplotlib.pyplot as plt
# # import cartopy.crs as ccrs
# # import cartopy.feature as cfeature
# # import numpy as np
# # import pandas as pd
# # from ppgnss import gnss_utils, gnss_geodesy

# # # ------------------------
# # # 1. 读取 GNSS 站点坐标
# # # ------------------------
# # coord_fn = "/mnt/public/igs-rinex-2024/stations.csv"

# # # 全部 30 个站点
# # stations_30 = [
# #     "abpo", "areq", "bogt", "cord", "cro1", "dgar", "glps", "gode", "godz", "gol2", "gold",
# #     "guam", "hlfx", "hrao", "iisc", "kokb", "madr", "mkea", "nlib", "pie1", "pimo",
# #     "pol2", "quin", "sant", "sthl", "suth", "tidb", "usn7", "usud", "ykro"
# # ]

# # # 特别标出的 5 个站点
# # stations_5 = ["mkea", "bogt", "ykro", "iisc", "guam"]

# # coord_df = pd.read_csv(coord_fn, names=["name", "num", "x", "y", "z"], header=0, index_col="name")
# # coord_df.index = coord_df.index.str.lower()

# # # 提取 30 个站点并转换为经纬度
# # selected = coord_df.loc[coord_df.index.isin([s.lower() for s in stations_30])]
# # blh_list = []
# # for name, row in selected.iterrows():
# #     lat, lon, hgt = gnss_geodesy.xyz2blh(row.x, row.y, row.z)
# #     blh_list.append((name, lat, lon, hgt))
# # blh_df = pd.DataFrame(blh_list, columns=["name", "lat", "lon", "hgt"]).set_index("name")

# # # ------------------------
# # # 2. 绘制 GNSS 站点分布图
# # # ------------------------
# # plt.figure(figsize=(12, 6))
# # ax = plt.axes(projection=ccrs.Robinson())
# # ax.set_global()

# # # 底图
# # ax.add_feature(cfeature.LAND, facecolor="lightgray", zorder=0)
# # ax.add_feature(cfeature.OCEAN, facecolor="white", zorder=0)
# # ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
# # ax.add_feature(cfeature.BORDERS, linewidth=0.3)

# # # 经纬网
# # gl = ax.gridlines(draw_labels=False, linewidth=0.2, linestyle="--", color="gray")
# # gl.xlocator = plt.FixedLocator(np.arange(-180, 181, 60))
# # gl.ylocator = plt.FixedLocator(np.arange(-90, 91, 30))

# # # 绘制 30 个站点（红色上三角形）
# # ax.scatter(
# #     blh_df["lon"], blh_df["lat"],
# #     color="red", s=40, marker="^",
# #     transform=ccrs.PlateCarree(), zorder=5
# # )

# # # 绘制 5 个特别站点（红色下三角形）
# # special_df = blh_df.loc[blh_df.index.isin(stations_5)]
# # ax.scatter(
# #     special_df["lon"], special_df["lat"],
# #     color="red", s=60, marker="v",
# #     transform=ccrs.PlateCarree(), zorder=6
# # )

# # # 标题与图例
# # plt.title("Distribution of 30 GNSS Stations (5 Key in Red Down Triangles)", fontsize=13, pad=15)
# # plt.legend(loc="lower left")

# # # 保存图片
# # out_fig = "/home/yxlei/cosmic2gim/scripts/plots/figures/4.png"
# # os.makedirs(os.path.dirname(out_fig), exist_ok=True)
# # plt.savefig(out_fig, dpi=500, bbox_inches="tight")
# # plt.close()

# # print(f"✅ GNSS 站点分布图已保存至：{out_fig}")
