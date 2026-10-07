# import os
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

# # ----------------- 1. 读取差分结果 DataFrame -----------------
# cosm_path = "/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_cosm_2024_all.pkl"
# code_path = "/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_code_2024_all.pkl"

# df_cosm = pd.read_pickle(cosm_path)
# df_code = pd.read_pickle(code_path)

# # ----------------- 2. 统一站点名大小写 -----------------
# df_cosm["site"] = df_cosm["site"].str.upper()
# df_code["site"] = df_code["site"].str.upper()

# # ----------------- 3. 计算按纬度分段的 RMSE -----------------
# def compute_latitude_rmse(df, lat_bin_width=1.0):
#     # 按纬度分bin
#     lat_bins = np.arange(-90, 90 + lat_bin_width, lat_bin_width)
#     df['lat_bin'] = pd.cut(df['lat'], bins=lat_bins, include_lowest=True)

#     # 计算每个纬度bin的RMSE
#     rmse_by_lat = df.groupby('lat_bin')['delta'].apply(lambda x: np.sqrt(np.nanmean(x**2)))

#     # 提取每个bin的中心值作为x轴
#     bin_centers = rmse_by_lat.index.map(lambda interval: interval.left + lat_bin_width/2)

#     return bin_centers, rmse_by_lat.values

# # ----------------- 4. 计算COSMIC和CODE的纬度RMSE -----------------
# lat_bin_width = 1.0  # 可以根据需要调整
# cosm_lat_centers, cosm_rmse = compute_latitude_rmse(df_cosm, lat_bin_width)
# code_lat_centers, code_rmse = compute_latitude_rmse(df_code, lat_bin_width)

# # ----------------- 5. 绘图 -----------------
# plt.rcParams['font.family'] = 'Arial'
# plt.rcParams['font.size'] = 10

# fig, ax = plt.subplots(figsize=(12/2.54, 9/2.54))

# ax.plot(cosm_lat_centers, cosm_rmse, label='Model TEC', color="#70bcf3", linewidth=1.8,
#             marker='s',
#             markersize=4)
# ax.plot(code_lat_centers, code_rmse, label='CODE TEC', color="#efc2ee", linewidth=1.8,
#             marker='s',
#             markersize=4)



# ax.set_xlabel("Latitude (°)", fontsize=10)
# ax.set_ylabel("RMSE (TECU)", fontsize=10)
# # ax.set_title("RMSE of ΔTEC by Latitude (2024)", fontsize=14)
# # ax.grid(True, linestyle='--', alpha=0.5)
# ax.grid(axis="y", linewidth=0.3, color='gray', alpha=0.7)

# ax.legend(fontsize=10)

# # 使用xlim去掉左右空白区域
# xmin, xmax = cosm_lat_centers.min(), cosm_lat_centers.max()
# ax.set_xlim(xmin, xmax)

# plt.tight_layout()

# # ----------------- 6. 保存图像 -----------------
# output_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
# os.makedirs(output_dir, exist_ok=True)
# output_path = os.path.join(output_dir, "10.png")
# plt.savefig(output_path, dpi=400, bbox_inches='tight')
# plt.close()

# print(f"✅ 绘图完成，已保存到：{output_path}")









import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ----------------- 1. 读取差分结果 DataFrame -----------------
cosm_path = "/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_cosm_2024_all.pkl"
code_path = "/home/yxlei/cosmic2gim/scripts/data/pd_diff_obs_vs_code_2024_all.pkl"

df_cosm = pd.read_pickle(cosm_path)
df_code = pd.read_pickle(code_path)

# ----------------- 2. 统一站点名大小写 -----------------
df_cosm["site"] = df_cosm["site"].str.upper()
df_code["site"] = df_code["site"].str.upper()

# ----------------- 3. 计算按纬度分段的 RMSE -----------------
def compute_latitude_rmse(df, lat_bin_width=1.0):
    # 按纬度分bin
    lat_bins = np.arange(-90, 90 + lat_bin_width, lat_bin_width)
    df['lat_bin'] = pd.cut(df['lat'], bins=lat_bins, include_lowest=True)

    # 计算每个纬度bin的RMSE
    rmse_by_lat = df.groupby('lat_bin')['delta'].apply(lambda x: np.sqrt(np.nanmean(x**2)))

    # 提取每个bin的中心值作为x轴
    bin_centers = rmse_by_lat.index.map(lambda interval: interval.left + lat_bin_width/2)

    return bin_centers, rmse_by_lat.values

# ----------------- 4. 计算COSMIC和CODE的纬度RMSE -----------------
lat_bin_width = 1.0  # 可以根据需要调整
cosm_lat_centers, cosm_rmse = compute_latitude_rmse(df_cosm, lat_bin_width)
code_lat_centers, code_rmse = compute_latitude_rmse(df_code, lat_bin_width)

# ----------------- 5. 绘图 -----------------
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10

fig, ax = plt.subplots(figsize=(12/2.54, 9/2.54))
# fig, ax = plt.subplots(figsize=(10, 6))

# ax.plot(cosm_lat_centers, cosm_rmse, label='COSMIC', color='#1f77b4', linewidth=1)
# ax.plot(code_lat_centers, code_rmse, label='CODE', color='#ff7f0e', linewidth=1)

ax.plot(cosm_lat_centers, cosm_rmse, label='GINI TEC', color="#63abdf", linewidth=1.8,marker='s',markersize=4)
ax.plot(code_lat_centers, code_rmse, label='CODE TEC', color="#bd4bbb", linewidth=1.8,marker='s',markersize=4)



ax.set_xlabel("Latitude (°)", fontsize=10)
ax.set_ylabel("RMSE (TECU)", fontsize=10)
# ax.set_title("RMSE of ΔTEC by Latitude (2024)", fontsize=14)
# ax.grid(True, linestyle='--', alpha=0.5)
ax.grid(axis="y", linewidth=0.3, color='gray', alpha=0.7)
ax.legend(fontsize=10)

ax.set_xlim(-2.513151,  25.719002)
ax.set_ylim(0,15)

plt.tight_layout()

# ----------------- 6. 保存图像 -----------------
output_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "10.png")
plt.savefig(output_path, dpi=600, bbox_inches='tight')
plt.close()

print(f"✅ 绘图完成，已保存到：{output_path}")
