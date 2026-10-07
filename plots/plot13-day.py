import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

# ========= 参数设置 =========
model_npz_path = "scripts/test_bylyx/train_save/scripts/compare_with_jason/jason_cosmic_interp_diff.npz"
code_npz_path  = "scripts/test_bylyx/train_save/scripts/compare_with_jason/jason_code_interp_diff.npz"
save_dir       = "scripts/testbylyx/train_save/scripts/compare_with_jason/figures"
os.makedirs(save_dir, exist_ok=True)

# ========= 辅助函数 =========
def load_and_group_daily(npz_path):
    """
    读取 npz 文件，转换时间，按天分组计算rmse, mae, std, count。
    返回按天统计的DataFrame，包含列：day, rmse, mae, std, count
    """
    data = np.load(npz_path)
    times = pd.to_datetime(data['time'])  # 转时间戳
    diffs = data['diff']

    df = pd.DataFrame({
        'time': times,
        'diff': diffs
    })
    df['day'] = df['time'].dt.floor('D')  # 按天取整

    grouped = df.groupby('day')['diff'].agg([
        ('rmse', lambda x: np.sqrt(np.nanmean(x**2))),
        ('mae',  lambda x: np.nanmean(np.abs(x))),
        ('std',  lambda x: np.nanstd(x)),
        ('count', 'count')
    ]).reset_index()

    return grouped

# ========= 加载数据并按天计算 =========
df_model = load_and_group_daily(model_npz_path)
df_code  = load_and_group_daily(code_npz_path)

# ========= 合并两个数据 =========
df_all = pd.merge(df_model, df_code, on='day', suffixes=('_model', '_code'))
df_all = df_all.sort_values('day').reset_index(drop=True)

# ========= 绘图函数 =========
def plot_metric(metric_name, ylabel):
    plt.figure(figsize=(12.9/2.54, 2.5))  # 转为英寸尺寸

    plt.plot(df_all['day'], df_all[f'{metric_name}_code'], label='CODE TEC', color='#3c7fb1')
    plt.plot(df_all['day'], df_all[f'{metric_name}_model'], label='GINI TEC', color='#b53289')

    plt.xlabel("Time (Month-Day, 2024)")
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(axis='y', linewidth=0.8, alpha=0.8)

    # 时间格式化
    # ax = plt.gca()
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    # ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))  # 每3天一个主刻度
    # plt.xticks(rotation=45)

    # 时间轴格式美化
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.xticks(rotation=45)

    # 设置x轴范围紧贴数据范围
    start_time = df_all['day'].min()
    end_time = df_all['day'].max()
    plt.xlim(start_time, end_time)

    plt.tight_layout()

    # 保存路径和文件名
    # fname = f"{metric_name}_daily_comparison.png"
    save_path =  "/home/yxlei/cosmic2gim/scripts/plots/figures/13-daily-rmse.png"
    plt.savefig(save_path, dpi=500)
    plt.close()
    print(f"图已保存：{save_path}")

# ========= 生成图像 =========
plot_metric('rmse', 'RMSE (TECU)')
# plot_metric('mae', 'MAE (TECU)')
# plot_metric('std', 'STD (TECU)')
