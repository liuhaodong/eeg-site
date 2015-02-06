import os
import subprocess
import csv


def train(model_name, task_file, eeg_file):
    raise Exception('eegml.train is unimplemented')


def apply(model_name, task_file, eeg_file):
    separate_sensors(eeg_file)
    data_path = os.path.dirnmae(task_file)
    cur_path = os.path.dirname(os.path.realpath(__file__))
    #test_sh = os.path.join(cur_path, 'eegml/src/run_apply_func.sh')
    #models_folder = os.path.join(cur_path, 'eegml/src')
    #model_path = os.path.join(models_folder, model_name)
    args = [data_path]

    output, _ = subprocess.Popen(['./run_apply_func.sh', '$MCRROOT'] + args,
                    stdout=subprocess.PIPE).communicate()
    success = True if output == 'success' else False
    return task_file if success else None

def separate_sensors(eeg_file):
    sensors = {}
    with open(eeg_file, 'rb') as f:
        reader = csv.reader(f, delimiter='\t'):
        header = reader.next()
        sensor_idx = header.index('sensor')

        for row in reader:
            sensor = row[sensor_idx]
            senseless_row = row[:sensor_idx] + row[sensor_idx+1:]
            try:
                sensors[sensor].append(senseless_row)
            except:
                sensors[sensor] = [senseless_row]

    eeg_path = os.path.dirname(eeg_file)
    senseless_header = header[:sensor_idx] + header[sensor_idx+1:]
    for sensor, rows in sensors.iteritems():
        with open(os.path.join(eeg_path, sensor + '.xls'), 'wb') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(senseless_header)
            for row in rows:
                writer.writerow(row)
