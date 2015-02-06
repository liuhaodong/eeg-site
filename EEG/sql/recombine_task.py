import csv
import sys
from datetime import datetime
from datetime import timedelta

def decode_time(timestr):
    #return datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S.%f")
    return datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")

def encode_time(timestruct):
    #return datetime.strftime(timestruct, "%Y-%m-%d %H:%M:%S.%f")
    return datetime.strftime(timestruct, "%Y-%m-%d %H:%M:%S")

# python recombine_task.py 2014-08-16\ game1\ kkchang\ blue/ block cond 1 2

data_path = sys.argv[1]
group_one = sys.argv[2]
group_two = sys.argv[3]
min_length = float(sys.argv[4])
max_length = float(sys.argv[5])

header = ['machine', 'subject', 'stim', 'block', 'start_time', 'end_time', 'cond', 'score']

START_TIME = header.index('start_time')
END_TIME = header.index('end_time')
GROUP_ONE = header.index(group_one)
GROUP_TWO = header.index(group_two)

# rows - load into []

rows = []
with open(data_path + '/task.xls', 'rb') as f:
    reader = csv.reader(f, delimiter='\t')
    header = reader.next()
    for row in reader:
        rows.append(row)

# rows1 - group by

rows1 = []
curr = rows[0]
for r in range(1, len(rows)):
    row = rows[r]
    if row[GROUP_ONE] == curr[GROUP_ONE] and row[GROUP_TWO] == curr[GROUP_TWO]:
        curr[END_TIME] = row[END_TIME]
    else:
        rows1.append(curr)
        curr = row
rows1.append(curr)

with open(data_path + '/task1.xls', 'wb') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(header)
    for row in rows1:
        writer.writerow(row)

# rows2 - filter by min_length, expand by max_length

rows2 = []
for row in rows1:

    cur_end_time = row[END_TIME][:]
    min_end_time = encode_time(decode_time(row[START_TIME]) + timedelta(seconds=min_length))
    max_end_time = encode_time(decode_time(row[START_TIME]) + timedelta(seconds=max_length))

    while row[END_TIME] > max_end_time:
        row[END_TIME] = max_end_time

        if row[END_TIME] > min_end_time:
            rows2.append(list(row))

            row[START_TIME] = max_end_time
            row[END_TIME] = cur_end_time
            min_end_time = encode_time(decode_time(row[START_TIME]) + timedelta(seconds=min_length))
            max_end_time = encode_time(decode_time(row[START_TIME]) + timedelta(seconds=max_length))

    if row[END_TIME] > min_end_time:
        rows2.append(list(row))

with open(data_path + '/task2.xls', 'wb') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(header)
    for row in rows2:
        writer.writerow(row)
