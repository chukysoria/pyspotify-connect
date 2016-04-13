from __future__ import unicode_literals

import unittest

import spotifyconnect
from tests import mock


class BaseSinkTest(object):

    def test_init_connects_to_music_delivery_event(self):
        self.session.player.on.assert_called_with(
            spotify.PlayerEvent.MUSIC_DELIVERY, self.sink._on_music_delivery)

    def test_off_disconnects_from_music_delivery_event(self):
        self.assertEqual(self.session.player.off.call_count, 0)

        self.sink.off()

        self.session.player.off.assert_called_with(
            spotify.PlayerEvent.MUSIC_DELIVERY, mock.ANY)

    def test_on_connects_to_music_delivery_event(self):
        self.assertEqual(self.session.player.on.call_count, 1)

        self.sink.off()
        self.sink.on()

        self.assertEqual(self.session.player.on.call_count, 2)