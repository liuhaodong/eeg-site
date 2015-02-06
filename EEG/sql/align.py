import csv
import sys

# python align.py . task.xls upload.xls task4.xls

data_path = sys.argv[1]
file1 = sys.argv[2]
file2 = sys.argv[3]
file3 = sys.argv[4]

values = {}

with open(data_path + '/' + file2, 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    header = reader.next()
    for row in reader:
        viewer, start_time, label_type, label = row[0], row[1], row[3], row[4]
        key = viewer + ' ' + start_time
        value = label
        values[key] = value

with open(data_path + '/' + file1, 'rb') as f, open(data_path + '/' + file3, 'wb') as f2:
    reader = csv.reader(f, delimiter='\t')
    writer = csv.writer(f2, delimiter='\t')

    header = reader.next()
    header.append(label_type)

    writer.writerow(header)
    for row in reader:
        subject, start_time = row[1], row[4]
        key = subject + ' ' + start_time

        entry = row

        if key in values:
            value = values[key]
        else:
            value = label_type

        entry.append(value)

        writer.writerow(entry)
