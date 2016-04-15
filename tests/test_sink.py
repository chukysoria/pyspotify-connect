from __future__ import unicode_literals

import unittest

import spotifyconnect
from tests import mock
import tests

class MockSink(spotifyconnect.Sink):

    def __init__(self):
        self.on()

class BaseSinkTest(unittest.TestCase):

    def setUp(self):
        self.session = mock.Mock()
        spotifyconnect._session_instance = self.session
        self.session.player.num_listeners.return_value = 0
        self.sink = MockSink()

    def tearDown(self):
        spotifyconnect._session_instance = None

    def test_init_connects_to_music_delivery_event(self):
        self.session.player.on.assert_called_with(
            spotifyconnect.PlayerEvent.MUSIC_DELIVERY, self.sink._on_music_delivery)

    def test_off_disconnects_from_music_delivery_event(self):
        self.assertEqual(self.session.player.off.call_count, 0)

        self.sink.off()

        self.session.player.off.assert_called_with(
            spotifyconnect.PlayerEvent.MUSIC_DELIVERY, mock.ANY)

    def test_on_connects_to_music_delivery_event(self):
        self.assertEqual(self.session.player.on.call_count, 1)

        self.sink.off()
        self.sink.on()

        self.assertEqual(self.session.player.on.call_count, 2)

    def test_raise_error_if_not_implemented(self):

        with self.assertRaises(NotImplementedError):
            self.sink._on_music_delivery(mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY)
