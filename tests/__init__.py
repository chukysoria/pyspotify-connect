from __future__ import unicode_literals

import gc
import platform
import unittest
import weakref

try:
    # Python 3.3+
    from unittest import mock
except ImportError:
    # From PyPI
    import mock

import spotifyconnect


def buffer_writer(string):
    """Creates a function that takes a ``buffer`` and ``buffer_size`` as the
    two last arguments and writes the given ``string`` to ``buffer``.
    """

    def func(*args):
        assert len(args) >= 2
        buffer_, buffer_size = args[-2:]

        # -1 to keep a char free for \0 terminating the string
        length = min(len(string), buffer_size - 1)

        # Due to Python 3 treating bytes as an array of ints, we have to
        # encode and copy chars one by one.
        for i in range(length):
            buffer_[i] = string[i].encode('utf-8')

        return len(string)

    return func


@mock.patch('spotifyconnect.player.lib', spec=spotifyconnect.lib)
@mock.patch('spotifyconnect.connection.lib', spec=spotifyconnect.lib)
def create_real_session(lib_mock, conn_lib_mock, player_lib_mock):
    """Create a real :class:`spotifyconnect.Session` using ``lib_mock``."""
    lib_mock.SpInit.return_value = spotifyconnect.ErrorType.Ok
    player_lib_mock.SpRegisterPlaybackCallbacks.return_value = spotifyconnect.ErrorType.Ok
    conn_lib_mock.SpRegisterConnectionCallbacks.return_value = spotifyconnect.ErrorType.Ok
    conn_lib_mock.SpRegisterDebugCallbacks.return_value = spotifyconnect.ErrorType.Ok
    config = spotifyconnect.Config()
    config.app_key = b'\x01' * 321
    return spotifyconnect.Session(config=config)


def create_session_mock():
    """Create a :class:`spotifyconnect.Session` mock for testing."""
    session = mock.Mock(spec=spotifyconnect.Session)
    spotifyconnect._session_instance = session
    return session

def create_real_player(lib_mock):
    """Create a :class:`spotifyconnect.Player` mock for testing."""
    lib_mock.SpRegisterPlaybackCallbacks.return_value = spotifyconnect.ErrorType.Ok
    session = create_session_mock()
    session.player = spotifyconnect.Player(session)
    return session

def create_real_connection(lib_mock):
    """Create a :class:`spotifyconnect.Player` mock for testing."""
    lib_mock.SpRegisterConnectionCallbacks.return_value = spotifyconnect.ErrorType.Ok
    lib_mock.SpRegisterDebugCallbacks.return_value = spotifyconnect.ErrorType.Ok
    session = create_session_mock()
    session.connection = spotifyconnect.Connection(session)
    return session

def mock_get_metadata(sp_metadata, offset):    
    metadata = spotifyconnect.ffi.new('SpMetadata *')
    metadata.playlist_name = b'Playlist'
    metadata.playlist_uri = b'Playlist uri'
    metadata.track_name = b'Track'
    metadata.track_uri = b'Track uri'
    metadata.artist_name = b'Artist'
    metadata.artist_uri = b'Artist uri'
    metadata.album_name = b'Album'
    metadata.album_uri = b'Album uri'
    metadata.cover_uri = b'Cover uri'
    metadata.duration = 32541    
    
    spotifyconnect.ffi.buffer(sp_metadata, 1668)[:] = spotifyconnect.ffi.buffer(metadata, 1668)[:]
    
    return spotifyconnect.ErrorType.Ok    

def mock_zeroconf(sp_zeroconf):
    zeroconf = spotifyconnect.ffi.new('SpZeroConfVars *')
    zeroconf.publicKey = b'Public key'
    zeroconf.deviceId = b'Device Id'
    zeroconf.activeUser = b'Active user'
    zeroconf.remoteName = b'Remote name'
    zeroconf.accountReq = b'Premium'
    zeroconf.deviceType = b'Dongle'
    zeroconf.libraryVersion = b'1.2.0'
    spotifyconnect.ffi.buffer(sp_zeroconf, 405)[:] = spotifyconnect.ffi.buffer(zeroconf, 405)[:]
    return spotifyconnect.ErrorType.Ok

def gc_collect():
    """Run enough GC collections to make object finalizers run."""

    # XXX Tests of GC and cleanup behavior are generally flaky and icky,
    # especially when you target all of Python 2.7, 3.3+ and PyPy. Their result
    # quickly depends on other tests, the arguments to the test runner and the
    # computer running the tests. This skips them all for now.
    raise unittest.SkipTest

    if platform.python_implementation() == 'PyPy':
        # Since PyPy use garbage collection instead of reference counting
        # objects are not finalized before the next major GC collection.
        # Currently, the best way we have to ensure a major GC collection has
        # run is to call gc.collect() a number of times.
        [gc.collect() for _ in range(10)]
    else:
        gc.collect()
