from __future__ import unicode_literals

from spotifyconnect import ffi, lib, serialized, utils
import spotifyconnect


__all__ = [
    'ImageSize',
    'Metadata'
]


class Metadata(object):

    """A Spotify track.
    """

    def __init__(self, sp_metadata):

        self.playlist_name = utils.to_unicode(sp_metadata.data0)
        self.track_name = utils.to_unicode(sp_metadata.track_name)
        self.track_uri = utils.to_unicode(sp_metadata.track_uri)
        self.artist_name = utils.to_unicode(sp_metadata.artist_name)
        self.artist_uri = utils.to_unicode(sp_metadata.artist_uri)
        self.album_name = utils.to_unicode(sp_metadata.album_name)
        self.album_uri = utils.to_unicode(sp_metadata.album_uri)
        self.cover_uri = utils.to_unicode(sp_metadata.cover_uri)
        self.duration = sp_metadata.duration


    def __repr__(self):
        return 'Metadata(%r)' % self.track_uri

    @serialized
    def get_image_url(self, image_size):
        image_url = ffi.new('char[512]')
        spotifyconnect.Error.maybe_raise(lib.SpGetMetadataImageURL(utils.to_char(self.cover_uri), image_size, image_url, ffi.sizeof(image_url)))
        return utils.to_unicode(image_url)

@utils.make_enum('kSpImageSize')
class ImageSize(utils.IntEnum):
    pass
