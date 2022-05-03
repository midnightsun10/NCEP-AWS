#!/usr/bin/env python
import os
import glob
import pandas as pd

actual_date   = "".join(str(os.environ["date_processing"]).split("-"))
OUTPUT_DIR    = str(os.environ["output"])

for ens in ["01"]: #,"02", "03", "04"
    list_exist = [ ff.split("/")[-1] for ff in glob.glob(f"/home/brayan/DATA/AWS/{actual_date}/{ens}/*grb2")]
    list_create = []
    list_original = []
    with open (f"/home/brayan/DATA/AWS/{actual_date}/{ens}/"+actual_date +"_download.txt", 'r') as myfile:
        for myline in myfile:           
            list_create.append(myline.split("/")[-1][:-1])
            list_original.append(myline)

    if len(list_create) == len(list_exist):
        with open(f"{OUTPUT_DIR}" + f"/{actual_date}/{ens}/" + actual_date + "_download.txt", "w") as f:
            f.write(" ")
    else:
        list_missing = list_create.copy()        
        [list_missing.remove(i) for i in list_exist]
        list_final = []
        for miss in list_missing:
            for find in list_original:
                if find[73:-1] == miss:
                    list_final.append(find)    
        with open(f"{OUTPUT_DIR}" + f"/{actual_date}/{ens}/" + actual_date + "_download.txt", "w") as f:
            for re in list_final:
                date = pd.date_range( re[77:77+4]+ "-" +re[77+4:77+6]+"-" + re[77+6:77+8] +" " +re[77+8:77+10] + ":00:00", periods=1, freq='6H').shift(6, freq='H')
                f.write(re[:77]+str(date.values[0])[:4]+str(date.values[0])[5:7]+str(date.values[0])[8:10]+str(date.values[0])[11:13]+re[87:])