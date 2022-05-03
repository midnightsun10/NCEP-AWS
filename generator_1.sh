#!/bin/bash

dirname=`pwd`
export output="/home/brayan/DATA/AWS/"
start=2018-11-02
end=2018-12-31

while ! [[ $start > $end ]]; do
    echo "$start"
    export date_processing="$start"

    ################# PHASE 1 #################
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
        sh *txt ##sh *txt
    done
    cd $dirname    

    ################# PHASE 2 #################
    # Missing script
    chmod u+rwx ./script_missing_files.py
    ./script_missing_files.py

    for i in 01 #02 03 04
    do
        cd "$output$start_join/$i/"
        sh *txt ##sh *txt
    done
    cd $dirname 

    ################# PHASE 3 #################
    #  Create day file
    chmod u+rwx ./script_create_day.py
    ./script_create_day.py

    # Eliminate
    for i in 01 #02 03 04
    do
        cd "$output$start_join/$i/"
        rm ocnf* | wc -l
        rm *.txt
    done

    # Aumenta en un dia
    start=$(date -d "$start + 1 day" +%F)
    cd $dirname

done






