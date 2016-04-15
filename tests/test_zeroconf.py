from __future__ import unicode_literals

import unittest

import spotifyconnect

class ZeroconfTest(unittest.TestCase):
    
    def test_zeroconf(self):
    
        sp_zeroconf = spotifyconnect.ffi.new('SpZeroConfVars *')
        sp_zeroconf.publicKey = b'Public key'
        sp_zeroconf.deviceId = b'Device Id'
        sp_zeroconf.activeUser = b'Active user'
        sp_zeroconf.remoteName = b'Remote name'
        sp_zeroconf.accountReq = b'Premium'
        sp_zeroconf.deviceType = b'Dongle'
        sp_zeroconf.libraryVersion = b'1.2.0'
        
        zeroconf = spotifyconnect.Zeroconf(sp_zeroconf)
        
        self.assertEqual(zeroconf.public_key, u'Public key')
        self.assertEqual(zeroconf.device_id, u'Device Id')
        self.assertEqual(zeroconf.active_user, u'Active user')
        self.assertEqual(zeroconf.remote_name, u'Remote name')
        self.assertEqual(zeroconf.account_req, u'Premium')
        self.assertEqual(zeroconf.device_type, u'Dongle')
        self.assertEqual(zeroconf.library_version, u'1.2.0')


class AvahiZeroConfServerTest(unittest.TestCase):

    def test_default_port(self):
    
        webserver = spotifyconnect.AvahiZeroConfServer()
        
        self.assertEqual(webserver.port, 6697)

    def test_port(self):
    
        webserver = spotifyconnect.AvahiZeroConfServer(8888)
        
        self.assertEqual(webserver.port, 8888)
        
    def test_run(self):
    
        webserver = spotifyconnect.AvahiZeroConfServer()
        webserver.start()
        
        client = webserver._application.test_client()

        self.assertEqual(client.get('/').status_code, 404)

        webserver.terminate()
        webserver.join()
