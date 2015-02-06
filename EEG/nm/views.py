from EEG.data_store.models import ContentGroup, Content, Session, VideoContent, VideoSeries, User, Viewer, LabelType, Label, Tag
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from EEG.utils.common import union
from urllib import urlencode
from EEG.data_store.utils import generate_viewer
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
def home(request):
    """
    The router for marketer login
     :Args:
        | request: a request object
     :Returns:
        | a HttpResponseRedirect object containing marketer home page
    """
    if not is_owner(request.user):
        return HttpResponseRedirect('/EEG/not_owner')
    content_groups = ContentGroup.objects.filter(owners=request.user.owner)
    if len(content_groups) == 0:
        return HttpResponseRedirect('/EEG/add_course')
    else:
        content_group_name = content_groups[0].name
        return HttpResponseRedirect('/EEG/market/cg/' + content_group_name)


def sort_by_name(things):
    return sorted(things, key=lambda thing: thing.name)


def owner_context(owner, content_group_name=None, content_name=None, series_name=None):

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
    # initialize all variables
    contents = []
    series = []
    current_content_group = None
    current_content = None
    current_series = None

    if content_group_name is None:
        content_groups = ContentGroup.objects.filter(owners=owner)
    else:
        current_content_group = ContentGroup.objects.filter(name=content_group_name,
                                                            owners=owner).get()
        content_groups = ContentGroup.objects.filter(owners=owner)
        contents = Content.objects.filter(group=current_content_group)
        videos = VideoContent.objects.filter(group=current_content_group)
        videos = sort_by_name(list(videos))
        series = VideoSeries.objects.filter(group=current_content_group)
        if content_name is not None:
            current_content = contents.filter(name=content_name).get()
        elif series_name is not None:
            current_series = series.filter(name=series_name).get()
        else:
            if len(contents) > 0:
                current_content = contents[0]
            else:
                current_content = None

        general_content = contents.exclude(name__in=[v.name for v in list(videos)])
        general_content = sort_by_name(list(general_content))
    return {
        'current_content_group': current_content_group,
        'content_groupall': content_groups,
        'contentall': general_content,
        'current_content': current_content,
        'videoall': videos,
        'seriesall': series,
        'current_series': current_series}


@login_required
def delete(request, content_group_name):
    if not is_owner(request.user):
        return HttpResponseRedirect('/EEG/not_owner')

    context_base = owner_context(
        request.user.owner, content_group_name, request.GET.get('content'), request.GET.get('series'))
    content = context_base['current_content']
    series = context_base['current_series']

    to_delete = content if content is not None else series
    to_delete.delete()
    return HttpResponseRedirect('/EEG/market/cg/' + content_group_name)


@login_required
def rename(request, content_group_name):
    if not is_owner(request.user):
        return HttpResponseRedirect('/EEG/not_owner')
    new_name = request.GET.get('name')

    context_base = owner_context(
        request.user.owner, content_group_name, request.GET.get('content'), request.GET.get('series'))
    content = context_base['current_content']
    series = context_base['current_series']

    to_change = content if content is not None else series
    to_change.name = new_name
    to_change.save()
    query = 'content' if content is not None else 'series'
    query = '?%s=%s' % (query, new_name);
    return HttpResponseRedirect('/EEG/market/cg/' + content_group_name + query)


@login_required
def clear(request, content_group_name):
    if not is_owner(request.user):
        return HttpResponseRedirect('/EEG/not_owner')

    context_base = owner_context(
        request.user.owner, content_group_name, request.GET.get('content'), request.GET.get('series'))
    content = context_base['current_content']
    series = context_base['current_series']

    sessions = content.sessions
    for session in sessions.all():
        tags = Tag.objects.filter(subject=session.viewers.all(),
                                  start_time__lt=session.end_time,
                                  end_time__gte=session.start_time)
        labels = Label.objects.filter(tag=tags)
        for t in tags.all():
            t.delete()
        for l in labels.all():
            l.delete()

    return HttpResponseRedirect('/EEG/market/cg/' + content_group_name)


@login_required
def content_group(request, content_group_name):
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
    context_base = owner_context(
        request.user.owner, content_group_name, request.GET.get('content'), request.GET.get('series'))
    current_content = context_base['current_content']
    if current_content is not None:
        if len(VideoContent.objects.filter(group=context_base['current_content_group'], name=current_content.name)) != 0:
            return video_page(request, current_content, context_base)
        elif current_content.name.lower() == 'pong':
            return game_page(request, current_content, context_base)
        else:
            return content_page(request, current_content, context_base)
    if context_base['current_series'] is not None:
        return series_page(request, context_base['current_series'], context_base)
    return render(request, '/EEG/no_series.html', context_base)


def gen_stats_for_sessions(sessions):
    viewers = [v for s in list(sessions.all()) for v in list(s.viewers.all())]
    return len(sessions), len(set(viewers))


def series_page(request, series, context):
    vids = series.content.split(';')
    sessions = Session.objects.filter(content__name__in=vids)
    num_views, num_viewers = gen_stats_for_sessions(sessions)
    return render(request, 'series.html', 
            union({'num_views': num_views, 'num_viewers': num_viewers}, context))


def content_page(request, content, context):
    sessions = Session.objects.filter(content=content)
    num_views, num_viewers = gen_stats_for_sessions(sessions)
    return render(request, 'content.html', 
            union({'num_views': num_views, 'num_viewers': num_viewers}, context))


def video_page(request, video, context):
    sessions = Session.objects.filter(content=video)
    num_views, num_viewers = gen_stats_for_sessions(sessions)
    return render(request, 'video.html', 
            union({'num_views': num_views, 'num_viewers': num_viewers}, context))


def game_page(request, game, context):
    sessions = Session.objects.filter(content=game)
    num_views, num_viewers = gen_stats_for_sessions(sessions)
    return render(request, 'game.html', 
            union({'num_views': num_views, 'num_viewers': num_viewers}, context))


class ContentGroupForm(forms.Form):
    """
    | content_group_name: <Char>

    .. note::
        ContentGroupForm allows us to create a new content_group
    """
    content_group_name = forms.CharField(max_length=1000)


@login_required
def add_campaign(request):
    """
    add a new campaign
    """
    if not is_owner(request.user):
        return HttpResponseRedirect('/EEG/not_owner')
    if request.method == 'GET':
        context_base = owner_context(request.user.owner)
        form = ContentGroupForm()
        return render_to_response('add_campaign.html',
                                  RequestContext(request, union({'form': form}, context_base)))
    else:
        form = ContentGroupForm(request.POST)
        if form.is_valid():
            content_group_name = form.cleaned_data['content_group_name']
            content_group_name = '_'.join(content_group_name.split(' '))
            content_group = ContentGroup.objects.create(name=content_group_name)
            content_group.owners.add(request.user.owner)
            content_group.save()

            return HttpResponseRedirect('/EEG/add_video/' + content_group_name)
    return HttpResponseRedirect('/EEG/add_campaign/')  # TODO: display an error message


class ContentForm(forms.Form):
    name = forms.CharField(max_length=999)


@login_required
def add_content(request, content_group_name):
    if not is_owner(request.user):
        return HttpResponseRedirect('/EEG/not_owner')
    if request.method == 'GET':
        context_base = owner_context(request.user.owner, content_group_name)
        context_base['current_content'] = None
        form = ContentForm()
        return render_to_response('add_content.html',
                                  RequestContext(request, union({'form': form}, context_base)))
    else:
        form = ContentForm(request.POST)
        if form.is_valid():
            content_group = ContentGroup.objects.get(name=content_group_name)
            name = form.cleaned_data['name']
            Content.objects.create(name=name,
                                   group=content_group,
                                   duration=100) # TODO: take duratino out of the content model

            return HttpResponseRedirect('/EEG/market/cg/' + content_group.name +
                                            '?' + urlencode({'content': name}))
    return HttpResponseRedirect('/EEG/add_content/' + content_group_name)


class VideoForm(forms.Form):
    """
        | name: <Char>
        | url: <Char>

        .. note::
            form to add a piece of video content
    """

    name = forms.CharField(max_length=999)
    url = forms.CharField(max_length=999)


@login_required
def add_video(request, content_group_name):
    """
        add video
    """

    if not is_owner(request.user):
        return HttpResponseRedirect('/EEG/not_owner')
    if request.method == 'GET':
        context_base = owner_context(request.user.owner, content_group_name)
        context_base['current_content'] = None
        form = VideoForm()
        return render_to_response('add_video.html',
                                  RequestContext(request, union({'form': form}, context_base)))
    else:
        form = VideoForm(request.POST)
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

            redirect = HttpResponseRedirect('/EEG/market/cg/' + content_group.name +
                                            '?' + urlencode({'content': name}))
            return redirect
    return HttpResponseRedirect('/EEG/add_video/' + content_group_name)


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
        VideoSeriesForm represent a series of video formed lecture.
    """
    name = forms.CharField(max_length=999)
    content = forms.CharField(max_length=9999,
                              widget=forms.Textarea(attrs={'cols': 50, 'rows': 20}))

    def clean_content(self):
        content_names = self.cleaned_data.get('content')
        content_names = [s.strip() for s in content_names.split(';')]
        for content_name in content_names:
            if Content.objects.filter(name=content_name).count() != 1:
                raise forms.ValidationError("content names not valid")
        return ';'.join(content_names)


@login_required
def add_video_series(request, content_group_name):
    """
        direct to a add vedio series page
        :Args:
        | request: a request object
        | content_group_name: the content group you want to add the videos to

        :Returns:
        | a HttpResponse object with that rendered add video text

    """
    if not is_owner(request.user):
        return HttpResponseRedirect('/EEG/not_owner')
    if request.method == 'POST':
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
                                            '?' + urlencode({'series': name}))
            return redirect
    elif request.method == 'GET':
        form = VideoSeriesForm()

    context_base = owner_context(request.user.owner, content_group_name)
    context_base['current_content'] = None
    return render_to_response('add_series.html',
                              RequestContext(request, union({'form': form}, context_base)))


@login_required
def setup_film(request, content_group_name):
    if not is_owner(request.user):
        return HttpResponseRedirect('/EEG/not_owner')
    context_base = owner_context(
        request.user.owner, content_group_name, request.GET.get('content'), request.GET.get('series'))
    if context_base['current_content'] is not None:
        form = FilmForm(context_base['current_content'].name)
        return render(request, 'setup_film.html', union({'form': form}, context_base))
    return HttpResponseRedirect('/EEG/market/cg/' + content_group_name)


class FilmForm(forms.Form):
    viewers = forms.CharField(required=False)
    content = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, content_name, *args, **kwargs):
        super(FilmForm, self).__init__(*args, **kwargs)
        self.fields['content'].initial = content_name


@login_required
def setup_game(request, content_group_name):
    if not is_owner(request.user):
        return HttpResponseRedirect('/EEG/not_owner')
    context_base = owner_context(
        request.user.owner, content_group_name, request.GET.get('content'), request.GET.get('series'))
    if context_base['current_content'] is not None:
        form = FilmForm(context_base['current_content'].name)
        return render(request, 'setup_game.html', union({'form': form}, context_base))
    return HttpResponseRedirect('/EEG/market/cg/' + content_group_name)


class GameForm(forms.Form):
    viewers = forms.CharField(required=False)
    content = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, content_name, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        self.fields['content'].initial = content_name


@login_required
def setup_experiment(request, content_group_name):
    """
        setup the necessary information to run an experiment
        :Args:
        | request: a request object
        | content_group_name: the content group you want to start
        :Returns:
        | a HttpResponse object containing the setup page
    """
    if not is_owner(request.user):
        return HttpResponseRedirect('/EEG/not_owner')
    context_base = owner_context(
        request.user.owner, content_group_name, request.GET.get('content'), request.GET.get('series'))
    if context_base['current_series'] is not None:
        form = ExperimentForm(context_base['current_series'].name)
        return render(request, 'setup_experiment.html', union({'form': form}, context_base))
    return HttpResponseRedirect('/EEG/market/cg/' + content_group_name)


class ExperimentForm(forms.Form):
    viewers = forms.CharField(required=False)
    left_sensor = forms.IntegerField(required=False)
    right_sensor = forms.IntegerField(required=False)
    center_sensor = forms.IntegerField(required=False)
    series = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, series_name, *args, **kwargs):
        super(ExperimentForm, self).__init__(*args, **kwargs)
        self.fields['series'].initial = series_name

    def clean(self):
        cleaned_data = super(ExperimentForm, self).clean()

        if (cleaned_data.get('center_sensor') is None and
           (cleaned_data.get('left_sensor') is None or cleaned_data.get('right_sensor') is None)):
            raise forms.ValidationError("please specify which sensors to use")


@login_required
def experiment_old(request, content_group_name):
    if not is_owner(request.user):
        return HttpResponseRedirect('/EEG/not_owner')
    content_group = ContentGroup.objects.get(name=content_group_name)
    series_name = request.GET.get('series')
    series = VideoSeries.objects.get(name=series_name,
                                     group=content_group)
    videos = []

    # gen calibration data
    calibration = ['Happy', 'Sad']
    random.shuffle(calibration)
    calibration = [calibration[0], 'Neutral', calibration[1]]

    # gen video data
    experiment_videos = series.content.split(';')
    random.shuffle(experiment_videos)

    video_names = calibration
    for vn in experiment_videos:
        video_names.append('Rest')
        video_names.append(vn)
    videos = [VideoContent.objects.get(name=vn, group=content_group) for vn in video_names]
    segments = [{'video': v} for v in videos]
    survey1 = {'id': 1, 'questions':
               [{'name': 'q1', 'text': 'question goes here', 'type': 'likert'},
                {'name': 'q2', 'text': 'question2 goes here', 'type': 'text'}]}
    rest = {'video': VideoContent.objects.get(name='Rest', group=content_group)}
    segments = [rest] + [{'survey': survey1}] + segments

    # gen viewers
    viewers = [generate_viewer()]
    content_group.viewers.add(*viewers)
    viewer_names = [v.user.username for v in viewers]

    # get device ids
    center_sensor = request.GET.get('center_sensor')
    left_sensor = request.GET.get('left_sensor')
    right_sensor = request.GET.get('right_sensor')
    if center_sensor != '':
        print center_sensor, 'sensor'
        sensors = [{'sensor': 'center', 'port': center_sensor}]
    elif left_sensor is not None and right_sensor is not None:
        sensors = [{'sensor': 'left', 'port': left_sensor},
                   {'sensor': 'right', 'port': right_sensor}]
    else:
        return HttpResponseRedirect('/EEG/experiment_bad_params')

    return render(request, 'run_experiment.html', {'viewers': viewer_names, 'videos': segments, 'sensors': sensors})


def game(request, content_group_name):
    if not is_owner(request.user):
        return HttpResponseRedirect('/EEG/not_owner')
    content_group = ContentGroup.objects.get(name=content_group_name)
    viewer_names = request.GET.get('viewers').split(';')
    content_name = request.GET.get('content')
    viewers = []
    for vn in viewer_names:
        try:
            v = Viewer.objects.get(user__username=vn)
        except Viewer.DoesNotExist:
            v = generate_viewer(vn)
        viewers.append(v)

    content_group.viewers.add(*viewers)
    viewer_names = [v.user.username for v in viewers]
    rest = {'video': VideoContent.objects.get(name='Rest')}
    segments = [rest] + [{'game': content_name}];

    return render(request, 'run_experiment.html', {'viewers': viewer_names, 'videos': segments, 'content_group_name': content_group_name})


def experiment(request, content_group_name):
    if not is_owner(request.user):
        return HttpResponseRedirect('/EEG/not_owner')
    content_group = ContentGroup.objects.get(name=content_group_name)
    # gen video data
    #videos = ['NBA', "Baseball", "Cooking"]
    #random.shuffle(videos)
    #videos = [VideoContent.objects.get(name=vn, group=content_group) for vn in videos]
    series_name = request.GET.get('series')
    series = VideoSeries.objects.get(name=series_name)
    # gen video data
    videos = series.content.split(';')
    videos = [VideoContent.objects.get(name=v, group=content_group) for v in videos]
    random.shuffle(videos)
    segments = []
    for i, v in enumerate(videos):
        engagement_text = "engage" if re.search(r'Engage', v.name) else "disengaged"
        notice = {'id': i, 'time': 10000, 'text': engagement_text}
        segments.append({'notice': notice})
        segments.append({'video': v})
        ad_survey = {'id': i, 'questions':
                     [{'name': 'q2', 'text': 'How engaged were you?', 'type': 'likert'}]}
        segments.append({'survey': ad_survey})
    rest = {'video': VideoContent.objects.get(name='Rest', group=content_group)}
    segments = [rest] + segments

    # gen viewers
    viewer_names = request.GET.get('viewers').split(';')
    viewers = []
    for vn in viewer_names:
        try:
            v = Viewer.objects.get(user__username=vn)
        except Viewer.DoesNotExist:
            v = generate_viewer(vn)
        viewers.append(v)

    content_group.viewers.add(*viewers)

    viewer_names = [v.user.username for v in viewers]

    # get device ids
    center_sensor = request.GET.get('center_sensor')
    left_sensor = request.GET.get('left_sensor')
    right_sensor = request.GET.get('right_sensor')
    if center_sensor != '':
        sensors = [{'sensor': 'center', 'port': center_sensor}]
    elif left_sensor is not None and right_sensor is not None:
        sensors = [{'sensor': 'left', 'port': left_sensor},
                   {'sensor': 'right', 'port': right_sensor}]
    else:
        return HttpResponseRedirect('/EEG/experiment_bad_params')

    return render(request, 'run_experiment.html', {'viewers': viewer_names, 'videos': segments, 'sensors': sensors,
             'content_group_name': content_group_name})


def film(request, content_group_name):
    if not is_owner(request.user):
        return HttpResponseRedirect('/EEG/not_owner')
    content_group = ContentGroup.objects.get(name=content_group_name)
    # series_name = request.GET.get('series')
    # gen viewers

    viewer_names = request.GET.get('viewers').split(';')
    content_name = request.GET.get('content')
    viewers = []
    for vn in viewer_names:
        try:
            v = Viewer.objects.get(user__username=vn)
        except Viewer.DoesNotExist:
            v = generate_viewer(vn)
        viewers.append(v)

    content_group.viewers.add(*viewers)
    viewer_names = [v.user.username for v in viewers]

    return render(request, 'run_film.html', 
            {'viewers': viewer_names,
             'content_name': content_name,
             'content_group_name': content_group_name})
