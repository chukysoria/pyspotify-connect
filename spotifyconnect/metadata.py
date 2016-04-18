from __future__ import unicode_literals

import spotifyconnect
from spotifyconnect import ffi, lib, serialized, utils


__all__ = [
    'ImageSize',
    'Metadata'
]


class Metadata(object):

    """A Spotify track.
    """

    def __init__(self, sp_metadata):

        self._sp_metadata = sp_metadata
        self.playlist_name = utils.to_unicode(sp_metadata.playlist_name)
        self.playlist_uri = utils.to_unicode(sp_metadata.playlist_uri)
        self.track_name = utils.to_unicode(sp_metadata.track_name)
        self.track_uri = utils.to_unicode(sp_metadata.track_uri)
        self.artist_name = utils.to_unicode(sp_metadata.artist_name)
        self.artist_uri = utils.to_unicode(sp_metadata.artist_uri)
        self.album_name = utils.to_unicode(sp_metadata.album_name)
        self.album_uri = utils.to_unicode(sp_metadata.album_uri)
        self.cover_uri = utils.to_unicode(sp_metadata.cover_uri)
        self.duration = sp_metadata.duration

    def __repr__(self):
        return 'Metadata(%s)' % self.track_uri

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._sp_metadata == other._sp_metadata
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self._sp_metadata)

    @serialized
    def get_image_url(self, image_size):
        image_url = ffi.new('char[512]')
        spotifyconnect.Error.maybe_raise(
            lib.SpGetMetadataImageURL(
                utils.to_char(
                    self.cover_uri),
                image_size,
                image_url,
                ffi.sizeof(image_url)))
        return utils.to_unicode(image_url)


@utils.make_enum('kSpImageSize')
class ImageSize(utils.IntEnum):
    pass
