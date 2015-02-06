from django.test import TestCase
from django.core.urlresolvers import reverse
from EEG.debug.utils import fill_db
import json


class StartSessionTest(TestCase):

    def test_good_input(self):
        fill_db()
        url = reverse("EEG.student.views.start_session")
        resp = self.client.post(url,
                                {"content_group_name": "software_management",
                                 "content_name": "lecture 1",
                                 "content_time": 0.0,
                                 "viewer_name":'["alice"]'})

        obj = json.loads(resp.content)
        self.assertEqual(obj['ok'], True)
        self.assertEqual(obj['session_name'], "session 1")
        # TODO: test start_time


class StopSessionTest(TestCase):

    def test_good_input(self):
        fill_db()
        # first start a session
        url = reverse("EEG.student.views.start_session")
        resp = self.client.post(url,
                                {"content_group_name": "software_management",
                                 "content_name": "lecture 1",
                                 "content_time": 0.0,
                                 "viewer_name":'["alice"]'})
        obj = json.loads(resp.content)
        session_name = obj['session_name']
        self.assertEqual(session_name, 'session 1')

        # now stop the session
        url = reverse("EEG.student.views.stop_session")
        resp = self.client.post(url,
                                {"content_group_name": "software_management",
                                 "content_name": "lecture 1",
                                 "session_name": session_name,
                                 "content_time": 0.0,
                                 "viewer_name":'["alice"]'})
        obj = json.loads(resp.content)
        self.assertEqual(obj['ok'], True)
        # TODO: test end_time

        # start another one
        url = reverse("EEG.student.views.start_session")
        resp = self.client.post(url,
                                {"content_group_name": "software_management",
                                 "content_name": "lecture 1",
                                 "content_time": 0.0,
                                 "viewer_name":'["alice"]'})
        obj = json.loads(resp.content)
        session_name = obj['session_name']
        self.assertEqual(session_name, 'session 2')
'''

class ProfHomeTest(TestCase):

    def test_smoke(self):
        fill_db()
        url = reverse("EEG.prof.views.profhome")
        self.client.login(username='prof', password='essor')
        resp = self.client.get(url)

        self.assertRedirects(resp, '/EEG/course/software_management')


class CourseTest(TestCase):

    def test_with_lecture(self):
        fill_db()
        url = reverse("EEG.prof.views.course", args=['software_management'])
        self.client.login(username='prof', password='essor')
        resp = self.client.get(url, {'lecture': 'lecture 2'})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['current_lecture'].name, 'lecture 2')
        self.assertEqual(resp.context['lectureall'][0].name, 'lecture 1')
        self.assertEqual(resp.context['lectureall'][1].name, 'lecture 2')
        self.assertEqual(len(resp.context['lectureall']), 2)
        self.assertEqual(resp.context['courseall'][0].name, 'software_management')
        self.assertEqual(resp.context['courseall'][1].name, 'bic_capstone')
        self.assertEqual(len(resp.context['courseall']), 2)
        self.assertEqual(resp.context['current_course'].name, 'software_management')


    def test_without_lecture(self):
        fill_db()
        url = reverse("EEG.prof.views.course", args=['software_management'])
        self.client.login(username='prof', password='essor')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['current_lecture'].name, 'lecture 1')
        self.assertEqual(resp.context['lectureall'][0].name, 'lecture 1')
        self.assertEqual(resp.context['lectureall'][1].name, 'lecture 2')
        self.assertEqual(len(resp.context['lectureall']), 2)
        self.assertEqual(resp.context['courseall'][0].name, 'software_management')
        self.assertEqual(resp.context['courseall'][1].name, 'bic_capstone')
        self.assertEqual(len(resp.context['courseall']), 2)
        self.assertEqual(resp.context['current_course'].name, 'software_management')

'''
