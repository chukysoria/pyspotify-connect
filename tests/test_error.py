from __future__ import unicode_literals

import unittest

import spotifyconnect
from spotifyconnect import utils


class ErrorTest(unittest.TestCase):

    def test_error_is_an_exception(self):
        error = spotifyconnect.Error(0)
        self.assertIsInstance(error, Exception)

    def test_maybe_raise(self):
        with self.assertRaises(spotifyconnect.LibError):
            spotifyconnect.Error.maybe_raise(spotifyconnect.ErrorType.WrongAPIVersion)

    def test_maybe_raise_does_not_raise_if_ok(self):
        spotifyconnect.Error.maybe_raise(spotifyconnect.ErrorType.Ok)

    def test_maybe_raise_does_not_raise_if_error_is_ignored(self):
        spotifyconnect.Error.maybe_raise(
            spotifyconnect.ErrorType.WrongAPIVersion,
            ignores=[spotifyconnect.ErrorType.WrongAPIVersion])

    def test_maybe_raise_works_with_any_iterable(self):
        spotifyconnect.Error.maybe_raise(
            spotifyconnect.ErrorType.WrongAPIVersion,
            ignores=(spotifyconnect.ErrorType.WrongAPIVersion,))


class LibErrorTest(unittest.TestCase):

    def test_is_an_error(self):
        error = spotifyconnect.LibError(0)
        self.assertIsInstance(error, spotifyconnect.Error)

    def test_has_error_type(self):
        error = spotifyconnect.LibError(0)
        self.assertEqual(error.error_type, 0)

        error = spotifyconnect.LibError(1)
        self.assertEqual(error.error_type, 1)

    def test_is_equal_if_same_error_type(self):
        self.assertEqual(spotifyconnect.LibError(0), spotifyconnect.LibError(0))

    def test_is_not_equal_if_different_error_type(self):
        self.assertNotEqual(spotifyconnect.LibError(0), spotifyconnect.LibError(1))

    def test_error_has_useful_repr(self):
        error = spotifyconnect.LibError(0)
        self.assertIn('Ok', repr(error))

    def test_error_has_useful_string_representation(self):
        error = spotifyconnect.LibError(0)
        self.assertEqual('%s' % error, 'Ok')
        self.assertIsInstance('%s' % error, utils.text_type)

        error = spotifyconnect.LibError(3)
        self.assertEqual('%s' % error, 'WrongAPIVersion')

    def test_has_error_constants(self):
        self.assertEqual(
            spotifyconnect.LibError.Ok, spotifyconnect.LibError(spotifyconnect.ErrorType.Ok))
        self.assertEqual(
            spotifyconnect.LibError.WrongAPIVersion,
            spotifyconnect.LibError(spotifyconnect.ErrorType.WrongAPIVersion))


class ErrorTypeTest(unittest.TestCase):

    def test_has_error_type_constants(self):
        self.assertEqual(spotifyconnect.ErrorType.Ok, 0)
        self.assertEqual(spotifyconnect.ErrorType.Failed, 1)
        self.assertEqual(spotifyconnect.ErrorType.InitFailed, 2)
        self.assertEqual(spotifyconnect.ErrorType.WrongAPIVersion, 3)
        self.assertEqual(spotifyconnect.ErrorType.NullArgument, 4)
        self.assertEqual(spotifyconnect.ErrorType.InvalidArgument, 5)
        self.assertEqual(spotifyconnect.ErrorType.Uninitialized, 6)
        self.assertEqual(spotifyconnect.ErrorType.AlreadyInitialized, 7)
        self.assertEqual(spotifyconnect.ErrorType.LoginBadCredentials, 8)
        self.assertEqual(spotifyconnect.ErrorType.NeedsPremium, 9)
        self.assertEqual(spotifyconnect.ErrorType.TravelRestriction, 10)
        self.assertEqual(spotifyconnect.ErrorType.ApplicationBanned, 11)
        self.assertEqual(spotifyconnect.ErrorType.GeneralLoginError, 12)
        self.assertEqual(spotifyconnect.ErrorType.Unsupported, 13)
        self.assertEqual(spotifyconnect.ErrorType.NotActiveDevice, 14)
        self.assertEqual(spotifyconnect.ErrorType.PlaybackErrorStart, 1000)
        self.assertEqual(spotifyconnect.ErrorType.GeneralPlaybackError, 1001)
        self.assertEqual(spotifyconnect.ErrorType.PlaybackRateLimited, 1002)
        self.assertEqual(spotifyconnect.ErrorType.Unknown, 1003)
        

class TimeoutTest(unittest.TestCase):

    def test_is_an_error(self):
        error = spotifyconnect.Timeout(0.5)
        self.assertIsInstance(error, spotifyconnect.Error)

    def test_has_useful_repr(self):
        error = spotifyconnect.Timeout(0.5)
        self.assertIn('Operation did not complete in 0.500s', repr(error))

    def test_has_useful_string_representation(self):
        error = spotifyconnect.Timeout(0.5)
        self.assertEqual('%s' % error, 'Operation did not complete in 0.500s')
        self.assertIsInstance('%s' % error, utils.text_type)
