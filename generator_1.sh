#!/bin/bash

dirname=`pwd`
export output="/home/brayan/DATA/AWS/"
start=2018-10-31
end=2018-11-01

while ! [[ $start > $end ]]; do
    echo "$start"
    export date_processing="$start"
    chmod u+rwx ./script_files_url.py
    ./script_files_url.py

    # Split and join date
    IFS="-" read -a params <<< "$start"
    start_join=""
    for j in "${params[@]}"; do
        start_join+="$j"
    done    


    # ejecuta la descarga
    for i in 01 #02 03 04
    do
        cd "$output$start_join/$i/"
        ls *txt
    done

    # 



    #Aumenta en un dia
    start=$(date -d "$start + 1 day" +%F)
    cd $dirname
done






