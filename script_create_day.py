#!/usr/bin/env python

import xarray as xr
import warnings
import numpy as np
import pandas as pd
import xesmf as xe
import sys
import os
sys.path.append('/home/brayan/mnsun/')
from utils import check_dir
warnings.filterwarnings('ignore')

# Dictorionary acumulation
day_year = {}
acum     = 0
day_year["01"] = acum
for contador, dm in enumerate([31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30]):
    acum += dm
    if contador < 8:
        day_year[f"0{contador+2}"] = acum
    else: 
        day_year[f"{contador+2}"] = acum

# Start code
actual_date = "".join(str(os.environ["date_processing"]).split("-"))
OUTPUT_DIR  = str(os.environ["output"])

for var in ["uflx","vflx"]: 
    CLIM = getattr(xr.open_dataset(f"/home/brayan/Documentos/DATA/Clim_{var}.nc"), var).rename(L="time")*-1
    CLIM["time"] = pd.date_range(actual_date[:4]+"-"+actual_date[4:6]+"-"+actual_date[6:], periods=45, freq="D") #COn el proposito de uniformizar
    for ens in ["01"]:
        DATA = xr.open_mfdataset(OUTPUT_DIR+actual_date+f"/{ens}/*{actual_date}00.grb2", 
                                 engine="cfgrib", concat_dim = 'time').sel(latitude=slice(30,-30),
                                                                           longitude=slice(90,298)) #.rename(longitude="lon").rename(latitude="lat")
        DATA["time"] = pd.date_range(actual_date[:4]+"-"+actual_date[4:6]+"-"+actual_date[6:], periods=45, freq="D")
        VAR1          = getattr(DATA, var).interp(latitude=np.arange(30,-30-.5,-.5)).rename(longitude="lon").rename(latitude="lat")
        
        
        DATA = xr.open_mfdataset(OUTPUT_DIR+actual_date+f"/{ens}/*{actual_date}06.grb2", 
                                 engine="cfgrib", concat_dim = 'time').sel(latitude=slice(30,-30),
                                                                           longitude=slice(90,298)) #.rename(longitude="lon").rename(latitude="lat")
        DATA["time"] = pd.date_range(actual_date[:4]+"-"+actual_date[4:6]+"-"+actual_date[6:], periods=45, freq="D")
        VAR2          = getattr(DATA, var).interp(latitude=np.arange(30,-30-.5,-.5)).rename(longitude="lon").rename(latitude="lat")        


        DATA = xr.open_mfdataset(OUTPUT_DIR+actual_date+f"/{ens}/*{actual_date}12.grb2", 
                                 engine="cfgrib", concat_dim = 'time').sel(latitude=slice(30,-30),
                                                                           longitude=slice(90,298)) #.rename(longitude="lon").rename(latitude="lat")
        DATA["time"] = pd.date_range(actual_date[:4]+"-"+actual_date[4:6]+"-"+actual_date[6:], periods=45, freq="D")
        VAR3          = getattr(DATA, var).interp(latitude=np.arange(30,-30-.5,-.5)).rename(longitude="lon").rename(latitude="lat")

        
        DATA = xr.open_mfdataset(OUTPUT_DIR+actual_date+f"/{ens}/*{actual_date}18.grb2", 
                                 engine="cfgrib", concat_dim = 'time').sel(latitude=slice(30,-30),
                                                                           longitude=slice(90,298)) #.rename(longitude="lon").rename(latitude="lat")
        DATA["time"] = pd.date_range(actual_date[:4]+"-"+actual_date[4:6]+"-"+actual_date[6:], periods=45, freq="D")
        VAR4          = getattr(DATA, var).interp(latitude=np.arange(30,-30-.5,-.5)).rename(longitude="lon").rename(latitude="lat")        

        VAR_ = xr.concat([ VAR1.expand_dims("hours"), VAR2.expand_dims("hours"),
                           VAR3.expand_dims("hours"), VAR4.expand_dims("hours")], dim="hours").assign_coords( hours = ("hours",
               pd.date_range(actual_date[:4]+"-"+actual_date[4:6]+"-"+actual_date[6:], periods=4, freq="6H"))).mean("hours")        
        
        ANOM = (VAR_ - CLIM.isel(dayofyear = day_year[actual_date[4:6]]+int(actual_date[6:]))).interpolate_na(dim="lat",use_coordinate=False).interpolate_na(dim="lon").rename(time="L").drop_vars(["surface","dayofyear"])
        ANOM["L"] = np.arange(0.5, 0.5+45, 1)
        DATASET = xr.Dataset({var:ANOM.expand_dims("time").assign_coords( time = ("time", pd.date_range(actual_date[:4]+"-"+actual_date[4:6]+"-"+actual_date[6:]+" 12:00:00",
                                                                                                        periods=1, freq="D")))}).chunk(chunks={"L":-1,"lat":-1,"lon":-1})
        w = open(OUTPUT_DIR+actual_date+f"/{ens}/"+f"{actual_date}_{var}.bin", "wb")
        w.write(np.float32(ANOM.isel(L=slice(1,None)).values))
        w.close()
        
        if actual_date == "20181031":
            check_dir( OUTPUT_DIR+"NCEP/", name=ens)
            DATASET.to_zarr(OUTPUT_DIR+"NCEP/"+ens+f"/{var}.zarr",consolidated=True)
        else:
            DATASET.to_zarr(OUTPUT_DIR+"NCEP/"+ens+f"/{var}.zarr",consolidated=True, append_dim='time')







