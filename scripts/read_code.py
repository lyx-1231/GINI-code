from ppgnss import gnss_io
from ppgnss import gnss_utils
import xarray as xr
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
doy = 1
filename = os.path.join(current_dir, "..", "code", f"CODG{doy:03d}0.22I")
xr_codg= gnss_io.read_ionex_file(filename)[:-1,:,:]
for doy in range(2, 35):
    filename = os.path.join(current_dir, "..", "code", f"CODG{doy:03d}0.22I")
    xr_gim = gnss_io.read_ionex_file(filename)[:-1,:,:]
    print(xr_gim.shape)
    xr_codg = xr.concat([xr_codg, xr_gim], dim='time')
out_file = os.path.join(current_dir, "..", "data", f"codg2022_034.obj")
gnss_utils.saveobject(xr_codg, out_file)