# encoding: utf-8

from unittest import TestCase

from ebspod_client import get_title
import re

class EbsPodClientTest(TestCase):
    def test_get_title(self):
        title = "한글"
        actual_titles = get_title(title).split(" - ")
        self.assertEqual(unicode(title, 'utf-8'), actual_titles[0])
        self.assertTrue(re.match("^[0-9]{4}/[0-9]{2}/[0-9]{2}$", actual_titles[1]))