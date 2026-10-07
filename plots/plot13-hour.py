# -------------------- 每小时误差 -----------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

# ========= 参数设置 =========
model_npz_path = "scripts/test_bylyx/train_save/scripts/compare_with_jason/jason_cosmic_interp_diff.npz"
code_npz_path  = "scripts/test_bylyx/train_save/scripts/compare_with_jason/jason_code_interp_diff.npz"
save_dir       = "scripts/test_bylyx/train_save/scripts/compare_with_jason/figures"
os.makedirs(save_dir, exist_ok=True)


# ========= 辅助函数 =========
def load_and_group_hourly(npz_path):
    data = np.load(npz_path)
    times = pd.to_datetime(data['time'])  # ndarray of datetime64[ns]
    diffs = data['diff']

    # 转为 DataFrame 以便分组
    df = pd.DataFrame({
        'time': times,
        'diff': diffs
    })
    df['hour'] = df['time'].dt.floor('h')

    # 分组统计
    grouped = df.groupby('hour')['diff'].agg([
        ('rmse', lambda x: np.sqrt(np.nanmean(x**2))),
        ('mae',  lambda x: np.nanmean(np.abs(x))),
        ('std',  lambda x: np.nanstd(x)),
        ('count', 'count')
    ]).reset_index()

    return grouped

# ========= 加载并计算 =========
df_model = load_and_group_hourly(model_npz_path)
df_code  = load_and_group_hourly(code_npz_path)

# 合并两个 DataFrame 以便对比绘图
df_all = pd.merge(df_model, df_code, on='hour', suffixes=('_model', '_code'))

# ========= 绘图函数 =========
def plot_metric(metric_name, ylabel):
    plt.figure(figsize=(12.9/2.54, 2.5))

    plt.plot(df_all['hour'], df_all[f'{metric_name}_code'], label='CODE TEC', color='#3c7fb1')
    plt.plot(df_all['hour'], df_all[f'{metric_name}_model'], label='Model TEC', color='#b53289')


    plt.xlabel("Time (Month-Day,2024))")
    plt.ylabel(ylabel)
    # plt.title(f"{ylabel} Comparison Over Time")
    plt.legend()
    plt.grid(axis='y', linewidth=0.8, alpha=0.8)

    # 时间轴格式美化
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.xticks(rotation=45)

    # 限制x轴范围去掉多余空白
    start_time = df_all['hour'].min()
    end_time = df_all['hour'].max()
    plt.xlim(start_time, end_time)
    
    plt.tight_layout()

    

    # 保存图像
    save_path = "/home/yxlei/cosmic2gim/scripts/plots/figures/13-hourly-rmse.png"
    plt.savefig(save_path, dpi=500)
    plt.close()
    print(f"图已保存：{save_path}")

# ========= 生成图像 =========
plot_metric('rmse', 'RMSE (TECU)')
# plot_metric('mae', 'MAE [TECU]')
# plot_metric('std', 'STD [TECU]')


