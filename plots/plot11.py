import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# ----------------- 1. 数据路径 -----------------
cosm_path = "/home/yxlei/cosmic2gim/scripts/IONPPP/results-fei/pd_diff_obs_vs_cosm_2024_003_30site.pkl"
code_path = "/home/yxlei/cosmic2gim/scripts/IONPPP/results-fei/pd_diff_obs_vs_code_2024_003_30site.pkl"

# ----------------- 2. 读取数据 -----------------
df_cosm = pd.read_pickle(cosm_path)
df_code = pd.read_pickle(code_path)

# ----------------- 3. 输出路径 -----------------
output_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "11-003.png")

# ----------------- 4. 参数设置 -----------------
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10

# ----------------- 5. 统一站点名大小写 -----------------
df_cosm["site"] = df_cosm["site"].str.upper()
df_code["site"] = df_code["site"].str.upper()

# ----------------- 6. 检查时间字段 -----------------
# 假设时间字段为 'datetime'，如果不是请改成你实际的列名
time_col = "time"
if time_col not in df_cosm.columns:
    raise ValueError(f"未找到时间列 '{time_col}'，请检查数据列名：{df_cosm.columns}")

# ----------------- 7. 计算每小时RMSE -----------------
def compute_hourly_rmse(df, label):
    # 只保留必要字段
    df = df[[time_col, "site", "delta"]].dropna()
    # 按小时聚合
    df["hour"] = df[time_col].dt.floor("H")
    # 对每个小时计算RMSE
    hourly_rmse = df.groupby("hour")["delta"].apply(lambda x: np.sqrt(np.mean(x**2)))
    return hourly_rmse

rmse_cosm = compute_hourly_rmse(df_cosm, "COSMIC")
rmse_code = compute_hourly_rmse(df_code, "CODE")

rmse_cosm = rmse_cosm[rmse_cosm.index.hour >= 1]
rmse_code = rmse_code[rmse_code.index.hour >= 1]


# ----------------- 8. 绘图 -----------------
fig, ax = plt.subplots(figsize=(12/2.54, 9/2.54), dpi=300)

# ax.plot(rmse_cosm.index, rmse_cosm.values, marker='o', linestyle='-', label='COSMIC vs OBS')
# ax.plot(rmse_code.index, rmse_code.values, marker='s', linestyle='-', label='CODE vs OBS')

ax.plot(rmse_cosm.index, rmse_cosm.values, label='GINI TEC', color="#63abdf", linewidth=1.8,marker='s',markersize=4)
ax.plot(rmse_code.index, rmse_code.values, label='CODE TEC', color="#bd4bbb", linewidth=1.8,marker='s',markersize=4)


ax.set_xlabel("Time (Hour-Minute,2024 DOY 003)")
ax.set_ylabel("RMSE (TECU)")
# ax.set_title("Hourly RMSE of ΔTEC (2024 DOY 003, All 30 Sites)")
ax.legend()

# 时间格式美化
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
fig.autofmt_xdate()

# 去除两端空白
ax.set_xlim(rmse_cosm.index.min(), rmse_cosm.index.max())

ax.set_ylim(0, 20)


# plt.grid(True, linestyle='--', alpha=0.5)
plt.grid(axis="y", linewidth=0.3, color='gray', alpha=0.7)

plt.tight_layout()
plt.savefig(output_path)
plt.show()

print(f"✅ 图像已保存至: {output_path}")








# import os
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates

# # ----------------- 1. 数据路径 -----------------
# cosm_path = "/home/yxlei/cosmic2gim/scripts/IONPPP/results-fei/pd_diff_obs_vs_cosm_2024_003_30site.pkl"
# code_path = "/home/yxlei/cosmic2gim/scripts/IONPPP/results-fei/pd_diff_obs_vs_code_2024_003_30site.pkl"

# # ----------------- 2. 读取数据 -----------------
# df_cosm = pd.read_pickle(cosm_path)
# df_code = pd.read_pickle(code_path)

# # ----------------- 3. 输出路径 -----------------
# output_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
# os.makedirs(output_dir, exist_ok=True)
# output_path_cosm = os.path.join(output_dir, "11_cosm.png")
# output_path_code = os.path.join(output_dir, "11_code.png")

# # ----------------- 4. 统一站点名大小写 -----------------
# df_cosm["site"] = df_cosm["site"].str.upper()
# df_code["site"] = df_code["site"].str.upper()

# # ----------------- 5. 设置绘图样式 -----------------
# plt.rcParams['font.family'] = 'Arial'
# plt.rcParams['font.size'] = 9

# # ----------------- 6. 获取站点列表 -----------------
# sites = sorted(df_cosm["site"].unique())
# print(f"共有 {len(sites)} 个站点：{sites}")

# # ----------------- 7. 函数：绘制每个站点的时间序列误差 -----------------
# def plot_station_deltas(df, title, output_path):
#     fig, ax = plt.subplots(figsize=(15/2.54, 8/2.54))

#     for site in sorted(df["site"].unique()):
#         df_site = df[df["site"] == site]
#         # 按时间排序
#         df_site = df_site.sort_values("time")

#         ax.plot(df_site["time"], df_site["delta"], linewidth=0.8, alpha=0.7, label=site)

#     # 时间轴格式化
#     ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
#     ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
#     plt.xticks(rotation=30)

#     ax.set_xlabel("Time (UTC)", fontsize=9)
#     ax.set_ylabel("ΔTEC (TECU)", fontsize=9)
#     ax.set_title(title, fontsize=10)
#     ax.grid(linewidth=0.3, color='gray', alpha=0.6)

#     # 图例太多 → 放在外侧
#     ax.legend(fontsize=6, ncol=3, loc='upper right', bbox_to_anchor=(1.25, 1.0))

#     plt.tight_layout()
#     plt.savefig(output_path, dpi=400, bbox_inches='tight')
#     plt.close()
#     print(f"✅ {title} 绘图完成，保存到：{output_path}")

# # ----------------- 8. 分别绘制两个来源 -----------------
# plot_station_deltas(df_cosm, "ΔTEC Time Series (COSMIC, 30 sites)", output_path_cosm)
# plot_station_deltas(df_code, "ΔTEC Time Series (CODE, 30 sites)", output_path_code)
