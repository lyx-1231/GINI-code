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

    # 通道名称、标题、colormap、取值范围
    channels = [
        ('occultation_flag', "Mask Layer (1=occultation)", "Greys", 0, 1),
        ('az_sin', "LEO Azimuth Sin", "bwr", -1, 1),
        ('az_cos', "LEO Azimuth Cos", "bwr", -1, 1),
        ('max_tec', "STEC (TECU)", "jet", 0, 100)
    ]

    # 自定义浅色底色 colormap for STEC
    jet = plt.cm.jet(np.linspace(0,1,256))
    jet[:20, :] = np.array([0.95,0.95,0.95,1.0])  # 前20个颜色改为浅灰
    new_cmap = mcolors.ListedColormap(jet)

    fig, axes = plt.subplots(4, 1, figsize=(12, 16),
                             subplot_kw={'projection': ccrs.PlateCarree()},
                             constrained_layout=True)

    for i, (ch_name, title, cmap, vmin, vmax) in enumerate(channels):
        ax = axes[i]
        data = xr_cosmic_t.sel(channel=ch_name).values

        # max_tec 使用浅色底色 colormap
        cmap_to_use = new_cmap if ch_name == 'max_tec' else cmap

        # 绘制 pcolormesh
        mesh = ax.pcolormesh(
            xr_cosmic_t.lon, xr_cosmic_t.lat, data,
            cmap=cmap_to_use, vmin=vmin, vmax=vmax,
            transform=ccrs.PlateCarree()
        )

        # 设置地图范围和海岸线
        ax.set_extent([-180, 180, -50, 50], crs=ccrs.PlateCarree())
        ax.add_feature(cfeature.COASTLINE.with_scale('110m'), linewidth=0.8)

        # 背景浅色细网格线，显示经纬度标签
        gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='lightgray', linestyle='--', alpha=0.7)
        gl.top_labels = False
        gl.right_labels = False
        gl.xlabel_style = {'size': 10}
        gl.ylabel_style = {'size': 10}

        # 设置标题和颜色条
        ax.set_title(title, fontsize=12)
        cbar = plt.colorbar(mesh, ax=ax, orientation='vertical', pad=0.02, shrink=0.8)
        cbar.set_label(title)

    # 保存路径
    save_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f"7.png")
    plt.savefig(save_path, dpi=300)
    plt.close()

    print(f"绘图完成，图片保存路径: {save_path}")


























# # from ppgnss import gnss_utils
# # import os
# # import pickle
# # import matplotlib.pyplot as plt

# # if __name__ == "__main__":
# #     current_dir = os.path.dirname(os.path.abspath(__file__))

# #     # cosmic_grids_file = os.path.join(current_dir, "..", "data", f"cosmic_grid_2022_034.obj")
# #     # cosmic_grids_file = os.path.join(current_dir, "..", "data", f"cosmic_grid_5ch_2022_034.obj")
# #     cosmic_grids_file = "/home/yxlei/cosmic2gim/data/cosmic_grid_5ch_2019to2024_nonan.obj"  # 6.15  2019-2024的完整cosmic数据


# #     xr_cosmic = gnss_utils.loadobject(cosmic_grids_file)

# #     print(xr_cosmic)


# #     time_sample = "2023-01-05 03:00:00"
# #     xr_cosmic = xr_cosmic.loc[time_sample]
# #     print(xr_cosmic.lat.min(), xr_cosmic.lat.max())
# #     print(xr_cosmic)
# #     fig, axes = plt.subplots(4,1, figsize=(10, 10))
# #     axes[0].pcolormesh(xr_cosmic.lon, xr_cosmic.lat, xr_cosmic.loc[:, :, "occultation_flag"])
# #     axes[1].pcolormesh(xr_cosmic.lon, xr_cosmic.lat, xr_cosmic.loc[:, :, "az_sin"])
# #     axes[2].pcolormesh(xr_cosmic.lon, xr_cosmic.lat, xr_cosmic.loc[:, :, "az_cos"])
# #     axes[3].pcolormesh(xr_cosmic.lon, xr_cosmic.lat, xr_cosmic.loc[:, :, "max_tec"])

# #     plt.savefig("/home/yxlei/cosmic2gim/scripts/plots/figures/occ.png")

# #     plt.close()
    










# # import os
# # import matplotlib.pyplot as plt
# # from ppgnss import gnss_utils

# # if __name__ == "__main__":
# #     # 文件路径
# #     cosmic_grids_file = "/home/yxlei/cosmic2gim/data/cosmic_grid_5ch_2019to2024_nonan.obj"
# #     xr_cosmic = gnss_utils.loadobject(cosmic_grids_file)

# #     # 选择时间
# #     time_sample = "2023-01-05 03:00:00"
# #     xr_cosmic_t = xr_cosmic.sel(time=time_sample)

# #     # 通道名称、标题、colormap、取值范围
# #     channels = [
# #         ('occultation_flag', "Mask Layer (1=occultation)", "Greys", 0, 1),
# #         ('az_sin', "LEO Azimuth Sin", "bwr", -1, 1),
# #         ('az_cos', "LEO Azimuth Cos", "bwr", -1, 1),
# #         ('max_tec', "STEC (TECU)", "jet", 0, 100)
# #     ]

# #     fig, axes = plt.subplots(4, 1, figsize=(12, 12), constrained_layout=True)

# #     for i, (ch_name, title, cmap, vmin, vmax) in enumerate(channels):
# #         ax = axes[i]
# #         # 取出通道数据 (lat, lon)
# #         data = xr_cosmic_t.sel(channel=ch_name).values
# #         mesh = ax.pcolormesh(
# #             xr_cosmic_t.lon, xr_cosmic_t.lat, data,
# #             cmap=cmap, vmin=vmin, vmax=vmax
# #         )
# #         ax.set_title(title, fontsize=12)
# #         ax.set_xlabel("Longitude (°)")
# #         ax.set_ylabel("Latitude (°)")
# #         ax.set_xlim([-180, 180])
# #         ax.set_ylim([-50, 50])
# #         cbar = plt.colorbar(mesh, ax=ax, orientation="vertical", pad=0.02)
# #         cbar.set_label(title)

# #     # 保存路径
# #     save_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
# #     os.makedirs(save_dir, exist_ok=True)
# #     save_path = os.path.join(save_dir, f"cosmic_input_{time_sample.replace(':','')}.png")
# #     plt.savefig(save_path, dpi=300)
# #     plt.close()

# #     print(f"绘图完成，图片保存路径: {save_path}")










# import os
# import matplotlib.pyplot as plt
# import cartopy.crs as ccrs
# import cartopy.feature as cfeature
# from ppgnss import gnss_utils

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
#         ('max_tec', "STEC (TECU)", "jet", 0, 100)
#     ]

#     fig, axes = plt.subplots(4, 1, figsize=(12, 16),
#                              subplot_kw={'projection': ccrs.PlateCarree()},
#                              constrained_layout=True)

#     for i, (ch_name, title, cmap, vmin, vmax) in enumerate(channels):
#         ax = axes[i]
#         data = xr_cosmic_t.sel(channel=ch_name).values

#         # 绘制 pcolormesh
#         mesh = ax.pcolormesh(
#             xr_cosmic_t.lon, xr_cosmic_t.lat, data,
#             cmap=cmap, vmin=vmin, vmax=vmax,
#             transform=ccrs.PlateCarree()
#         )

#         # 设置地图
#         ax.set_extent([-180, 180, -50, 50], crs=ccrs.PlateCarree())
#         ax.add_feature(cfeature.COASTLINE.with_scale('110m'), linewidth=0.8)
#         # ax.add_feature(cfeature.BORDERS.with_scale('110m'), linestyle=':')
#         ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

#         # 标题和颜色条
#         ax.set_title(title, fontsize=12)
#         cbar = plt.colorbar(mesh, ax=ax, orientation='vertical', pad=0.02, shrink=0.8)
#         cbar.set_label(title)

#     # 保存路径
#     save_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
#     os.makedirs(save_dir, exist_ok=True)
#     save_path = os.path.join(save_dir, f"7.png")
#     plt.savefig(save_path, dpi=300)
#     plt.close()

#     print(f"绘图完成，图片保存路径: {save_path}")








# # import os
# # import matplotlib.pyplot as plt
# # import cartopy.crs as ccrs
# # import cartopy.feature as cfeature
# # from ppgnss import gnss_utils
# # import numpy as np

# # if __name__ == "__main__":
# #     # 文件路径
# #     cosmic_grids_file = "/home/yxlei/cosmic2gim/data/cosmic_grid_5ch_2019to2024_nonan.obj"
# #     xr_cosmic = gnss_utils.loadobject(cosmic_grids_file)

# #     # 选择时间
# #     time_sample = "2023-01-05 03:00:00"
# #     xr_cosmic_t = xr_cosmic.sel(time=time_sample)

# #     # 通道名称、标题、colormap、取值范围
# #     channels = [
# #         ('occultation_flag', "Mask Layer (1=occultation)", "Greys", 0, 1),
# #         ('az_sin', "LEO Azimuth Sin", "bwr", -1, 1),
# #         ('az_cos', "LEO Azimuth Cos", "bwr", -1, 1),
# #         ('max_tec', "STEC (TECU)", "jet", 0, 100)
# #     ]

# #     fig, axes = plt.subplots(4, 1, figsize=(12, 16),
# #                              subplot_kw={'projection': ccrs.PlateCarree()},
# #                              constrained_layout=True)

# #     for i, (ch_name, title, cmap, vmin, vmax) in enumerate(channels):
# #         ax = axes[i]
# #         data = xr_cosmic_t.sel(channel=ch_name).values

# #         # 对 STEC 图使用浅色底图
# #         if ch_name == 'max_tec':
# #             ax.set_facecolor("whitesmoke")  # 浅灰背景

# #         # 绘制 pcolormesh
# #         mesh = ax.pcolormesh(
# #             xr_cosmic_t.lon, xr_cosmic_t.lat, data,
# #             cmap=cmap, vmin=vmin, vmax=vmax,
# #             transform=ccrs.PlateCarree()
# #         )

# #         # 地图设置
# #         ax.set_extent([-180, 180, -50, 50], crs=ccrs.PlateCarree())
# #         ax.add_feature(cfeature.COASTLINE.with_scale('110m'), linewidth=0.8)
# #         # ax.add_feature(cfeature.BORDERS.with_scale('110m'), linestyle=':')
# #         ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

# #         # 标题和颜色条
# #         ax.set_title(title, fontsize=12)
# #         cbar = plt.colorbar(mesh, ax=ax, orientation='vertical', pad=0.02, shrink=0.8)
# #         cbar.set_label(title)

# #     # 保存路径
# #     save_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
# #     os.makedirs(save_dir, exist_ok=True)
# #     save_path = os.path.join(save_dir, f"7.png")
# #     plt.savefig(save_path, dpi=300)
# #     plt.close()

# #     print(f"绘图完成，图片保存路径: {save_path}")









# # import os
# # import matplotlib.pyplot as plt
# # import matplotlib.colors as mcolors
# # import cartopy.crs as ccrs
# # import cartopy.feature as cfeature
# # from ppgnss import gnss_utils
# # import numpy as np

# # cosmic_grids_file = "/home/yxlei/cosmic2gim/data/cosmic_grid_5ch_2019to2024_nonan.obj"
# # xr_cosmic = gnss_utils.loadobject(cosmic_grids_file)

# # time_sample = "2023-01-05 03:00:00"
# # xr_cosmic_t = xr_cosmic.sel(time=time_sample)

# # channels = [
# #     ('occultation_flag', "Mask Layer (1=occultation)", "Greys", 0, 1),
# #     ('az_sin', "LEO Azimuth Sin", "bwr", -1, 1),
# #     ('az_cos', "LEO Azimuth Cos", "bwr", -1, 1),
# #     ('max_tec', "STEC (TECU)", "jet", 0, 100)
# # ]

# # # 自定义浅色低值 colormap for max_tec
# # jet = plt.cm.jet(np.linspace(0,1,256))
# # # jet[:10, :] = np.array([0.9,0.9,0.9,1.0])  # 前10个颜色改为浅灰
# # new_cmap = mcolors.ListedColormap(jet)

# # fig, axes = plt.subplots(4, 1, figsize=(12, 16),
# #                          subplot_kw={'projection': ccrs.PlateCarree()},
# #                          constrained_layout=True)

# # for i, (ch_name, title, cmap, vmin, vmax) in enumerate(channels):
# #     ax = axes[i]
# #     data = xr_cosmic_t.sel(channel=ch_name).values

# #     # # max_tec 使用浅色低值 colormap
# #     cmap_to_use = new_cmap if ch_name == 'max_tec' else cmap

# #     mesh = ax.pcolormesh(
# #         xr_cosmic_t.lon, xr_cosmic_t.lat, data,
# #         cmap=cmap_to_use, 
# #         vmin=vmin, vmax=vmax,
# #         transform=ccrs.PlateCarree()
# #     )

# #     ax.set_extent([-180, 180, -50, 50], crs=ccrs.PlateCarree())
# #     ax.add_feature(cfeature.COASTLINE.with_scale('110m'), linewidth=0.8)
# #     # ax.add_feature(cfeature.BORDERS.with_scale('110m'), linestyle=':', linewidth=0.5)

# #     # 设置浅色细网格线
# #     gl = ax.gridlines(
# #         draw_labels=True,
# #         linewidth=0.2,
# #         color='lightgray',
# #         linestyle='--',
# #         alpha=0.5
# #     )
# #     gl.top_labels = False
# #     gl.right_labels = False

# #     ax.set_title(title, fontsize=12)
# #     cbar = plt.colorbar(mesh, ax=ax, orientation='vertical', pad=0.02, shrink=0.8)
# #     cbar.set_label(title)

# # save_dir = "/home/yxlei/cosmic2gim/scripts/plots/figures"
# # os.makedirs(save_dir, exist_ok=True)
# # save_path = os.path.join(save_dir, f"7.png")
# # plt.savefig(save_path, dpi=300)
# # plt.close()

# # print(f"绘图完成，图片保存路径: {save_path}")
