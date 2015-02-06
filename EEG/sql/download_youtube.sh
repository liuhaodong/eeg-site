#!/bin/bash

# get video.xls

#mysql ebdb -h aamjedx8lst96w.cumpptz5rdj5.us-east-1.rds.amazonaws.com -P 3306 -u ebroot -p < dev/video.sql > video.xls

echo -e "url\tname" > video.xls

CAMPAIGN='TrailerCalculus'

LABEL='Engage'
QUERY='movie+trailer+official+2014'
URL=https://www.youtube.com/results\?search_query=$QUERY
echo $URL
wget $URL -O $LABEL.htm
cat $LABEL.htm | grep 'data-context-item-id' | sed 's/.*data-context-item-id=\"\([^ ]*\)\".*/http:\/\/www.youtube.com\/watch?v=\1/' | tail -n +2 > $LABEL.txt
cat $LABEL.txt | awk -v CAMPAIGN=$CAMPAIGN -v LABEL=$LABEL '{print $1 "\t" CAMPAIGN "_" LABEL "_" (NR - 1)}' >> video.xls
rm $LABEL.*

LABEL='Disengage'
QUERY='calculus+lecture+professor+leonard'
URL=https://www.youtube.com/results\?filters=short\&search_query=$QUERY
echo $URL
wget $URL -O $LABEL.htm
cat $LABEL.htm | grep 'data-context-item-id' | sed 's/.*data-context-item-id=\"\([^ ]*\)\".*/http:\/\/www.youtube.com\/watch?v=\1/' | tail -n +2 > $LABEL.txt
cat $LABEL.txt | awk -v CAMPAIGN=$CAMPAIGN -v LABEL=$LABEL '{print $1 "\t" CAMPAIGN "_" LABEL "_" (NR - 1)}' >> video.xls
rm $LABEL.*

# download videos

tail -n +2 video.xls | awk '{system("youtube-dl " $1 " -o " $2 ".mp4")}'

mv *.mp4 ../static/video
rm video.xls *.part
