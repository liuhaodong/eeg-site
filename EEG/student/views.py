from EEG.data_store.models import ContentGroup, Content, VideoContent, Session, Viewer, SurveyAnswer, SessionTag
#from django.shortcuts import render_to_response
#from django import forms
#from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from EEG.utils import timefixer
import datetime
import json
#from EEG.utils.common import union
#from urllib import urlencode

# TODO make sure all requests here are get requests


def is_viewer(user):
    return hasattr(user, 'viewer')


@login_required
def studenthome(request):
    if not is_viewer(request.user):
        return HttpResponseRedirect('/EEG/not_viewer')
    content_groups = ContentGroup.objects.filter(viewers=request.user.viewer)  # TODO: fix this
    if len(content_groups) == 0:
        return HttpResponseRedirect('/EEG/student/no_classes')
    content_group_name = content_groups[0].name
    return HttpResponseRedirect('/EEG/student/course/' + content_group_name)


'''
assumes user is viewer
assumes this is a get request
'''
def viewer_context(viewer, content_group_name=None, content_name=None):
    if content_group_name is None:
        content_groups = ContentGroup.objects.filter(viewers=viewer)
        contents = []
        current_content_group = None
        current_content = None
    else:
        current_content_group = ContentGroup.objects.filter(name=content_group_name, viewers=viewer).get()
        content_groups = ContentGroup.objects.filter(viewers=viewer)
        contents = VideoContent.objects.filter(group=current_content_group)  # add invite to this
        if content_name is None:
            if len(contents) > 0:
                current_content = contents[0]
            else:
                current_content = None
        else:
            current_content = contents.filter(name=content_name).get()

    return {
        'current_content_group': current_content_group,
        'content_groups': content_groups,
        'contents': contents,
        'viewer_name': viewer.user.username,
        'current_content': current_content}


def student_context(viewer, course_name=None, lecture_name=None):
    c = viewer_context(viewer, course_name, lecture_name)

    return {
        'courseall': c['content_groups'],
        'current_course': c['current_content_group'],
        'lectureall': c['contents'],
        'viewer_name': c['viewer_name'],
        'current_lecture': c['current_content']}


@login_required
def course(request, content_group_name):
    if not is_viewer(request.user):
        return HttpResponseRedirect('/EEG/not_viewer')
    context_base = student_context(
        request.user.viewer, content_group_name, request.GET.get('lecture'))
    return render(request, 'studenthome.html', context_base)


def start_session(request):
    # TODO: check that the viewer has permission to start this
    success = False
    session_name = None
    if request.method != 'POST':
        #TODO: log not POST
        pass
    else:
        content_group_name = request.POST.get('content_group_name')
        content_name = request.POST.get('content_name')
        content_time = int(float(request.POST.get('content_time')))
        viewer_names = json.loads(request.POST.get('viewer_name'))
        # TODO: search only under current user's invited contents
        viewers = Viewer.objects.filter(user__username__in=viewer_names)

        content_group = ContentGroup.objects.get(name=content_group_name)
        content = Content.objects.filter(name=content_name,
                                         group=content_group).get()
        session_count = content.sessions.count()
        session_name = 'session %d' % session_count
        session = Session.objects.create(content=content,
                                         name=session_name,
                                         start_time=timefixer.now(),
                                         end_time=timefixer.now() + datetime.timedelta(minutes=1),
                                         content_start_sec=content_time,
                                         content_end_sec=content.duration)
        print content.name, session_name
        session.viewers.add(*viewers)
        session.save()
        success = True
    return HttpResponse(json.dumps({'ok': success, 'session_name': session_name}), content_type="application/json")


def stop_session(request):
    # TODO: check that the viewer has permission to stop this
    success = False
    if request.method != 'POST':
        #TODO: log not POST
        pass
    else:
        content_group_name = request.POST.get('content_group_name')
        content_name = request.POST.get('content_name')
        content_time = int(float(request.POST.get('content_time')))
        session_name = request.POST.get('session_name')
        # TODO: search only under current user's invited contents
        content_group = ContentGroup.objects.get(name=content_group_name)
        content = Content.objects.filter(name=content_name,
                                         group=content_group).get()
        print content.name, session_name
        session = Session.objects.filter(name=session_name,
                                         content=content).get()
        session.end_time = timefixer.now()
        session.content_end_sec = content_time
        session.save()

        success = True
    return HttpResponse(json.dumps({'ok': success, 'session_name': session_name}), content_type="application/json")


def store_answers(request):
    # TODO: check that the viewer has permission to stop this
    success = False
    if request.method != 'POST':
        #TODO: log not POST
        pass
    else:
        content_group_name = request.POST.get('content_group_name')
        content_name = request.POST.get('content_name')
        session_name = request.POST.get('session_name')
        viewer_names = json.loads(request.POST.get('viewer_name'))
        answers = request.POST.get('answers')
        # TODO: search only under current user's invited contents
        viewers = Viewer.objects.filter(user__username__in=viewer_names)
        print len(viewers)
        content_group = ContentGroup.objects.get(name=content_group_name)
        content = Content.objects.filter(name=content_name,
                                         group=content_group).get()
        print content.name, session_name
        session = Session.objects.filter(name=session_name,
                                         content=content).get()
        for viewer in viewers:
            SurveyAnswer.objects.create(subject=viewer,
                                         start_time=session.start_time,
                                         end_time=session.end_time,
                                         question=content_name,
                                         answer=answers)
        success = True

    return HttpResponse(json.dumps({'ok': success}), content_type="application/json")


def store_session_tag(request):
    # TODO: check that the viewer has permission to stop this
    success = False
    if request.method != 'POST':
        #TODO: log not POST
        pass
    else:
        content_group_name = request.POST.get('content_group_name')
        content_name = request.POST.get('content_name')
        session_name = request.POST.get('session_name')
        data = request.POST.get('data')
        # TODO: search only under current user's invited contents
        content_group = ContentGroup.objects.get(name=content_group_name)
        content = Content.objects.filter(name=content_name,
                                         group=content_group).get()
        session = Session.objects.filter(name=session_name,
                                         content=content).get()
        tag_time = timefixer.now()
        SessionTag.objects.create(session=session,
                time=tag_time,
                data=data)
        success = True

    return HttpResponse(json.dumps({'ok': success}), content_type="application/json")
