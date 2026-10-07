# # # import numpy as np
# # # import pandas as pd

# # # # ===================== 参数设置 =====================
# # # model_npz_path = "scripts/test_bylyx/train_save/scripts/compare_with_jason/jason_cosmic_interp_diff.npz"

# # # # ===================== 读取数据函数 =====================
# # # def load_diff_data(npz_path):
# # #     data = np.load(npz_path)
# # #     times = pd.to_datetime(data['time'])
# # #     lats = data['lat']
# # #     lons = data['lon']
# # #     diffs = data['diff']
# # #     return times, lats, lons, diffs


# # # def build_dataframe(times, lats, lons, diffs):
# # #     return pd.DataFrame({'time': times, 'lat': lats, 'lon': lons, 'diff': diffs})


# # # def get_season(month):
# # #     if month in [3, 4, 5]:
# # #         return 'Spring'
# # #     elif month in [6, 7, 8]:
# # #         return 'Summer'
# # #     elif month in [9, 10, 11]:
# # #         return 'Autumn'
# # #     else:
# # #         return 'Winter'


# # # def get_local_period(row):
# # #     local_hour = (row['time'].hour + row['lon'] / 15) % 24
# # #     if 12 <= local_hour < 16:
# # #         return 'day'
# # #     elif 0 <= local_hour < 4:
# # #         return 'night'
# # #     else:
# # #         return None


# # # def compute_rmse(x):
# # #     return np.sqrt(np.nanmean(x ** 2))


# # # # ===================== 加载与处理数据 =====================
# # # times_m, lats_m, lons_m, diffs_m = load_diff_data(model_npz_path)
# # # df_model = build_dataframe(times_m, lats_m, lons_m, diffs_m)

# # # df_model['season'] = df_model['time'].dt.month.apply(get_season)
# # # df_model['period'] = df_model.apply(get_local_period, axis=1)
# # # df_model = df_model[df_model['period'].notnull()]  # 只保留夜间和白天数据

# # # # ===================== 计算RMSE和STD =====================
# # # season_order = ['Spring', 'Summer', 'Autumn', 'Winter']
# # # period_order = ['night', 'day']

# # # results = []

# # # for season in season_order:
# # #     for period in period_order:
# # #         sub_df = df_model[(df_model['season'] == season) & (df_model['period'] == period)]
# # #         if len(sub_df) == 0:
# # #             continue
# # #         rmse = compute_rmse(sub_df['diff'].values)
# # #         std = np.nanstd(sub_df['diff'].values)
# # #         results.append([season, period, len(sub_df), rmse, std])

# # # # ===================== 打印结果 =====================
# # # result_df = pd.DataFrame(results, columns=['Season', 'Period', 'Count', 'RMSE', 'STD'])
# # # print("\n==== RMSE & STD by Season and Period ====\n")
# # # print(result_df.to_string(index=False, justify='center', float_format="%.3f"))


















# # import numpy as np
# # import pandas as pd

# # # ===================== 参数设置 =====================
# # # model_npz_path = "scripts/test_bylyx/train_save/scripts/compare_with_jason/jason_cosmic_interp_diff.npz"
# # model_npz_path = "scripts/test_bylyx/train_save/scripts/compare_with_jason/jason_code_interp_diff.npz"


# # # ===================== 读取数据函数 =====================
# # def load_diff_data(npz_path):
# #     data = np.load(npz_path)
# #     times = pd.to_datetime(data['time'])
# #     lats = data['lat']
# #     lons = data['lon']
# #     diffs = data['diff']
# #     return times, lats, lons, diffs


# # def build_dataframe(times, lats, lons, diffs):
# #     # 转换为浮点数，并忽略无法转换的项
# #     diffs = pd.to_numeric(pd.Series(diffs).astype(str), errors='coerce')
# #     return pd.DataFrame({'time': times, 'lat': lats, 'lon': lons, 'diff': diffs})


# # def get_season(month):
# #     if month in [3, 4, 5]:
# #         return 'Spring'
# #     elif month in [6, 7, 8]:
# #         return 'Summer'
# #     elif month in [9, 10, 11]:
# #         return 'Autumn'
# #     else:
# #         return 'Winter'


# # def get_local_period(row):
# #     local_hour = (row['time'].hour + row['lon'] / 15) % 24
# #     if 12 <= local_hour < 16:
# #         return 'day'
# #     elif 0 <= local_hour < 4:
# #         return 'night'
# #     else:
# #         return None


# # def compute_rmse(x):
# #     return np.sqrt(np.mean(x ** 2))


# # # ===================== 加载与处理数据 =====================
# # times_m, lats_m, lons_m, diffs_m = load_diff_data(model_npz_path)
# # df_model = build_dataframe(times_m, lats_m, lons_m, diffs_m)

# # # 删除 NaN 值
# # df_model = df_model.dropna(subset=['diff'])

# # df_model['season'] = df_model['time'].dt.month.apply(get_season)
# # df_model['period'] = df_model.apply(get_local_period, axis=1)
# # df_model = df_model[df_model['period'].notnull()]  # 只保留夜间和白天数据

# # # ===================== 计算RMSE和STD =====================
# # season_order = ['Spring', 'Summer', 'Autumn', 'Winter']
# # period_order = ['night', 'day']

# # results = []

# # for season in season_order:
# #     for period in period_order:
# #         sub_df = df_model[(df_model['season'] == season) & (df_model['period'] == period)]
# #         if len(sub_df) == 0:
# #             continue
# #         vals = sub_df['diff'].dropna().values
# #         rmse = np.sqrt(np.mean(vals ** 2))
# #         std = np.std(vals)
# #         results.append([season, period, len(vals), rmse, std])

# # # ===================== 打印结果 =====================
# # result_df = pd.DataFrame(results, columns=['Season', 'Period', 'Count', 'RMSE', 'STD'])
# # print("\n==== RMSE & STD by Season and Period ====\n")
# # print(result_df.to_string(index=False, justify='center', float_format="%.3f"))
 








# import numpy as np
# import pandas as pd

# # ===================== 参数设置 =====================
# model_npz_path = "scripts/test_bylyx/train_save/scripts/compare_with_jason/jason_cosmic_interp_diff.npz"

# # ===================== 读取数据函数 =====================
# def load_diff_data(npz_path):
#     data = np.load(npz_path)
#     times = pd.to_datetime(data['time'])
#     lats = data['lat']
#     lons = data['lon']
#     diffs = data['diff']
#     return times, lats, lons, diffs


# def build_dataframe(times, lats, lons, diffs):
#     # 转换为浮点数，并忽略无法转换的项
#     diffs = pd.to_numeric(pd.Series(diffs).astype(str), errors='coerce')
#     return pd.DataFrame({'time': times, 'lat': lats, 'lon': lons, 'diff': diffs})


# def get_season(month):
#     if month in [3, 4, 5]:
#         return 'Spring'
#     elif month in [6, 7, 8]:
#         return 'Summer'
#     elif month in [9, 10, 11]:
#         return 'Autumn'
#     else:
#         return 'Winter'


# def get_local_period(row):
#     local_hour = (row['time'].hour + row['lon'] / 15) % 24
#     if 12 <= local_hour < 16:
#         return 'day'
#     elif 0 <= local_hour < 4:
#         return 'night'
#     else:
#         return None


# # ===================== 加载与处理数据 =====================
# times_m, lats_m, lons_m, diffs_m = load_diff_data(model_npz_path)
# df_model = build_dataframe(times_m, lats_m, lons_m, diffs_m)

# # 删除 NaN 值
# df_model = df_model.dropna(subset=['diff'])

# df_model['season'] = df_model['time'].dt.month.apply(get_season)
# df_model['period'] = df_model.apply(get_local_period, axis=1)
# df_model = df_model[df_model['period'].notnull()]  # 只保留夜间和白天数据

# # ===================== 计算全年两个时间段的diff平均值 =====================
# period_order = ['night', 'day']
# results_annual_mean = []

# for period in period_order:
#     sub_df_all = df_model[df_model['period'] == period]
#     mean_diff = sub_df_all['diff'].mean()
#     count = len(sub_df_all)
#     results_annual_mean.append([period, count, mean_diff])

# # ===================== 打印结果 =====================
# result_annual_mean_df = pd.DataFrame(results_annual_mean, columns=['Period', 'Count', 'Mean Diff'])
# print("\n==== Annual Mean Diff for Night (00:00-04:00 UT) and Day (12:00-16:00 UT) ====\n")
# print(result_annual_mean_df.to_string(index=False, justify='center', float_format="%.6f"))










import numpy as np
import pandas as pd

# ===================== 参数设置 =====================
model_npz_path = "scripts/test_bylyx/train_save/scripts/compare_with_jason/jason_code_interp_diff.npz"

# ===================== 读取数据函数 =====================
def load_diff_data(npz_path):
    data = np.load(npz_path)
    times = pd.to_datetime(data['time'])
    lats = data['lat']
    lons = data['lon']
    diffs = data['diff']
    return times, lats, lons, diffs


def build_dataframe(times, lats, lons, diffs):
    # 转换为浮点数，并忽略无法转换的项
    diffs = pd.to_numeric(pd.Series(diffs).astype(str), errors='coerce')
    return pd.DataFrame({'time': times, 'lat': lats, 'lon': lons, 'diff': diffs})


def get_local_period(row):
    local_hour = (row['time'].hour + row['lon'] / 15) % 24
    if 12 <= local_hour < 16:
        return True  # 白天
    elif 0 <= local_hour < 4:
        return True  # 夜间
    else:
        return False


# ===================== 加载与处理数据 =====================
times_m, lats_m, lons_m, diffs_m = load_diff_data(model_npz_path)
df_model = build_dataframe(times_m, lats_m, lons_m, diffs_m)

# 删除 NaN 值
df_model = df_model.dropna(subset=['diff'])

# 过滤只保留夜间和白天时间段数据
df_model['in_target_period'] = df_model.apply(get_local_period, axis=1)
df_filtered = df_model[df_model['in_target_period']]

# 计算整体平均 diff
overall_mean_diff = df_filtered['diff'].mean()

print(f"\n==== Overall Mean diff for 00:00-04:00 and 12:00-16:00 UT ====\n")
print(f"Mean diff: {overall_mean_diff:.4f}")
