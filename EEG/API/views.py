import django.utils.timezone as timezone
import datetime
from EEG.data_store.models import ContentGroup, Content, Session, LabelType, Label, Tag, Raw, Owner, Viewer
from django.http import HttpResponse
from EEG.utils.timefixer import str_to_datetime, UTC, now
from django.views.decorators.csrf import csrf_exempt
from django import forms
from EEG.data_store import aggregator
import json
import csv

def course_list(request):
    """
     :Args:
          | request: HTTP GET resquest getting the course list for the professor

     :Returns:
          | return a http response course list separate by ","
    """
    prof_name = request.GET.get('owner')
    prof = Owner.objects.filter(user__username=prof_name)
    if len(prof) == 0:
        prof = Owner.objects.filter(user__username='prof') # test prof
    courseall = ContentGroup.objects.filter(owners=prof)
    course_names = [c.name for c in courseall]
    return HttpResponse(",".join(course_names))


@csrf_exempt
def input(request):

    """
     :Args:
          | request:Http post request storing student's confusion information

     :Returns:
          |  returns "EEG" if OK
    """

    POST = request.POST
    ok = True

    student = POST.get('student')
    viewer = Viewer.objects.filter(user__username=student).get()
    start_time = str_to_datetime(POST.get("start_time"), UTC)
    end_time = str_to_datetime(POST.get("end_time"), UTC)

    sensor = POST.get("sensor")
    raw = POST.get("raw")

    label_names = POST.get("label_names")
    label_values = POST.get("label_values")

    print start_time

    if label_names is not None:
        label_names = json.loads(label_names)
        label_values = json.loads(label_values)
        for ln, lv in zip(label_names, label_values):
            label_type = LabelType.objects.filter(name=ln).get()
            tag = Tag.objects.create(subject=viewer,
                                     start_time=start_time,
                                     end_time=end_time)
            label = Label.objects.create(label_type=label_type,
                                         tag=tag,
                                         true=lv,
                                         predicted=-1)
        # uncomment to apply classifier
        # task_qs = ConfusionTask.objects.get(pk=conf_data.pk)
        # classify.classifySingleTask(task_qs, 'default.model', 'confusion')

    elif raw is not None:
        rawToks = raw.split(' ')
        waves = []
        att = -1
        sig = -1
        for raw in rawToks:
            if raw[0] == 'S':
                sig = int(raw[3:])
            elif raw[0] == 'A':
                att = int(raw[3:])
            else:
                waves.append(raw)
        waves = ' '.join(waves)
        raw_data = Raw(subject=viewer,
                       start_time=start_time,
                       end_time=end_time,
                       sensor=sensor,
                       attention=att,
                       sigqual=sig,
                       rawwave=waves)
        if sig == 200:
            ok = False
        raw_data.save()

    return HttpResponse('ok' if ok else 'not ok')


def get_next_lecture(request, course_name):
    """
     :Args:
          | request:Http request getting the next lectures
          | course_name: The content group name(eg.Machine Learning)

     :Returns:
          |  upcomming lecture  whose end is closest to now
    """
    course = ContentGroup.objects.filter(name=course_name).get()
    now_time = timezone.make_aware(datetime.datetime.now(),
                                   timezone.get_default_timezone())

    lectures = Session.objects.filter(content=course.content.all(),
                                      end_time__gt=now_time)

    lectures = lectures.order_by("end_time")
    if len(lectures) > 0:
        dat = json.dumps({
            'start_time': str(lectures[0].start_time),
            'end_time': str(lectures[0].end_time)})
        return HttpResponse(dat, content_type="application/json")
    return HttpResponse('')


def get_label_sequence(request):
    """
     :Args:
          | request:HTTP GET request getting average confusion level of -sections- for a course

     :Returns:
          |  a json format grouping the average confusion level in that sessions
    """
    if request.method != 'GET':
        return HttpResponse('ERROR: this API endpoint accepts only GET requests')
    #return HttpResponse("HEY STOP RUNNING THIS CLIENT, IT'S OUT OF DATE")  # TODO: remove this

    content_group_name = request.GET.get('content_group_name')
    content_name = request.GET.get('content_name')
    label_type_names = json.loads(request.GET.get('label_type_names'))
    segments = json.loads(request.GET.get('segments'))
    q = aggregator.get_label_sequence(content_group_name,
                                      content_name,
                                      label_type_names,
                                      segments)
    return HttpResponse(json.dumps(q), content_type="application/json")


def estimate_content_duration(request):
    if request.method != 'GET':
        return HttpResponse('ERROR: this API endpoint accepts only GET requests')
    content_group_name = request.GET.get('content_group_name')
    content_name = request.GET.get('content_name')
    content = Content.objects.get(name=content_name, group__name=content_group_name)
    sessions = content.sessions.all()
    if len(sessions) == 0:
        e_duration = 0
    else:
        e_duration = max([s.content_end_sec for s in list(sessions)])
    return HttpResponse(str(e_duration))


class FileForm(forms.Form):
    file = forms.FileField()


@csrf_exempt
def upload_labels(request):
    if request.method != 'POST':
        return HttpResponse("HEY! ONLY USE POST FOR THIS URL")

    form = FileForm(request.POST, request.FILES)
    if form.is_valid():
        # parse file here
        f = request.FILES['file']
        create_tags_from_file(f)
        return HttpResponse("OK")
    else:
        return HttpResponse("NOT OK")


def create_tags_from_file(f):
    viewers = {}
    label_types = {}
    reader = csv.reader(f, delimiter=",")
    reader.next()
    for row in reader:
        viewer_name, start, end, label_type_name, label_str = row
        start = str_to_datetime(start.strip(), UTC)
        end = str_to_datetime(end.strip(), UTC)
        if not viewer_name in viewers:
            print viewer_name
            viewers[viewer_name] = Viewer.objects.get(user__username=viewer_name.strip())
        if not label_type_name in label_types:
            label_types[label_type_name] = LabelType.objects.get(name=label_type_name.strip())
        tag=Tag.objects.create(subject=viewers[viewer_name], start_time=start, end_time=end)
        Label.objects.create(label_type=label_types[label_type_name], true=-1, predicted=int(label_str), tag=tag)


def check_eeg(request):
    viewer_names = json.loads(request.GET.get('viewer_names'))
    bad_connections = []
    for viewer_name in viewer_names:
        now_time = now()
        cut_off = now_time - datetime.timedelta(seconds=10)
        eegs = Raw.objects.filter(subject__user__username=viewer_name, end_time__gt=cut_off)
        if len(eegs) == 0:
            bad_connections.append(viewer_name)
    if len(bad_connections) > 0:
        return HttpResponse("bad connections: %s " % "; ".join(bad_connections))
    return HttpResponse("OK")
