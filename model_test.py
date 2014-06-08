# encoding: utf-8

from unittest import TestCase
from model import *


class ModelTest(TestCase):
    def tearDown(self):
        db.delete(ClientKey.all())
        db.delete(Episode.all())
        db.delete(Program.all())


class ClientKeyTest(ModelTest):
    def test_crud(self):
        expected = ClientKey(key_name="key")
        expected.save()

        actual = ClientKey.get(expected.key())
        self.assertEqual(expected.key(), actual.key())


    def test_find_by_client_key(self):
        expected = ClientKey(key_name="key")
        expected.save()

        actual = ClientKey.get_by_key_name(expected.key().name())
        self.assertEqual(expected.key(), actual.key())

        self.assertTrue(None == ClientKey.get_by_key_name("empty"))


class ProgramTest(ModelTest):
    def test_get_or_create_should_create_when_program_not_found(self):
        self.assertEqual(0, Program.all().count())
        Program.get_or_insert("program", title="program")
        self.assertEqual(1, Program.all().count())

    def test_get_or_create_should_return_old_program(self):
        expected = Program(key_name='program', title="program")
        expected.put()
        self.assertEqual(1, Program.all().count())

        actual = Program.get_or_insert("program", title="program")
        self.assertEqual(1, Program.all().count())
        self.assertEqual(expected.key(), actual.key())


class EpisodeTest(ModelTest):
    def test_create(self):
        self.assertEqual(0, Program.all().count())
        self.assertEqual(0, Episode.all().count())
        episode = Episode.create("program", "episode title", "http://~~~")

        self.assertTrue(episode.program != None)
        self.assertEqual(1, Program.all().count())
        self.assertEqual(1, Episode.all().count())
