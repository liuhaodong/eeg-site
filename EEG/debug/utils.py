from EEG.data_store.models import Content, ContentLabel, VideoContent, ContentGroup, Session, VideoSeries, User, Raw, Owner, Viewer, LabelType, Label, Tag
from EEG.utils import timefixer
import datetime


def fill_db(now=None):
    # fill in default params
    if now is None:
        now = timefixer.now()
    # clear the db
    LabelType.objects.all().delete()
    Label.objects.all().delete()
    Tag.objects.all().delete()
    Raw.objects.all().delete()
    User.objects.all().delete()
    ContentGroup.objects.all().delete()
    Content.objects.all().delete()
    VideoContent.objects.all().delete()
    Session.objects.all().delete()

    # create label type
    confusion_label_type = LabelType.objects.create(name='confusion')

    # create prof
    user = User.objects.create(username='prof')
    user.set_password('essor')
    user.save()
    owner = Owner.objects.create(user=user, marketer=False)

    # create students
    viewer_names = ['bic1', 'alice']
    viewers = []
    for name in viewer_names:
        user = User.objects.create(username=name)
        user.set_password('thomas')
        user.save()
        viewer = Viewer.objects.create(user=user)
        viewers.append(viewer)

    # create classes
    content_group_names = ['software_management', 'bic_capstone']
    lecture_length = 60 * 2
    for content_group_name in content_group_names:
        content_group = ContentGroup.objects.create(
            name=content_group_name)
        content_group.owners.add(owner)
        content_group.viewers.add(*viewers)
        content_group.save()
        # create lecture 1
        content1 = Content.objects.create(group=content_group,
                                          duration=lecture_length,
                                          name='lecture 1')
        content1.invited_viewers.add(*viewers)
        content1.save()
        d = now + datetime.timedelta(minutes=1)
        session1 = Session.objects.create(content=content1,
                                          start_time=d,
                                          end_time=d + datetime.timedelta(seconds=lecture_length),
                                          content_start_sec=0,
                                          content_end_sec=lecture_length)
        session1.viewers.add(*viewers)
        session1.save()
        # create lecture 2
        content2 = Content.objects.create(group=content_group,
                                          duration=lecture_length,
                                          name='lecture 2')
        content1.invited_viewers.add(*viewers)
        content2.save()
        start_18 = timefixer.str_to_datetime('2018-01-01 00:00:00')
        end_18 = start_18 + datetime.timedelta(lecture_length)
        session2 = Session.objects.create(content=content2,
                                          start_time=start_18,
                                          end_time=end_18,
                                          content_start_sec=0,
                                          content_end_sec=lecture_length)
        session2.viewers.add(*viewers)
        session2.save()
        # gen data for each student
        for viewer in viewers:
            step = 10  # seconds
            for i, t in enumerate(range(0, 300, step)):
                d = session1.start_time
                start_time = d + datetime.timedelta(seconds=t)
                end_time = start_time + datetime.timedelta(seconds=step)
                confusion = i % 2
                predicted_confusion = 1 - i
                tag = Tag.objects.create(subject=viewer,
                                         start_time=start_time,
                                         end_time=end_time)
                label = Label.objects.create(label_type=confusion_label_type,
                                             tag=tag,
                                             true=confusion,
                                             predicted=predicted_confusion)
                raw_data = Raw.objects.create(subject=viewer,
                                              start_time=start_time,
                                              end_time=end_time,
                                              sensor="center",
                                              rawwave='1 2 3 4 5')


def fill_db_nm(now=None):
    # fill in default params
    if now is None:
        now = timefixer.now()
    # clear the db
    LabelType.objects.all().delete()
    Label.objects.all().delete()
    Tag.objects.all().delete()
    Raw.objects.all().delete()
    User.objects.all().delete()
    ContentGroup.objects.all().delete()
    Content.objects.all().delete()
    VideoContent.objects.all().delete()
    Session.objects.all().delete()

    # create label type
    label_type = {}
    label_type['engagement'] = LabelType.objects.create(name='engagement')
    label_type['happy'] = LabelType.objects.create(name='happy')
    label_type['sad'] = LabelType.objects.create(name='sad')

    # create prof
    user = User.objects.create(username='mark')
    user.set_password('eter')
    user.save()
    owner = Owner.objects.create(user=user, marketer=True)

    # create campaigns
    content_group_names = ['dogs']
    for content_group_name in content_group_names:
        content_group = ContentGroup.objects.create(
            name=content_group_name)
        content_group.owners.add(owner)
        content_group.save()
        # create happy video
        content1 = VideoContent.objects.create(group=content_group,
                                               video_url='https://www.youtube.com/watch?v=I6yNcW2gmhc',
                                               duration=2 * 60,
                                               name='Happy')
        # create sad video
        content2 = VideoContent.objects.create(group=content_group,
                                               video_url='https://www.youtube.com/watch?v=t_9iKAvSybQ',
                                               duration=2 * 60,
                                               name='Sad')

        series = VideoSeries.objects.create(group=content_group,
                                            name='Experiment 1',
                                            content='Happy;Sad')


'''
def fill_db_pilot(now=None):
    # fill in default params
    if now is None:
        now = timefixer.now()
    # clear the db
    LabelType.objects.all().delete()
    Label.objects.all().delete()
    Tag.objects.all().delete()
    Raw.objects.all().delete()
    User.objects.all().delete()
    ContentGroup.objects.all().delete()
    Content.objects.all().delete()
    VideoContent.objects.all().delete()
    Session.objects.all().delete()

    # create label type
    label_type = {}
    engagement_label_type = LabelType.objects.create(name='engagement')
    happy_label_type = LabelType.objects.create(name='happy')
    sad_label_type = LabelType.objects.create(name='sad')

    # create prof
    user = User.objects.create(username='mark')
    user.set_password('eter')
    user.save()
    owner = Owner.objects.create(user=user, marketer=True)

    # create campaigns
    content_group = ContentGroup.objects.create(name='dogs')
    content_group.owners.add(owner)
    content_group.save()
    # create neutral video
    neutral = VideoContent.objects.create(group=content_group,
                                          video_url='http://youtu.be/xNEHFr7z5PI',
                                          duration=1 * 60 + 12,
                                          name='Neutral')
    ContentLabel.objects.create(label_type=happy_label_type,
                                content=neutral,
                                value=0)
    ContentLabel.objects.create(label_type=sad_label_type,
                                content=neutral,
                                value=0)
    # create happy video
    happy = VideoContent.objects.create(group=content_group,
                                        video_url='http://youtu.be/J-pRv6mVCEU',
                                        duration=2 * 60 + 28,
                                        name='Happy')
    ContentLabel.objects.create(label_type=happy_label_type,
                                content=happy,
                                value=1)
    ContentLabel.objects.create(label_type=sad_label_type,
                                content=happy,
                                value=0)
    # create sad video
    sad = VideoContent.objects.create(group=content_group,
                                      video_url='http://youtu.be/aZUBpdUHlyk',
                                      duration=2 * 60 + 17,
                                      name='Sad')
    ContentLabel.objects.create(label_type=happy_label_type,
                                content=sad,
                                value=0)
    ContentLabel.objects.create(label_type=sad_label_type,
                                content=sad,
                                value=1)
    # create rest video
    rest = VideoContent.objects.create(group=content_group,
                                       video_url='http://youtu.be/B3gQaE-43o8',
                                       duration=42,
                                       name='Rest')
    # create pilot video
    VideoContent.objects.create(group=content_group,
                                video_url='http://www.youtube.com/watch?v=443Vy3I0gJs',
                                duration=42,
                                name='Inspire1')
    VideoContent.objects.create(group=content_group,
                                video_url='http://www.youtube.com/watch?v=0hySFt8O11A',
                                duration=42,
                                name='Sad1')
    VideoContent.objects.create(group=content_group,
                                video_url='http://www.youtube.com/watch?v=f_SwD7RveNE',
                                duration=42,
                                name='Annoy1')
    VideoContent.objects.create(group=content_group,
                                video_url='http://www.youtube.com/watch?v=_z5LXyWn3-w',
                                duration=42,
                                name='Excite1')
    VideoContent.objects.create(group=content_group,
                                video_url='http://www.youtube.com/watch?v=QpydugTkt1U',
                                duration=42,
                                name='Inspire2')
    VideoContent.objects.create(group=content_group,
                                video_url='http://www.youtube.com/watch?v=ywfA0EEHioM',
                                duration=42,
                                name='Sad2')
    VideoContent.objects.create(group=content_group,
                                video_url='http://www.youtube.com/watch?v=D1UY7eDRXrs',
                                duration=42,
                                name='Annoy2')
    VideoContent.objects.create(group=content_group,
                                video_url='http://www.youtube.com/watch?v=iXGl_aBwoVk',
                                duration=42,
                                name='Excite2')
    VideoContent.objects.create(group=content_group,
                                video_url='https://www.youtube.com/watch?v=Q3qTl7_JJ6k',
                                duration=42,
                                name='Bad')
    VideoContent.objects.create(group=content_group,
                                video_url='http://www.youtube.com/watch?v=GVxhaBU7sOI',
                                duration=1,
                                name='Short')
    VideoContent.objects.create(group=content_group,
                                video_url='http://www.youtube.com/watch?v=EiC8o7i_ZqE',
                                duration=1,
                                name='Baseball')
    VideoContent.objects.create(group=content_group,
                                video_url='http://www.youtube.com/watch?v=q14ooGPJZBs',
                                duration=1,
                                name='NBA')
    VideoContent.objects.create(group=content_group,
                                video_url='http://www.youtube.com/watch?v=ozRK7VXQl-k',
                                duration=1,
                                name='Cooking')
    # create commercials to test
    up = VideoContent.objects.create(group=content_group,
                                     video_url='https://www.youtube.com/watch?v=F2bk_9T482g',
                                     duration=7 * 60 + 41,
                                     name='Up')
    series = VideoSeries.objects.create(group=content_group,
                                        name='Pilot Experiment',
                                        content='Up')


'''

def fill_db_pilot(now=None):
    # fill in default params
    if now is None:
        now = timefixer.now()
    # clear the db
    LabelType.objects.all().delete()
    Label.objects.all().delete()
    Tag.objects.all().delete()
    Raw.objects.all().delete()
    User.objects.all().delete()
    ContentGroup.objects.all().delete()
    Content.objects.all().delete()
    VideoContent.objects.all().delete()
    Session.objects.all().delete()

    # create label type
    label_type = {}
    engage_label_type = LabelType.objects.create(name='engage')

    # create prof
    user = User.objects.create(username='mark')
    user.set_password('eter')
    user.save()
    owner = Owner.objects.create(user=user, marketer=True)

    # create viewer
    user = User.objects.create(username='viewer')
    user.set_password('default')
    user.save()
    viewer = Viewer.objects.create(user=user)

    # create campaigns
    content_group = ContentGroup.objects.create(name='data_collection')
    content_group.owners.add(owner)
    content_group.save()

    vids = {}

    '''
    vids['TED'] = [[], []]
    vids['TED'][0] = [  # engage
    'http://www.youtube.com/watch?v=t8PtN4y3TH8',
    'http://www.youtube.com/watch?v=5AUVBXWiJ3Y',
    'http://www.youtube.com/watch?v=2xvA2M8jn_U',
    'http://www.youtube.com/watch?v=WZKQoWtS-aI',
    'http://www.youtube.com/watch?v=jZTWTQ4ddOc',
    'http://www.youtube.com/watch?v=MNlqpJQfqCc',
    'http://www.youtube.com/watch?v=z8jCuCXmFbQ',
    'http://www.youtube.com/watch?v=fiZFAiZTL5A',
    'http://www.youtube.com/watch?v=2wigi2nL464',
    'http://www.youtube.com/watch?v=2P__7VUNDH0',
    'http://www.youtube.com/watch?v=DHGabjH0eTM',
    'http://www.youtube.com/watch?v=zNqAFw4rBqs',
    'http://www.youtube.com/watch?v=436bdwzqc20',
    'http://www.youtube.com/watch?v=ykUuTgbCCmg',
    'http://www.youtube.com/watch?v=VvynK3E90jA',
    'http://www.youtube.com/watch?v=3qzR2rQWqzw',
    'http://www.youtube.com/watch?v=OdlaA9xscoA',
    'http://www.youtube.com/watch?v=IqttkRSIlvw',
    'http://www.youtube.com/watch?v=eaNN0yUDsfI',
    'http://www.youtube.com/watch?v=PUIKoBiXZ4U']
    vids['TED'][1] = [  # disengage
    'http://www.youtube.com/watch?v=meiU6TxysCg',
    'http://www.youtube.com/watch?v=LCHtw6WbbnM',
    'http://www.youtube.com/watch?v=zAFcV7zuUDA',
    'http://www.youtube.com/watch?v=CK62I-4cuSY',
    'http://www.youtube.com/watch?v=PmDTtkZlMwM',
    'http://www.youtube.com/watch?v=mKXXc14H6RM',
    'http://www.youtube.com/watch?v=6WQtRI7A064',
    'http://www.youtube.com/watch?v=Y6bbMQXQ180',
    'http://www.youtube.com/watch?v=dQpGwnN3dfc',
    'http://www.youtube.com/watch?v=d0NHOpeczUU',
    'http://www.youtube.com/watch?v=DkGMY63FF3Q',
    'http://www.youtube.com/watch?v=nw52e0dfCaA',
    'http://www.youtube.com/watch?v=OzJbpA8_wl4',
    'http://www.youtube.com/watch?v=SosPuPjf3W4',
    'http://www.youtube.com/watch?v=jb7gspHxZiI',
    'http://www.youtube.com/watch?v=-mha1uuMr6k',
    'http://www.youtube.com/watch?v=NHopJHSlVo4',
    'http://www.youtube.com/watch?v=JNJlhtNpuiU',
    'http://www.youtube.com/watch?v=AeTmPRNmwNk',
    'http://www.youtube.com/watch?v=-KSryJXDpZo']
    vids['SuperPoli'] = [[], []]
    vids['SuperPoli'][0] = [  # engage
    'http://www.youtube.com/watch?v=uQB7QRyF4p4',
    'http://www.youtube.com/watch?v=aoRD1wmvwUc',
    'http://www.youtube.com/watch?v=q33drZUXSzY',
    'http://www.youtube.com/watch?v=tnUEcG4iH34',
    'http://www.youtube.com/watch?v=gKKVQLDYYcw',
    'http://www.youtube.com/watch?v=AMpZ0TGjbWE',
    'http://www.youtube.com/watch?v=SKL254Y_jtc',
    'http://www.youtube.com/watch?v=bwwJvVUGxas',
    'http://www.youtube.com/watch?v=KmpiwU50f5w',
    'http://www.youtube.com/watch?v=KlSn8Isv-3M',
    'http://www.youtube.com/watch?v=ANhmS6QLd5Q',
    'http://www.youtube.com/watch?v=K7L5QByvXOQ',
    'http://www.youtube.com/watch?v=1aDhfTGkLTg',
    'http://www.youtube.com/watch?v=dhQKyg6EyTI',
    'http://www.youtube.com/watch?v=dKMyCKx50kQ',
    'http://www.youtube.com/watch?v=anLqu77uTH0',
    'http://www.youtube.com/watch?v=jr2gdPY-88w',
    'http://www.youtube.com/watch?v=dOMrA-BGuLY',
    'http://www.youtube.com/watch?v=9g9wXBkdWEg',
    'http://www.youtube.com/watch?v=68al-o2XSpE']
    vids['SuperPoli'][1] = [  # disengage
    'http://www.youtube.com/watch?v=FBorRZnqtMo',
    'http://www.youtube.com/watch?v=tdAjGXFJw3s',
    'http://www.youtube.com/watch?v=v31chfx7PeY',
    'http://www.youtube.com/watch?v=7h3GPc_yMCE',
    'http://www.youtube.com/watch?v=EZ3B8WvVjL4',
    'http://www.youtube.com/watch?v=grqp-JQMFuM',
    'http://www.youtube.com/watch?v=v30Dpbvvj8s',
    'http://www.youtube.com/watch?v=fbdd_Fasz0k',
    'http://www.youtube.com/watch?v=UPy7RnHwvmA',
    'http://www.youtube.com/watch?v=Y_zTN4BXvYI',
    'http://www.youtube.com/watch?v=X0wkR9goqJ0',
    'http://www.youtube.com/watch?v=EC9j6Wfdq3o',
    'http://www.youtube.com/watch?v=9l4sUV6uSCo',
    'http://www.youtube.com/watch?v=PoU41UwL5LI',
    'http://www.youtube.com/watch?v=DWc7XCLMKfQ',
    'http://www.youtube.com/watch?v=HQdTgkY321s',
    'http://www.youtube.com/watch?v=j3MpFKGNZZA',
    'http://www.youtube.com/watch?v=dDTBnsqxZ3k',
    'http://www.youtube.com/watch?v=Svbcwx6FZPA']
    '''
    vids['TrailerDrug'] = [[], []]
    vids['TrailerDrug'][0] = [  # engage
    'http://www.youtube.com/watch?v=KYBF3HKzrmE',
    'http://www.youtube.com/watch?v=KVu3gS7iJu4',
    'http://www.youtube.com/watch?v=T6DJcgm3wNY',
    'http://www.youtube.com/watch?v=nCjsWpM9zFU',
    'http://www.youtube.com/watch?v=nbp3Ra3Yp74',
    'http://www.youtube.com/watch?v=GokKUqLcvD8',
    'http://www.youtube.com/watch?v=vIu85WQTPRc',
    'http://www.youtube.com/watch?v=HcwTxRuq-uk',
    'http://www.youtube.com/watch?v=atCfTRMyjGU',
    'http://www.youtube.com/watch?v=g8evyE9TuYk',
    'http://www.youtube.com/watch?v=INmtQXUXez8',
    'http://www.youtube.com/watch?v=F_UxLEqd074',
    'http://www.youtube.com/watch?v=g8FBRATbJoA',
    'http://www.youtube.com/watch?v=7VdONYkKFmQ',
    'http://www.youtube.com/watch?v=NLWsK1ZFunA',
    'http://www.youtube.com/watch?v=siQgD9qOhRs',
    'http://www.youtube.com/watch?v=dUkCaPW8xCM',
    'http://www.youtube.com/watch?v=G0k3kHtyoqc',
    'http://www.youtube.com/watch?v=j1p0_R8ZLB0',
    'http://www.youtube.com/watch?v=cRdxXPV9GNQ']
    vids['TrailerDrug'][1] = [  # disengage
    'http://www.youtube.com/watch?v=P8KAaf45g5U',
    'http://www.youtube.com/watch?v=xN0254u56Mc',
    'http://www.youtube.com/watch?v=ub_a2t0ZfTs',
    'http://www.youtube.com/watch?v=n4X2lbxc5O4',
    'http://www.youtube.com/watch?v=a7nbmjkImHQ',
    'http://www.youtube.com/watch?v=hkBHp1M3_Is',
    'http://www.youtube.com/watch?v=iE7ukc7MV-k',
    'http://www.youtube.com/watch?v=TePVtnXtaPs',
    'http://www.youtube.com/watch?v=bvS0wYB09Ew',
    'http://www.youtube.com/watch?v=90rw7_6cUDE',
    'http://www.youtube.com/watch?v=F-t8HsHNN-k',
    'http://www.youtube.com/watch?v=DC0O5OVnDkY',
    'http://www.youtube.com/watch?v=qSXrTrhx6Us',
    'http://www.youtube.com/watch?v=pBvC_NCkn7I',
    'http://www.youtube.com/watch?v=wdpOIaGnzvA',
    'http://www.youtube.com/watch?v=acwo6OCB9kg',
    'http://www.youtube.com/watch?v=hwBg56bjfMM',
    'http://www.youtube.com/watch?v=yLR2OKesTw0',
    'http://www.youtube.com/watch?v=PaYZn2f8IW8',
    'http://www.youtube.com/watch?v=C7FGtYVQMFc']
    '''
    vids['TrailerSilence'] = [[], []]
    vids['TrailerSilence'][0] = [  # engage
    'http://www.youtube.com/watch?v=KYBF3HKzrmE',
    'http://www.youtube.com/watch?v=KVu3gS7iJu4',
    'http://www.youtube.com/watch?v=T6DJcgm3wNY',
    'http://www.youtube.com/watch?v=nCjsWpM9zFU',
    'http://www.youtube.com/watch?v=nbp3Ra3Yp74',
    'http://www.youtube.com/watch?v=GokKUqLcvD8',
    'http://www.youtube.com/watch?v=vIu85WQTPRc',
    'http://www.youtube.com/watch?v=HcwTxRuq-uk',
    'http://www.youtube.com/watch?v=atCfTRMyjGU',
    'http://www.youtube.com/watch?v=g8evyE9TuYk',
    'http://www.youtube.com/watch?v=INmtQXUXez8',
    'http://www.youtube.com/watch?v=F_UxLEqd074',
    'http://www.youtube.com/watch?v=g8FBRATbJoA',
    'http://www.youtube.com/watch?v=7VdONYkKFmQ',
    'http://www.youtube.com/watch?v=NLWsK1ZFunA',
    'http://www.youtube.com/watch?v=siQgD9qOhRs',
    'http://www.youtube.com/watch?v=dUkCaPW8xCM',
    'http://www.youtube.com/watch?v=G0k3kHtyoqc',
    'http://www.youtube.com/watch?v=j1p0_R8ZLB0',
    'http://www.youtube.com/watch?v=cRdxXPV9GNQ']
    vids['TrailerSilence'][1] = [  # disengage
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8',
    'http://youtu.be/B3gQaE-43o8']
    '''
    for vid_type in vids.keys():
        for i, url in enumerate(vids[vid_type][0]):
            vid = VideoContent.objects.create(group=content_group,
                                            video_url=url,
                                            duration=180,
                                            name=vid_type + '_Engage_' + str(i))
            ContentLabel.objects.create(label_type=engage_label_type,
                                        content=vid,
                                        value=1)
        for i, url in enumerate(vids[vid_type][1]):
            vid = VideoContent.objects.create(group=content_group,
                                            video_url=url,
                                            duration=180,
                                            name=vid_type + '_Disengage_' + str(i))
            ContentLabel.objects.create(label_type=engage_label_type,
                                        content=vid,
                                        value=0)
    VideoContent.objects.create(group=content_group,
                                   video_url='https://www.youtube.com/watch?v=Q2dQy5l072g',
                                   duration=20,
                                   name='Fixation')
    # create rest video
    VideoContent.objects.create(group=content_group,
                               video_url='http://youtu.be/B3gQaE-43o8',
                               duration=42,
                               name='Rest')
    '''
    VideoSeries.objects.create(group=content_group,
                                        name='TED',
                                        content='Rest')
    VideoSeries.objects.create(group=content_group,
                                         name='SuperPoli',
                                         content='Rest')
    '''
    VideoSeries.objects.create(group=content_group,
                                 name='TrailerDrug',
                                 content='Rest')
