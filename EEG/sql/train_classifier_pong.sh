#!/bin/bash

# load from database

if [[ $# < 1 ]]; then
    echo 'USAGE:' `basename $0` '[dev|prod]'
    exit
elif [[ $1 == 'dev' ]]; then
    sqlite3 ../../prod.sqlite3 -header -separator $'\t' < dev/pong.sql | sed 's/\\t\\t/\\t/g' > pong.xls
    sqlite3 ../../prod.sqlite3 -header -separator $'\t' < dev/eeg.sql > eeg.xls
elif [[ $1 == 'prod' ]]; then
    mysql ebdb -h aamjedx8lst96w.cumpptz5rdj5.us-east-1.rds.amazonaws.com -P 3306 -u ebroot -p < prod/task.sql > task.xls
    mysql ebdb -h aamjedx8lst96w.cumpptz5rdj5.us-east-1.rds.amazonaws.com -P 3306 -u ebroot -p < prod/eeg.sql > eeg.xls
fi

# label pong

DATA_PATH='.'
LABEL='positive'

python label_task.py "$DATA_PATH" $LABEL
cp task.xls task0.xls

# recombine rows

#DATA_PATH='.'
#GROUP_ONE='block'
#GROUP_TWO='cond'
#MIN_LENGTH=0
#MAX_LENGTH=10

#python recombine_task.py "$DATA_PATH" $GROUP_ONE $GROUP_TWO $MIN_LENGTH $MAX_LENGTH
#cp task2.xls task.xls

# filter by cond ($7) (2nd awk command also prints 1 line before the event as contrast)

awk -F'\t' '$7 != 0' task.xls > task3.xls
#head -n1 task.xls > task3.xls && awk -F'\t' '$7 == 2 && l { print l; print $0 }; { l=$0 }' task.xls >> task3.xls
cp task3.xls task.xls

# separate sensors

python separate_sensors.py eeg.xls

# train classifier

cp task.xls TP9.xls FP1.xls FP2.xls TP10.xls ~ec2-user

# download ~ec2-user/*.xls to $EEG_ML/expt/IS_WS/standalone_test/data
# cd $EEG_ML/expt/IS_WS/standalone_test/src
# clear all; train_script;
# upload $EEG_ML/expt/IS_WS/standalone_test/result/c.mat to ~ec2-user/

rm c.mat *.xls *.csv
