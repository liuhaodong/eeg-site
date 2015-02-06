from django.test import TestCase
from django.core.urlresolvers import reverse
from EEG.data_store.models import ContentGroup, Session, Raw, Label
from EEG.debug.utils import fill_db
import json


class CourseListTest(TestCase):

    def test_basic(self):
        fill_db()
        url = reverse("EEG.API.views.course_list")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, "software_management,bic_capstone")

    def test_owner(self):
        fill_db()
        url = reverse("EEG.API.views.course_list")
        resp = self.client.get(url, {'owner': 'prof'})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, "software_management,bic_capstone")


class InputTest(TestCase):

    def test_basic(self):
        fill_db()
        url = reverse("EEG.API.views.input")

        # TODO: figure out time zone of source
        # confusionTask
        resp = self.client.post(url,
                                {'course': 'software_management',
                                'student': 'alice',
                                'label_names': '["confusion"]',
                                'label_values': '[1]',
                                'start_time': '2018-01-01 06:00:00',
                                'end_time': '2018-01-01 06:00:10'})
        self.assertEqual(resp.status_code, 200)
        course = ContentGroup.objects.filter(name='software_management').get()
        lecture = Session.objects.filter(content__name='lecture 2', content__group=course).get()
        confs = Label.objects.filter(tag__start_time__lte=lecture.end_time,
                                     tag__end_time__gt=lecture.start_time,
                                     label_type__name="confusion")
        self.assertEqual(len(confs), 1)
        self.assertEqual(confs[0].true, 1)
        self.assertEqual(confs[0].tag.subject.user.username, 'alice')

        # raw/attention
        resp = self.client.post(url,
                                {'course': 'software_management',
                                'student': 'alice',
                                'attention': 1,
                                'raw': '1 2 3 4 5',
                                'start_time': '2018-01-01 06:00:00',
                                'end_time': '2018-01-01 06:00:10'})
        self.assertEqual(resp.status_code, 200)
        raws = Raw.objects.filter(start_time__lte=lecture.end_time,
                                  end_time__gt=lecture.start_time)
        self.assertEqual(len(raws), 1)
        self.assertEqual(raws[0].rawwave, '1 2 3 4 5')


class GetNextLectureTest(TestCase):

    def test_basic(self):
        fill_db()
        url = reverse("EEG.API.views.get_next_lecture", args=['software_management'])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(resp.content), 10)  # TODO: properly check date


class GetLabelSequenceTest(TestCase):

    def test_basic(self):
        fill_db()
        url = reverse("EEG.API.views.get_label_sequence")
        resp = self.client.get(url,
                               {"content_group_name": "software_management",
                               "content_name": "lecture 1",
                               "label_type_names": '["confusion"]',
                               "subsections": "[[0, 1], [1, 2], [11, 12]]"})
        self.assertEqual(resp.status_code, 200)
        obj = json.loads(resp.content)
        self.assertEqual(obj['confusion'], [[0, 0], [1, 0], [2, 1]])
