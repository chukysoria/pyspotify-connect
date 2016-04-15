from __future__ import unicode_literals

import unittest

import spotifyconnect


class AudioBufferStatsTest(unittest.TestCase):

    def test_samples(self):
        stats = spotifyconnect.AudioBufferStats(100, 5)

        self.assertEqual(stats.samples, 100)

    def test_stutter(self):
        stats = spotifyconnect.AudioBufferStats(100, 5)

        self.assertEqual(stats.stutter, 5)


class AudioFormatTest(unittest.TestCase):

    def setUp(self):
        self._sp_audioformat = spotifyconnect.ffi.new('SpSampleFormat *')
        self._sp_audioformat.sample_type = (
            spotifyconnect.SampleType.S16NativeEndian)
        self._sp_audioformat.sample_rate = 44100
        self._sp_audioformat.channels = 2
        self.audio_format = spotifyconnect.AudioFormat(self._sp_audioformat)

    def test_sample_type(self):
        self.assertIs(
            self.audio_format.sample_type,
            spotifyconnect.SampleType.S16NativeEndian)

    def test_sample_rate(self):
        self.assertEqual(self.audio_format.sample_rate, 44100)

    def test_channels(self):
        self.assertEqual(self.audio_format.channels, 2)

    def test_frame_size(self):
        # INT16 means 16 bits aka 2 bytes per channel
        self.assertEqual(self.audio_format.frame_size, 2)

    def test_frame_size_fails_if_sample_type_is_unknown(self):
        self._sp_audioformat.sample_type = 666

        with self.assertRaises(ValueError):
            self.audio_format.frame_size()


class BitrateTest(unittest.TestCase):

    def test_has_contants(self):
        self.assertEqual(spotifyconnect.Bitrate.BITRATE_90k, 0)
        self.assertEqual(spotifyconnect.Bitrate.BITRATE_160k, 1)
        self.assertEqual(spotifyconnect.Bitrate.BITRATE_320k, 2)


class SampleTypeTest(unittest.TestCase):

    def test_has_constants(self):
        self.assertEqual(spotifyconnect.SampleType.S16NativeEndian, 0)
