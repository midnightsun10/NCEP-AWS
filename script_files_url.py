#!/usr/bin/env python

import pandas as pd
import sys
sys.path.append('/home/brayan/mnsun/')
from utils import check_dir
import os

actual_date   = "".join(str(os.environ["date_processing"]).split("-")) #"20181031"
base_line     = "wget https://noaa-cfs-pds.s3.amazonaws.com/cfs.{ACTUAL_DATE}/{INIT}/6hrly_grib_{ENS}/ocnf{DATE_FORECAST}{INIT_FORE}.{ENS}.{ACTUAL_DATE}{INIT}.grb2"
OUTPUT_DIR    = str(os.environ["output"]) #"/home/brayan/DATA/AWS/"
check_dir( OUTPUT_DIR, name=actual_date)
init_hour     = {"00":"06", "06":"12", "12":"18", "18":"00"}
date_forecast = pd.date_range(actual_date, freq="D", periods=45+1)
for ens in ["01"]: #,"02", "03", "04"
    check_dir( OUTPUT_DIR+f"/{actual_date}/", name=ens)
    with open(f"{OUTPUT_DIR}" + f"/{actual_date}/{ens}/" + actual_date + "_download.txt", "w") as f:
        for hour in ["00", "06", "12", "18"]:
            for t in range(45):
                if t == 0:
                    f.write(base_line.format(ACTUAL_DATE = actual_date, INIT = hour, ENS = ens, INIT_FORE = init_hour[hour],
                                             DATE_FORECAST = ''.join(str(date_forecast[t+1])[:10].split("-")) if hour == "18" else ''.join(str(date_forecast[t])[:10].split("-")) )+ "\n")
                else:
                    if hour == "18":
                        f.write(base_line.format(ACTUAL_DATE = actual_date, INIT = hour, ENS = ens, INIT_FORE = hour,
                                 DATE_FORECAST = ''.join(str(date_forecast[t])[:10].split("-")) if hour == "18" else ''.join(str(date_forecast[t])[:10].split("-")) )+ "\n")
                    else:
                        f.write(base_line.format(ACTUAL_DATE = actual_date, INIT = hour, ENS = ens, INIT_FORE = hour,
                                 DATE_FORECAST = ''.join(str(date_forecast[t+1])[:10].split("-")) if hour == "18" else ''.join(str(date_forecast[t])[:10].split("-")) )+ "\n")