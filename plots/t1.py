import numpy as np


# ---- 查看文件
data = np.load("/home/yxlei/cosmic2gim/data/20191001_20241231_dst_series.npz", allow_pickle=True)
timestamps = data['timestamps']
dst = data['dst']

print("Timestamps:", timestamps)
print("dst Index:",dst)









# import pandas as pd
# import numpy as np

# # ----------------- 1. 文件路径 -----------------
# cosm_path = "/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_cosm_2024_all.pkl"
# code_path = "/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_code_2024_all.pkl"

# # ----------------- 2. 读取数据 -----------------
# df_cosm = pd.read_pickle(cosm_path)
# df_code = pd.read_pickle(code_path)

# # ----------------- 3. 定义检查函数 -----------------
# def check_doy_coverage(df, name):
#     # 从 time 提取 day of year
#     df["doy"] = df["time"].dt.dayofyear
    
#     # 仅统计有 delta 的条目
#     df_valid = df[~df["delta"].isna()]
    
#     # 每天的有效记录数量
#     doy_counts = df_valid.groupby("doy")["delta"].count()
    
#     all_doys = np.arange(1, 367)  # 2024 是闰年
#     available_doys = sorted(doy_counts.index.tolist())
#     missing_doys = sorted(set(all_doys) - set(available_doys))
    
#     print(f"\n📘 {name} 数据检查结果：")
#     print(f"共有 {len(available_doys)} 天存在 delta 数据")
#     print(f"每日样本数范围：min={doy_counts.min()}, max={doy_counts.max()}")
    
#     if missing_doys:
#         print(f"❌ 缺少 {len(missing_doys)} 天：{missing_doys}")
#     else:
#         print("✅ 数据覆盖完整（1–366 天均存在 delta 数据）")
    
#     # 可选：返回每天的样本数 DataFrame 供后续分析
#     return doy_counts

# # ----------------- 4. 执行检查 -----------------
# cosm_doy_counts = check_doy_coverage(df_cosm, "COSMIC")
# code_doy_counts = check_doy_coverage(df_code, "CODE")

# # ----------------- 5. 可选：保存每日数据统计到 CSV -----------------
# # cosm_doy_counts.to_csv("/home/yxlei/cosmic2gim/scripts/data/cosmic_doy_counts.csv")
# # code_doy_counts.to_csv("/home/yxlei/cosmic2gim/scripts/data/code_doy_counts.csv")











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
# output_path = os.path.join(output_dir, "9-2.png")

# # ----------------- 4. 设置要分析的站点 -----------------
# selected_sites = ["MKEA", "BOGT", "YKRO", "IISC", "GUAM"]

# # ----------------- 5. 计算每天每个站点的 RMSE -----------------
# def compute_daily_rmse(df, sites):
#     df["doy"] = df["time"].dt.dayofyear
#     results = []
#     for site in sites:
#         df_site = df[df["site"] == site]
#         daily_rmse = df_site.groupby("doy")["delta"].apply(lambda x: np.sqrt(np.nanmean(x**2)))
#         results.append(daily_rmse.rename(site))
#     df_rmse = pd.concat(results, axis=1)
#     return df_rmse

# daily_rmse_cosm = compute_daily_rmse(df_cosm, selected_sites)
# daily_rmse_code = compute_daily_rmse(df_code, selected_sites)

# # ----------------- 6. 绘图设置 -----------------
# plt.rcParams['font.family'] = 'Arial'
# plt.rcParams['font.size'] = 10

# colors = ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e']  # 5种配色

# fig, axes = plt.subplots(2, 1, figsize=(12/2.54, 9/2.54), sharex=True)

# # 上图：COSMIC
# ax1 = axes[0]
# for site, color in zip(selected_sites, colors):
#     ax1.plot(daily_rmse_cosm.index, daily_rmse_cosm[site], label=site, color=color, linewidth=1)
# ax1.set_ylabel("RMSE (TECU)")
# ax1.set_title("COSMIC vs Observation (Daily RMSE)")
# ax1.grid(alpha=0.3)
# ax1.legend(fontsize=8, ncol=3, loc='upper right')

# # 下图：CODE
# ax2 = axes[1]
# for site, color in zip(selected_sites, colors):
#     ax2.plot(daily_rmse_code.index, daily_rmse_code[site], label=site, color=color, linewidth=1)
# ax2.set_xlabel("Day of Year (2024)")
# ax2.set_ylabel("RMSE (TECU)")
# ax2.set_title("CODE vs Observation (Daily RMSE)")
# ax2.grid(alpha=0.3)

# plt.tight_layout()
# plt.savefig(output_path, dpi=400, bbox_inches='tight')
# plt.close()

# print(f"✅ 绘图完成，已保存到：{output_path}")










# import pandas as pd

# # ----------------- 1. 文件路径 -----------------
# cosm_path = "/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_cosm_2024_all.pkl"
# code_path = "/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_code_2024_all.pkl"

# # ----------------- 2. 读取数据 -----------------
# print("Loading data, please wait ...")
# df_cosm = pd.read_pickle(cosm_path)
# df_code = pd.read_pickle(code_path)

# # ----------------- 3. 计算年积日（DOY） -----------------
# df_cosm["doy"] = df_cosm["time"].dt.dayofyear
# df_code["doy"] = df_code["time"].dt.dayofyear

# # ----------------- 4. 筛选 DOY 100–150 的数据 -----------------
# df_cosm_sel = df_cosm[(df_cosm["doy"] >= 100) & (df_cosm["doy"] <= 150)]
# df_code_sel = df_code[(df_code["doy"] >= 100) & (df_code["doy"] <= 150)]

# # ----------------- 5. 打印信息 -----------------
# print("\n=== COSMIC 数据 (DOY 100–150) ===")
# print(df_cosm_sel.info())
# print(df_cosm_sel.head(10))
# print("... (共", len(df_cosm_sel), "条记录)\n")

# print("\n=== CODE 数据 (DOY 100–150) ===")
# print(df_code_sel.info())
# print(df_code_sel.head(10))
# print("... (共", len(df_code_sel), "条记录)\n")

# # ----------------- 6. 如需保存筛选结果，可取消注释以下代码 -----------------
# # df_cosm_sel.to_pickle("/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_cosm_2024_DOY100_150.pkl")
# # df_code_sel.to_pickle("/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_code_2024_DOY100_150.pkl")











# import pickle
# import pandas as pd

# # ----------------- 1. 读取 xarray 对象 -----------------
# def load_object(filename):
#     with open(filename, "rb") as f:
#         return pickle.load(f)

# # ----------------- 2. 读取差分结果 DataFrame -----------------
# pd_diff_obs_vs_cosm = pd.read_pickle("/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_cosm_2024_all.pkl")
# pd_diff_obs_vs_code = pd.read_pickle("/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_code_2024_all.pkl")


# print(pd_diff_obs_vs_cosm.info())




# # ----------------- 3. 分别统计 lat 的取值范围 -----------------
# cosm_lat_min = pd_diff_obs_vs_cosm["lat"].min()
# cosm_lat_max = pd_diff_obs_vs_cosm["lat"].max()

# code_lat_min = pd_diff_obs_vs_code["lat"].min()
# code_lat_max = pd_diff_obs_vs_code["lat"].max()

# # ----------------- 4. 打印结果 -----------------
# print("=== 纬度取值范围统计 ===")
# print(f"COSMIC 数据：lat_min = {cosm_lat_min:.6f}, lat_max = {cosm_lat_max:.6f}")
# print(f"CODE   数据：lat_min = {code_lat_min:.6f}, lat_max = {code_lat_max:.6f}")

# # 若想确认纬度范围一致，可加如下校验
# if abs(cosm_lat_min - code_lat_min) < 1e-6 and abs(cosm_lat_max - code_lat_max) < 1e-6:
#     print("\n✅ 两个数据集的纬度范围一致。")
# else:
#     print("\n⚠️ 注意：两个数据集的纬度范围不完全一致。")
