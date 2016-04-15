from __future__ import unicode_literals

import unittest
import json

import tests
from tests import mock

import spotifyconnect
from spotifyconnect import _zeroconfserver

class ZeroconfTest(unittest.TestCase):
    
    def setUp(self):
        self.client = _zeroconfserver.app.test_client()

    def test_login_zeroconf_empty_get(self):
        data = self.client.get('/login/_zeroconf').data.decode()
        result = json.loads(data)

        self.assertEqual(result['status'], 301)
        self.assertEqual(result['spotifyError'], 0)
        self.assertEqual(result['statusString'], 'ERROR-MISSING-ACTION')

    def test_login_zeroconf_wrong_action(self):
        data = self.client.get('/login/_zeroconf?action=foo').data.decode()
        result = json.loads(data)

        self.assertEqual(result['status'], 301)
        self.assertEqual(result['spotifyError'], 0)
        self.assertEqual(result['statusString'], 'ERROR-INVALID-ACTION')

    @mock.patch('spotifyconnect.session.lib', spec=spotifyconnect.lib)
    def test_login_zeroconf_get_info(self, lib_mock):
        lib_mock.SpZeroConfGetVars.side_effect = tests.mock_zeroconf
        tests.create_real_session(lib_mock)
                
        data = self.client.get('/login/_zeroconf?action=getInfo').data.decode()
        result = json.loads(data)

        self.assertEqual(result['status'], 101)
        self.assertEqual(result['spotifyError'], 0)
        self.assertEqual(result['activeUser'], 'Active user')
        self.assertEqual(result['brandDisplayName'], 'DummyBrand')
        self.assertEqual(result['accountReq'], 'Premium')
        self.assertEqual(result['deviceID'], 'Device Id')
        self.assertEqual(result['publicKey'], 'Public key')
        self.assertEqual(result['version'], '2.0.1')
        self.assertEqual(result['deviceType'], 'Dongle')
        self.assertEqual(result['modelDisplayName'], 'DummyModel')
        self.assertEqual(result['statusString'], 'ERROR-OK')
        self.assertEqual(result['remoteName'], 'Remote name')

    @mock.patch('spotifyconnect.connection.lib', spec=spotifyconnect.lib)
    def test_login_zeroconf_post_user(self, lib_mock):
        lib_mock.SpConnectionLoginZeroConf.return_value = spotifyconnect.ErrorType.Ok
        tests.create_real_connection(lib_mock)
        
          
        data = self.client.post('/login/_zeroconf?action=addUser', data=dict(
            userName='foo',
            blob='longstring',
            clientKey='longkey')).data.decode()
        result = json.loads(data)

        self.assertEqual(result['status'], 101)
        self.assertEqual(result['spotifyError'], 0)
        self.assertEqual(result['statusString'], 'ERROR-OK')
        lib_mock.SpConnectionLoginZeroConf.assert_called_once_with(mock.ANY, 'longstring', 'longkey')
        self.assertEqual(spotifyconnect.ffi.string(lib_mock.SpConnectionLoginZeroConf.call_args[0][0]), b'foo')
