from EEG.data_store.dbserializer import get_data_as_xls
from django.http import HttpResponse
from EEG.data_store.models import LabelType, Label, Tag, Raw, Viewer, VideoContent, Session, Owner, ContentGroup, Content, VideoSeries
from EEG.utils import timefixer
import datetime
from EEG.classify import classify
from EEG.debug.utils import fill_db_pilot
from datetime import timedelta as td
from EEG.utils.timefixer import str_to_datetime, UTC
import os


def dump(request):
    tags = Tag.objects.all()
    label_types = LabelType.objects.filter(name__in=['engage'])
    raws = Raw.objects.all()
    get_data_as_xls(tags, label_types, raws, task_file='task_full.xls', eeg_file='eeg.xls')
    calibration_tags = tags
    for lt in label_types:
        calibration_tags = calibration_tags.filter(labels__label_type=lt)
    get_data_as_xls(calibration_tags, label_types, raws,
                    task_file='task.xls', eeg_file='eeg.xls',
                    seg_length=td(seconds=5), margins=(td(seconds=10), td(seconds=5)))
    return HttpResponse("data dumped!")


def fill_db(request):
    fill_db_pilot()
    #add_engagement_test()
    return HttpResponse('db filled')


def add_engagement_test():
    st = timefixer.now()
    et = st + datetime.timedelta(seconds=100)
    viewer = Viewer.objects.get(user__username="viewer")
    c = VideoContent.objects.all()[0]
    print c.name
    sess = Session.objects.create(content=c, name='asdf',
            start_time=st, end_time=et,
            content_start_sec=0, content_end_sec=100)
    sess.viewers.add(viewer)
    for i in range(0, 10):
        st_ = st + datetime.timedelta(seconds=i*10)
        et_ = st_ + datetime.timedelta(seconds=10)
        tag = Tag.objects.create(subject=viewer, start_time=st_, end_time=et_)
        engage = LabelType.objects.get(name='engage')
        Label.objects.create(tag=tag, label_type=engage, true=int(i/5), predicted=int(i/3))


def directInput(request):
    student = request.GET.get('student')
    val = int(request.GET.get('confusion'))
    start_time = timefixer.now()
    end_time = start_time + datetime.timedelta(minutes=1)
    confusion_label_type = LabelType.objects.filter(name="confusion").get()
    for i in range(5):
        if i < val:
            confusion = 1
        else:
            confusion = 0
        viewer = Viewer.objects.filter(user__username=student).get()
        tag = Tag.objects.create(subject=viewer,
                                 start_time=start_time,
                                 end_time=end_time)
        label = Label.objects.create(label_type=confusion_label_type,
                                     tag=tag,
                                     true=confusion,
                                     predicted=-1)
    return HttpResponse("input received")


def run_java_test(request):
    success = classify.run()
    return HttpResponse(success)


def train_on_past_data(request):
    classify.trainAllData()
    return HttpResponse('training successful')


def debug(request):
    sess = Session.objects.filter(content__name__startswith="Football")
    return HttpResponse(str(sess))


def add_series_vids(name):
    series = VideoSeries.objects.get(name=name)
    vids = [v.name for v in VideoContent.objects.filter(name__startswith=series.name)]
    series.content = ";".join(vids)
    series.save()


def load_static_videos(request):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    vids = os.listdir(cur_dir + '/../static/video')
    vids = [os.path.splitext(v)[0] for v in vids]
    group = ContentGroup.objects.get(name='data_collection')
    vids_added = []
    for v in vids:
        if len(VideoContent.objects.filter(name=v)) == 0:
            VideoContent.objects.create(group=group, name=v, public=True, duration=100)
            vids_added.append(v)
    map(lambda vs: add_series_vids(vs.name), VideoSeries.objects.all())
    return HttpResponse('videos added: ' + ' '.join(vids_added))


def add_game(request):
    owner = Owner.objects.get(user__username='mark')
    ContentGroup.objects.filter(name='Pong').delete()
    Content.objects.filter(name='pong').delete()
    game_group = ContentGroup.objects.create(name='Pong')
    game_group.owners.add(owner)
    Content.objects.create(group=game_group, name="pong", public=True, duration=0)
    return HttpResponse('game added')

def clear_godzilla(request):
    sessions = Content.objects.get(name='Movie_Engage_Godzilla').sessions
    for session in sessions.all():
        tags = Tag.objects.filter(subject=session.viewers.all(),
                                  start_time__lt=session.end_time,
                                  end_time__gte=session.start_time)
        labels = Label.objects.filter(tag=tags)
        for t in tags.all():
            t.delete()
        for l in labels.all():
            l.delete()

    return HttpResponse('ok')

def splitsubs(request):
    sessions = Session.objects.filter(viewers__user__username='qiwen;haodongl;jiacongh')
    subjects = ['qiwenz', 'haodongl', 'jiacongh']
    subjects = Viewer.objects.filter(user__username__in=subjects) 
    for s in sessions:
        s2 = Session.objects.create(content=s.content,
                name=s.name,
                start_time=s.start_time,
                end_time=s.end_time,
                content_start_sec=s.content_start_sec,
                content_end_sec=s.content_end_sec)
        s2.viewers.add(*subjects)
        s2.save()
    sessions.delete()
    return HttpResponse("ok")

def add_session_endpoint(request):
    #add_session('2014-10-17 00:25:46', '2014-10-17 00:26:16', 'Rest', ['kkchang', 'yuerany'])
    #add_session('2014-10-17 17:43:37', '2014-10-17 17:44:07', 'Rest', ['qiwenz', 'haodongl', 'jiacongh'])
    #add_session('2014-10-19 17:59:26', '2014-10-19 17:59:56', 'Rest', ['kkchang', 'yuerany'])
    #add_session('2014-10-19 22:15:23', '2014-10-19 22:15:53', 'Rest', ['kkchang'])
    #add_session('2014-10-21 00:31:47', '2014-10-21 00:32:17', 'Rest', ['kkchang'])
    #add_session('2014-11-09 17:58:47', '2014-11-09 17:59:17', 'Rest', ['kkchang'])
    return HttpResponse('ok')

def add_session(start, end, content_name, viewers):
    start_time = str_to_datetime(start, UTC)
    end_time = str_to_datetime(end, UTC)
    duration = end_time - start_time
    content = Content.objects.get(name=content_name)
    session_name = content_name + str(len(Session.objects.filter(content=content)))
    session = Session.objects.create(content=content, name=session_name,
            start_time=start_time, end_time=end_time, 
            content_start_sec=0, content_end_sec=duration.total_seconds())
    viewers = Viewer.objects.filter(user__username__in=viewers)
    session.viewers.add(*viewers)

def del_raw_endpoint(request):
    #del_raw(1, '2014-10-17 14:44:07', '2014-10-17 21:19:11')
    #del_raw(16, '2014-10-17 14:44:07', '2014-10-17 21:19:11')
    #del_raw(2, '2014-10-21 00:00:00', '2014-10-21 04:00:00')
    return HttpResponse('ok')

def del_raw(viewer, start, end):
    start_time = str_to_datetime(start, UTC)
    end_time = str_to_datetime(end, UTC)
    raws = Raw.objects.filter(subject_id=viewer, start_time__range=(start_time, end_time))
    print raws[0].subject_id, raws[0].start_time, raws[0].end_time
    raws.delete()
