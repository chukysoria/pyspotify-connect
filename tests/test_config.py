# encoding: utf-8

from __future__ import unicode_literals

import tempfile
import unittest

import spotifyconnect
from tests import mock


class ConfigTest(unittest.TestCase):

    def setUp(self):
        self.config = spotifyconnect.Config()

    def test_defaults(self):
        
        self.assertEqual(self.config.version, 4)
        self.assertEqual(self.config.buffer_size, 0x100000)
        self.assertEqual(self.config.remote_name, 'Spotify-Connect')
        self.assertEqual(self.config.brand_name, 'DummyBrand')
        self.assertEqual(self.config.model_name, 'DummyModel')
        self.assertEqual(self.config.device_type, spotifyconnect.DeviceType.AudioDongle)
    
    def test_api_version(self):
        self.config.version = 4

        self.assertEqual(self.config._sp_session_config.version, 4)
        self.assertEqual(self.config.version, 4)

    def test_buffer_size(self):
        self.config.buffer_size = 400
        
        self.assertEqual(self.config._sp_session_config.buffer_size, 400)
        self.assertEqual(self.config.buffer_size, 400)        
    
    def test_app_key(self):
        self.config.app_key = b'\x02' * 321

        self.assertEqual(
            spotifyconnect.ffi.string(spotifyconnect.ffi.cast(
                'char *', self.config._sp_session_config.app_key)),
            b'\x02' * 321)
        self.assertEqual(self.config.app_key, b'\x02' * 321)

    def test_app_key_is_unknown(self):
        self.assertIsNone(self.config.app_key)

    def test_app_key_size_is_zero_by_default(self):
        self.assertEqual(
            self.config._sp_session_config.app_key_size, 0)

    def test_app_key_size_is_calculated_correctly(self):
        self.config.app_key = b'\x01' * 321

        self.assertEqual(
            self.config._sp_session_config.app_key_size, 321)

    def test_appn_key_can_be_reset_to_none(self):
        self.config.app_key = None

        self.assertIsNone(self.config.app_key)
        self.assertEqual(
            self.config._sp_session_config.app_key_size, 0)

    def test_app_key_fails_if_invalid_key(self):
        with self.assertRaises(AssertionError):
            self.config.app_key = 'way too short key'

    def test_load_application_key_file_can_load_key_from_file(self):
        self.config.app_key = None
        filename = tempfile.mkstemp()[1]
        with open(filename, 'wb') as f:
            f.write(b'\x03' * 321)

        self.config.load_application_key_file(filename)

        self.assertEqual(self.config.app_key, b'\x03' * 321)

    def test_load_application_key_file_defaults_to_a_file_in_cwd(self):
        open_mock = mock.mock_open(read_data='\x04' * 321)
        with mock.patch('spotifyconnect.config.open', open_mock, create=True) as m:
            self.config.load_application_key_file()

        m.assert_called_once_with(b'spotify_appkey.key', 'rb')
        self.assertEqual(self.config.app_key, b'\x04' * 321)

    def test_load_application_key_file_fails_if_no_key_found(self):
        with self.assertRaises(EnvironmentError):
            self.config.load_application_key_file(b'/nonexistant')

    def test_device_id(self):
        self.config.device_id = '123abc'

        self.assertEqual(
            spotifyconnect.ffi.string(self.config._sp_session_config.deviceId),
            b'123abc')
        self.assertEqual(self.config.device_id, '123abc')

    def test_device_id_converts_empty_string_to_none(self):
        self.config.device_id = ''

        self.assertEqual(
            self.config._sp_session_config.deviceId, spotifyconnect.ffi.NULL)
        self.assertIsNone(self.config.device_id)
        
    def test_remote_name(self):
        self.config.remote_name = 'remote123'

        self.assertEqual(
            spotifyconnect.ffi.string(self.config._sp_session_config.remoteName),
            b'remote123')
        self.assertEqual(self.config.remote_name, 'remote123')

    def test_remote_name_converts_empty_string_to_none(self):
        self.config.remote_name = ''

        self.assertEqual(
            self.config._sp_session_config.remoteName, spotifyconnect.ffi.NULL)
        self.assertIsNone(self.config.remote_name)

    def test_brand_name(self):
        self.config.brand_name = 'brand123'

        self.assertEqual(
            spotifyconnect.ffi.string(self.config._sp_session_config.brandName),
            b'brand123')
        self.assertEqual(self.config.brand_name, 'brand123')

    def test_brand_name_converts_empty_string_to_none(self):
        self.config.brand_name = ''

        self.assertEqual(
            self.config._sp_session_config.brandName, spotifyconnect.ffi.NULL)
        self.assertIsNone(self.config.brand_name)

    def test_model_name(self):
        self.config.model_name = 'model123'

        self.assertEqual(
            spotifyconnect.ffi.string(self.config._sp_session_config.modelName),
            b'model123')
        self.assertEqual(self.config.model_name, 'model123')

    def test_model_name_converts_empty_string_to_none(self):
        self.config.model_name = ''

        self.assertEqual(
            self.config._sp_session_config.modelName, spotifyconnect.ffi.NULL)
        self.assertIsNone(self.config.model_name)
    
    def test_device_type(self):
        self.config.device_type = spotifyconnect.DeviceType.AudioDongle
        
        self.assertEqual(self.config._sp_session_config.deviceType,
            spotifyconnect.DeviceType.AudioDongle)
        self.assertEqual(self.config.device_type, spotifyconnect.DeviceType.AudioDongle)
        
    def test_client_id(self):
        self.config.client_id = 'client123'

        self.assertEqual(
            spotifyconnect.ffi.string(self.config._sp_session_config.client_id),
            b'client123')
        self.assertEqual(self.config.client_id, 'client123')

    def test_client_id_converts_empty_string_to_none(self):
        self.config.client_id = ''

        self.assertEqual(
            self.config._sp_session_config.client_id, spotifyconnect.ffi.NULL)
        self.assertIsNone(self.config.client_id)

    def test_client_secret(self):
        self.config.client_secret = 'secret123'

        self.assertEqual(
            spotifyconnect.ffi.string(self.config._sp_session_config.client_secret),
            b'secret123')
        self.assertEqual(self.config.client_secret, 'secret123')

    def test_client_secret_converts_empty_string_to_none(self):
        self.config.client_secret = ''

        self.assertEqual(
            self.config._sp_session_config.client_secret, spotifyconnect.ffi.NULL)
        self.assertIsNone(self.config.client_secret)                             

    def test_sp_session_config_has_unicode_encoded_as_utf8(self):
        self.config.device_id = 'æ device_id'
        self.config.remote_name = 'æ remoteName'
        self.config.brand_name = 'æ brandName'
        self.config.model_name = 'æ modelName'
        self.config.client_id = 'æ client_id'
        self.config.client_secret = 'æ client_secret'

        self.assertEqual(
            spotifyconnect.ffi.string(self.config._sp_session_config.deviceId),
            b'\xc3\xa6 device_id')
        self.assertEqual(
            spotifyconnect.ffi.string(self.config._sp_session_config.remoteName),
            b'\xc3\xa6 remoteName')
        self.assertEqual(
            spotifyconnect.ffi.string(self.config._sp_session_config.brandName),
            b'\xc3\xa6 brandName')
        self.assertEqual(
            spotifyconnect.ffi.string(self.config._sp_session_config.modelName),
            b'\xc3\xa6 modelName')
        self.assertEqual(
            spotifyconnect.ffi.string(self.config._sp_session_config.client_id),
            b'\xc3\xa6 client_id')
        self.assertEqual(
            spotifyconnect.ffi.string(self.config._sp_session_config.client_secret),
            b'\xc3\xa6 client_secret')

    def test_userdata(self):        
        userdata_python = 'handle'
        userdata = spotifyconnect.ffi.new_handle(userdata_python)
        self.config.userdata = userdata
        
        self.assertEqual(self.config._sp_session_config.userdata, userdata)
        self.assertEqual(self.config.userdata, userdata)
        self.assertEqual(spotifyconnect.ffi.from_handle(self.config.userdata),
            'handle')

    def test_userdata_is_unknown(self):
        self.assertEqual(self.config._sp_session_config.userdata, spotifyconnect.ffi.NULL)
        self.assertEqual(self.config.userdata, spotifyconnect.ffi.NULL)

    @spotifyconnect.ffi.callback('void(SpError error, void *userdata)')
    def error_callback(error, sp_userdata):
        pass
            
    def test_error_callback(self): 
        self.config.error_callback = self.error_callback
        
        self.assertEqual(self.config._sp_session_config.error_callback, self.error_callback)
        self.assertEqual(self.config.error_callback, self.error_callback)

    def test_error_callback_is_unknown(self):
        self.assertEqual(self.config._sp_session_config.error_callback, spotifyconnect.ffi.NULL)
        self.assertEqual(self.config.error_callback, spotifyconnect.ffi.NULL)    
    
        
class DeviceTypeTest(unittest.TestCase):

    def test_has_contants(self):
        self.assertEqual(spotifyconnect.DeviceType.Unknown, 0)
        self.assertEqual(spotifyconnect.DeviceType.Computer, 1)
        self.assertEqual(spotifyconnect.DeviceType.Tablet, 2)
        self.assertEqual(spotifyconnect.DeviceType.Smartphone, 3)
        self.assertEqual(spotifyconnect.DeviceType.Speaker, 4)
        self.assertEqual(spotifyconnect.DeviceType.TV, 5)
        self.assertEqual(spotifyconnect.DeviceType.AVR, 6)
        self.assertEqual(spotifyconnect.DeviceType.STB, 7)
        self.assertEqual(spotifyconnect.DeviceType.AudioDongle, 8)
