*********
pyspotify-connect
*********

pyspotify-connect provides a Python interface to
`Spotify Connect's <http://www.spotify.com/>`__ online music streaming service.

With pyspotify-connect you can create a Spotify Connect player oon your device.
 All from your own Python applications.

pyspotify use `CFFI <https://cffi.readthedocs.org/>`_ to make a pure Python
wrapper around the `libspotify-connect`__ library. It works
on CPython 2.7 and 3.3+, as well as PyPy 2.6+ and PyPy3 2.5+.  It is known to
work on Linux.

This wrapper is heavily based on the 
`pyspotify <https://github.com/mopidy/pyspotify>`_ wrapper for libspotify and
the spotify-connect implementation 
`<https://github.com/chukysoria/spotify-connect-web>`_

Spotify Connect Library
=======================

As Spotify Connect library is not available directly from spotify you should 
grab it from one of the links below depending you Linux version.

- `armel - armv6 <https://github.com/sashahilton00/spotify-connect-resources/blob/master/libs/armel/armv6/release-esdk-1.18.0-v1.18.0-g121b4b2b/libspotify_embedded_shared.so>`_
- `armhf - armv7 <https://github.com/sashahilton00/spotify-connect-resources/tree/master/libs/armhf/armv7/release-esdk-1.20.0-v1.20.0-g594175d4>`_

Project resources
=================

- `Source code <https://github.com/chukysoria/pyspotify-connect>`_
- `Issue tracker <https://github.com/chukysoria/pyspotify-connect/issues>`_
- `Spotify Connect resources <https://github.com/sashahilton00/spotify-connect-resources>`_