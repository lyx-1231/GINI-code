import os  
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from ppgnss import gnss_utils
import numpy as np

if __name__ == "__main__":
    # 文件路径
    cosmic_grids_file = "/home/yxlei/cosmic2gim/data/cosmic_grid_5ch_2019to2024_nonan.obj"
    xr_cosmic = gnss_utils.loadobject(cosmic_grids_file)

    # 选择时间
    time_sample = "2023-01-05 03:00:00"
    xr_cosmic_t = xr_cosmic.sel(time=time_sample)

    # 通道名称、colormap、取值范围
    channels = [
        ('occultation_flag', "Mask Layer", "Greys", 0, 1),
        ('az_sin', "LEO Azimuth Sin", "bwr", -1, 1),
        ('az_cos', "LEO Azimuth Cos", "bwr", -1, 1),
        ('max_tec', "STEC (TECU)", "jet", 0, 500)
    ]

    subplot_labels = ['(a)', '(b)', '(c)', '(d)']

    # 自定义浅色底色 colormap for STEC
    jet = plt.cm.jet(np.linspace(0, 1, 256))
    jet[:20, :] = np.array([0.95, 0.95, 0.95, 1.0])
    new_cmap = mcolors.ListedColormap(jet)

    fig, axes = plt.subplots(
        4, 1, figsize=(12, 14),
        subplot_kw={'projection': ccrs.PlateCarree()}
    )

    # 手动控制子图间距（比 constrained_layout 更可控）
    fig.subplots_adjust(hspace=0.000001)

    for i, (ch_name, cbar_label, cmap, vmin, vmax) in enumerate(channels):
        ax = axes[i]
        data = xr_cosmic_t.sel(channel=ch_name).values

        cmap_to_use = new_cmap if ch_name == 'max_tec' else cmap

        mesh = ax.pcolormesh(
            xr_cosmic_t.lon, xr_cosmic_t.lat, data,
            cmap=cmap_to_use, vmin=vmin, vmax=vmax,
            transform=ccrs.PlateCarree()
        )

        # 地图范围与海岸线
        ax.set_extent([-180, 180, -50, 50], crs=ccrs.PlateCarree())
        ax.add_feature(cfeature.COASTLINE.with_scale('110m'), linewidth=0.8)

        # 经纬网
        gl = ax.gridlines(
            draw_labels=True,
            linewidth=0.4,
            color='lightgray',
            linestyle='--',
            alpha=0.7
        )
        gl.top_labels = False
        gl.right_labels = False
        gl.xlabel_style = {'size': 12}
        gl.ylabel_style = {'size': 12}

        # 左上角子图编号 (a)(b)(c)(d)
        ax.text(
            0.02, 0.96, subplot_labels[i],
            transform=ax.transAxes,
            fontsize=15,
            # fontweight='bold',
            va='top',
            ha='left'
        )

        # 颜色条
        cbar = plt.colorbar(
            mesh, ax=ax,
            orientation='vertical',
            pad=0.015,
            shrink=0.85
        )
        cbar.set_label(cbar_label, fontsize=15)
        cbar.ax.tick_params(labelsize=15)

    # 保存路径
    save_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(
        save_dir,
        f"cosmic_input_{time_sample.replace(':','')}.png"
    )

    # plt.savefig(save_path, dpi=500, bbox_inches="tight")
    plt.savefig(save_path, dpi=500)
    plt.close()

    print(f"绘图完成，图片保存路径: {save_path}")











# import os 
# import matplotlib.pyplot as plt
# import matplotlib.colors as mcolors
# import cartopy.crs as ccrs
# import cartopy.feature as cfeature
# from ppgnss import gnss_utils
# import numpy as np

# if __name__ == "__main__":
#     # 文件路径
#     cosmic_grids_file = "/home/yxlei/cosmic2gim/data/cosmic_grid_5ch_2019to2024_nonan.obj"
#     xr_cosmic = gnss_utils.loadobject(cosmic_grids_file)

#     # 选择时间
#     time_sample = "2023-01-05 03:00:00"
#     xr_cosmic_t = xr_cosmic.sel(time=time_sample)

#     # 通道名称、标题、colormap、取值范围
#     channels = [
#         ('occultation_flag', "Mask Layer (1=occultation)", "Greys", 0, 1),
#         ('az_sin', "LEO Azimuth Sin", "bwr", -1, 1),
#         ('az_cos', "LEO Azimuth Cos", "bwr", -1, 1),
#         ('max_tec', "STEC (TECU)", "jet", 0, 500)
#     ]

#     # 自定义浅色底色 colormap for STEC
#     jet = plt.cm.jet(np.linspace(0,1,256))
#     jet[:20, :] = np.array([0.95,0.95,0.95,1.0])  # 前20个颜色改为浅灰
#     new_cmap = mcolors.ListedColormap(jet)

#     fig, axes = plt.subplots(4, 1, figsize=(12, 16),
#                              subplot_kw={'projection': ccrs.PlateCarree()},
#                              constrained_layout=True)

#     for i, (ch_name, title, cmap, vmin, vmax) in enumerate(channels):
#         ax = axes[i]
#         data = xr_cosmic_t.sel(channel=ch_name).values

#         # max_tec 使用浅色底色 colormap
#         cmap_to_use = new_cmap if ch_name == 'max_tec' else cmap

#         # 绘制 pcolormesh
#         mesh = ax.pcolormesh(
#             xr_cosmic_t.lon, xr_cosmic_t.lat, data,
#             cmap=cmap_to_use, vmin=vmin, vmax=vmax,
#             transform=ccrs.PlateCarree()
#         )

#         # 设置地图范围和海岸线
#         ax.set_extent([-180, 180, -50, 50], crs=ccrs.PlateCarree())
#         ax.add_feature(cfeature.COASTLINE.with_scale('110m'), linewidth=0.8)

#         # 背景浅色细网格线，显示经纬度标签
#         gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='lightgray', linestyle='--', alpha=0.7)
#         gl.top_labels = False
#         gl.right_labels = False
#         gl.xlabel_style = {'size': 10}
#         gl.ylabel_style = {'size': 10}

#         # 设置标题和颜色条
#         ax.set_title(title, fontsize=12)
#         cbar = plt.colorbar(mesh, ax=ax, orientation='vertical', pad=0.02, shrink=0.8)
#         cbar.set_label(title)

#     # 保存路径
#     save_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
#     os.makedirs(save_dir, exist_ok=True)
#     save_path = os.path.join(save_dir, f"cosmic_input_{time_sample.replace(':','')}.png")
#     plt.savefig(save_path, dpi=300)
#     plt.close()

#     print(f"绘图完成，图片保存路径: {save_path}")
























# import os
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.colors as mcolors
# import cartopy.crs as ccrs
# import cartopy.feature as cfeature
# from ppgnss import gnss_utils


# if __name__ == "__main__":

#     # =========================
#     # 1. 数据读取
#     # =========================
#     cosmic_grids_file = "/home/yxlei/cosmic2gim/data/cosmic_grid_5ch_2019to2024_nonan.obj"
#     xr_cosmic = gnss_utils.loadobject(cosmic_grids_file)

#     # 选择时间
#     time_sample = "2023-01-05 03:00:00"
#     xr_cosmic_t = xr_cosmic.sel(time=time_sample)

#     # =========================
#     # 2. 查看 max_tec 取值范围
#     # =========================
#     max_tec = xr_cosmic_t.sel(channel="max_tec").values
#     flag = xr_cosmic_t.sel(channel="occultation_flag").values

#     # 仅保留掩星区域
#     max_tec_occ = np.where(flag == 1, max_tec, np.nan)

#     print("=" * 50)
#     print(f"time = {time_sample}")
#     print("【全区域 max_tec】")
#     print("  min :", np.nanmin(max_tec))
#     print("  max :", np.nanmax(max_tec))
#     print("  p95 :", np.nanpercentile(max_tec, 95))
#     print("  p99 :", np.nanpercentile(max_tec, 99))

#     print("\n【掩星区域 max_tec（occultation_flag=1）】")
#     print("  min :", np.nanmin(max_tec_occ))
#     print("  max :", np.nanmax(max_tec_occ))
#     print("  p95 :", np.nanpercentile(max_tec_occ, 95))
#     print("  p99 :", np.nanpercentile(max_tec_occ, 99))
#     print("=" * 50)

#     # =========================
#     # 3. 绘图参数
#     # =========================
#     channels = [
#         ('occultation_flag', "Mask Layer (1 = Occultation)", "Greys", 0, 1),
#         ('az_sin', "LEO Azimuth Sin", "bwr", -1, 1),
#         ('az_cos', "LEO Azimuth Cos", "bwr", -1, 1),
#         ('max_tec', "STEC (TECU)", "jet", 0, 60)  # vmax 可根据上面统计结果调整
#     ]

#     # max_tec 浅色底色 colormap
#     jet = plt.cm.jet(np.linspace(0, 1, 256))
#     jet[:20, :] = np.array([0.95, 0.95, 0.95, 1.0])
#     new_cmap = mcolors.ListedColormap(jet)

#     # =========================
#     # 4. 开始绘图
#     # =========================
#     fig, axes = plt.subplots(
#         4, 1,
#         figsize=(12, 16),
#         subplot_kw={'projection': ccrs.PlateCarree()},
#         constrained_layout=True
#     )

#     for i, (ch_name, title, cmap, vmin, vmax) in enumerate(channels):
#         ax = axes[i]
#         data = xr_cosmic_t.sel(channel=ch_name).values

#         cmap_to_use = new_cmap if ch_name == 'max_tec' else cmap

#         mesh = ax.pcolormesh(
#             xr_cosmic_t.lon,
#             xr_cosmic_t.lat,
#             data,
#             cmap=cmap_to_use,
#             vmin=vmin,
#             vmax=vmax,
#             transform=ccrs.PlateCarree()
#         )

#         ax.set_extent([-180, 180, -50, 50], crs=ccrs.PlateCarree())
#         ax.add_feature(cfeature.COASTLINE.with_scale('110m'), linewidth=0.8)

#         gl = ax.gridlines(
#             draw_labels=True,
#             linewidth=0.5,
#             color='lightgray',
#             linestyle='--',
#             alpha=0.7
#         )
#         gl.top_labels = False
#         gl.right_labels = False
#         gl.xlabel_style = {'size': 10}
#         gl.ylabel_style = {'size': 10}

#         ax.set_title(title, fontsize=12)
#         cbar = plt.colorbar(mesh, ax=ax, pad=0.02, shrink=0.8)
#         cbar.set_label(title)

#     # =========================
#     # 5. 保存图像
#     # =========================
#     save_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
#     os.makedirs(save_dir, exist_ok=True)
#     save_path = os.path.join(
#         save_dir,
#         f"cosmic_input_{time_sample.replace(':', '')}.png"
#     )

#     plt.savefig(save_path, dpi=300)
#     plt.close()

#     print(f"绘图完成，图片保存路径:\n{save_path}")
