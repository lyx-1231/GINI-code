# # import os
# # import pickle
# # import pandas as pd
# # import numpy as np
# # import matplotlib.pyplot as plt

# # # ----------------- 1. 读取差分结果 DataFrame -----------------
# # cosm_path = "/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_cosm_2024_all.pkl"
# # code_path = "/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_code_2024_all.pkl"

# # pd_diff_obs_vs_cosm = pd.read_pickle(cosm_path)
# # pd_diff_obs_vs_code = pd.read_pickle(code_path)

# # # ----------------- 2. 设置输出路径 -----------------
# # output_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
# # os.makedirs(output_dir, exist_ok=True)
# # output_path = os.path.join(output_dir, "8.png")

# # # ----------------- 3. 选择需要的站点 -----------------
# # selected_sites = ["mkea","bogt","ykro","iisc","guam"]

# # # ----------------- 4. 计算每个站点的全年 RMSE -----------------
# # def compute_rmse(df, sites):
# #     rmse_results = {}
# #     for site in sites:
# #         df_site = df[df["site"] == site]
# #         if len(df_site) == 0:
# #             print(f"⚠️  站点 {site} 数据为空，跳过。")
# #             rmse_results[site] = np.nan
# #         else:
# #             rmse_results[site] = np.sqrt(np.nanmean(df_site["delta"] ** 2))
# #     return rmse_results

# # rmse_cosm = compute_rmse(pd_diff_obs_vs_cosm, selected_sites)
# # rmse_code = compute_rmse(pd_diff_obs_vs_code, selected_sites)

# # # ----------------- 5. 组合结果为 DataFrame -----------------
# # df_rmse = pd.DataFrame({
# #     "COSMIC": rmse_cosm,
# #     "CODE": rmse_code
# # }).T  # 行是模型，列是站点
# # print("\n=== RMSE 对比表 ===")
# # print(df_rmse)

# # # ----------------- 6. 绘制柱状图 -----------------
# # x = np.arange(len(selected_sites))
# # width = 0.35

# # fig, ax = plt.subplots(figsize=(12.9/2.54, 3.5))

# # bars1 = ax.bar(x - width/2, df_rmse.loc["COSMIC"], width, label="COSMIC", color='#4C9F70')  # 清新绿色
# # bars2 = ax.bar(x + width/2, df_rmse.loc["CODE"], width, label="CODE", color='#F4A261')     # 柔橙色

# # # bars1 = ax.bar(x - width/2, df_rmse.loc["COSMIC"], width, label="COSMIC", color='#90bfd5')
# # # bars2 = ax.bar(x + width/2, df_rmse.loc["CODE"], width, label="CODE", color='#d4e1ee')

# # # bars1 = ax.bar(x - width/2, df_rmse.loc["COSMIC"], width, label="COSMIC", color='#2E86AB')  # 蓝
# # # bars2 = ax.bar(x + width/2, df_rmse.loc["CODE"], width, label="CODE", color='#E76F51')      # 橙红


# # # bars1 = ax.bar(x - width/2, df_rmse.loc["COSMIC"], width, label="COSMIC", color='#3A7CA5')  # 蓝
# # # bars2 = ax.bar(x + width/2, df_rmse.loc["CODE"], width, label="CODE", color='#9D79BC')      # 紫


# # #d4e1ee  #9AC9DB #d2e2ef

# # plt.rcParams['font.family']='Arial'
# # plt.rcParams['font.size']=10


# # ax.set_xlabel("GNSS Station", fontsize=10)
# # ax.set_ylabel("RMSE (TECU)", fontsize=10)
# # # ax.set_title("Annual RMSE Comparison of 5 Stations (2024)", fontsize=15)
# # ax.set_xticks(x)
# # ax.set_xticklabels(selected_sites, fontsize=10)
# # ax.legend(fontsize=10)
# # ax.grid(axis="y", linewidth=0.3, color='gray', alpha=0.7)

# # # 显示数值标签
# # for bars in [bars1, bars2]:
# #     ax.bar_label(bars, fmt="%.2f", padding=3, fontsize=10)

# # plt.tight_layout()
# # plt.savefig(output_path, dpi=300)
# # plt.close()

# # print(f"✅ 已保存图像至：{output_path}")








# import os
# import pickle
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

# # ----------------- 1. 读取差分结果 DataFrame -----------------
# cosm_path = "/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_cosm_2024_all.pkl"
# code_path = "/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_code_2024_all.pkl"

# pd_diff_obs_vs_cosm = pd.read_pickle(cosm_path)
# pd_diff_obs_vs_code = pd.read_pickle(code_path)

# # ----------------- 2. 设置输出路径 -----------------
# output_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
# os.makedirs(output_dir, exist_ok=True)
# output_path = os.path.join(output_dir, "8.png")

# # ----------------- 3. 选择需要的站点 -----------------
# # selected_sites = ["mkea","bogt","ykro","iisc","guam"]
# selected_sites = ["MKEA","BOGT","YKRO","IISC","GUAM"]


# # ----------------- 4. 计算每个站点的全年 RMSE -----------------
# def compute_rmse(df, sites):
#     rmse_results = {}
#     for site in sites:
#         df_site = df[df["site"] == site]
#         if len(df_site) == 0:
#             print(f"⚠️  站点 {site} 数据为空，跳过。")
#             rmse_results[site] = np.nan
#         else:
#             rmse_results[site] = np.sqrt(np.nanmean(df_site["delta"] ** 2))
#     return rmse_results

# rmse_cosm = compute_rmse(pd_diff_obs_vs_cosm, selected_sites)
# rmse_code = compute_rmse(pd_diff_obs_vs_code, selected_sites)

# # ----------------- 5. 组合结果为 DataFrame -----------------
# df_rmse = pd.DataFrame({
#     "COSMIC": rmse_cosm,
#     "CODE": rmse_code
# }).T  # 行是模型，列是站点
# print("\n=== RMSE 对比表 ===")
# print(df_rmse)


# # ----------------- 6. 绘制柱状图 -----------------
# x = np.arange(len(selected_sites))
# width = 0.35

# fig, ax = plt.subplots(figsize=(12.9/2.54, 3.5))

# bars1 = ax.bar(x - width/2, df_rmse.loc["COSMIC"], width, label="Model", color='#4C9F70')
# bars2 = ax.bar(x + width/2, df_rmse.loc["CODE"], width, label="CODE", color='#F4A261')

# plt.rcParams['font.family'] = 'Arial'
# plt.rcParams['font.size'] = 10

# ax.set_xlabel("GNSS Station", fontsize=10)
# ax.set_ylabel("RMSE (TECU)", fontsize=10)
# ax.set_xticks(x)
# ax.set_xticklabels(selected_sites, fontsize=10)
# ax.legend(fontsize=10)
# ax.grid(axis="y", linewidth=0.3, color='gray', alpha=0.7)

# # ---- 关键调整部分 ----

# # 1️⃣ 控制 y 轴范围，留出顶部空间
# ymax = max(df_rmse.max()) * 1.15   # 给柱顶留 15% 空间
# ax.set_ylim(0, ymax)

# # 2️⃣ 调整标签位置，让数值始终在图内
# for bars in [bars1, bars2]:
#     ax.bar_label(bars, fmt="%.2f", padding=2, fontsize=9)

# # 3️⃣ 优化布局，确保边缘不被裁剪
# plt.tight_layout()
# plt.savefig(output_path, dpi=500, bbox_inches='tight')  # ✅ 加 bbox_inches='tight'
# plt.close()










import os
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ----------------- 1. 读取差分结果 DataFrame -----------------
cosm_path = "/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_cosm_2024_all.pkl"
code_path = "/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_code_2024_all.pkl"

pd_diff_obs_vs_cosm = pd.read_pickle(cosm_path)
pd_diff_obs_vs_code = pd.read_pickle(code_path)

# ----------------- 2. 统一站点名大小写 -----------------
pd_diff_obs_vs_cosm["site"] = pd_diff_obs_vs_cosm["site"].str.upper()
pd_diff_obs_vs_code["site"] = pd_diff_obs_vs_code["site"].str.upper()

# ----------------- 3. 设置输出路径 -----------------
output_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "8.png")

# ----------------- 4. 选择需要的站点 -----------------
selected_sites = ["MKEA", "BOGT", "YKRO", "IISC", "GUAM"]

# ----------------- 5. 计算每个站点的全年 RMSE -----------------
def compute_rmse(df, sites):
    rmse_results = {}
    for site in sites:
        df_site = df[df["site"] == site]
        if len(df_site) == 0:
            print(f"⚠️  站点 {site} 数据为空，跳过。")
            rmse_results[site] = np.nan
        else:
            rmse_results[site] = np.sqrt(np.nanmean(df_site["delta"] ** 2))
    return rmse_results

rmse_cosm = compute_rmse(pd_diff_obs_vs_cosm, selected_sites)
rmse_code = compute_rmse(pd_diff_obs_vs_code, selected_sites)

# ----------------- 6. 组合结果为 DataFrame -----------------
df_rmse = pd.DataFrame({
    "COSMIC": rmse_cosm,
    "CODE": rmse_code
}).T  # 行是模型，列是站点
print("\n=== RMSE 对比表 ===")
print(df_rmse)

# ----------------- 7. 绘制柱状图 -----------------
x = np.arange(len(selected_sites))
width = 0.35

fig, ax = plt.subplots(figsize=(12.9/2.54, 3.5))

bars1 = ax.bar(x - width/2, df_rmse.loc["COSMIC"], width, label="GINI TEC", color="#B0D4E8")
bars2 = ax.bar(x + width/2, df_rmse.loc["CODE"], width, label="CODE TEC", color="#E59EEC")

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10

ax.set_xlabel("GNSS Station", fontsize=10)
ax.set_ylabel("RMSE (TECU)", fontsize=10)
ax.set_xticks(x)
ax.set_xticklabels(selected_sites, fontsize=10)
ax.legend(fontsize=10)
ax.grid(axis="y", linewidth=0.3, color='gray', alpha=0.7)

# ---- 关键调整部分 ----

# 1️⃣ 控制 y 轴范围，留出顶部空间
ymax = max(df_rmse.max()) * 1.15   # 给柱顶留 15% 空间
# ax.set_ylim(0, ymax)

ax.set_ylim(0, 20)


# 2️⃣ 调整标签位置，让数值始终在图内
for bars in [bars1, bars2]:
    ax.bar_label(bars, fmt="%.2f", padding=2, fontsize=9)

# 3️⃣ 优化布局，确保边缘不被裁剪
plt.tight_layout()
plt.savefig(output_path, dpi=500, bbox_inches='tight')  # ✅ 加 bbox_inches='tight'
plt.close()
