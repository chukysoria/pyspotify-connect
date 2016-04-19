from __future__ import unicode_literals

import logging

import spotifyconnect
from spotifyconnect import ffi, lib, utils
from spotifyconnect.connection import error_callback


__all__ = [
    'Session'
]

logger = logging.getLogger(__name__)


class Session:

    """The Spotify session.

    If no ``config`` is provided, the default config is used.

    The session object will emit a number of events. See :class:`SessionEvent`
    for a list of all available events and how to connect your own listener
    functions up to get called when the events happens.

    .. warning::

        You can only have one :class:`Session` instance per process. This is a
        libspotify limitation. If you create a second :class:`Session` instance
        in the same process pyspotify-connect will raise a :exc:`RuntimeError`
        with the message "Session has already been initialized".

    :param config: the session config
    :type config: :class:`Config` or :class:`None`
    """

    def __init__(self, config=None):

        if spotifyconnect._session_instance is not None:
            raise RuntimeError('Session has already been initialized')

        userdata = ffi.new_handle(self)
        self._userdata = userdata

        if config is not None:
            self.config = config
        else:
            self.config = spotifyconnect.Config()

        self.config.error_callback = error_callback
        self.config.userdata = userdata

        spotifyconnect.Error.maybe_raise(
            lib.SpInit(self.config.sp_session_config))

        self.connection = spotifyconnect.Connection(userdata)
        self.player = spotifyconnect.Player(userdata)

        spotifyconnect._session_instance = self

    config = None
    """A :class:`Config` instance with the current configuration.

    Once the session has been created, changing the attributes of this object
    will generally have no effect.
    """

    connection = None
    """An :class:`~spotifyconnect.connection.Connection` instance for
    controlling the connection to the Spotify servers."""

    player = None
    """A :class:`~spotifyconnect.connection.Connection` instance for
    controlling playback."""

    _userdata = None
    """A internal variable to store the CData object handler for the
    :class:`~spotifyconnect.session.Session`"""

    def set_remote_name(self, remote_name):
        name = utils.to_char_or_null(remote_name or None)
        spotifyconnect.Error.maybe_raise(lib.SpSetDisplayName(name))

    def get_zeroconf_vars(self):
        zeroconf_vars = ffi.new('SpZeroConfVars *')
        spotifyconnect.Error.maybe_raise(lib.SpZeroConfGetVars(zeroconf_vars))
        zeroconf = spotifyconnect.Zeroconf(zeroconf_vars)
        return zeroconf

    def process_events(self):
        """Process pending events in libspotify.
        This method must be called for most callbacks to be called. Without
        calling this method, you'll only get the callbacks that are called from
        internal libspotify threads. When the
        pyspotify provides an :class:`~spotifyconnect.EventLoop` that you can
        use for processing events when needed.
        """
        spotifyconnect.Error.maybe_raise(lib.SpPumpEvents())

    @property
    def library_version(self):
        version = lib.SpGetLibraryVersion()
        return utils.to_unicode(version)

    def free_session(self):
        lib.SpFree()
        spotifyconnect._session_instance = None
