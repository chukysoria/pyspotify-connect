from __future__ import unicode_literals

import unittest

import spotifyconnect
from spotifyconnect.player import _PlayerCallbacks

import tests
from tests import mock


@mock.patch('spotifyconnect.player.lib', spec=spotifyconnect.lib)
class PlayerTest(unittest.TestCase):

    def tearDown(self):
        spotifyconnect._session_instance = None

    def test_player_play(self, lib_mock):
        lib_mock.SpPlaybackPlay.return_value = spotifyconnect.ErrorType.Ok
        session = tests.create_real_player(lib_mock)

        session.player.play()

        lib_mock.SpPlaybackPlay.assert_called_once_with()

    def test_player_play_fail_raises_error(self, lib_mock):
        lib_mock.SpPlaybackPlay.return_value = (
            spotifyconnect.ErrorType.WrongAPIVersion)
        session = tests.create_real_player(lib_mock)

        with self.assertRaises(spotifyconnect.Error):
            session.player.play()

    def test_player_pause(self, lib_mock):
        lib_mock.SpPlaybackPause.return_value = spotifyconnect.ErrorType.Ok
        session = tests.create_real_player(lib_mock)

        session.player.pause()

        lib_mock.SpPlaybackPause.assert_called_once_with()

    def test_player_pause_fail_raises_error(self, lib_mock):
        lib_mock.SpPlaybackPause.return_value = spotifyconnect.ErrorType.WrongAPIVersion
        session = tests.create_real_player(lib_mock)

        with self.assertRaises(spotifyconnect.Error):
            session.player.pause()
            
    def test_player_skip_to_next(self, lib_mock):
        lib_mock.SpPlaybackSkipToNext.return_value = spotifyconnect.ErrorType.Ok
        session = tests.create_real_player(lib_mock)

        session.player.skip_to_next()

        lib_mock.SpPlaybackSkipToNext.assert_called_once_with()

    def test_player_skip_to_next_fail_raises_error(self, lib_mock):
        lib_mock.SpPlaybackSkipToNext.return_value = spotifyconnect.ErrorType.WrongAPIVersion
        session = tests.create_real_player(lib_mock)

        with self.assertRaises(spotifyconnect.Error):
            session.player.skip_to_next()

    def test_player_skip_to_prev(self, lib_mock):
        lib_mock.SpPlaybackSkipToPrev.return_value = spotifyconnect.ErrorType.Ok
        session = tests.create_real_player(lib_mock)

        session.player.skip_to_prev()

        lib_mock.SpPlaybackSkipToPrev.assert_called_once_with()

    def test_player_skip_to_prev_fail_raises_error(self, lib_mock):
        lib_mock.SpPlaybackSkipToPrev.return_value = spotifyconnect.ErrorType.WrongAPIVersion
        session = tests.create_real_player(lib_mock)

        with self.assertRaises(spotifyconnect.Error):
            session.player.skip_to_prev() 
    
    def test_player_seek(self, lib_mock):
        lib_mock.SpPlaybackSeek.return_value = spotifyconnect.ErrorType.Ok
        session = tests.create_real_player(lib_mock)

        session.player.seek(45000)

        lib_mock.SpPlaybackSeek.assert_called_once_with(45000)

    def test_player_seek_fail_raises_error(self, lib_mock):
        lib_mock.SpPlaybackSeek.return_value = (
            spotifyconnect.ErrorType.WrongAPIVersion)
        session = tests.create_real_player(lib_mock)

        with self.assertRaises(spotifyconnect.Error):
            session.player.seek(45000)   
            
    def test_player_enable_shuffle(self, lib_mock):
        lib_mock.SpPlaybackEnableShuffle.return_value = spotifyconnect.ErrorType.Ok
        session = tests.create_real_player(lib_mock)

        session.player.enable_shuffle(True)

        lib_mock.SpPlaybackEnableShuffle.assert_called_once_with(True)     
    
    def test_player_disable_shuffle(self, lib_mock):
        lib_mock.SpPlaybackEnableShuffle.return_value = spotifyconnect.ErrorType.Ok
        session = tests.create_real_player(lib_mock)

        session.player.enable_shuffle(False)

        lib_mock.SpPlaybackEnableShuffle.assert_called_once_with(False)  
    
    def test_player_switch_shuffle(self, lib_mock):
        lib_mock.SpPlaybackEnableShuffle.return_value = spotifyconnect.ErrorType.Ok
        lib_mock.SpPlaybackIsShuffled.retun_value = True
        session = tests.create_real_player(lib_mock)

        session.player.enable_shuffle()

        lib_mock.SpPlaybackEnableShuffle.assert_called_once_with(False)
        
    def test_player_enable_shuffle_fail_raises_error(self, lib_mock):
        lib_mock.SpPlaybackEnableShuffle.return_value = spotifyconnect.ErrorType.WrongAPIVersion
        session = tests.create_real_player(lib_mock)
        
        with self.assertRaises(spotifyconnect.Error):
            session.player.enable_shuffle(True)     

            
    def test_player_enable_repeat(self, lib_mock):
        lib_mock.SpPlaybackEnableRepeat.return_value = spotifyconnect.ErrorType.Ok
        session = tests.create_real_player(lib_mock)

        session.player.enable_repeat(True)

        lib_mock.SpPlaybackEnableRepeat.assert_called_once_with(True)     
    
    def test_player_disable_repeat(self, lib_mock):
        lib_mock.SpPlaybackEnableRepeat.return_value = spotifyconnect.ErrorType.Ok
        session = tests.create_real_player(lib_mock)

        session.player.enable_repeat(False)

        lib_mock.SpPlaybackEnableRepeat.assert_called_once_with(False)  
    
    def test_player_switch_repeat(self, lib_mock):
        lib_mock.SpPlaybackEnableRepeat.return_value = spotifyconnect.ErrorType.Ok
        lib_mock.SpPlaybackIsRepeated.retun_value = True
        session = tests.create_real_player(lib_mock)

        session.player.enable_repeat()

        lib_mock.SpPlaybackEnableRepeat.assert_called_once_with(False)
        
    def test_player_enable_repeat_fail_raises_error(self, lib_mock):
        lib_mock.SpPlaybackEnableRepeat.return_value = spotifyconnect.ErrorType.WrongAPIVersion
        session = tests.create_real_player(lib_mock)
        
        with self.assertRaises(spotifyconnect.Error):
            session.player.enable_repeat(True)   
    
    def test_player_playing(self, lib_mock):
        lib_mock.SpPlaybackIsPlaying.retun_value = True
        session = tests.create_real_player(lib_mock)

        self.assertTrue(session.player.playing)
        
    def test_player_shuffled(self, lib_mock):
        lib_mock.SpPlaybackIsShuffled.retun_value = True
        session = tests.create_real_player(lib_mock)

        self.assertTrue(session.player.shuffled)

    def test_player_repeated(self, lib_mock):
        lib_mock.SpPlaybackIsRepeated.retun_value = True
        session = tests.create_real_player(lib_mock)

        self.assertTrue(session.player.repeated)
        
    def test_player_active_device(self, lib_mock):
        lib_mock.SpPlaybackIsActiveDevice.retun_value = True
        session = tests.create_real_player(lib_mock)

        self.assertTrue(session.player.active_device)
    
    def test_player_get_volume(self, lib_mock):
        lib_mock.SpPlaybackGetVolume.return_value = 39321
        session = tests.create_real_player(lib_mock)
        
        result = session.player.volume

        lib_mock.SpPlaybackGetVolume.assert_called_once_with()
        self.assertEqual(result, 60.0)
 
    def test_player_set_volume(self, lib_mock):
        lib_mock.SpPlaybackUpdateVolume.return_value = spotifyconnect.ErrorType.Ok
        session = tests.create_real_player(lib_mock)
        
        session.player.volume = 60.0
        
        lib_mock.SpPlaybackUpdateVolume.assert_called_once_with(39321)               

    def test_player_set_volume_fail_raises_error(self, lib_mock):
        lib_mock.SpPlaybackUpdateVolume.return_value = spotifyconnect.ErrorType.WrongAPIVersion
        session = tests.create_real_player(lib_mock)        
        
        with self.assertRaises(spotifyconnect.Error):
            session.player.volume = 180

    def test_get_current_track(self, lib_mock):
        lib_mock.SpGetMetadata.side_effect = tests.mock_get_metadata
        session = tests.create_real_player(lib_mock)
        
        result = session.player.current_track
        
        lib_mock.SpGetMetadata.assert_called_once_with(mock.ANY, 0)
        self.assertEqual(result.track_name, 'Track')

    def test_get_track_metadata(self, lib_mock):
        lib_mock.SpGetMetadata.side_effect = tests.mock_get_metadata
        session = tests.create_real_player(lib_mock)
        
        result = session.player.get_track_metadata(5)
        
        lib_mock.SpGetMetadata.assert_called_once_with(mock.ANY, 5)
        self.assertEqual(result.track_name, 'Track')

    def test_get_track_metadata_fails_with_assert(self, lib_mock):
        lib_mock.SpGetMetadata.return_value = spotifyconnect.ErrorType.WrongAPIVersion
        session = tests.create_real_player(lib_mock)
        
        with self.assertRaises(spotifyconnect.Error):
            session.player.get_track_metadata(0)

    def test_metadata_valid_range(self, lib_mock):
        def mock_metadata_valid_range(start, end):
            new_start = spotifyconnect.ffi.new("int *", -5)
            new_end = spotifyconnect.ffi.new("int *", 10)
            spotifyconnect.ffi.buffer(start, 4)[:] = spotifyconnect.ffi.buffer(new_start, 4)[:]
            spotifyconnect.ffi.buffer(end, 4)[:] = spotifyconnect.ffi.buffer(new_end, 4)[:]
            return spotifyconnect.ErrorType.Ok    
        
        lib_mock.SpGetMetadataValidRange.side_effect = mock_metadata_valid_range
        session = tests.create_real_player(lib_mock)
        
        result = session.player.metadata_valid_range
        
        lib_mock.SpGetMetadataValidRange.assert_called_once_with(mock.ANY, mock.ANY) 
        self.assertEqual(result['start'], -5)
        self.assertEqual(result['end'], 10)
                    
    def test_player_set_bitrate(self, lib_mock):
        lib_mock.SpPlaybackSetBitrate.return_value = spotifyconnect.ErrorType.Ok
        session = tests.create_real_player(lib_mock)
        
        session.player.set_bitrate(spotifyconnect.Bitrate.BITRATE_90k)
        
        lib_mock.SpPlaybackSetBitrate.assert_called_once_with(spotifyconnect.Bitrate.BITRATE_90k)               

    def test_player_set_bitrate_fail_raises_error(self, lib_mock):
        lib_mock.SpPlaybackSetBitrate.return_value = spotifyconnect.ErrorType.WrongAPIVersion
        session = tests.create_real_player(lib_mock)        
        
        with self.assertRaises(spotifyconnect.Error):
            session.player.set_bitrate(17)
 


@mock.patch('spotifyconnect.player.lib', spec=spotifyconnect.lib)
class ConnectionCallbacksTest(unittest.TestCase):

    def tearDown(self):
        spotifyconnect._session_instance = None

    def test_playback_notify_callback(self, lib_mock):
        callback = mock.Mock()
        session = tests.create_real_player(lib_mock)
        session_handle = spotifyconnect.ffi.new_handle(session)
        session.player.on(spotifyconnect.PlayerEvent.PLAYBACK_NOTIFY, callback)
        
        notify = spotifyconnect.PlaybackNotify.Pause
        
        _PlayerCallbacks.playback_notify(notify, session_handle)
        
        callback.assert_called_once_with(notify, session)    

    def test_playback_notify_callback_when_no_instance(self, lib_mock):
        callback = mock.Mock()
        session = tests.create_real_player(lib_mock)
        spotifyconnect._session_instance = None
        session_handle = spotifyconnect.ffi.new_handle(session)
        session.player.on(spotifyconnect.PlayerEvent.PLAYBACK_NOTIFY, callback)        
        notify = spotifyconnect.PlaybackNotify.Pause
        
        _PlayerCallbacks.playback_notify(notify, session_handle)
        
        self.assertFalse(callback.called)

    def test_music_delivery_callback(self, lib_mock):
        sp_audioformat = spotifyconnect.ffi.new('SpSampleFormat *')
        sp_audioformat.channels = 2
        audio_format = spotifyconnect.AudioFormat(sp_audioformat)

        num_frames = 10
        frames_size = audio_format.frame_size * num_frames
        frames = spotifyconnect.ffi.new('char[]', frames_size)
        frames[0:3] = [b'a', b'b', b'c']
        frames_void_ptr = spotifyconnect.ffi.cast('void *', frames)

        pending = spotifyconnect.ffi.new('unsigned int *', 8)

        callback = mock.Mock()
        callback.return_value = num_frames
        session = tests.create_real_player(lib_mock)
        session_handle = spotifyconnect.ffi.new_handle(session)
        session.player.on(spotifyconnect.PlayerEvent.MUSIC_DELIVERY, callback)

        result = _PlayerCallbacks.playback_data(frames_void_ptr, num_frames, sp_audioformat, pending, session_handle)

        callback.assert_called_once_with(
            mock.ANY, mock.ANY, num_frames, pending, session)
        self.assertEqual(
            callback.call_args[0][0]._sp_audioformat, sp_audioformat)
        self.assertEqual(callback.call_args[0][1][:5], b'abc\x00\x00')
        self.assertEqual(result, num_frames)

    def test_music_delivery_without_callback_does_not_consume(self, lib_mock):
        session = tests.create_real_player(lib_mock)
        session_handle = spotifyconnect.ffi.new_handle(session)

        sp_audioformat = spotifyconnect.ffi.new('SpSampleFormat *')
        num_frames = 10
        frames = spotifyconnect.ffi.new('char[]', 0)
        frames_void_ptr = spotifyconnect.ffi.cast('void *', frames)
        pending = spotifyconnect.ffi.new('unsigned int *', 8)

        result = _PlayerCallbacks.playback_data(frames_void_ptr, num_frames, sp_audioformat, pending, session_handle)


        self.assertEqual(result, 0)
    def test_music_delivery_without_callback_when_no_instance(self, lib_mock):
        callback = mock.Mock()
        session = tests.create_real_player(lib_mock)
        spotifyconnect._session_instance = None
        session_handle = spotifyconnect.ffi.new_handle(session)
        session.player.on(spotifyconnect.PlayerEvent.MUSIC_DELIVERY, callback)

        sp_audioformat = spotifyconnect.ffi.new('SpSampleFormat *')
        num_frames = 10
        frames = spotifyconnect.ffi.new('char[]', 0)
        frames_void_ptr = spotifyconnect.ffi.cast('void *', frames)
        pending = spotifyconnect.ffi.new('unsigned int *', 8)

        _PlayerCallbacks.playback_data(frames_void_ptr, num_frames, sp_audioformat, pending, session_handle)

        self.assertFalse(callback.called)

    def test_playback_seek_callback(self, lib_mock):
        callback = mock.Mock()
        session = tests.create_real_player(lib_mock)
        session_handle = spotifyconnect.ffi.new_handle(session)
        session.player.on(spotifyconnect.PlayerEvent.PLAYBACK_SEEK, callback)
        
        seek = 45879
        
        _PlayerCallbacks.playback_seek(seek, session_handle)
        
        callback.assert_called_once_with(seek, session)    

    def test_playback_seek_callback_when_no_instance(self, lib_mock):
        callback = mock.Mock()
        session = tests.create_real_player(lib_mock)
        spotifyconnect._session_instance = None
        session_handle = spotifyconnect.ffi.new_handle(session)
        session.player.on(spotifyconnect.PlayerEvent.PLAYBACK_SEEK, callback)        
        seek = 45879
        
        _PlayerCallbacks.playback_seek(seek, session_handle)
        
        self.assertFalse(callback.called)    

    def test_playback_volume_callback(self, lib_mock):
        callback = mock.Mock()
        session = tests.create_real_player(lib_mock)
        session_handle = spotifyconnect.ffi.new_handle(session)
        session.player.on(spotifyconnect.PlayerEvent.PLAYBACK_VOLUME, callback)
        
        _PlayerCallbacks.playback_volume(39321, session_handle)
        
        callback.assert_called_once_with(60, session)    

    def test_playback_volume_callback_when_no_instance(self, lib_mock):
        callback = mock.Mock()
        session = tests.create_real_player(lib_mock)
        spotifyconnect._session_instance = None
        session_handle = spotifyconnect.ffi.new_handle(session)
        session.player.on(spotifyconnect.PlayerEvent.PLAYBACK_VOLUME, callback)        
        
        _PlayerCallbacks.playback_volume(39321, session_handle)
                
        self.assertFalse(callback.called)    

class PlaybackNotifyTest(unittest.TestCase):    
    
    def test_has_notify_constants(self):
        self.assertEqual(spotifyconnect.PlaybackNotify.Play, 0)
        self.assertEqual(spotifyconnect.PlaybackNotify.Pause, 1)
        self.assertEqual(spotifyconnect.PlaybackNotify.TrackChanged, 2)
        self.assertEqual(spotifyconnect.PlaybackNotify.Next, 3)
        self.assertEqual(spotifyconnect.PlaybackNotify.Prev, 4)
        self.assertEqual(spotifyconnect.PlaybackNotify.ShuffleEnabled, 5)
        self.assertEqual(spotifyconnect.PlaybackNotify.ShuffleDisabled, 6)
        self.assertEqual(spotifyconnect.PlaybackNotify.RepeatEnabled, 7)
        self.assertEqual(spotifyconnect.PlaybackNotify.RepeatDisabled, 8)
        self.assertEqual(spotifyconnect.PlaybackNotify.BecameActive, 9)
        self.assertEqual(spotifyconnect.PlaybackNotify.BecameInactive, 10)
        self.assertEqual(spotifyconnect.PlaybackNotify.PlayTokenLost, 11)
        self.assertEqual(spotifyconnect.PlaybackNotify.AudioFlush, 12)
        