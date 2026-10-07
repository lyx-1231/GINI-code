# import os
# import pandas as pd
# import matplotlib.pyplot as plt
# import cartopy.crs as ccrs
# import cartopy.feature as cfeature

# # ----------------- 1. 读取差分结果 DataFrame -----------------
# code_path = "/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_code_2024_all.pkl"
# df_code = pd.read_pickle(code_path)

# # ----------------- 2. 统一站点名大小写 -----------------
# df_code["site"] = df_code["site"].str.upper()

# # ----------------- 3. 清理缺失经纬度数据 -----------------
# df_code = df_code.dropna(subset=["lat", "lon"])

# # ----------------- 4. 绘图 -----------------
# plt.rcParams["font.family"] = "Arial"
# plt.rcParams["font.size"] = 10

# fig = plt.figure(figsize=(12.9/2.54, 3.5))
# ax = plt.axes(projection=ccrs.Robinson())
# ax.set_global()

# # 底图
# ax.add_feature(cfeature.LAND, facecolor="lightgray")
# ax.add_feature(cfeature.OCEAN, facecolor="white")
# ax.add_feature(cfeature.COASTLINE, linewidth=0.2)
# # ax.add_feature(cfeature.BORDERS, linewidth=0.3)
# ax.gridlines(draw_labels=False, linewidth=0.2, linestyle="--", color="gray", alpha=0.7)

# # 绘制穿刺点分布，散点小且半透明
# ax.scatter(
#     df_code["lon"], df_code["lat"],
#     color="#63abdf", s=0.5, alpha=0.5,
#     transform=ccrs.PlateCarree(),
#     label="IPPs"
# )

# # 标题与图例
# # ax.set_title("Global Distribution of CODE TEC Ionospheric Pierce Points (2024)", fontsize=12, pad=10)
# ax.legend(loc="lower left", fontsize=10, frameon=True)

# plt.tight_layout()

# # ----------------- 5. 保存图像 -----------------
# output_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
# os.makedirs(output_dir, exist_ok=True)
# output_path = os.path.join(output_dir, "10-ipps.png")
# plt.savefig(output_path, dpi=400, bbox_inches="tight")
# plt.close()

# print(f"✅ CODE TEC 穿刺点经纬度分布图已保存至：{output_path}")



# import os
# import pandas as pd
# import matplotlib.pyplot as plt
# import cartopy.crs as ccrs
# import cartopy.feature as cfeature

# # ----------------- 1. 读取差分结果 DataFrame -----------------
# code_path = "/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_code_2024_all.pkl"
# df_code = pd.read_pickle(code_path)

# # ----------------- 2. 统一站点名大小写 -----------------
# df_code["site"] = df_code["site"].str.upper()

# # ----------------- 3. 清理缺失经纬度数据 -----------------
# df_code = df_code.dropna(subset=["lat", "lon"])

# # ----------------- 4. 绘图 -----------------
# plt.rcParams["font.family"] = "Arial"
# plt.rcParams["font.size"] = 10

# fig = plt.figure(figsize=(12.9/2.54, 3.5))
# # 保持罗宾逊投影，以保留椭圆形状
# ax = plt.axes(projection=ccrs.Robinson())

# # --- 关键修改：设置视图范围 ---
# # 使用 set_extent 替代 set_global()，将范围限制在经度[-180, 180]和纬度[-45, 45]
# # 并指定范围坐标系为 PlateCarree
# ax.set_extent([-180, 180, -45, 45], crs=ccrs.PlateCarree())
# # -----------------------------

# # 底图
# ax.add_feature(cfeature.LAND, facecolor="lightgray")
# ax.add_feature(cfeature.OCEAN, facecolor="white")
# ax.add_feature(cfeature.COASTLINE, linewidth=0.2)
# # ax.add_feature(cfeature.BORDERS, linewidth=0.3)
# ax.gridlines(draw_labels=False, linewidth=0.2, linestyle="--", color="gray", alpha=0.7)

# # 绘制穿刺点分布，散点小且半透明
# # 筛选数据，只保留纬度在 [-45, 45] 范围内的点，以避免超出显示范围的点影响绘图效率或显示
# df_subset = df_code[(df_code['lat'] >= -45) & (df_code['lat'] <= 45)]

# ax.scatter(
#     df_subset["lon"], df_subset["lat"],
#     color="#63abdf", s=0.5, alpha=0.5,
#     transform=ccrs.PlateCarree(),
#     label="IPPs"
# )

# # 标题与图例
# # ax.set_title("Global Distribution of CODE TEC Ionospheric Pierce Points (2024)", fontsize=12, pad=10)
# ax.legend(loc="lower left", fontsize=10, frameon=True)

# plt.tight_layout()

# # ----------------- 5. 保存图像 -----------------
# output_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
# os.makedirs(output_dir, exist_ok=True)
# output_path = os.path.join(output_dir, "10-ipps_lat45.png") # 更改文件名以区分
# plt.savefig(output_path, dpi=400, bbox_inches="tight")
# plt.close()

# print(f"✅ CODE TEC 穿刺点经纬度分布图 (纬度[-45, 45]) 已保存至：{output_path}")





import os
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# ----------------- 1. 读取差分结果 DataFrame -----------------
code_path = "/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_code_2024_all.pkl"
df_code = pd.read_pickle(code_path)

# ----------------- 2. 统一站点名大小写 -----------------
df_code["site"] = df_code["site"].str.upper()

# ----------------- 3. 清理缺失经纬度数据 -----------------
df_code = df_code.dropna(subset=["lat", "lon"])

# ----------------- 4. 筛选指定日期 -----------------
# 假设时间列名为 'time'，格式是 datetime64[ns]，如果不是，可以先转换：
df_code['time'] = pd.to_datetime(df_code['time'])

# 设置目标日期，比如 2024-06-15
target_date = pd.Timestamp("2024-01-01")

# 只选这一天的数据（忽略时间，只比对日期部分）
df_code_day = df_code[df_code['time'].dt.date == target_date.date()]

# ----------------- 5. 绘图 -----------------
plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = 10

fig = plt.figure(figsize=(12.9/2.54, 3.5))
ax = plt.axes(projection=ccrs.Robinson())

ax.set_extent([-180, 180, -45, 45], crs=ccrs.PlateCarree())

ax.add_feature(cfeature.LAND, facecolor="lightgray")
ax.add_feature(cfeature.OCEAN, facecolor="white")
ax.add_feature(cfeature.COASTLINE, linewidth=0.2)
ax.gridlines(draw_labels=False, linewidth=0.2, linestyle="--", color="gray", alpha=0.7)

# 只保留纬度在[-45, 45]范围内
df_subset = df_code_day[(df_code_day['lat'] >= -45) & (df_code_day['lat'] <= 45)]

ax.scatter(
    df_subset["lon"], df_subset["lat"],
    color="#63abdf", s=0.1, alpha=0.5,
    transform=ccrs.PlateCarree(),
    label=f"IPPs on {target_date.strftime('%Y-%m-%d')}"
)

ax.legend(loc="lower left", fontsize=10, frameon=True)

plt.tight_layout()

# ----------------- 6. 保存图像 -----------------
output_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, f"10-ipps_{target_date.strftime('%Y%m%d')}.png")
plt.savefig(output_path, dpi=400, bbox_inches="tight")
plt.close()

print(f"✅ CODE TEC 穿刺点经纬度分布图（{target_date.strftime('%Y-%m-%d')}）已保存至：{output_path}")
