# encoding: utf-8

from __future__ import unicode_literals

import unittest

import spotifyconnect

import tests
from tests import mock


@mock.patch('spotifyconnect.session.lib', spec=spotifyconnect.lib)
class SessionTest(unittest.TestCase):

    def tearDown(self):
        spotifyconnect._session_instance = None

    def test_raises_error_if_a_session_already_exists(self, lib_mock):
        tests.create_real_session(lib_mock)

        with self.assertRaises(RuntimeError):
            tests.create_real_session(lib_mock)

    @mock.patch('spotifyconnect.player.lib', spec=spotifyconnect.lib)
    @mock.patch('spotifyconnect.connection.lib', spec=spotifyconnect.lib)
    @mock.patch('spotifyconnect.Config')
    def test_creates_config_if_none_provided(self, config_cls_mock, conn_lib_mock, player_lib_mock, lib_mock):
        lib_mock.SpInit.return_value = spotifyconnect.ErrorType.Ok
        player_lib_mock.SpRegisterPlaybackCallbacks.return_value = spotifyconnect.ErrorType.Ok
        conn_lib_mock.SpRegisterConnectionCallbacks.return_value = spotifyconnect.ErrorType.Ok
        conn_lib_mock.SpRegisterDebugCallbacks.return_value = spotifyconnect.ErrorType.Ok
        
        session = spotifyconnect.Session()

        config_cls_mock.assert_called_once_with()
        self.assertEqual(session.config, config_cls_mock.return_value)

    def test_raises_error_if_not_ok(self, lib_mock):
        lib_mock.SpInit.return_value = (
            spotifyconnect.ErrorType.WrongAPIVersion)
        config = spotifyconnect.Config()
        config.application_key = b'\x01' * 321

        with self.assertRaises(spotifyconnect.Error):
            spotifyconnect.Session(config=config)

    def test_set_remote_name(self, lib_mock):
        lib_mock.SpSetDisplayName.return_value = spotifyconnect.ErrorType.Ok

        session = tests.create_real_session(lib_mock)

        session.set_remote_name('a connect name')
        
        lib_mock.SpSetDisplayName.called_once_with(mock.ANY)
        self.assertEqual(
            spotifyconnect.ffi.string(lib_mock.SpSetDisplayName.call_args[0][0]),
            b'a connect name')
            
    def test_set_remote_name_fails_with_assert(self, lib_mock):
        lib_mock.SpSetDisplayName.return_value = spotifyconnect.ErrorType.WrongAPIVersion
        
        session = tests.create_real_session(lib_mock)
        
        with self.assertRaises(spotifyconnect.Error):
            session.set_remote_name('a connect name')
    
    def test_get_zeroconf_vars(self, lib_mock):          
        lib_mock.SpZeroConfGetVars.side_effect = tests.mock_zeroconf

        session = tests.create_real_session(lib_mock)

        result = session.get_zeroconf_vars()
        
        lib_mock.SpZeroConfGetVars.called_once_with(mock.ANY)
        self.assertEqual(result.public_key, 'Public key')
            
    def test_get_zeroconf_vars_fails_with_assert(self, lib_mock):
        lib_mock.SpZeroConfGetVars.return_value = spotifyconnect.ErrorType.WrongAPIVersion
        
        session = tests.create_real_session(lib_mock)
        
        with self.assertRaises(spotifyconnect.Error):
            session.get_zeroconf_vars()

    def test_process_events_fail_raises_error(self, lib_mock):
        lib_mock.SpPumpEvents.return_value = (
            spotifyconnect.ErrorType.WrongAPIVersion)
        session = tests.create_real_session(lib_mock)

        with self.assertRaises(spotifyconnect.Error):
            session.process_events()

    def test_library_version(self, lib_mock):
        lib_mock.SpGetLibraryVersion.return_value = spotifyconnect.ffi.new('char[]', b'versionX')

        session = tests.create_real_session(lib_mock)

        result = session.library_version
        
        lib_mock.SpGetLibraryVersion.called_once_with()		
        self.assertEqual(result, 'versionX')

    def test_free_session(self, lib_mock):
        lib_mock.SpFree.return_value = spotifyconnect.ErrorType.Ok

        session = tests.create_real_session(lib_mock)

        session.free_session()
        
        lib_mock.SpFree.called_once_with()		
        self.assertEqual(spotifyconnect._session_instance, None)
