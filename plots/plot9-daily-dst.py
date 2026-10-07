import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# ----------------- 1. 数据路径 -----------------
cosm_path = "/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_cosm_2024_all.pkl"
code_path = "/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_code_2024_all.pkl"
dst_path = "/home/yxlei/cosmic2gim/data/20191001_20241231_dst_series.npz"

# ----------------- 2. 读取数据 -----------------
df_cosm = pd.read_pickle(cosm_path)
df_code = pd.read_pickle(code_path)

# 读取 DST 数据
data = np.load(dst_path, allow_pickle=True)
timestamps = pd.to_datetime(data['timestamps'])
dst = data['dst']

# 筛选 2024 年数据
mask_2024 = (timestamps >= "2024-01-01") & (timestamps < "2025-01-01")
timestamps_2024 = timestamps[mask_2024]
dst_2024 = dst[mask_2024]

# ----------------- 3. 输出路径 -----------------
output_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "9-daily_dst.png")

# ----------------- 4. 选择站点 -----------------
selected_sites = ["MKEA", "BOGT", "YKRO", "IISC", "GUAM"]

# ----------------- 5. 统一站点名大小写 -----------------
df_cosm["site"] = df_cosm["site"].str.upper()
df_code["site"] = df_code["site"].str.upper()

# ----------------- 6. 定义每日RMSE计算函数 -----------------
def compute_daily_rmse(df, sites):
    df["doy"] = df["time"].dt.dayofyear

    rmse_results = []
    for site in sites:
        df_site = df[df["site"] == site].copy()
        if df_site.empty:
            print(f"⚠️ 站点 {site} 数据为空，跳过。")
            continue

        daily_rmse = (
            df_site.groupby("doy")["delta"]
            .apply(lambda x: np.sqrt(np.nanmean(x**2)) if np.any(~np.isnan(x)) else np.nan)
        )
        daily_rmse = daily_rmse.reindex(range(1, 367))
        rmse_results.append(daily_rmse.rename(site))

    df_rmse = pd.concat(rmse_results, axis=1)
    return df_rmse

daily_rmse_cosm = compute_daily_rmse(df_cosm, selected_sites)
daily_rmse_code = compute_daily_rmse(df_code, selected_sites)

# ----------------- 7. 日期处理 -----------------
year = 2024
dates = pd.to_datetime(f'{year}-01-01') + pd.to_timedelta(np.arange(366), unit='D')

# ----------------- 8. 绘图 -----------------
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10

colors = ["#d8d21a", '#d95f02', '#7570b3', '#e7298a', '#66a61e']
fig, axes = plt.subplots(2, 1, figsize=(12/2.54, 9/2.54), sharex=True)

# 上图：CODE vs OBS
ax1 = axes[0]
for site, color in zip(selected_sites, colors):
    if site in daily_rmse_code.columns:
        ax1.plot(dates, daily_rmse_code[site], label=site, color=color, linewidth=1)
ax1.set_ylabel("CODE TEC\nRMSE (TECU)", fontsize=10)
ax1.grid(axis="y", linewidth=0.3, color='gray', alpha=0.7)
ax1.legend(fontsize=8, ncol=3, loc='upper left')
ax1.set_xlim(dates[0], dates[-1])
ax1.set_ylim(0, 40)

# 下图：COSMIC vs OBS + DST（双y轴）
ax2 = axes[1]
for site, color in zip(selected_sites, colors):
    if site in daily_rmse_cosm.columns:
        ax2.plot(dates, daily_rmse_cosm[site], label=site, color=color, linewidth=1)
ax2.set_xlabel("Month (Year,2024)", fontsize=10)
ax2.set_ylabel("GINI TEC\nRMSE (TECU)", fontsize=10)
ax2.grid(axis="y", linewidth=0.3, color='gray', alpha=0.7)
ax2.set_xlim(dates[0], dates[-1])
ax2.set_ylim(0, 40)

# 创建右侧 y 轴：DST 指数
ax2_dst = ax2.twinx()
ax2_dst.plot(timestamps_2024, dst_2024, color='skyblue', linewidth=0.8, label='DST Index')
ax2_dst.set_ylabel("DST (nT)", fontsize=10, color='skyblue')
ax2_dst.tick_params(axis='y', labelcolor='skyblue')
ax2_dst.set_ylim(-320, 70)

# 设置x轴为月份刻度，只显示每个月第一天
months = mdates.MonthLocator()
months_fmt = mdates.DateFormatter('%m')
ax2.xaxis.set_major_locator(months)
ax2.xaxis.set_major_formatter(months_fmt)

plt.tight_layout()
plt.savefig(output_path, dpi=400, bbox_inches='tight')
plt.close()

print(f"✅ 绘图完成，已保存到：{output_path}")
