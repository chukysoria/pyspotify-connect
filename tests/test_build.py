import unittest
from tests import mock


class BuildTests(unittest.TestCase):

    @mock.patch('os.getenv')
    def test_travis_deploy_exception(self, os_env):
        os_env.return_value = 'travis'

        from spotifyconnect._spotifyconnect_build import machine

        os_env.assert_called_once_with('DEPLOY')
        self.assertEqual(machine, 'armv7l')

    @mock.patch('platform.machine')
    def test_platform_exception(self, platform):
        platform.return_value = 'x86_64'

        with self.assertRaises(RuntimeError):
            import spotifyconnect._spotifyconnect_build  # noqa
