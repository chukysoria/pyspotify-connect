*****************
pyspotify-connect
*****************

pyspotify-connect provides a Python interface to `Spotify Connect's <http://www.spotify.com/>`_ online music streaming service.

With pyspotify-connect you can create a Spotify Connect player on your device.
All from your own Python applications.

pyspotify-connect uses `CFFI <https://cffi.readthedocs.org/>`_ to make a pure Python
wrapper around the `libspotify_embedded_shared` library. It works
on CPython 2.7 and 3.3+, as well as PyPy 2.6+ and PyPy3 2.5+.  It is known to
work only on Linux.

This wrapper is heavily based on the 
`pyspotify <https://github.com/mopidy/pyspotify>`_ wrapper for libspotify and
the spotify-connect implementation 
`Spotify Connect Web <https://github.com/Fornoth/spotify-connect-web>`_.

Dependencies
============

- A Spotify Premium subscription. pyspotify-connect **will not** work with Spotify
  Free, just Spotify Premium.

- ``libspotify_embeded_shared``, see below for instructions..

Spotify Connect Library
=======================

As Spotify Connect library is not available directly from spotify you should 
grab it from one of the links below depending you Linux version.

- `armel - armv6 <https://github.com/sashahilton00/spotify-connect-resources/blob/master/libs/armel/armv6/release-esdk-1.18.0-v1.18.0-g121b4b2b/libspotify_embedded_shared.so>`_
- `armhf - armv7 <https://github.com/sashahilton00/spotify-connect-resources/tree/master/libs/armhf/armv7/release-esdk-1.20.0-v1.20.0-g594175d4>`_

Copy the appropiated library for your architecture to ``\usr\lib``.

Installation
============

Install the dependencies listed above yourself, and then install the
package from PyPI::

    pip install pyspotify


Project resources
=================

- `Source code <https://github.com/chukysoria/pyspotify-connect>`_
- `Issue tracker <https://github.com/chukysoria/pyspotify-connect/issues>`_
- `Spotify Connect resources <https://github.com/sashahilton00/spotify-connect-resources>`_

.. image:: https://img.shields.io/pypi/v/pyspotify-connect.svg?style=flat
    :target: https://pypi.python.org/pypi/pyspotify-connect
 
.. image:: https://img.shields.io/pypi/status/pyspotify-connect.svg?style=flat
    :target: https://pypi.python.org/pypi/pyspotify-connect
 
.. image:: https://img.shields.io/pypi/dm/pyspotify-connect.svg?style=flat
    :target: https://pypi.python.org/pypi/pyspotify-connect
