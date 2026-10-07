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

# # ----------------- 4. 时间字段处理 -----------------
# df_code["time"] = pd.to_datetime(df_code["time"])

# # ----------------- 5. 设置目标日期 -----------------
# target_date = pd.Timestamp("2024-01-03")

# # 仅保留目标日期的数据
# df_code_day = df_code[df_code["time"].dt.date == target_date.date()]

# # ----------------- 6. 构造整点参考时刻 ±15 min 窗口 -----------------
# time_windows = []

# for hour in range(24):
#     ref_time = target_date + pd.Timedelta(hours=hour)
#     start_time = ref_time - pd.Timedelta(minutes=5)
#     end_time = ref_time + pd.Timedelta(minutes=5)

#     df_window = df_code_day[
#         (df_code_day["time"] >= start_time) &
#         (df_code_day["time"] <= end_time)
#     ]

#     time_windows.append(df_window)

# # 合并所有整点时间窗内的数据
# df_ref = pd.concat(time_windows, ignore_index=True)

# # ----------------- 7. 纬度范围筛选 -----------------
# df_ref = df_ref[(df_ref["lat"] >= -45) & (df_ref["lat"] <= 45)]

# # ----------------- 8. 绘图 -----------------
# plt.rcParams["font.family"] = "Arial"
# plt.rcParams["font.size"] = 10

# fig = plt.figure(figsize=(12.9 / 2.54, 3.5))
# ax = plt.axes(projection=ccrs.Robinson())

# ax.set_extent([-180, 180, -45, 45], crs=ccrs.PlateCarree())

# ax.add_feature(cfeature.LAND, facecolor="lightgray")
# ax.add_feature(cfeature.OCEAN, facecolor="white")
# ax.add_feature(cfeature.COASTLINE, linewidth=0.2)
# ax.gridlines(draw_labels=False, linewidth=0.2, linestyle="--",
#              color="gray", alpha=0.7)

# ax.scatter(
#     df_ref["lon"], df_ref["lat"],
#     color="#63abdf",
#     s=0.1,
#     alpha=0.5,
#     transform=ccrs.PlateCarree(),
#     label="IPPs within ±15 min of each hourly reference time"
# )

# ax.legend(loc="lower left", fontsize=9, frameon=True)

# plt.tight_layout()

# # ----------------- 9. 保存图像 -----------------
# output_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
# os.makedirs(output_dir, exist_ok=True)

# output_path = os.path.join(
#     output_dir,
#     f"ipps_hourly_pm15min_{target_date.strftime('%Y%m%d')}.png"
# )

# plt.savefig(output_path, dpi=400, bbox_inches="tight")
# plt.close()

# print(
#     f"✅ CODE TEC 穿刺点（整点 ±5 min，{target_date.strftime('%Y-%m-%d')}）"
#     f"已保存至：{output_path}"
# )




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

# ----------------- 4. 时间处理 -----------------
df_code["time"] = pd.to_datetime(df_code["time"])

# 目标日期
target_date = pd.Timestamp("2024-01-03")

# 模型参考时刻（整点 01:00）
ref_time = target_date + pd.Timedelta(hours=1)

# 前后 30 分钟时间窗
time_start = ref_time - pd.Timedelta(minutes=30)
time_end   = ref_time + pd.Timedelta(minutes=30)

# 仅保留该时间窗内的数据
df_code_window = df_code[
    (df_code["time"] >= time_start) &
    (df_code["time"] <= time_end)
]

# ----------------- 5. 纬度范围筛选 -----------------
df_subset = df_code_window[
    (df_code_window["lat"] >= -45) &
    (df_code_window["lat"] <= 45)
]

# ----------------- 6. 绘图 -----------------
plt.rcParams["font.family"] = "Arial"
plt.rcParams["font.size"] = 10

fig = plt.figure(figsize=(12.9 / 2.54, 3.5))
ax = plt.axes(projection=ccrs.Robinson())

ax.set_extent([-180, 180, -45, 45], crs=ccrs.PlateCarree())

ax.add_feature(cfeature.LAND, facecolor="lightgray")
ax.add_feature(cfeature.OCEAN, facecolor="white")
ax.add_feature(cfeature.COASTLINE, linewidth=0.2)
ax.gridlines(draw_labels=False, linewidth=0.2,
             linestyle="--", color="gray", alpha=0.7)

ax.scatter(
    df_subset["lon"],
    df_subset["lat"],
    color="#63abdf",
    s=0.1,
    alpha=0.5,
    transform=ccrs.PlateCarree(),
    label="IPPs within ±30 min around 01:00"
)

ax.legend(loc="lower left", fontsize=9, frameon=True)

plt.tight_layout()

# ----------------- 7. 保存图像 -----------------
output_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(
    output_dir,
    f"10-ipps_{target_date.strftime('%Y%m%d')}_0100pm30.png"
)

plt.savefig(output_path, dpi=400, bbox_inches="tight")
plt.close()

print(
    f"✅ 穿刺点分布图已生成\n"
    f"时间窗口：{time_start} ~ {time_end}\n"
    f"保存路径：{output_path}"
)
