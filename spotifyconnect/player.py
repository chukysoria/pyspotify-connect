from __future__ import division, unicode_literals

import weakref

import spotifyconnect
from spotifyconnect import ffi, lib, serialized, utils


__all__ = [
    'Player',
    'PlayerEvent',
    'PlaybackNotify'
]


class Player(utils.EventEmitter):

    """Playback controller.

    You'll never need to create an instance of this class yourself. You'll find
    it ready to use as the :attr:`~Session.player` attribute on the
    :class:`Session` instance.
    """
    @serialized
    def __init__(self, session):
        super(Player, self).__init__()

        spotifyconnect._player_instance = self

        self._cache = weakref.WeakValueDictionary()
        self._emitters = []
        self._callback_handles = set()

        spotifyconnect.Error.maybe_raise(
            lib.SpRegisterPlaybackCallbacks(
                _PlayerCallbacks.get_struct(), session))

    _cache = None
    """A mapping from sp_* objects to their corresponding Python instances.

    The ``_cached`` helper constructors on wrapper objects use this cache for
    finding and returning existing alive wrapper objects for the sp_* object it
    is about to create a wrapper for.

    The cache *does not* keep objects alive. It's only a means for looking up
    the objects if they are kept alive somewhere else in the application.

    Internal attribute.
    """

    _emitters = None
    """A list of event emitters with attached listeners.

    When an event emitter has attached event listeners, we must keep the
    emitter alive for as long as the listeners are attached. This is achieved
    by adding them to this list.

    When creating wrapper objects around sp_* objects we must also return the
    existing wrapper objects instead of creating new ones so that the set of
    event listeners on the wrapper object can be modified. This is achieved
    with a combination of this list and the :attr:`_cache` mapping.

    Internal attribute.
    """

    _callback_handles = None
    """A set of handles returned by :meth:`spotify.ffi.new_handle`.

    These must be kept alive for the handle to remain valid until the callback
    arrives, even if the end user does not maintain a reference to the object
    the callback works on.

    Internal attribute.
    """

    @serialized
    def play(self):
        """Play the currently loaded track.

        This will cause alsa_sink data to be passed to the
        :attr:`~SessionCallbacks.music_delivery` callback.
        """
        spotifyconnect.Error.maybe_raise(lib.SpPlaybackPlay())

    @serialized
    def pause(self):
        """Pause the currently loaded track.
        """
        spotifyconnect.Error.maybe_raise(lib.SpPlaybackPause())

    @serialized
    def skip_to_next(self):
        """Skips to the next track on the playlist.
        """
        spotifyconnect.Error.maybe_raise(lib.SpPlaybackSkipToNext())

    @serialized
    def skip_to_prev(self):
        """Skips to the previous track on the playlist.
        """
        spotifyconnect.Error.maybe_raise(lib.SpPlaybackSkipToPrev())

    @serialized
    def seek(self, offset):
        """Seek to the offset in ms in the currently loaded track."""
        spotifyconnect.Error.maybe_raise(lib.SpPlaybackSeek(offset))

    @serialized
    def enable_shuffle(self, value=None):
        """Enable shuffle mode
        """
        if value is None:
            value = not self.shuffled
        spotifyconnect.Error.maybe_raise(lib.SpPlaybackEnableShuffle(value))

    @serialized
    def enable_repeat(self, value=None):
        """Enable repeat mode
        """
        if value is None:
            value = not self.repeated
        spotifyconnect.Error.maybe_raise(lib.SpPlaybackEnableRepeat(value))

    @property
    @serialized
    def playing(self):
        return lib.SpPlaybackIsPlaying()

    @property
    @serialized
    def shuffled(self):
        return lib.SpPlaybackIsShuffled()

    @property
    @serialized
    def repeated(self):
        return lib.SpPlaybackIsRepeated()

    @property
    @serialized
    def active_device(self):
        return lib.SpPlaybackIsActiveDevice()

    @property
    @serialized
    def volume(self):
        value = lib.SpPlaybackGetVolume()
        corrected_value = value / 655.35
        return corrected_value

    @volume.setter
    @serialized
    def volume(self, value):
        corrected_value = int(value * 655.35)
        spotifyconnect.Error.maybe_raise(
            lib.SpPlaybackUpdateVolume(corrected_value))

    @property
    def current_track(self):
        return self.get_track_metadata()

    @property
    @serialized
    def metadata_valid_range(self):
        start = ffi.new("int *")
        end = ffi.new("int *")
        spotifyconnect.Error.maybe_raise(
            lib.SpGetMetadataValidRange(start, end))
        valid_range = {
            'start': start[0],
            'end': end[0]
        }
        return valid_range

    @serialized
    def get_track_metadata(self, offset=0):
        sp_metadata = ffi.new('SpMetadata *')
        spotifyconnect.Error.maybe_raise(
            lib.SpGetMetadata(sp_metadata, offset))
        return spotifyconnect.Metadata(sp_metadata)

    @serialized
    def set_bitrate(self, bitrate):
        spotifyconnect.Error.maybe_raise(lib.SpPlaybackSetBitrate(bitrate))


class PlayerEvent(object):

    """AlsaSink events.
    """
    PLAYBACK_NOTIFY = 'playback_notify'
    MUSIC_DELIVERY = 'playback_data'
    PLAYBACK_SEEK = 'playback_seek'
    PLAYBACK_VOLUME = 'playback_volume'


class _PlayerCallbacks(object):

    """Internal class."""

    @classmethod
    def get_struct(cls):
        return ffi.new('SpPlaybackCallbacks *', {
            'notify': cls.playback_notify,
            'audio_data': cls.playback_data,
            'seek': cls.playback_seek,
            'apply_volume': cls.playback_volume
        })

    # XXX Avoid use of the spotify._session_instance global in the following
    # callbacks.

    @staticmethod
    @ffi.callback('void(SpPlaybackNotify notify, void *userdata)')
    def playback_notify(sp_playback_notify, sp_userdata):
        if not spotifyconnect._session_instance:
            return
        playback_notify = PlaybackNotify(sp_playback_notify)
        spotifyconnect._session_instance.player.emit(
            PlayerEvent.PLAYBACK_NOTIFY,
            playback_notify,
            ffi.from_handle(sp_userdata))

    @staticmethod
    @ffi.callback(
        'uint32_t(void *data, uint32_t num_samples, SpSampleFormat *format, '
        'uint32_t *pending, void *userdata)')
    def playback_data(
            samples,
            num_samples,
            sp_audioformat,
            sp_pending,
            sp_userdata):
        if not spotifyconnect._session_instance:
            return
        if spotifyconnect._session_instance.player.num_listeners(
                PlayerEvent.MUSIC_DELIVERY) == 0:
            return 0

        audio_format = spotifyconnect.AudioFormat(sp_audioformat)

        # Make sure waudio_formate don't pass incomplete frames
        num_samples -= num_samples % audio_format.frame_size

        samples_buffer = ffi.buffer(
            samples, num_samples * audio_format.sample_size)
        samples_bytes = samples_buffer[:]
        num_samples_consumed = spotifyconnect._session_instance.player.call(
            PlayerEvent.MUSIC_DELIVERY,
            audio_format,
            samples_bytes,
            num_samples,
            sp_pending,
            ffi.from_handle(sp_userdata))
        return num_samples_consumed

    @staticmethod
    @ffi.callback('void(uint32_t millis, void *userdata)')
    def playback_seek(sp_millis, sp_userdata):
        if not spotifyconnect._session_instance:
            return
        millis = int(sp_millis)
        spotifyconnect._session_instance.player.emit(
            PlayerEvent.PLAYBACK_SEEK, millis, ffi.from_handle(sp_userdata))

    @staticmethod
    @ffi.callback('void(uint16_t volume, void *userdata)')
    def playback_volume(sp_volume, sp_userdata):
        if not spotifyconnect._session_instance:
            return
        volume = sp_volume / 655.35
        spotifyconnect._session_instance.player.emit(
            PlayerEvent.PLAYBACK_VOLUME, volume, ffi.from_handle(sp_userdata))


@utils.make_enum('kSpPlaybackEvent')
@utils.make_enum('kSpPlaybackNotify')
class PlaybackNotify(utils.IntEnum):
    pass
