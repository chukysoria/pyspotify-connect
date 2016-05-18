from __future__ import unicode_literals

import collections

from spotifyconnect import utils


__all__ = [
    'AudioBufferStats',
    'AudioFormat',
    'Bitrate',
    'SampleType',
]


class AudioBufferStats(collections.namedtuple(
        'AudioBufferStats', ['samples', 'stutter'])):

    """Stats about the application's alsa_sink buffers."""
    pass


@utils.make_enum('kSpBitrate', 'BITRATE_')
class Bitrate(utils.IntEnum):
    pass


@utils.make_enum('kSpSampleType')
class SampleType(utils.IntEnum):
    pass


class AudioFormat(object):

    """A Spotify alsa_sink format object.

    You'll never need to create an instance of this class yourself, but you'll
    get :class:`AudioFormat` objects as the ``audio_format`` argument to the
    :attr:`~spotifyconnect.PlayerCallbacks.MUSIC_DELIVERY` callback.
    """

    def __init__(self, sp_audioformat):
        self._sp_audioformat = sp_audioformat

    @property
    def sample_type(self):
        """The :class:`SampleType`, currently always
        :attr:`SampleType.S16NativeEndian`."""
        return SampleType(self._sp_audioformat.sample_type)

    @property
    def sample_rate(self):
        """The sample rate, typically 44100 Hz."""
        return self._sp_audioformat.sample_rate

    @property
    def channels(self):
        """The number of audio channels, typically 2."""
        return self._sp_audioformat.channels

    @property
    def frame_size(self):
        """The byte size of a single frame of this format."""
        if self.sample_type == SampleType.S16NativeEndian:
            # Sample size is 2 bytes
            return self.sample_size * self.channels
        else:
            raise ValueError('Unknown sample type: %d', self.sample_type)

    @property
    def sample_size(self):
        """The byte size of a single frame of this format."""
        if self.sample_type == SampleType.S16NativeEndian:
            # Sample size is 2 bytes
            return 2
        else:
            raise ValueError('Unknown sample type: %d', self.sample_type)
