from django.test import TestCase
from django.core.urlresolvers import reverse
from EEG.data_store.models import VideoContent
from EEG.debug.utils import fill_db


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


class AddCourseTest(TestCase):

    def test_get_form(self):
        fill_db()
        url = reverse("EEG.prof.views.add_course")
        self.client.login(username='prof', password='essor')
        resp = self.client.get(url, {'lecture': 'lecture 2'})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['lectureall']), 0)
        self.assertEqual(resp.context['courseall'][0].name, 'software_management')
        self.assertEqual(resp.context['courseall'][1].name, 'bic_capstone')
        self.assertEqual(len(resp.context['courseall']), 2)

    def test_good_input(self):
        fill_db()
        url = reverse("EEG.prof.views.add_course")
        self.client.login(username='prof', password='essor')
        resp = self.client.post(url, {'content_group_name': 'rocket_science',
                                      'students': ''})
        self.assertRedirects(resp, '/EEG/add_lecture/rocket_science')


class AddLectureTest(TestCase):

    def test_get_form(self):
        fill_db()
        url = reverse("EEG.prof.views.add_lecture", args=['software_management'])
        self.client.login(username='prof', password='essor')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertIsNone(resp.context['current_lecture'])
        self.assertEqual(resp.context['lectureall'][0].name, 'lecture 1')
        self.assertEqual(resp.context['lectureall'][1].name, 'lecture 2')
        self.assertEqual(len(resp.context['lectureall']), 2)
        self.assertEqual(resp.context['courseall'][0].name, 'software_management')
        self.assertEqual(resp.context['courseall'][1].name, 'bic_capstone')
        self.assertEqual(len(resp.context['courseall']), 2)
        self.assertEqual(resp.context['current_course'].name, 'software_management')

    def test_good_input(self):
        fill_db()
        url = reverse("EEG.prof.views.add_lecture", args=['software_management'])
        self.client.login(username='prof', password='essor')
        resp = self.client.post(url, {'name': 'lecture 0',
                                      'start_date': '2020-01-01 00:00:00',
                                      'end_date': '2020-01-01 01:00:00'})

        expected_start = 'http://testserver/EEG/course/software_management?'
        self.assertEqual(resp['location'][:len(expected_start)], expected_start)

        # check whether lecture was added
        resp2 = self.client.get(resp['location'])
        self.assertEqual(len(resp2.context['lectureall']), 3)
        self.assertEqual(resp2.context['current_lecture'].name, 'lecture 0')


class AddVideoLectureTest(TestCase):

    def test_get_form(self):
        fill_db()
        url = reverse("EEG.prof.views.add_video_lecture", args=['software_management'])
        self.client.login(username='prof', password='essor')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertIsNone(resp.context['current_lecture'])
        self.assertEqual(resp.context['lectureall'][0].name, 'lecture 1')
        self.assertEqual(resp.context['lectureall'][1].name, 'lecture 2')
        self.assertEqual(len(resp.context['lectureall']), 2)
        self.assertEqual(resp.context['courseall'][0].name, 'software_management')
        self.assertEqual(resp.context['courseall'][1].name, 'bic_capstone')
        self.assertEqual(len(resp.context['courseall']), 2)
        self.assertEqual(resp.context['current_course'].name, 'software_management')

    def test_good_input(self):
        fill_db()
        url = reverse("EEG.prof.views.add_video_lecture", args=['software_management'])
        self.client.login(username='prof', password='essor')
        video_url = 'https://www.youtube.com/watch?v=ACjLuMvbAnM'
        resp = self.client.post(url, {'name': 'lecture 0',
                                      'url': video_url})

        expected_start = 'http://testserver/EEG/course/software_management?'
        self.assertEqual(resp['location'][:len(expected_start)], expected_start)

        # check whether lecture was added
        resp2 = self.client.get(resp['location'])
        self.assertEqual(len(resp2.context['lectureall']), 3)
        self.assertEqual(resp2.context['current_lecture'].name, 'lecture 0')
        self.assertEqual(len(VideoContent.objects.filter(video_url=video_url)), 1)
