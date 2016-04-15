from __future__ import unicode_literals

import unittest

import spotifyconnect
import tests
from tests import mock
from spotifyconnect import utils


class MetadataTest(unittest.TestCase):

    def test_eq(self):
        sp_metadata = spotifyconnect.ffi.new('SpMetadata *')
        sp_metadata.track_uri = b'uri:9382403284032'
        metadata1 = spotifyconnect.Metadata(sp_metadata)
        metadata2 = spotifyconnect.Metadata(sp_metadata)

        self.assertTrue(metadata1 == metadata2)
        self.assertFalse(metadata1 == 'foo')

    def test_ne(self):
        sp_metadata = spotifyconnect.ffi.new('SpMetadata *')
        sp_metadata.track_uri = b'uri:9382403284032'
        metadata1 = spotifyconnect.Metadata(sp_metadata)
        metadata2 = spotifyconnect.Metadata(sp_metadata)

        self.assertFalse(metadata1 != metadata2)

    def test_hash(self):
        sp_metadata = spotifyconnect.ffi.new('SpMetadata *')
        sp_metadata.track_uri = b'uri:9382403284032'
        metadata1 = spotifyconnect.Metadata(sp_metadata)
        metadata2 = spotifyconnect.Metadata(sp_metadata)

        self.assertEqual(hash(metadata1), hash(metadata2))
        
    def test_repr(self):
        sp_metadata = spotifyconnect.ffi.new('SpMetadata *')
        sp_metadata.track_uri = b'uri:9382403284032'
        metadata = spotifyconnect.Metadata(sp_metadata)

        self.assertEqual(metadata.__repr__(), 'Metadata(uri:9382403284032)')
        
    def test_playlist_uri(self):
        sp_metadata = spotifyconnect.ffi.new('SpMetadata *')
        sp_metadata.playlist_uri = b'uri:9382403284032'
        metadata = spotifyconnect.Metadata(sp_metadata)

        self.assertEqual(metadata.playlist_uri, 'uri:9382403284032')

    def test_playlist_name(self):
        sp_metadata = spotifyconnect.ffi.new('SpMetadata *')
        sp_metadata.playlist_name = b'Foo Bar Baz'
        metadata = spotifyconnect.Metadata(sp_metadata)

        self.assertEqual(metadata.playlist_name, 'Foo Bar Baz')
        
    def test_track_uri(self):
        sp_metadata = spotifyconnect.ffi.new('SpMetadata *')
        sp_metadata.track_uri = b'uri:9382403284032'
        metadata = spotifyconnect.Metadata(sp_metadata)

        self.assertEqual(metadata.track_uri, 'uri:9382403284032')

    def test_track_name(self):
        sp_metadata = spotifyconnect.ffi.new('SpMetadata *')
        sp_metadata.track_name = b'Foo Bar Baz'
        metadata = spotifyconnect.Metadata(sp_metadata)

        self.assertEqual(metadata.track_name, 'Foo Bar Baz')
        
    def test_album_uri(self):
        sp_metadata = spotifyconnect.ffi.new('SpMetadata *')
        sp_metadata.album_uri = b'uri:9382403284032'
        metadata = spotifyconnect.Metadata(sp_metadata)

        self.assertEqual(metadata.album_uri, 'uri:9382403284032')

    def test_album_name(self):
        sp_metadata = spotifyconnect.ffi.new('SpMetadata *')
        sp_metadata.album_name = b'Foo Bar Baz'
        metadata = spotifyconnect.Metadata(sp_metadata)

        self.assertEqual(metadata.album_name, 'Foo Bar Baz')
        
    def test_artist_uri(self):
        sp_metadata = spotifyconnect.ffi.new('SpMetadata *')
        sp_metadata.artist_uri = b'uri:9382403284032'
        metadata = spotifyconnect.Metadata(sp_metadata)

        self.assertEqual(metadata.artist_uri, 'uri:9382403284032')

    def test_artist_name(self):
        sp_metadata = spotifyconnect.ffi.new('SpMetadata *')
        sp_metadata.artist_name = b'Foo Bar Baz'
        metadata = spotifyconnect.Metadata(sp_metadata)

        self.assertEqual(metadata.artist_name, 'Foo Bar Baz')

    def test_cover_uri(self):
        sp_metadata = spotifyconnect.ffi.new('SpMetadata *')
        sp_metadata.cover_uri = b'uri:9382403284032'
        metadata = spotifyconnect.Metadata(sp_metadata)

        self.assertEqual(metadata.cover_uri, 'uri:9382403284032')
                                      
    def test_duration(self):
        sp_metadata = spotifyconnect.ffi.new('SpMetadata *')
        sp_metadata.duration = 60000
        metadata = spotifyconnect.Metadata(sp_metadata)

        self.assertEqual(metadata.duration, 60000)
    
    @mock.patch('spotifyconnect.metadata.lib', spec=spotifyconnect.lib)
    def test_image_url(self, lib_mock):
        
        lib_mock.SpGetMetadataImageURL.side_effect = mock_SpGetMetadataImageURL
        
        sp_metadata = spotifyconnect.ffi.new('SpMetadata *')
        metadata = spotifyconnect.Metadata(sp_metadata)
        
        result = metadata.get_image_url(spotifyconnect.ImageSize.Normal)
        
        lib_mock.SpGetMetadataImageURL.called_once_with(mock.ANY, spotifyconnect.ImageSize.Normal, mock.ANY, 512)
        self.assertEqual(
            utils.to_unicode(lib_mock.SpGetMetadataImageURL.call_args[0][0]),
            metadata.cover_uri)
        self.assertEqual(result, 'http://url.test')

    @mock.patch('spotifyconnect.metadata.lib', spec=spotifyconnect.lib)
    def test_image_url_fails_with_assert(self, lib_mock):
        
        lib_mock.SpGetMetadataImageURL.return_value = spotifyconnect.ErrorType.WrongAPIVersion
        
        sp_metadata = spotifyconnect.ffi.new('SpMetadata *')
        metadata = spotifyconnect.Metadata(sp_metadata)
        
        with self.assertRaises(spotifyconnect.Error):
            metadata.get_image_url(spotifyconnect.ImageSize.Normal)
        
def mock_SpGetMetadataImageURL(uri, image_size, image_url, image_url_size):
    new_image_url = spotifyconnect.ffi.new('char[]', b'http://url.test')    
    spotifyconnect.ffi.buffer(image_url, spotifyconnect.ffi.sizeof(new_image_url))[:] = (
        spotifyconnect.ffi.buffer(new_image_url, spotifyconnect.ffi.sizeof(new_image_url))[:])
    return spotifyconnect.ErrorType.Ok

class ImageSizeTest(unittest.TestCase):
    
        def test_has_image_size_constants(self):
            self.assertEqual(spotifyconnect.ImageSize.Small, 0)
            self.assertEqual(spotifyconnect.ImageSize.Normal, 1)
            self.assertEqual(spotifyconnect.ImageSize.Large, 2)
