from django.test import TestCase
from django.core.urlresolvers import reverse
from EEG.data_store.models import ContentGroup
from django.contrib.auth.models import User
from EEG.debug.utils import fill_db


class DirectInputTest(TestCase):

    # smoke test
    def test_direct_input(self):
        fill_db()
        url = reverse("EEG.debug.views.directInput")
        resp = self.client.get(url, {'student': 'alice',
                                     'confusion': 1})

        self.assertEqual(resp.status_code, 200)
