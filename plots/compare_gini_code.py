import argparse
import gc
import sys
from pathlib import Path

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
import torch
from ppgnss import gnss_utils


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parents[1]
DATA_DIR = PROJECT_DIR / "data"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compare the 5-channel CNN GINI grid with CODE GIM for one hourly epoch."
    )

    parser.add_argument(
        "--time",
        default="2024-01-10T00:00:00",
        # default="2024-10-05T00:00:00",
        help="UTC epoch in YYYY-MM-DDTHH:MM:SS format (must be an exact hour).",
    )

    parser.add_argument(
        "--model",
        type=Path,
        default="/home/yxlei/cosmic2gim/scripts/test_bylyx/train_save/5ch_LAST_TEST_best_model.pth",
        help="Path to the trained 5-channel model weights.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output PNG path (defaults to scripts/plots/figures).",
    )

    parser.add_argument(
        "--vmax",
        type=float,
        default=120.0,
        help="Shared upper limit of the TEC color scale in TECU.",
    )

    return parser.parse_args()


def load_epoch(filename, epoch, label):
    data = gnss_utils.loadobject(str(filename))

    try:
        return data.sel(
            time=epoch,
            lat=slice(-50, 50),
        )

    except KeyError as exc:
        raise ValueError(
            f"{label} has no exact sample at {epoch}."
        ) from exc

    finally:
        del data
        gc.collect()


def main():

    args = parse_args()

    epoch = np.datetime64(
        args.time,
        "ns",
    )

    if epoch.astype("datetime64[h]") != epoch:
        raise ValueError(
            "--time must specify an exact hour, "
            "e.g. 2024-06-28T12:00:00."
        )

    if epoch.astype("datetime64[Y]") != np.datetime64("2024", "Y"):
        raise ValueError(
            "--time must be within calendar year 2024."
        )

    if args.vmax <= 0:
        raise ValueError(
            "--vmax must be positive."
        )

    if not args.model.is_file():
        raise FileNotFoundError(
            f"Model weights not found: {args.model}"
        )

    # ==============================================================
    # Import model
    # ==============================================================

    sys.path.insert(
        0,
        str(PROJECT_DIR / "scripts"),
    )

    from DualBranchCNN import DualBranchCNN

    # ==============================================================
    # Load data
    # ==============================================================

    cosmic = load_epoch(
        DATA_DIR / "cosmic_grid_5ch_2019to2024_nonan.obj",
        epoch,
        "COSMIC input",
    )

    iri = load_epoch(
        DATA_DIR / "IRI20_data" / "i202024_2025.obj",
        epoch,
        "IRI input",
    )

    code = load_epoch(
        DATA_DIR / "codg_gim" / "CODG_2024_2025.obj",
        epoch,
        "CODE GIM",
    )

    cosmic, iri, code = __import__("xarray").align(
        cosmic,
        iri,
        code,
        join="inner",
    )

    # ==============================================================
    # Check dimensions
    # ==============================================================

    if cosmic.sizes.get("channel") != 5:
        raise ValueError(
            f"Expected 5 COSMIC channels, "
            f"got {cosmic.sizes.get('channel')}."
        )

    if (
        cosmic.sizes.get("lat") != 41
        or cosmic.sizes.get("lon") != 73
    ):
        raise ValueError(
            "Aligned grids must be 41x73; got "
            f"COSMIC={cosmic.shape}, "
            f"IRI={iri.shape}, "
            f"CODE={code.shape}."
        )

    # ==============================================================
    # Load model
    # ==============================================================

    device = torch.device("cpu")

    model = DualBranchCNN(
        channels=5
    ).to(device)

    state_dict = torch.load(
        args.model,
        map_location=device,
        weights_only=True,
    )

    model.load_state_dict(
        state_dict
    )

    model.eval()

    # ==============================================================
    # Prepare input
    # ==============================================================

    iri_input = torch.as_tensor(
        np.asarray(
            iri.values,
            dtype=np.float32,
        )[None, None, :, :],
        device=device,
    )

    cosmic_input = torch.as_tensor(
        np.asarray(
            np.transpose(
                cosmic.values,
                (2, 0, 1),
            ),
            dtype=np.float32,
        )[None, :, :, :],
        device=device,
    )

    # ==============================================================
    # Inference
    # ==============================================================

    with torch.inference_mode():

        gini = model(
            (
                iri_input,
                cosmic_input,
            )
        )[0, 0].cpu().numpy()

    # ==============================================================
    # Prepare plotting data
    # ==============================================================

    code_grid = np.asarray(
        code.values
    )

    lat = cosmic.lat.values
    lon = cosmic.lon.values

    # ==============================================================
    # Figure
    # ==============================================================
    #
    # Instead of plt.subplots(), manually position the two
    # Cartopy GeoAxes.
    #
    # This avoids the large empty vertical space introduced by
    # Cartopy's automatic aspect-ratio handling.
    # ==============================================================

    fig = plt.figure(
        figsize=(12, 7),
    )

    # --------------------------------------------------------------
    # Manually define map positions
    #
    # [left, bottom, width, height]
    #
    # Coordinates are normalized to [0, 1].
    # --------------------------------------------------------------

    map_left = 0.065
    map_width = 0.82

    map_height = 0.34

    # Upper map
    ax1 = fig.add_axes(
        [
            map_left,
            0.535,
            map_width,
            map_height,
        ],
        projection=ccrs.PlateCarree(),
    )

    # Lower map
    ax2 = fig.add_axes(
        [
            map_left,
            0.075,
            map_width,
            map_height,
        ],
        projection=ccrs.PlateCarree(),
    )

    axes = [
        ax1,
        ax2,
    ]

    # ==============================================================
    # Plot GINI and CODE
    # ==============================================================

    mesh = None

    for ax, values, title in zip(
        axes,
        (gini, code_grid),
        (
            "GINI TEC",
            "CODE TEC",
        ),
    ):

        mesh = ax.pcolormesh(
            lon,
            lat,
            values,
            transform=ccrs.PlateCarree(),
            shading="auto",
            cmap="turbo",
            vmin=0,
            vmax=args.vmax,
        )

        ax.set_extent(
            [
                -180,
                180,
                -50,
                50,
            ],
            crs=ccrs.PlateCarree(),
        )

        ax.add_feature(
            cfeature.COASTLINE.with_scale(
                "110m"
            ),
            linewidth=0.55,
        )

        gridlines = ax.gridlines(
            draw_labels=True,
            linewidth=0.35,
            color="gray",
            linestyle="--",
            alpha=0.5,
        )

        gridlines.top_labels = False
        gridlines.right_labels = False

        # ----------------------------------------------------------
        # Title
        # ----------------------------------------------------------

        ax.set_title(
            title,
            fontsize=18,
            pad=2,
        )

    # ==============================================================
    # Colorbar
    # ==============================================================

    cbar_ax = fig.add_axes(
        [
            0.905,
            0.125,
            0.028,
            0.75,
        ]
    )

    colorbar = fig.colorbar(
        mesh,
        cax=cbar_ax,
        orientation="vertical",
    )

    colorbar.set_label(
        "VTEC (TECU)",
        fontsize=14,
    )

    colorbar.ax.tick_params(
        labelsize=12,
    )

    # ==============================================================
    # Output path
    # ==============================================================

    time_str = (
        epoch.astype("datetime64[m]")
        .astype(str)
        .replace("-", "")
        .replace(":", "")
        .replace("T", "_")
    )

    output = args.output or (
        SCRIPT_DIR
        / "figures"
        / f"gini_vs_code_{time_str}.png"
    )

    output = (
        output
        .expanduser()
        .resolve()
    )

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ==============================================================
    # Save
    # ==============================================================

    fig.savefig(
        output,
        dpi=900,
        bbox_inches="tight",
        pad_inches=0.05,
    )

    plt.close(fig)

    # ==============================================================
    # Print information
    # ==============================================================

    print(
        f"Saved comparison map: {output}"
    )

    print(
        f"GINI range: "
        f"{np.nanmin(gini):.2f} "
        f"to "
        f"{np.nanmax(gini):.2f} TECU"
    )

    print(
        f"CODE range: "
        f"{np.nanmin(code_grid):.2f} "
        f"to "
        f"{np.nanmax(code_grid):.2f} TECU"
    )


if __name__ == "__main__":
    main()