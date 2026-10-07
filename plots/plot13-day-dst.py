import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

# ========= 参数设置 =========
model_npz_path = "scripts/test_bylyx/train_save/scripts/compare_with_jason/jason_cosmic_interp_diff.npz"
code_npz_path  = "scripts/test_bylyx/train_save/scripts/compare_with_jason/jason_code_interp_diff.npz"
dst_npz_path   = "/home/yxlei/cosmic2gim/data/20191001_20241231_dst_series.npz"
save_dir       = "scripts/testbylyx/train_save/scripts/compare_with_jason/figures"
os.makedirs(save_dir, exist_ok=True)

# ========= 辅助函数 =========
def load_and_group_daily(npz_path):
    """读取 npz 文件，转换时间，按天分组计算rmse, mae, std, count。"""
    data = np.load(npz_path)
    times = pd.to_datetime(data['time'])
    diffs = data['diff']

    df = pd.DataFrame({
        'time': times,
        'diff': diffs
    })
    df['day'] = df['time'].dt.floor('D')

    grouped = df.groupby('day')['diff'].agg([
        ('rmse', lambda x: np.sqrt(np.nanmean(x**2))),
        ('mae',  lambda x: np.nanmean(np.abs(x))),
        ('std',  lambda x: np.nanstd(x)),
        ('count', 'count')
    ]).reset_index()

    return grouped

# ========= 加载数据 =========
df_model = load_and_group_daily(model_npz_path)
df_code  = load_and_group_daily(code_npz_path)

df_all = pd.merge(df_model, df_code, on='day', suffixes=('_model', '_code')).sort_values('day').reset_index(drop=True)

# ========= 加载Dst指数 =========
dst_data = np.load(dst_npz_path, allow_pickle=True)
dst_time = pd.to_datetime(dst_data['timestamps'])
dst_value = dst_data['dst']

df_dst = pd.DataFrame({'time': dst_time, 'dst': dst_value})
df_dst['day'] = df_dst['time'].dt.floor('D')
df_dst_daily = df_dst.groupby('day')['dst'].mean().reset_index()  # 按天平均

# ========= 绘图函数 =========
def plot_metric(metric_name, ylabel):
    fig, ax1 = plt.subplots(figsize=(12.9/2.54, 2.5))

    # 左轴：RMSE/MAE/STD
    ax1.plot(df_all['day'], df_all[f'{metric_name}_code'], label='CODE TEC', color='#3c7fb1', linewidth=1.2)
    ax1.plot(df_all['day'], df_all[f'{metric_name}_model'], label='GINI TEC', color='#b53289', linewidth=1.2)
    ax1.set_xlabel("Time (Month-Day, 2024)")
    ax1.set_ylabel(ylabel)
    ax1.grid(axis='y', linewidth=0.8, alpha=0.8)
    ymin, ymax = ax1.get_ylim()
    ax1.set_ylim(ymin, ymax * 1.4)   # 让上边多留 10%


    # 右轴：Dst指数（橙色）
    ax2 = ax1.twinx()
    ax2.plot(df_dst_daily['day'], df_dst_daily['dst'], color='orange', label='DST', linewidth=1.0, alpha=0.85)
    ax2.set_ylabel("DST (nT)", color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')
    ax2.set_ylim(-320, 70)

    # 时间轴格式化
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    ax1.xaxis.set_major_locator(mdates.MonthLocator())
    plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')

    # 对齐x轴范围
    start_time = df_all['day'].min()
    end_time = df_all['day'].max()
    ax1.set_xlim(start_time, end_time)
    ax2.set_xlim(start_time, end_time)

    # 合并图例 —— 横向放置在左上角
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(
        lines_1 + lines_2,
        labels_1 + labels_2,
        loc='upper left',
        bbox_to_anchor=(0, 1.04),  # 上移一点，避免遮挡图像
        ncol=3,                    # 横向排列
        fontsize=8,
        frameon=False               # 去掉边框（可改为True保留）
    )

    plt.tight_layout()
    save_path = "/home/yxlei/cosmic2gim/scripts/plots/figures/13-daily-rmse_dst.png"
    plt.savefig(save_path, dpi=500)
    plt.close()
    print(f"图已保存：{save_path}")

# ========= 生成图像 =========
plot_metric('rmse', 'RMSE (TECU)')
# plot_metric('mae', 'MAE (TECU)')
# plot_metric('std', 'STD (TECU)')
