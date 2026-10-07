import os
import datetime
import h5py
import numpy as np
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
from ppgnss import gnss_utils

# jason_dir = "/mnt/geodata/Jason/2022"
jason_dir = "/home/yxlei/cosmic2gim/data/Jason/2024"

current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, "..", "data/Jason")
out_vtec_file = os.path.join(data_dir, "jason3_vtec_2024.obj")
df_all = pd.DataFrame(columns=["time", "lat", "lon", "hgt", "tec"])
count = 0
filelist = sorted(os.listdir(jason_dir))
for jfile in filelist :
    if not jfile.endswith("nc"): continue
    jfilename = os.path.join(jason_dir, jfile)
    print(jfilename)
    data_ku = xr.open_dataset(jfilename, group='/data_01/ku')
    data_01 = xr.open_dataset(jfilename, group='/data_01')
    time = data_01["time"]
    freq = 13.575E9
    tec = - data_ku["iono_cor_alt_filtered"]*freq*freq*1E-16/40.3
    tec[tec<0] = np.nan
    lats = data_01["latitude"]
    lons = data_01["longitude"]
    hgts = data_01["altitude"]
    df = pd.DataFrame({"time": time, "lat": lats, "lon": lons, "hgt": hgts,
                        "tec": tec})
    
    df_all = pd.concat([df_all, df])
    # count += 1
    # if count > 2:
    #     break

# df_all = df_all[df_all["tec"] > 0]
gnss_utils.saveobject(df_all, out_vtec_file)

print(f"Saved {out_vtec_file}")


# 绘图
plt.scatter(df_all["lon"], df_all["lat"], s=1, c=df_all["tec"])
plt.savefig("/home/yxlei/cosmic2gim/scripts/figures_Jason/iono.png")
plt.close()

plt.plot(df_all["time"], df_all["tec"])
plt.savefig("/home/yxlei/cosmic2gim/scripts/figures_Jason/iono1.png")
plt.close()
    