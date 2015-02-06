import os
import csv
from EEG.utils.timefixer import datetime_to_str
from EEG.data_store.models import SurveyAnswer, Viewer
import datetime
import math


def get_data_as_xls(tag_qs, label_type_qs, eeg_qs,
                    task_file='task.xls', eeg_file='eeg.xls', survey_file='survey.xls',
                    seg_length=None, margins=None):
    cur_path = os.path.dirname(os.path.realpath(__file__))
    task_file_path = os.path.join(cur_path, '../static/', task_file)
    eeg_file_path = os.path.join(cur_path, '../static/', eeg_file)
    survey_file_path = os.path.join(cur_path, '../static/', survey_file)
    task_to_xls(tag_qs, label_type_qs, task_file_path, seg_length, margins)
    raw_to_xls(eeg_qs, eeg_file_path)
    survey_to_xls(tag_qs, survey_file_path)
    return task_file_path, eeg_file_path, survey_file_path


def survey_to_xls(tag_qs, xls_path):
    header = ['subject', 'start_time', 'end_time', 'question', 'answer']
    surveys = SurveyAnswer.objects.all()

    with open(xls_path, 'wb') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(header)

        for s in surveys:
            row = [s.subject.user.username,
                   datetime_to_str(s.start_time), datetime_to_str(s.end_time),
                   s.question, s.answer]
            writer.writerow(row)

def task_to_xls(tag_qs, label_type_qs, xls_path, seg_length=None, margins=None):
    tags = tag_qs
    label_types = label_type_qs
    header = ['content', 'subject', 'start_time', 'end_time']
    for lt in label_types:
        header.append(lt.name)

    with open(xls_path, 'wb') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(header)

        for t in tags:
            # find the session this tag is in
            session = t.get_session()
            if session == None:
                continue

            start_time = t.start_time
            end_time = t.end_time
            if margins is not None:
                if len(margins) == 1:
                    margins = (margins, margins)
                start_time += margins[0]
                end_time -= margins[1]
                start_time = min(start_time, end_time)
                end_time = max(start_time, end_time)

            if seg_length is None:
                times = [start_time, end_time]
            else:
                secs = int(math.ceil(seg_length.total_seconds()))
                total_secs = int(math.floor((end_time - start_time).total_seconds()))
                times = [start_time + datetime.timedelta(seconds=i) for i in range(0, total_secs + 1, secs)]

            for i in range(1, len(times)):
                row_start_time = times[i - 1]
                row_end_time = times[i]
                row = [session.content.name, t.subject.user.username,
                       datetime_to_str(row_start_time), datetime_to_str(row_end_time)]
                for lt in label_types:
                    l = t.labels.filter(label_type=lt)
                    if len(l) == 1:
                        row.append(l[0].true)
                    else:
                        row.append(-1)
                writer.writerow(row)


def raw_to_xls(raw_qs, xls_path):
    header = ['subject', 'sensor', 'start_time', 'end_time', 'attention', 'sigqual', 'rawwave']
    with open(xls_path, 'wb') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(header)
    viewers = Viewer.objects.all()
    num_viewers = len(viewers)
    for i, v in enumerate(viewers):
        print str(i * 100 / num_viewers) + '% dumped'
        with open(xls_path, 'a+b') as f:
            writer = csv.writer(f, delimiter='\t')
            raws = raw_qs.filter(subject=v)

            for r in raws:
                # skip the rows that are likely to exceed the max field size and cause file io
                # erors
                if len(r.rawwave) > 9999:
                    continue
                # also, skip the empties
                elif len(r.rawwave) == 0:
                    continue
                row = [r.subject.user.username, r.sensor,
                    datetime_to_str(r.start_time), datetime_to_str(r.end_time),
                    r.attention, r.sigqual, r.rawwave]
                writer.writerow(row)


# TODO: update this function
def xls_to_task(label, task_qs, xls_path):
    with open(xls_path, 'rb') as f:
        reader = csv.reader(f, delimiter='\t')
        header = reader.next()
        for row in reader:
            pk, machine, subject, start_time, end_time, stim, block, cond = row
            task = task_qs.get(pk=pk)
            setattr(task, label, int(cond) + 1)
            task.save()
