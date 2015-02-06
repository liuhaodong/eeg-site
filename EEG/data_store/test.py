from django.test import TestCase
from EEG.debug.utils import fill_db
from EEG.data_store.aggregator import get_label_sequence


class TestGetConfusionData(TestCase):

    def test_direct_input(self):
        fill_db()
        sequences = get_label_sequence("software_management",
                                       "lecture 1",
                                       ["confusion"],
                                       [(1, 2), (2, 3), (11, 12)])
        confusions = sequences["confusion"]
        self.assertEqual(confusions, [(0, 0), (1, 0), (2, 1)])

    '''
    def test_with_limits(self):
        fill_db()
        sequences = get_label_sequence("software_management",
                                       "lecture 1",
                                       ["confusion"],
                                       [(1, 2), (2, 3), (11, 12)],
                                       ['bic1', 'alice'])
        confusions = sequences["confusion"]
        self.assertEqual(confusions, [(0, 0), (1, 0), (2, 1)])
    '''
