import os
import tarfile
import tempfile
import datetime
import netCDF4 as nc
import numpy as np
import pandas as pd
from ppgnss import gnss_geodesy
from ppgnss.gnss_geodesy import arr_xyz2az_el


def find_base_point(A, B, C):
    AB = B - A
    AC = C - A
    AB_unit = AB / np.linalg.norm(AB)
    projection_length = np.dot(AC, AB_unit)
    P = A + projection_length * AB_unit
    return P


def podtec2maxtec(filename):
    try:
        dataset = nc.Dataset(filename)
        prn = filename[-19:-16]
        leo = filename[-44:-40]

        tec_data = dataset.variables["TEC"][:]
        max_tec = np.max(tec_data)
        max_index = np.argmax(tec_data)

        gpstime_maxtec = dataset.variables["time"][max_index]
        x_leo = dataset.variables["x_LEO"][max_index]
        y_leo = dataset.variables["y_LEO"][max_index]
        z_leo = dataset.variables["z_LEO"][max_index]
        x_gps = dataset.variables["x_GPS"][max_index]
        y_gps = dataset.variables["y_GPS"][max_index]
        z_gps = dataset.variables["z_GPS"][max_index]

        time_maxtec = datetime.datetime(1980, 1, 6) + datetime.timedelta(seconds=gpstime_maxtec)

        A = np.array([x_leo, y_leo, z_leo])
        B = np.array([x_gps, y_gps, z_gps])
        C = np.array([0, 0, 0])
        P = find_base_point(A, B, C)

        lat, lon, hgt = gnss_geodesy.xyz2blh(P[0]*1000, P[1]*1000, P[2]*1000)

        ref_point = np.array([[P[0]*1000, P[1]*1000, P[2]*1000]])
        satellite = np.array([[x_leo*1000, y_leo*1000, z_leo*1000]])
        az, el = arr_xyz2az_el(satellite, ref_point)

        return {
            "time": time_maxtec,
            "leo": leo,
            "prn": prn,
            "lat": lat,
            "lon": lon,
            "max_tec": max_tec,
            "az": az[0]
        }
    except Exception as e:
        print(f"Error processing {filename}: {e}")
        return None


def append_to_pickle(df, pickle_file):
    if df.empty:
        return
    try:
        if os.path.exists(pickle_file):
            existing = pd.read_pickle(pickle_file)
            combined = pd.concat([existing, df], ignore_index=True)
        else:
            combined = df
        combined.to_pickle(pickle_file)
        print(f"Saved to {pickle_file}")
    except Exception as e:
        print(f"Error saving to {pickle_file}: {e}")


def process_nc_files(nc_file_paths):
    records = []
    for path in nc_file_paths:
        record = podtec2maxtec(path)
        if record is not None:
            records.append(record)
    return pd.DataFrame(records)


def extract_tar_gz(archive_path, extract_dir):
    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(path=extract_dir)
        return True
    except Exception as e:
        print(f"Failed to extract {archive_path}: {e}")
        return False


def process_all_archives(main_dir, output_pkl):
    for archive_name in sorted(os.listdir(main_dir)):
        if not archive_name.endswith(".tar.gz"):
            continue

        archive_path = os.path.join(main_dir, archive_name)
        print(f"Processing archive: {archive_path}")

        with tempfile.TemporaryDirectory() as tmpdir:
            if extract_tar_gz(archive_path, tmpdir):
                nc_files = []
                for root, dirs, files in os.walk(tmpdir):
                    for f in files:
                        nc_files.append(os.path.join(root, f))

                df = process_nc_files(nc_files)
                append_to_pickle(df, output_pkl)
            else:
                print(f"Skipping archive due to extract failure: {archive_path}")


if __name__ == "__main__":
    input_dir = "/mnt/geodata/cosmic2/podtc2/2024"
    output_pkl = "/home/yxlei/cosmic2gim/data/pod_data/pod_2024YEAR_data.pkl"
    process_all_archives(input_dir, output_pkl)
    print(f"All archives processed and saved to {output_pkl}")
