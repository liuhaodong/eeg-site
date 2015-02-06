from EEG.data_store.models import ContentGroup, Content, VideoContent, VideoSeries, Session, User, Viewer
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.core import mail
from django import forms
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from EEG.utils.common import union
from urllib import urlencode
from EEG.data_store.utils import generate_viewer
import pytz
import sys
import random
import requests
import json
import re

YT_API_KEY = "AIzaSyCX-kOkPxwk8auhPdnVDMwJDmGPMLKXag0"

# TODO make sure all requests here are get requests


def is_owner(user):
    """
     :Args:
        | user: a user object

     :Returns:
        | a boolean
    """

    return hasattr(user, 'owner')


@login_required
def profhome(request):
    """
    Retrieves the home(default) page show to professor users when he login.

     :Args:
        | request: a request object

     :Returns:
        | a HttpResponseRedirect object containing professor home page
    """

    if not is_owner(request.user):
        return HttpResponseRedirect('/EEG/not_owner')
    content_groups = ContentGroup.objects.filter(owners=request.user.owner)
    if len(content_groups) == 0:
        return HttpResponseRedirect('/EEG/add_course')
    else:
        content_group_name = content_groups[0].name
        return HttpResponseRedirect('/EEG/course/' + content_group_name)


'''
assumes user is owner
assumes this is a get request
'''


def owner_context(owner, content_group_name=None, content_name=None):

    """
    Retrieves context the owner controls, can specify content group and content name.
    If content_group_name is specified, the current content group will be set to the one.
    Otherwise it will be set to None.
    If content_name is specified, the current content will be set to corresponding one.
    Otherwise it will be set to first content int contents list.

    :Args:
        | owner: a Owner object
        | content_group_name: a str representing the name of a content group
        | content_name: a str representing the name of a content

    :Returns:
        | A dict mapping keys to 'current_content_group', 'content_groups', 'contents' and'current_content'

    """
    if content_group_name is None:
        content_groups = ContentGroup.objects.filter(owners=owner)
        contents = []
        current_content_group = None
        current_content = None
    else:
        current_content_group = ContentGroup.objects.filter(name=content_group_name,
                                                            owners=owner).get()
        content_groups = ContentGroup.objects.filter(owners=owner)
        contents = Content.objects.filter(group=current_content_group)
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
        'current_content': current_content}


def prof_context(owner, course_name=None, lecture_name=None):

    """
    Retrieves context the professor controls, can specify content group and content name.
    If content_group_name is specified, the current content group will be set to the one.
    Otherwise it will be set to None.
    If content_name is specified, the current content will be set to corresponding one.
    Otherwise it will be set to first content int contents list.

    :Args:
        | owner: a Owner object
        | content_group_name: a str representing the name of a content group
        | content_name: a str representing the name of a content

    :Returns:
        | A dict mapping keys to 'current_content_group', 'content_groups', 'contents' and'current_content'
    """

    c = owner_context(owner, course_name, lecture_name)
    return {
        'courseall': c['content_groups'],
        'current_course': c['current_content_group'],
        'lectureall': c['contents'],
        'current_lecture': c['current_content']}


@login_required
def course(request, content_group_name):
    """
    Combines a course template with a given content_group_name and returns an HttpResponse object with that rendered text.

    :Args:
        | request: a request object
        | content_group_name: a str representing the name of a content group

    :Returns:
        | a HttpResponse object with that course text

    """

    if not is_owner(request.user):
        return HttpResponseRedirect('/EEG/not_owner')
    context_base = prof_context(
        request.user.owner, content_group_name, request.GET.get('lecture'))
    return render(request, 'course.html', context_base)


class ContentGroupForm(forms.Form):
    """
    | content_group_name: <Char>
    | students: <Char>

    .. note::
        ContentGroupForm represent the content group, including content and enrolled students.
        e.g a serials of course, Machine Learning.
    """
    content_group_name = forms.CharField(max_length=1000)
    # TODO: factor student into different subform
    students = forms.CharField(max_length=9999, required=False,
                               widget=forms.Textarea(attrs={'cols': 50, 'rows': 20}))


@login_required
def add_course(request):
    """
    direct to a add course page
    :Args:
        | request: a request object

    :Returns:
        | a HttpResponse object with that rendered add course text

    """
    if not is_owner(request.user):
        return HttpResponseRedirect('/EEG/not_owner')
    if request.method == 'GET':
        context_base = prof_context(request.user.owner)
        form = ContentGroupForm()
        return render_to_response('add_course.html',
                                  RequestContext(request, union({'form': form}, context_base)))
    else:
        form = ContentGroupForm(request.POST)
        if form.is_valid():
            content_group_name = form.cleaned_data['content_group_name']
            content_group_name = '_'.join(content_group_name.split(' '))
            content_group = ContentGroup.objects.create(name=content_group_name)
            content_group.owners.add(request.user.owner)
            content_group.save()

            user = request.user
            userID = user.username
            studentsList = form.cleaned_data['students'].split(';')
            if len(studentsList[0]) > 0:
                registration_address = request.get_host() + reverse('EEG.account.views.register')
                registration_address += '?' + urlencode({'student': True})
                mailText = 'Hi, SynMetricer \n\nPlease register this course: ' + content_group_name + '\nTaught by ' + userID
                mailText += ' at ' + registration_address
                mail.send_mail('REGISTER for a new course on SynMetric', mailText, from_email='wanghaohan8903@gmail.com',
                               recipient_list=studentsList)
                for s in studentsList:
                    # TODO: 9999 collisions is not infinite, must report error
                    viewers = Viewer.objects.filter(user__email=s)
                    if (len(viewers) == 0):
                        viewer = generate_viewer()
                    else:
                        viewer = viewers[0]
                    content_group.viewers.add(viewer)
                    content_group.save()

            return HttpResponseRedirect('/EEG/add_lecture/' + content_group_name)
    return HttpResponseRedirect('/EEG/add_course/')  # TODO: display an error message


class LectureForm(forms.Form):
    """
        | name: <Char>
        | start_date: <DateTime>
        | end_date: <DateTime>

        .. note::
            LectureForm represent a lecture.
            e.g Machine Learning lecture 1.
    """

    name = forms.CharField(max_length=1000)
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()


@login_required
def add_lecture(request, content_group_name):
    """
        direct to a add course page
        :Args:
        | request: a request object

        :Returns:
        | a HttpResponse object with that rendered add course text

    """
    if not is_owner(request.user):
        return HttpResponseRedirect('/EEG/not_owner')
    if request.method == 'GET':
        context_base = prof_context(request.user.owner, content_group_name)
        context_base['current_lecture'] = None
        form = LectureForm()
        return render_to_response('add_lecture.html',
                                  RequestContext(request, union({'form': form}, context_base)))
    else:
        form = LectureForm(request.POST)
        if form.is_valid():
            content_group = ContentGroup.objects.get(name=content_group_name)
            name = form.cleaned_data['name']
            start_time = form.cleaned_data['start_date']
            end_time = form.cleaned_data['end_date']
            start_time.astimezone(pytz.utc)  # convert to utc
            end_time.astimezone(pytz.utc)  # convert to utc
            duration_secs = (start_time - end_time).total_seconds()

            # TODO: add invited viewers
            content = Content.objects.create(name=name,
                                             group=content_group,
                                             duration=duration_secs)
            session = Session.objects.create(start_time=start_time,
                                             end_time=end_time,
                                             content_start_sec=0,
                                             content_end_sec=duration_secs,
                                             name=name,
                                             content=content)

            redirect = HttpResponseRedirect('/EEG/course/' + content_group.name +
                                            '?' + urlencode({'lecture': name}))
            return redirect
    return HttpResponseRedirect('/EEG/add_lecture/' + content_group_name)


class VideoLectureForm(forms.Form):
    """
        | name: <Char>
        | url: <Char>

        .. note::
            VideoLectureForm represent a video formed lecture.
    """

    name = forms.CharField(max_length=999)
    url = forms.CharField(max_length=999)


@login_required
def add_video_lecture(request, content_group_name):
    """
        direct to a add vedio lecture page
        :Args:
            | request: a request object
            | content_group_name: the content group you want to add the lecture to

        :Returns:
            | a HttpResponse object with that rendered add course text

    """

    if not is_owner(request.user):
        return HttpResponseRedirect('/EEG/not_owner')
    if request.method == 'GET':
        context_base = prof_context(request.user.owner, content_group_name)
        context_base['current_lecture'] = None
        form = VideoLectureForm()
        return render_to_response('add_video_lecture.html',
                                  RequestContext(request, union({'form': form}, context_base)))
    else:
        form = VideoLectureForm(request.POST)
        if form.is_valid():
            content_group = ContentGroup.objects.get(name=content_group_name)
            name = form.cleaned_data['name']
            url = form.cleaned_data['url']
            vid_id = url[-11:]
            duration_secs = get_video_length(vid_id)
            VideoContent.objects.create(name=name,
                                        group=content_group,
                                        video_url=url,
                                        duration=duration_secs)

            redirect = HttpResponseRedirect('/EEG/course/' + content_group.name +
                                            '?' + urlencode({'lecture': name}))
            return redirect
    return HttpResponseRedirect('/EEG/add_video_lecture/' + content_group_name)


def get_video_length(videoId):
    """
        retrieve lecture length, in seconds
        :Args:
            | videoId: videoId that specific a video

        :Returns:
            | a interger indicate the length of video in seconds

    """
    params = {'id': videoId,
              'key': YT_API_KEY,
              'part': 'contentDetails',
              'fields': 'items(contentDetails(duration))'}
    r = requests.get("https://www.googleapis.com/youtube/v3/videos", params=params)
    # TODO: check for errors in the response
    yt_info = json.loads(r.text)
    if not 'items' in yt_info:
        return 5 * 60  # default to 5 minutes
    duration = yt_info['items'][0]['contentDetails']['duration']
    # TODO: parse this without such a stupid try catch ladder
    hours = 0
    minutes = 0
    seconds = 0
    try:
        match = re.match(r'PT(.*)S', duration)
        seconds = int(match.group(1))
    except:
        try:
            match = re.match(r'PT(.*)M(.*)S', duration)
            minutes = int(match.group(1))
            seconds = int(match.group(2))
        except:
            match = re.match(r'PT(.*)H(.*)M(.*)S', duration)
            hours = int(match.group(1))
            minutes = int(match.group(2))
            seconds = int(match.group(3))
    return hours * 60 * 60 + minutes * 60 + seconds


class VideoSeriesForm(forms.Form):
    """
        | name: <Char>
        | content: <Char>
        .. note::
        VideoSeriesForm is the form to create a series of video
    """
    name = forms.CharField(max_length=999)
    content = forms.CharField(max_length=9999,
                              widget=forms.Textarea(attrs={'cols': 50, 'rows': 20}))


@login_required
def add_video_series(request, content_group_name):
    """
        page to add video series
        :Args:
        | request: a request object
        | content_group_name: the content group you want to add the videos to
    """
    if not is_owner(request.user):
        return HttpResponseRedirect('/EEG/not_owner')
    if request.method == 'GET':
        context_base = prof_context(request.user.owner, content_group_name)
        context_base['current_lecture'] = None
        form = VideoSeriesForm()
        return render_to_response('add_video_series.html',
                                  RequestContext(request, union({'form': form}, context_base)))
    else:
        form = VideoSeriesForm(request.POST)
        if form.is_valid():
            content_group = ContentGroup.objects.get(name=content_group_name)
            name = form.cleaned_data['name']
            content = form.cleaned_data['content']
            # TODO: validate that these are all real content names
            VideoSeries.objects.create(name=name,
                                       group=content_group,
                                       content=content)

            redirect = HttpResponseRedirect('/EEG/market/cg/' + content_group.name +
                                            '?' + urlencode({'content': name}))
            return redirect
    return HttpResponseRedirect('/EEG/add_video_series/' + content_group_name)


@login_required
def show_series(request, content_group_name):
    """
        direct to a page that show all the series given a content group name
        :Args:
        | request: a request object
        | content_group_name: the content group you want to query to

        :Returns:
        | a HttpResponse object with that rendered show video text

    """
    if not is_owner(request.user):
        return HttpResponseRedirect('/EEG/not_owner')
    series_name = request.GET.get("series")
    series = VideoSeries.objects.filter(group__name=content_group_name,
                                        name=series_name,
                                        group__owner__user__username=request.user).get()
    return render_to_response('show_series.html',
                              {'series': series})
