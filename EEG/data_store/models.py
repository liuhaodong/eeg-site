from django.db import models
from django.contrib.auth.models import User
from EEG.utils.timefixer import time_overlap


class Viewer(models.Model):
    """
    | test: haohan
    | user: OneToOneField(User)
    | matching_email: <Char>

    .. note::
        Viewer represent the participants join one lecture.
    """
    user = models.OneToOneField(User, related_name='viewer')
    matching_email = models.CharField(max_length=999)


class Owner(models.Model):
    """
    | user: OneToOneField(Owner)

    .. note::
        Owner represents the instructor.

    """
    user = models.OneToOneField(User, related_name='owner')
    marketer = models.BooleanField(default=False)


class ContentGroup(models.Model):
    """
    | name: <Char>
    | owners: ManyToManyField(Owner)
    | viewers: ManyToManyField(Viewer)

    .. note::
        ContentGroup is one class with semester-long
        It contains daily lecure(Content class).
    """
    name = models.CharField(max_length=999)
    owners = models.ManyToManyField(Owner, related_name='content_groups')
    viewers = models.ManyToManyField(Viewer, related_name='content_groups')


class Content(models.Model):
    """
    | group: ForeignKey(ContentGroup)
    | Contentname: <Char>
    | invited_viewers: <Viewer>
    | public: <BOOL>
    | duration: <Integer>

    .. note::
        Daily lecture contains different sessions
    """
    group = models.ForeignKey(ContentGroup, related_name='content')
    name = models.CharField(max_length=999)
    invited_viewers = models.ManyToManyField(Viewer, related_name='invited_content')
    public = models.BooleanField(default=False)
    duration = models.IntegerField()


class VideoContent(Content):
    video_url = models.CharField(max_length=999)


class VideoSeries(models.Model):
    group = models.ForeignKey(ContentGroup, related_name='video_series')
    name = models.CharField(max_length=999)
    content = models.CharField(max_length=9999)


class Session(models.Model):
    """
    | content: ForeignKey(Content)
    | viewers: ManyToManyField(Viewer)
    | name: <Char>
    | start_time: DateTimeField()
    | end_time: DateTimeField()
    | content_start_sec: <Integer>
    | content_end_sec: <Integer>

    .. note::
           Basic unit contains start_time and end_time of the session
    """
    content = models.ForeignKey(Content, related_name='sessions')
    viewers = models.ManyToManyField(Viewer, related_name='sessions')
    name = models.CharField(max_length=999)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    content_start_sec = models.IntegerField()
    content_end_sec = models.IntegerField()


class SessionTag(models.Model):
    session = models.ForeignKey(Session, related_name='session_tags', null=True)
    time = models.DateTimeField()
    data = models.CharField(max_length=999)


class Tag(models.Model):
    """
    | subject: ForeignKey(Viewer)
    | start_time: DateTimeField()
    | end_time: DateTimeField()
    | labels: Label[]

    .. note::
        Tag represents a reference to a segment of EEG data.
        It contains a number of possible labels of the mental states of the subject.
    """
    subject = models.ForeignKey(Viewer, related_name='confusion_data')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def get_session(self):
        sessions = Session.objects.filter(start_time__lt=self.end_time,
                                          end_time__gt=self.start_time,
                                          viewers=self.subject)
        max_overlap, best_session = 0, None
        for s in sessions:
            overlap = time_overlap([s.start_time, s.end_time],
                                   [self.start_time, self.end_time])
            if overlap > max_overlap:
                best_session = s
                max_overlap = overlap
        return best_session


class LabelType(models.Model):
    """
    | name: <Char>
    | labels: Label[]
    """
    name = models.CharField(max_length=999)


class Label(models.Model):
    """
    | label_type: <Char>
    | true: <Integer>
    | predicted: <Integer>

    .. note::
        Label labels a tag with mental states
        (true) represents the true label of the mental state as tagged by humans
        (predicted) represents the label given by a machine learning algorithm
    """
    tag = models.ForeignKey(Tag, related_name='labels')
    label_type = models.ForeignKey(LabelType, related_name='labels')
    true = models.IntegerField()
    predicted = models.IntegerField()


class SurveyAnswer(models.Model):
    subject = models.ForeignKey(Viewer, related_name='survey_answers')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    question = models.CharField(max_length=999)
    answer = models.CharField(max_length=999)


class ContentLabel(models.Model):
    label_type = models.ForeignKey(LabelType, related_name='content_labels')
    value = models.IntegerField()
    content = models.ForeignKey(Content, related_name='labels')


class Raw(models.Model):
    """
    | subject: ForeignKey(Viewer)
    | start_time: DateTimeField()
    | end_time: DateTimeField()
    | rawwave: <Char>
    """
    subject = models.ForeignKey(Viewer, related_name='raw_data')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    sensor = models.CharField(max_length=99)
    attention = models.CharField(max_length=10)
    sigqual = models.CharField(max_length=10)
    rawwave = models.CharField(max_length=4000)
