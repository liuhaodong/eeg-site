import csv
import sys

def convert_outs(task_file, label_file, label_type, upload_file):
            
    label_dict = {}
    with open(label_file, 'rb') as lf:
        label_reader = csv.reader(lf, delimiter=',')
        for row in label_reader:
            i, scores = row[0], row[1:]
            label = scores.index(max(scores))
            label_dict[str(i)] = label
    
    rows = []
    with open(task_file, 'rb') as tf:
        task_reader = csv.reader(tf, delimiter='\t')
        task_header = task_reader.next()
        sub_index = task_header.index('subject')
        st_index = task_header.index('start_time')
        et_index = task_header.index('end_time')
        for i, row in enumerate(task_reader):
            subject, start_time, end_time = row[sub_index], row[st_index], row[et_index]
            try:
                label = label_dict[str(i)]
                subject, start_time, end_time = row[sub_index], row[st_index], row[et_index]
                rows.append([subject, start_time, end_time, label_type, label])
            except:
                pass

    with open(upload_file, 'wb') as uf:
        writer = csv.writer(uf, delimiter=',')
        writer.writerow(['viewer', 'start_time', 'end_time', 'label_type', 'label'])
        for r in rows:
            writer.writerow(r)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "USAGE: python convert_outs.py [task_file] [label_file] [label_type] [out_file]"
    else:
        convert_outs(*sys.argv[1:])
