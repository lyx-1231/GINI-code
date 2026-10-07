import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ----------------- 1. 数据路径 -----------------
cosm_path = "/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_cosm_2024_all.pkl"
code_path = "/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_code_2024_all.pkl"

# ----------------- 2. 读取数据 -----------------
df_cosm = pd.read_pickle(cosm_path)
df_code = pd.read_pickle(code_path)

# ----------------- 3. 输出路径 -----------------
output_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "9-monthly.png")

# ----------------- 4. 选择站点 -----------------
selected_sites = ["MKEA", "BOGT", "YKRO", "IISC", "GUAM"]

# ----------------- 5. 统一站点名大小写 -----------------
df_cosm["site"] = df_cosm["site"].str.upper()
df_code["site"] = df_code["site"].str.upper()

# ----------------- 6. 定义每月RMSE计算函数 -----------------
def compute_monthly_rmse(df, sites):
    df["month"] = df["time"].dt.month

    rmse_results = []
    for site in sites:
        df_site = df[df["site"] == site].copy()
        if df_site.empty:
            print(f"⚠️ 站点 {site} 数据为空，跳过。")
            continue

        monthly_rmse = (
            df_site.groupby("month")["delta"]
            .apply(lambda x: np.sqrt(np.nanmean(x**2)) if np.any(~np.isnan(x)) else np.nan)
        )
        monthly_rmse = monthly_rmse.reindex(range(1, 13))
        rmse_results.append(monthly_rmse.rename(site))

    df_rmse = pd.concat(rmse_results, axis=1)
    return df_rmse

monthly_rmse_cosm = compute_monthly_rmse(df_cosm, selected_sites)
monthly_rmse_code = compute_monthly_rmse(df_code, selected_sites)

# ----------------- 7. 绘图 -----------------
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10

colors = ["#d8d21a", '#d95f02', '#7570b3', '#e7298a', '#66a61e']
months_num = np.arange(1, 13)

fig, axes = plt.subplots(2, 1, figsize=(12/2.54, 9/2.54), sharex=True)

# 上图：CODE vs OBS
ax1 = axes[0]
for site, color in zip(selected_sites, colors):
    if site in monthly_rmse_code.columns:
        ax1.plot(months_num, monthly_rmse_code[site], label=site, color=color, linewidth=1)
ax1.set_ylabel("CODE TEC\nRMSE (TECU)", fontsize=10)
ax1.grid(axis="y", linewidth=0.3, color='gray', alpha=0.7)
ax1.legend(fontsize=8, ncol=3, loc='upper left')
ax1.set_xlim(1, 12)

# 下图：COSMIC vs OBS
ax2 = axes[1]
for site, color in zip(selected_sites, colors):
    if site in monthly_rmse_cosm.columns:
        ax2.plot(months_num, monthly_rmse_cosm[site], label=site, color=color, linewidth=1)
ax2.set_xlabel("Month (Year, 2024)", fontsize=10)
ax2.set_ylabel("Model TEC\nRMSE (TECU)", fontsize=10)
ax2.grid(axis="y", linewidth=0.3, color='gray', alpha=0.7)
ax2.set_xlim(1, 12)

# 设置x轴为数字月份标签，格式 01, 02, ..., 12
ax2.set_xticks(months_num)
ax2.set_xticklabels([f"{m:02d}" for m in months_num])

plt.tight_layout()
plt.savefig(output_path, dpi=400, bbox_inches='tight')
plt.close()

print(f"✅ 绘图完成，已保存到：{output_path}")
