import EEG.data_store.dbserializer as dbs
from EEG.data_store.models import *


def run():
    params = {}
    label_names = ['engage']
    params['model_name'] = 'c.mat'
    tags = Tag.objects.all()
    label_types = LabelType.objects.filter(name__in=label_names)
    for lt in label_types:
        tags = tags.filter(labels__label_type=lt)
    raws = Raw.objects.all()
    params['task_qs'] = tags
    params['label_qs'] = label_types
    params['eeg_qs'] = raws
    import eegml
    params['trainer'] = eegml.train
    params['applier'] = eegml.apply
    return _apply(params)


def _train(p):
    task_file, eeg_file = dbs.get_data_as_xls(p['task_qs'], p['label_types'], p['eeg_qs'])
    classifier_file_path = params['trainer'](p['model_name'], task_file, eeg_file)
    return p['model_name']


def _apply(p):
    task_file, eeg_file = dbs.get_data_as_xls(p['task_qs'], p['label_types'], p['eeg_qs'])
    task_file = params['applier'](p['model_name'], task_file, eeg_file)
    dbs.xls_to_task('predicted_' + p['label'], p['task_qs'], task_file)


def classifySingleTask(task_qs, model, label):
    task = task_qs
    eeg_qs = Raw.objects.filter(start_time__lte=task.end_time,
                                end_time__gte=task.start_time,
                                student_name=task.student_name,
                                course=task.course)
    p = {'task_qs': task_qs,
         'eeg_qs': eeg_qs,
         'label': label,
         'model_name': model_name}
    _apply(p)


def train(table, label, start_time, end_time):
    kwargs = {label, -1}
    task_qs = table.objects.exclude(**kwargs).filter(
        start_time__gte=start_time, start_time__lt=end_time)
    eeg_qs = Raw.objects.all()
    model_name = 'default.{0}.model' % label
    p = {'task_qs': task_qs,
         'eeg_qs': eeg_qs,
         'label': label,
         'model_name': model_name}
    _train(p)
