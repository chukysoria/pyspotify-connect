from __future__ import unicode_literals

import spotifyconnect

__all__ = [
    'Sink'
]


class Sink(object):

    def on(self):
        """Turn on the alsa_sink sink.

        This is done automatically when the sink is instantiated, so you'll
        only need to call this method if you ever call :meth:`off` and want to
        turn the sink back on.
        """
        assert spotifyconnect._session_instance.player.num_listeners(
            spotifyconnect.PlayerEvent.MUSIC_DELIVERY) == 0
        spotifyconnect._session_instance.player.on(
            spotifyconnect.PlayerEvent.MUSIC_DELIVERY, self._on_music_delivery)

    def off(self):
        """Turn off the alsa_sink sink.

        This disconnects the sink from the relevant session events.
        """
        spotifyconnect._session_instance.player.off(
            spotifyconnect.PlayerEvent.MUSIC_DELIVERY, self._on_music_delivery)
        assert spotifyconnect._session_instance.player.num_listeners(
            spotifyconnect.PlayerEvent.MUSIC_DELIVERY) == 0
        self._close()

    def _on_music_delivery(
            self,
            audio_format,
            frames,
            num_frames,
            pending,
            session):
        # This method is called from an internal libspotify thread and must
        # not block in any way.
        raise NotImplementedError

    def _close(self):
        pass
