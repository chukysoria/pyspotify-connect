from __future__ import unicode_literals

import uuid

from spotifyconnect import ffi, utils


__all__ = [
    'Config',
    'DeviceType'
]


class Config(object):

    """The session config.

    Create an instance and assign to its attributes to configure. Then use the
    config object to create a session::

        >>> config = spotify.Config()
        >>> config.user_agent = 'My awesome Spotify client'
        >>> # Etc ...
        >>> session = spotify.Session(config=config)
    """

    def __init__(self):
        self._sp_session_config = ffi.new('SpConfig *')
             
        self.version = 4
        self._sp_session_config.buffer = ffi.dlopen(None).malloc(0x100000)
        self._sp_session_config.buffer_size = 0x100000
        self.load_application_key_file() 
        self.device_id = str(uuid.uuid4())
        self.remote_name = 'Spotify-Connect'
        self.brand_name = 'DummyBrand'
        self.model_name = 'DummyModel'
        self.device_type = DeviceType.AudioDongle
        self.userdata = ffi.new_handle(self)
    
    @property
    def sp_session_config(self):
        return self._sp_session_config
    
    @property
    def version(self):
        """The API version of the libspotify we're using.

        You should not need to change this. It defaults to the value provided
        by libspotify through :func:`spotify.get_libspotify_api_version`.
        """
        return self._sp_session_config.version

    @version.setter
    def version(self, value):
        self._sp_session_config.version = value

    @property
    def app_key(self):
        """Your libspotify application key.

        Must be a bytestring. Alternatively, you can call
        :meth:`load_application_key_file`, and pyspotify will correctly read
        the file into :attr:`application_key`.
        """
        return utils.to_bytes_or_none(
            ffi.cast('char *', self._sp_session_config.app_key))

    @app_key.setter
    def app_key(self, value):
        if value is None:
            size = 0
        else:
            size = len(value)
        assert size in (0, 321), (
            'Invalid application key; expected 321 bytes, got %d bytes' % size)

        self._application_key = utils.to_char_or_null(value)
        self._sp_session_config.app_key = ffi.cast(
            'void *', self._application_key)
        self._sp_session_config.app_key_size = size

    def load_application_key_file(self, filename=b'spotify_appkey.key'):
        """Load your libspotify application key file.

        If called without arguments, it tries to read ``spotify_appkey.key``
        from the current working directory.

        This is an alternative to setting :attr:`application_key` yourself. The
        file must be a binary key file, not the C code key file that can be
        compiled into an application.
        """
        with open(filename, 'rb') as fh:
            self.app_key = fh.read()
    
    @property
    def device_id(self):
        """Device ID for offline synchronization and logging purposes.

        Defaults to :class:`None`.

        The Device ID must be unique to the particular device instance, i.e. no
        two units must supply the same Device ID. The Device ID must not change
        between sessions or power cycles. Good examples is the device's MAC
        address or unique serial number.

        Setting the device ID to an empty string has the same effect as setting
        it to :class:`None`.
        """
        return utils.to_unicode_or_none(self._sp_session_config.deviceId)

    @device_id.setter
    def device_id(self, value):
        # NOTE libspotify segfaults if device_id is set to an empty string,
        # thus we convert empty strings to NULL.
        self._deviceId = utils.to_char_or_null(value or None)
        self._sp_session_config.deviceId = self._deviceId

    @property
    def remote_name(self):
        return utils.to_unicode_or_none(self._sp_session_config.remoteName)

    @remote_name.setter
    def remote_name(self, value):
        self._remoteName = utils.to_char_or_null(value or None)
        self._sp_session_config.remoteName = self._remoteName

    @property
    def brand_name(self):
        return utils.to_unicode_or_none(self._sp_session_config.brandName)

    @brand_name.setter
    def brand_name(self, value):
        self._brandName = utils.to_char_or_null(value or None)
        self._sp_session_config.brandName = self._brandName

    @property
    def model_name(self):
        return utils.to_unicode_or_none(self._sp_session_config.modelName)

    @model_name.setter
    def model_name(self, value):
        self._modelName = utils.to_char_or_null(value or None)
        self._sp_session_config.modelName = self._modelName

    @property
    def device_type(self):
        return DeviceType(self._sp_session_config.deviceType)

    @device_type.setter
    def device_type(self, value):
        self._sp_session_config.deviceType = value

    @property
    def userdata(self):
        return self._sp_session_config.userdata

    @userdata.setter
    def userdata(self, value):
        self._sp_session_config.userdata = value
        
    @property
    def error_callback(self):
        return self._sp_session_config.error_callback

    @error_callback.setter
    def error_callback(self, value):
        self._sp_session_config.error_callback = value
                
@utils.make_enum('kSpDeviceType')       
class DeviceType(utils.IntEnum):
    pass
