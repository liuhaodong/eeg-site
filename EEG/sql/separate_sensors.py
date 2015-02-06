import csv
import os
import sys

def separate_sensors(eeg_file):
    sensors = {}
    with open(eeg_file, 'rb') as f:
        reader = csv.reader(f, delimiter='\t')
        header = reader.next()
        sensor_idx = header.index('location')

        for row in reader:
            sensor = row[sensor_idx]
            senseless_row = row[:sensor_idx] + row[sensor_idx+1:]
            try:
                sensors[sensor].append(senseless_row)
            except:
                sensors[sensor] = [senseless_row]

    eeg_path = os.path.dirname(eeg_file)
    senseless_header = header[:sensor_idx] + header[sensor_idx+1:] + ['sigqual']
    for sensor, rows in sensors.iteritems():
        sensor = sensor.upper()
        with open(os.path.join(eeg_path, sensor + '.xls'), 'wb') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(senseless_header)
            for row in rows:
                writer.writerow(row + ['0'])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "USAGE: python separate_sensors.py [eeg_file]"
    separate_sensors(sys.argv[1])
