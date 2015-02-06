from django.test import TestCase
from django.core.urlresolvers import reverse
from EEG.data_store.models import VideoContent
from EEG.debug.utils import fill_db_nm


class HomeTest(TestCase):

    def test_smoke(self):
        fill_db_nm()
        url = reverse("EEG.nm.views.home")
        self.client.login(username='mark', password='eter')
        resp = self.client.get(url)

        self.assertRedirects(resp, '/EEG/market/cg/dogs')


class ContentGroupTest(TestCase):

    def test_with_content(self):
        fill_db_nm()
        url = reverse("EEG.nm.views.content_group", args=['dogs'])
        self.client.login(username='mark', password='eter')
        resp = self.client.get(url, {'content': 'Sad'})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['current_lecture'].name, 'Sad')
        self.assertEqual(resp.context['lectureall'][0].name, 'Happy')
        self.assertEqual(resp.context['lectureall'][1].name, 'Sad')
        self.assertEqual(len(resp.context['lectureall']), 2)
        self.assertEqual(resp.context['courseall'][0].name, 'dogs')
        self.assertEqual(len(resp.context['courseall']), 1)
        self.assertEqual(resp.context['current_course'].name, 'dogs')

    def test_without_content(self):
        fill_db_nm()
        url = reverse("EEG.nm.views.content_group", args=['dogs'])
        self.client.login(username='mark', password='eter')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['current_lecture'].name, 'Happy')
        self.assertEqual(resp.context['lectureall'][0].name, 'Happy')
        self.assertEqual(resp.context['lectureall'][1].name, 'Sad')
        self.assertEqual(len(resp.context['lectureall']), 2)
        self.assertEqual(resp.context['courseall'][0].name, 'dogs')
        self.assertEqual(len(resp.context['courseall']), 1)
        self.assertEqual(resp.context['current_course'].name, 'dogs')


class AddCampaignTest(TestCase):

    def test_get_form(self):
        fill_db_nm()
        url = reverse("EEG.nm.views.add_campaign")
        self.client.login(username='mark', password='eter')
        resp = self.client.get(url, {'content': 'Sad'})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['lectureall']), 0)
        self.assertEqual(resp.context['courseall'][0].name, 'dogs')
        self.assertEqual(len(resp.context['courseall']), 1)

    def test_good_input(self):
        fill_db_nm()
        url = reverse("EEG.nm.views.add_campaign")
        self.client.login(username='mark', password='eter')
        resp = self.client.post(url, {'content_group_name': 'cats'})
        self.assertRedirects(resp, '/EEG/add_video/cats')


class AddVideoTest(TestCase):

    def test_get_form(self):
        fill_db_nm()
        url = reverse("EEG.nm.views.add_video", args=['dogs'])
        self.client.login(username='mark', password='eter')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertIsNone(resp.context['current_lecture'])
        self.assertEqual(resp.context['lectureall'][0].name, 'Happy')
        self.assertEqual(resp.context['lectureall'][1].name, 'Sad')
        self.assertEqual(len(resp.context['lectureall']), 2)
        self.assertEqual(resp.context['courseall'][0].name, 'dogs')
        self.assertEqual(len(resp.context['courseall']), 1)
        self.assertEqual(resp.context['current_course'].name, 'dogs')

    def test_good_input(self):
        fill_db_nm()
        url = reverse("EEG.nm.views.add_video", args=['dogs'])
        self.client.login(username='mark', password='eter')
        video_url = 'https://www.youtube.com/watch?v=ACjLuMvbAnM'
        resp = self.client.post(url, {'name': 'Engaging',
                                      'url': video_url})

        expected_start = 'http://testserver/EEG/market/cg/dogs?'
        self.assertEqual(resp['location'][:len(expected_start)], expected_start)

        # check whether lecture was added
        resp2 = self.client.get(resp['location'])
        self.assertEqual(len(resp2.context['lectureall']), 3)
        self.assertEqual(resp2.context['current_lecture'].name, 'Engaging')
        self.assertEqual(len(VideoContent.objects.filter(video_url=video_url)), 1)
