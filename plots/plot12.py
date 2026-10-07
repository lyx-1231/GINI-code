import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# ----------------- 1. 数据路径 -----------------
# cosm_path = "/home/yxlei/cosmic2gim/scripts/IONPPP/results-fei/pd_diff_obs_vs_cosm_2024_180_30site.pkl"
# code_path = "/home/yxlei/cosmic2gim/scripts/IONPPP/results-fei/pd_diff_obs_vs_code_2024_180_30site.pkl"
cosm_path = "/home/yxlei/cosmic2gim/scripts/IONPPP/results/pd_diff_obs_vs_cosm_2024_285-29sites.pkl"
code_path = "/home/yxlei/cosmic2gim/scripts/IONPPP/results/pd_diff_obs_vs_code_2024_285-29sites.pkl"

# ----------------- 2. 读取数据 -----------------
df_cosm = pd.read_pickle(cosm_path)
df_code = pd.read_pickle(code_path)

# ----------------- 3. 输出路径 -----------------
output_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "12-285.png")

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

# ----------------- 8. 绘图 -----------------
fig, ax = plt.subplots(figsize=(12/2.54, 9/2.54), dpi=300)

# ax.plot(rmse_cosm.index, rmse_cosm.values, marker='o', linestyle='-', label='COSMIC vs OBS')
# ax.plot(rmse_code.index, rmse_code.values, marker='s', linestyle='-', label='CODE vs OBS')

ax.plot(rmse_cosm.index, rmse_cosm.values, label='GINI TEC', color="#63abdf", linewidth=1.8,marker='s',markersize=4)
ax.plot(rmse_code.index, rmse_code.values, label='CODE TEC', color="#bd4bbb", linewidth=1.8,marker='s',markersize=4)


ax.set_xlabel("Time (Hour-Minute,2024 DOY 285)")
ax.set_ylabel("RMSE (TECU)")
# ax.set_title("Hourly RMSE of ΔTEC (2024 DOY 003, All 30 Sites)")
ax.legend()

# 时间格式美化
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
fig.autofmt_xdate()

# 去除两端空白
ax.set_xlim(rmse_cosm.index.min(), rmse_cosm.index.max())

# plt.grid(True, linestyle='--', alpha=0.5)
plt.grid(axis="y", linewidth=0.3, color='gray', alpha=0.7)

plt.tight_layout()
plt.savefig(output_path, dpi=500)
plt.show()

print(f"✅ 图像已保存至: {output_path}")








