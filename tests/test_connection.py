from __future__ import unicode_literals

import unittest

import spotifyconnect
from spotifyconnect.connection import _ConnectionCallbacks, _DebugCallbacks, error_callback

import tests
from tests import mock


@mock.patch('spotifyconnect.connection.lib', spec=spotifyconnect.lib)
class ConnectionTest(unittest.TestCase):

    def tearDown(self):
        spotifyconnect._session_instance = None

    def test_connection_state(self, lib_mock):
        lib_mock.SpConnectionIsLoggedIn.return_value = True
        session = tests.create_real_connection(lib_mock)

        result = session.connection.connection_state

        lib_mock.SpConnectionIsLoggedIn.assert_called_once_with()
        self.assertEqual(result, spotifyconnect.ConnectionState.LoggedIn)

    def test_login(self, lib_mock):
        lib_mock.SpConnectionLoginPassword.return_value = spotifyconnect.ErrorType.Ok
        session = tests.create_real_connection(lib_mock)

        session.connection.login(username='foo', password='bar')

        lib_mock.SpConnectionLoginPassword.assert_called_once_with(mock.ANY, mock.ANY)
        self.assertEqual(
            spotifyconnect.ffi.string(lib_mock.SpConnectionLoginPassword.call_args[0][0]),
            b'foo')
        self.assertEqual(
            lib_mock.SpConnectionLoginPassword.call_args[0][1],
            'bar')

    def test_login_fails_with_assert(self, lib_mock):
        lib_mock.SpConnectionLoginPassword.return_value = spotifyconnect.ErrorType.WrongAPIVersion
        session = tests.create_real_connection(lib_mock)

        with self.assertRaises(spotifyconnect.Error):
            session.connection.login(username='foo', password='bar')

    def test_login_blob(self, lib_mock):
        lib_mock.SpConnectionLoginBlob.return_value = spotifyconnect.ErrorType.Ok
        session = tests.create_real_connection(lib_mock)

        session.connection.login(username='foo', blob='bar')

        lib_mock.SpConnectionLoginBlob.assert_called_once_with(mock.ANY, mock.ANY)
        self.assertEqual(
            spotifyconnect.ffi.string(lib_mock.SpConnectionLoginBlob.call_args[0][0]),
            b'foo')
        self.assertEqual(
            lib_mock.SpConnectionLoginBlob.call_args[0][1],
            'bar')

    def test_login_blob_fails_with_assert(self, lib_mock):
        lib_mock.SpConnectionLoginBlob.return_value = spotifyconnect.ErrorType.WrongAPIVersion
        session = tests.create_real_connection(lib_mock)

        with self.assertRaises(spotifyconnect.Error):
            session.connection.login(username='foo', blob='bar')

    def test_login_zeroconf(self, lib_mock):
        lib_mock.SpConnectionLoginZeroConf.return_value = spotifyconnect.ErrorType.Ok
        session = tests.create_real_connection(lib_mock)

        session.connection.login(username='foo', zeroconf=('bar', 'bar2'))

        lib_mock.SpConnectionLoginZeroConf.assert_called_once_with(mock.ANY, 'bar', 'bar2')
        self.assertEqual(
            spotifyconnect.ffi.string(lib_mock.SpConnectionLoginZeroConf.call_args[0][0]),
            b'foo')

    def test_login_zeroconf_fails_with_assert(self, lib_mock):
        lib_mock.SpConnectionLoginZeroConf.return_value = spotifyconnect.ErrorType.WrongAPIVersion
        session = tests.create_real_connection(lib_mock)

        with self.assertRaises(spotifyconnect.Error):
            session.connection.login(username='foo', zeroconf='bar')            
    
    def test_login_empty_fails_with_assert(self, lib_mock):
        session = tests.create_real_connection(lib_mock)

        with self.assertRaises(AttributeError):
            session.connection.login(username='foo')
    
    def test_logout(self, lib_mock):
        lib_mock.SpConnectionLogout.return_value = spotifyconnect.ErrorType.Ok
        session = tests.create_real_connection(lib_mock)
        
        session.connection.logout()
        
        lib_mock.SpConnectionLogout.assert_called_once_with()
        
    def test_logout_fails_with_assert(self, lib_mock):
        lib_mock.SpConnectionLogout.return_value = spotifyconnect.ErrorType.WrongAPIVersion
        session = tests.create_real_connection(lib_mock)
        
        with self.assertRaises(spotifyconnect.Error):
            session.connection.logout()     

@mock.patch('spotifyconnect.connection.lib', spec=spotifyconnect.lib)
class ConnectionCallbacksTest(unittest.TestCase):

    def tearDown(self):
        spotifyconnect._session_instance = None

    def test_connection_new_credentials_callback(self, lib_mock):
        callback = mock.Mock()
        session = tests.create_real_connection(lib_mock)
        session_handle = spotifyconnect.ffi.new_handle(session)
        session.connection.on(spotifyconnect.ConnectionEvent.NEW_CREDENTIALS, callback)
        data = spotifyconnect.ffi.new('char[]', b'a credentials blob')

        _ConnectionCallbacks.connection_new_credentials(
            data, session_handle)

        callback.assert_called_once_with('a credentials blob', session)

    def test_connection_callbacks_not_called_if_not_session(self, lib_mock):
        callback = mock.Mock()
        session = tests.create_real_connection(lib_mock)
        spotifyconnect._session_instance = None
        session_handle = spotifyconnect.ffi.new_handle(session)
        
        session.connection.on(spotifyconnect.ConnectionEvent.NEW_CREDENTIALS, callback)
        session.connection.on(spotifyconnect.ConnectionEvent.CONNECTION_NOTIFY_UPDATED, callback)
        
        data = spotifyconnect.ffi.new('char[]', b'a credentials blob')
        status = spotifyconnect.ConnectionState.LoggedOut

        _ConnectionCallbacks.connection_new_credentials(data, session_handle)
        _ConnectionCallbacks.connection_notify(status, session_handle)

        self.assertFalse(callback.called)

    def test_connection_state_updated_callback(self, lib_mock):
        callback = mock.Mock()
        session = tests.create_real_connection(lib_mock)
        session_handle = spotifyconnect.ffi.new_handle(session)
        status = spotifyconnect.ConnectionState.LoggedOut
        session.connection.on(spotifyconnect.ConnectionEvent.CONNECTION_NOTIFY_UPDATED, callback)

        _ConnectionCallbacks.connection_notify(status, session_handle)

        callback.assert_called_once_with(status, session)

    def test_error_callback(self, lib_mock):
        callback = mock.Mock()
        session = tests.create_real_connection(lib_mock)
        session_handle = spotifyconnect.ffi.new_handle(session)
        error = spotifyconnect.ErrorType.WrongAPIVersion
        session.connection.on(spotifyconnect.ConnectionEvent.ERROR_NOTIFICATION, callback)

        error_callback(error, session_handle)

        callback.assert_called_once_with(error, session)        
    
@mock.patch('spotifyconnect.connection.lib', spec=spotifyconnect.lib)
class DebugCallbacksTest(unittest.TestCase):

    def tearDown(self):
        spotifyconnect._session_instance = None

    def test_debug_message_callback(self, lib_mock):
        callback = mock.Mock()
        session = tests.create_real_connection(lib_mock)
        spotifyconnect._session_instance = None
        session_handle = spotifyconnect.ffi.new_handle(session)
        session.connection.on(spotifyconnect.DebugEvent.DEBUG_MESSAGE, callback)
        data = spotifyconnect.ffi.new('char[]', b'a debug message')

        _DebugCallbacks.debug_message(data, session_handle)

        self.assertFalse(callback.called)

    def test_debug_message_callback_not_called_if_not_session(self, lib_mock):
        callback = mock.Mock()
        session = tests.create_real_connection(lib_mock)
        session_handle = spotifyconnect.ffi.new_handle(session)
        session.connection.on(spotifyconnect.DebugEvent.DEBUG_MESSAGE, callback)
        data = spotifyconnect.ffi.new('char[]', b'a debug message')

        _DebugCallbacks.debug_message(data, session_handle)

        callback.assert_called_once_with('a debug message', session)
        
class ConnectionStateTest(unittest.TestCase):

    def test_contains_values(self):
        self.assertEqual(spotifyconnect.ConnectionState.LoggedIn, 0)
        self.assertEqual(spotifyconnect.ConnectionState.LoggedOut, 1)
        self.assertEqual(spotifyconnect.ConnectionState.TemporaryError, 2)
