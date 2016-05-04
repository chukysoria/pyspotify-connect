from __future__ import unicode_literals

import weakref

import spotifyconnect
from spotifyconnect import ffi, lib, serialized, utils


__all__ = [
    'Connection',
    'ConnectionEvent',
    'DebugEvent',
    'ConnectionState'
]


class Connection(utils.EventEmitter):

    """Connection controller.

    You'll never need to create an instance of this class yourself. You'll find
    it ready to use as the :attr:`~Session.connection` attribute on the
    :class:`Session` instance.
    """

    @serialized
    def __init__(self, session):
        super(Connection, self).__init__()

        self._connectionStatus = ConnectionState.LoggedOut
        spotifyconnect._connection_instance = self

        self._cache = weakref.WeakValueDictionary()
        self._emitters = []
        self._callback_handles = set()

        spotifyconnect.Error.maybe_raise(
            lib.SpRegisterConnectionCallbacks(
                _ConnectionCallbacks.get_struct(), session))
        spotifyconnect.Error.maybe_raise(
            lib.SpRegisterDebugCallbacks(
                _DebugCallbacks.get_struct(), session))

    @property
    @serialized
    def connection_state(self):
        """The session's current :class:`ConnectionState`.

        The mapping is as follows

        - :attr:`~ConnectionState.LoggedIn`: authenticated, online
        - :attr:`~ConnectionState.LoggedOut`: not authenticated
        - :attr:`~ConnectionState.TemporaryError`: Unknown error

        Register listeners for the
        :attr:`spotify.SessionEvent.CONNECTION_STATE_UPDATED` event to be
        notified when the connection state changes.
        """
        return ConnectionState(not lib.SpConnectionIsLoggedIn())

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
    def login(self, username, password=None, blob=None, zeroconf=None):
        """Authenticate to Spotify's servers.

        You can login with one of three combinations:

        - ``username`` and ``password``
        - ``username`` and ``blob``
        - ``username`` and ``zeroconf``

        To get the ``blob`` string, you must once log in with ``username`` and
        ``password``. You'll then get the ``blob`` string passed to the
        :attr:`~ConnectionCallbacks.new_credentials` callback.
        """

        username = utils.to_char(username)

        if password is not None:
            password = utils.to_char(password)
            spotifyconnect.Error.maybe_raise(
                lib.SpConnectionLoginPassword(
                    username, password))
        elif blob is not None:
            blob = utils.to_char(blob)
            spotifyconnect.Error.maybe_raise(
                lib.SpConnectionLoginBlob(username, blob))
        elif zeroconf is not None:
            spotifyconnect.Error.maybe_raise(
                lib.SpConnectionLoginZeroConf(
                    username, *zeroconf))
        else:
            raise AttributeError(
                "Must specify a login method (password, blob or zeroconf)")

    @serialized
    def logout(self):
        """Log out the current user.
        """
        spotifyconnect.Error.maybe_raise(lib.SpConnectionLogout())


class ConnectionEvent(object):

    """Connection events.
    """

    CONNECTION_NOTIFY_UPDATED = 'connection_notify'
    NEW_CREDENTIALS = 'connection_new_credentials'
    ERROR_NOTIFICATION = 'error_notification'


class DebugEvent(object):

    """Connection events.
    """

    DEBUG_MESSAGE = 'debug_message'


class _ConnectionCallbacks(object):

    """Internal class."""

    @classmethod
    def get_struct(cls):
        return ffi.new('SpConnectionCallbacks *', {
            'notify': cls.connection_notify,
            'new_credentials': cls.connection_new_credentials
        })

    # XXX Avoid use of the spotify._session_instance global in the following
    # callbacks.

    @staticmethod
    @ffi.callback('void(SpConnectionNotify type, void *userdata)')
    def connection_notify(sp_connection_notify, sp_userdata):
        if not spotifyconnect._session_instance:
            return
        connection_notify = ConnectionState(sp_connection_notify)
        spotifyconnect._session_instance.connection.emit(
            ConnectionEvent.CONNECTION_NOTIFY_UPDATED,
            connection_notify, ffi.from_handle(sp_userdata))

    @staticmethod
    @ffi.callback('void(char *blob, void *userdata)')
    def connection_new_credentials(sp_blob, sp_userdata):
        if not spotifyconnect._session_instance:
            return
        blob = utils.to_unicode(sp_blob)
        spotifyconnect._session_instance.connection.emit(
            ConnectionEvent.NEW_CREDENTIALS,
            blob,
            ffi.from_handle(sp_userdata))


class _DebugCallbacks(object):

    """Internal class."""

    @classmethod
    def get_struct(cls):
        return ffi.new('SpDebugCallbacks *', {
            'message': cls.debug_message
        })

    # XXX Avoid use of the spotify._session_instance global in the following
    # callbacks.

    @staticmethod
    @ffi.callback('void(char *msg, void *userdata)')
    def debug_message(sp_message, sp_userdata):
        if not spotifyconnect._session_instance:
            return
        message = utils.to_unicode(sp_message)
        spotifyconnect._session_instance.connection.emit(
            DebugEvent.DEBUG_MESSAGE,
            message, ffi.from_handle(sp_userdata))


@utils.make_enum('kSpConnectionNotify')
class ConnectionState(utils.IntEnum):
    pass

# Error callbacks


@ffi.callback('void(SpError error, void *userdata)')
def error_callback(error, sp_userdata):
    spotifyconnect._session_instance.connection.emit(
        ConnectionEvent.ERROR_NOTIFICATION,
        spotifyconnect.ErrorType(error),
        ffi.from_handle(sp_userdata))
