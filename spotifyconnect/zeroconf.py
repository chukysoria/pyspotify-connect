from __future__ import unicode_literals

from multiprocessing import Process

from spotifyconnect import _zeroconfserver, utils


__all__ = [
    'Zeroconf',
    'AvahiZeroConfServer'
]


class Zeroconf(object):

    """A Spotify ZeroConf object.
    """

    def __init__(self, sp_zeroconf):

        self.public_key = utils.to_unicode(sp_zeroconf.publicKey)
        self.device_id = utils.to_unicode(sp_zeroconf.deviceId)
        self.active_user = utils.to_unicode(sp_zeroconf.activeUser)
        self.remote_name = utils.to_unicode(sp_zeroconf.remoteName)
        self.account_req = utils.to_unicode(sp_zeroconf.accountReq)
        self.device_type = utils.to_unicode(sp_zeroconf.deviceType)
        self.library_version = utils.to_unicode(sp_zeroconf.libraryVersion)


class AvahiZeroConfServer(Process):
    """A SpotifyConnect ZeroConf server.
    """

    daemon = True
    name = 'SpotifyConnectServer'

    def __init__(self, port=6697):
        Process.__init__(self)

        self._application = _zeroconfserver.app
        self.port = port

    _application = None
    port = None

    def run(self):

        # First run the command avahi-publish-service SpotifyConnect
        # _spotify-connect._tcp 6697 VERSION=1.0 CPath=/login/_zeroconf
        self._application.run(
            host='0.0.0.0',
            port=self.port,
            debug=True,
            use_reloader=False,
            threaded=True)  # pragma: no cover
