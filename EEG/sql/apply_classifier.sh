#!/bin/bash

# load from database

if [[ $# < 1 ]]; then
    echo 'USAGE:' `basename $0` '[dev|prod] [engage|winning]'
    exit
elif [[ $1 == 'dev' ]]; then
    #cp ~ec2-user/task.xls .
    sqlite3 ../../prod.sqlite3 -header -separator $'\t' < dev/task.sql > task.xls
    sqlite3 ../../prod.sqlite3 -header -separator $'\t' < dev/eeg.sql > eeg.xls
elif [[ $1 == 'prod' ]]; then
    mysql ebdb -h aamjedx8lst96w.cumpptz5rdj5.us-east-1.rds.amazonaws.com -P 3306 -u ebroot -p < prod/task.sql > task.xls
    mysql ebdb -h aamjedx8lst96w.cumpptz5rdj5.us-east-1.rds.amazonaws.com -P 3306 -u ebroot -p < prod/eeg.sql > eeg.xls
fi

cp task.xls task0.xls

# recombine rows

DATA_PATH='.'
GROUP_ONE='subject'
GROUP_TWO='stim'
MIN_LENGTH=0
MAX_LENGTH=10

python recombine_task.py "$DATA_PATH" $GROUP_ONE $GROUP_TWO $MIN_LENGTH $MAX_LENGTH
cp task2.xls task.xls

# filter by cond ($7) (2nd awk command also prints 1 line before the event as contrast)

awk -F'\t' '$7 != 0' task.xls > task3.xls
#head -n1 task.xls > task3.xls && awk -F'\t' '$7 == 2 && l { print l; print $0 }; { l=$0 }' task.xls >> task3.xls
cp task3.xls task.xls

# separate sensors

python separate_sensors.py eeg.xls

# apply classifier

if [[ $2 == 'engage' ]]; then
    #ln -s classifier/c.engage0.kkchang.mat c.mat
    ln -s classifier/c.engage.kkchang.mat c.mat
    #ln -s classifier/c.engage.yuerany.mat c.mat
elif [[ $2 == 'winning' ]]; then
    ln -s classifier/c.possessing.mat c.mat
fi

./apply_func.sh $MCRROOT .

# convert output for upload

python convert_outs.py task.xls outs.csv $2 upload.csv

# upload to database

#if [[ $1 == 'dev' ]]; then
#    curl -F "file=@upload.csv" 54.164.147.181:8000/EEG/upload_labels
#elif [[ $1 == 'prod' ]]; then
#    curl -F "file=@upload.csv" http://eeg-site-env-ri3efmjbmv.elasticbeanstalk.com/EEG/upload_labels
#fi

cp task3.xls ~ec2-user
cp FP1.xls FP2.xls TP9.xls TP10.xls ~ec2-user
cp upload.csv ~ec2-user
#rm c.mat *.xls *.csv
