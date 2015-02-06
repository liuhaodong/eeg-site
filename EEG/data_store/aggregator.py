from __future__ import division
from EEG.data_store.models import ContentGroup, Content, LabelType, Label, Tag, Viewer
import datetime


def get_label_sequence(content_group_name,
                       content_name,
                       label_type_names,
                       segments,
                       viewer_names=None):
    """
     :Args:
          | content_group_name: Course name e.g Machine Leaning
          | content_name: content_name e.g M_L lecture 1
          | segments: a list of (start_sec, end_sec)
          | viewer_names: the way to limit the viewers whose data is used in the response

     :Returns:
          | TODO: document the return value
    """

    content_group = ContentGroup.objects.filter(name=content_group_name).get()
    content = Content.objects.filter(name=content_name, group=content_group).get()
    sessions = content.sessions.all()

    label_types = LabelType.objects.filter(name__in=label_type_names)

    viewers = None
    if not viewer_names is None:
        viewers = Viewer.objects.filter(user__username__in=viewer_names)

    # read data points from db

    label_sequences = {}
    for lt in label_types:
        label_sequences[lt.name] = []

    for i, segment in enumerate(segments):
        # get the data in each segment
        start_sec, end_sec = segment
        _sessions = sessions.filter(content_start_sec__lt=end_sec,
                                    content_end_sec__gte=start_sec)
        label_n = {}
        label_N = {}
        for lt in label_types:
            label_n[lt.name] = 0
            label_N[lt.name] = 0

        for session in _sessions:
            start_time = (session.start_time +
                          datetime.timedelta(seconds=start_sec - session.content_start_sec))
            end_time = (session.start_time +
                        datetime.timedelta(seconds=end_sec - session.content_start_sec))
            #tags = Tag.objects.filter(subject=session.viewers.all(),
            tags = Tag.objects.filter( # TODO: unbreak this
                                      start_time__lt=end_time,
                                      end_time__gte=start_time)
            if viewers:
                tags = tags.filter(subject=viewers)

            # store data

            for lt in label_types:
                labels = Label.objects.filter(tag=tags, label_type=lt)
                if lt.name == 'comment':
                    n = 0
                    N = 0
                    for j in labels.all().values():
                        n = n + j['predicted']
                        N = N + 100 # HACK, maximum number of comment at a time is 100
                else:
                    n = labels.filter(predicted=1).count()
                    N = len(labels)
                
                #print 'lt.name, n, N:', lt.name, n, N
                label_n[lt.name] = label_n[lt.name] + n
                label_N[lt.name] = label_N[lt.name] + N

        for lt in label_types:
            if label_N[lt.name] > 0:
                datapoint = (i, label_n[lt.name] / label_N[lt.name])
                #print 'lt.name, label_n, label_N, datapoint:', lt.name, label_n[lt.name], label_N[lt.name], datapoint
                label_sequences[lt.name].append(datapoint)

    return label_sequences
