import os
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# ------------------------
# 参数与路径设置
# ------------------------
coord_fn = "/mnt/public/igs-rinex-2024/stations.csv"
out_fig = "/home/yxlei/cosmic2gim/scripts/plots/figures/4.png"

# 要绘制的站点列表

# # 30+5
# stations = [
#     "abpo", "areq", "bogt", "cord", "cro1", "dgar", "glps", "gode", "godz", "gol2", "gold",
#     "guam", "hlfx", "hrao", "iisc", "kokb", "madr", "mkea", "nlib", "pie1", "pimo",
#     "pol2", "quin", "sant", "sthl", "suth", "tidb", "usn7", "usud", "ykro",
#     # 重复提到的
#     "mkea", "bogt", "ykro", "iisc", "guam"
# ]

# 30
stations = [
    "abpo", "areq", "bogt", "cord", "cro1", "dgar", "glps", "gode", "godz", "gol2", "gold",
    "guam", "hlfx", "hrao", "iisc", "kokb", "madr", "mkea", "nlib", "pie1", "pimo",
    "pol2", "quin", "sant", "sthl", "suth", "tidb", "usn7", "usud", "ykro"
]

# ------------------------
# 1. 读取站点坐标
# ------------------------
coord_df = pd.read_csv(coord_fn, names=["name", "num", "x", "y", "z"], header=0, index_col="name")
coord_df.index = coord_df.index.str.lower()

# 筛选站点
selected = coord_df.loc[coord_df.index.isin([s.lower() for s in stations])].copy()

# 计算经纬度（ECEF -> BLH）
from ppgnss import gnss_geodesy
blh_list = []
for name, row in selected.iterrows():
    lat, lon, hgt = gnss_geodesy.xyz2blh(row.x, row.y, row.z)
    blh_list.append((name, lat, lon, hgt))

blh_df = pd.DataFrame(blh_list, columns=["name", "lat", "lon", "hgt"]).set_index("name")

# ------------------------
# 2. 绘制全球分布图
# ------------------------
plt.figure(figsize=(12, 6))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_global()

# 添加地理要素
ax.add_feature(cfeature.LAND, facecolor="lightgray")
ax.add_feature(cfeature.OCEAN, facecolor="aliceblue")
# ax.add_feature(cfeature.BORDERS, linewidth=0.5)
ax.add_feature(cfeature.COASTLINE, linewidth=0.6)
ax.gridlines(draw_labels=True, linewidth=0.3, linestyle="--", color="gray")

# 绘制站点
ax.scatter(
    blh_df["lon"], blh_df["lat"],
    color="red", s=40, marker="^", transform=ccrs.PlateCarree(), label="GNSS Station"
)

# # 添加站点名称标注
# for name, row in blh_df.iterrows():
#     ax.text(
#         row["lon"] + 2, row["lat"] + 0.5, name.upper(),
#         fontsize=8, color="darkred", transform=ccrs.PlateCarree()
#     )

from adjustText import adjust_text

texts = []
for name, row in blh_df.iterrows():
    txt = ax.text(
        row["lon"], row["lat"], name.upper(),
        fontsize=8, color="darkred",
        transform=ccrs.PlateCarree()
    )
    texts.append(txt)

# 自动调整文本避免重叠
adjust_text(
    texts, 
    ax=ax, 
    expand_points=(1.2, 1.2),
    expand_text=(1.2, 1.4),
    arrowprops=dict(arrowstyle="-", color='gray', lw=0.5)
)


# plt.title("Global Distribution of Selected GNSS Stations", fontsize=14)
plt.legend(loc="lower left")

# 保存图片
os.makedirs(os.path.dirname(out_fig), exist_ok=True)
plt.savefig(out_fig, dpi=300, bbox_inches="tight")
plt.close()

print(f"✅ GNSS 站点分布图已保存至：{out_fig}")
