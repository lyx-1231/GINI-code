# import os
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

# # ----------------- 1. 数据路径 -----------------
# cosm_path = "/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_cosm_2024_all.pkl"
# code_path = "/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_code_2024_all.pkl"

# # ----------------- 2. 读取数据 -----------------
# df_cosm = pd.read_pickle(cosm_path)
# df_code = pd.read_pickle(code_path)

# # ----------------- 3. 输出路径 -----------------
# output_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
# os.makedirs(output_dir, exist_ok=True)
# output_path = os.path.join(output_dir, "9-daily.png")

# # ----------------- 4. 选择站点 -----------------
# selected_sites = ["MKEA", "BOGT", "YKRO", "IISC", "GUAM"]

# # ----------------- 5. 统一站点名大小写 -----------------
# df_cosm["site"] = df_cosm["site"].str.upper()
# df_code["site"] = df_code["site"].str.upper()

# # ----------------- 6. 定义每日RMSE计算函数 -----------------
# def compute_daily_rmse(df, sites):
#     df["doy"] = df["time"].dt.dayofyear

#     rmse_results = []
#     for site in sites:
#         df_site = df[df["site"] == site].copy()
#         if df_site.empty:
#             print(f"⚠️ 站点 {site} 数据为空，跳过。")
#             continue

#         daily_rmse = (
#             df_site.groupby("doy")["delta"]
#             .apply(lambda x: np.sqrt(np.nanmean(x**2)) if np.any(~np.isnan(x)) else np.nan)
#         )
#         daily_rmse = daily_rmse.reindex(range(1, 367))
#         rmse_results.append(daily_rmse.rename(site))

#     df_rmse = pd.concat(rmse_results, axis=1)
#     return df_rmse

# daily_rmse_cosm = compute_daily_rmse(df_cosm, selected_sites)
# daily_rmse_code = compute_daily_rmse(df_code, selected_sites)

# # ----------------- 7. 绘图 -----------------
# plt.rcParams['font.family'] = 'Arial'
# plt.rcParams['font.size'] = 10

# colors = ["#d8d21a", '#d95f02', '#7570b3', '#e7298a', '#66a61e']  # 5个站颜色
# fig, axes = plt.subplots(2, 1, figsize=(12/2.54, 9/2.54), sharex=True)

# # 上图：CODE vs OBS
# ax1 = axes[0]
# for site, color in zip(selected_sites, colors):
#     if site in daily_rmse_code.columns:
#         ax1.plot(daily_rmse_code.index, daily_rmse_code[site], label=site, color=color, linewidth=1)
# ax1.set_ylabel("CODE TEC\nRMSE (TECU)", fontsize=10)  # 换行实现两列效果
# ax1.grid(axis="y", linewidth=0.3, color='gray', alpha=0.7)
# ax1.legend(fontsize=8, ncol=3, loc='upper left')
# ax1.set_xlim(1, 366)  # 设置横轴范围，去除空白

# # 下图：COSMIC vs OBS
# ax2 = axes[1]
# for site, color in zip(selected_sites, colors):
#     if site in daily_rmse_cosm.columns:
#         ax2.plot(daily_rmse_cosm.index, daily_rmse_cosm[site], label=site, color=color, linewidth=1)
# ax2.set_xlabel("Day of Year (2024)", fontsize=10)
# ax2.set_ylabel("Model TEC\nRMSE (TECU)", fontsize=10)  # 换行
# ax2.grid(axis="y", linewidth=0.3, color='gray', alpha=0.7)
# ax2.set_xlim(1, 366)  # 同上

# plt.tight_layout()
# plt.savefig(output_path, dpi=400, bbox_inches='tight')
# plt.close()

# print(f"✅ 绘图完成，已保存到：{output_path}")












# import os
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# from datetime import datetime, timedelta

# # ----------------- 1. 数据路径 -----------------
# cosm_path = "/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_cosm_2024_all.pkl"
# code_path = "/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_code_2024_all.pkl"

# # ----------------- 2. 读取数据 -----------------
# df_cosm = pd.read_pickle(cosm_path)
# df_code = pd.read_pickle(code_path)

# # ----------------- 3. 输出路径 -----------------
# output_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
# os.makedirs(output_dir, exist_ok=True)
# output_path = os.path.join(output_dir, "9-daily.png")

# # ----------------- 4. 选择站点 -----------------
# selected_sites = ["MKEA", "BOGT", "YKRO", "IISC", "GUAM"]

# # ----------------- 5. 统一站点名大小写 -----------------
# df_cosm["site"] = df_cosm["site"].str.upper()
# df_code["site"] = df_code["site"].str.upper()

# # ----------------- 6. 定义每日RMSE计算函数 -----------------
# def compute_daily_rmse(df, sites):
#     df["doy"] = df["time"].dt.dayofyear

#     rmse_results = []
#     for site in sites:
#         df_site = df[df["site"] == site].copy()
#         if df_site.empty:
#             print(f"⚠️ 站点 {site} 数据为空，跳过。")
#             continue

#         daily_rmse = (
#             df_site.groupby("doy")["delta"]
#             .apply(lambda x: np.sqrt(np.nanmean(x**2)) if np.any(~np.isnan(x)) else np.nan)
#         )
#         daily_rmse = daily_rmse.reindex(range(1, 367))
#         rmse_results.append(daily_rmse.rename(site))

#     df_rmse = pd.concat(rmse_results, axis=1)
#     return df_rmse

# daily_rmse_cosm = compute_daily_rmse(df_cosm, selected_sites)
# daily_rmse_code = compute_daily_rmse(df_code, selected_sites)

# # ----------------- 7. 日期处理 -----------------
# year = 2024
# dates = pd.to_datetime(f'{year}-01-01') + pd.to_timedelta(np.arange(366), unit='D')


# # ----------------- 8. 绘图 -----------------
# plt.rcParams['font.family'] = 'Arial'
# plt.rcParams['font.size'] = 10

# colors = ["#d8d21a", '#d95f02', '#7570b3', '#e7298a', '#66a61e']
# fig, axes = plt.subplots(2, 1, figsize=(12/2.54, 9/2.54), sharex=True)

# # 上图：CODE vs OBS
# ax1 = axes[0]
# for site, color in zip(selected_sites, colors):
#     if site in daily_rmse_code.columns:
#         ax1.plot(dates, daily_rmse_code[site], label=site, color=color, linewidth=1)
# ax1.set_ylabel("CODE TEC\nRMSE (TECU)", fontsize=10)
# ax1.grid(axis="y", linewidth=0.3, color='gray', alpha=0.7)
# ax1.legend(fontsize=8, ncol=3, loc='upper left')
# ax1.set_xlim(dates[0], dates[-1])

# # 下图：COSMIC vs OBS
# ax2 = axes[1]
# for site, color in zip(selected_sites, colors):
#     if site in daily_rmse_cosm.columns:
#         ax2.plot(dates, daily_rmse_cosm[site], label=site, color=color, linewidth=1)
# ax2.set_xlabel("Month (Year,2024)", fontsize=10)
# ax2.set_ylabel("Model TEC\nRMSE (TECU)", fontsize=10)
# ax2.grid(axis="y", linewidth=0.3, color='gray', alpha=0.7)
# ax2.set_xlim(dates[0], dates[-1])

# # 设置x轴为月份刻度，只显示每个月第一天
# months = mdates.MonthLocator()  # 每个月第一天定位器
# # months_fmt = mdates.DateFormatter('%b')  # 格式化为月份缩写，如 Jan, Feb
# months_fmt = mdates.DateFormatter('%m')  # 数字月份，且格式是两位数


# ax2.xaxis.set_major_locator(months)
# ax2.xaxis.set_major_formatter(months_fmt)

# plt.tight_layout()
# plt.savefig(output_path, dpi=400, bbox_inches='tight')
# plt.close()

# print(f"✅ 绘图完成，已保存到：{output_path}")









import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# ----------------- 1. 数据路径 -----------------
cosm_path = "/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_cosm_2024_all.pkl"
code_path = "/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_code_2024_all.pkl"

# ----------------- 2. 读取数据 -----------------
df_cosm = pd.read_pickle(cosm_path)
df_code = pd.read_pickle(code_path)

# ----------------- 3. 输出路径 -----------------
output_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "9-daily.png")

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
ax1.set_ylim(0, 35)

# 下图：COSMIC vs OBS
ax2 = axes[1]
for site, color in zip(selected_sites, colors):
    if site in daily_rmse_cosm.columns:
        ax2.plot(dates, daily_rmse_cosm[site], label=site, color=color, linewidth=1)
ax2.set_xlabel("Month (Year,2024)", fontsize=10)
ax2.set_ylabel("Model TEC\nRMSE (TECU)", fontsize=10)
ax2.grid(axis="y", linewidth=0.3, color='gray', alpha=0.7)
ax2.set_xlim(dates[0], dates[-1])
ax2.set_ylim(0, 35)

# 设置x轴为月份刻度，只显示每个月第一天
months = mdates.MonthLocator()  # 每个月第一天定位器
# months_fmt = mdates.DateFormatter('%b')  # 格式化为月份缩写，如 Jan, Feb
months_fmt = mdates.DateFormatter('%m')  # 数字月份，且格式是两位数


ax2.xaxis.set_major_locator(months)
ax2.xaxis.set_major_formatter(months_fmt)

plt.tight_layout()
plt.savefig(output_path, dpi=400, bbox_inches='tight')
plt.close()

print(f"✅ 绘图完成，已保存到：{output_path}")









