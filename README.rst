*****************
pyspotify-connect
*****************

pyspotify-connect provides a Python interface to `Spotify Connect's <http://www.spotify.com/>`_ online music streaming service.

With pyspotify-connect you can create a Spotify Connect player on your device.
All from your own Python applications.

pyspotify-connect uses `CFFI <https://cffi.readthedocs.org/>`_ to make a pure Python
wrapper around the `libspotify_embedded_shared` library. It has been tested on
on CPython 2.7 and 3.4, as well as PyPy 2.6. The library is only available for arm
linux architectures: armv6 armel and armv7 armhf.

This wrapper is heavily based on the 
`pyspotify <https://github.com/mopidy/pyspotify>`_ wrapper for libspotify and
the spotify-connect implementation 
`Spotify Connect Web <https://github.com/Fornoth/spotify-connect-web>`_.

Dependencies
============

- A Spotify Premium subscription. pyspotify-connect **will not** work with Spotify
  Free, just Spotify Premium.

- ``libspotify_embeded_shared``, see below for instructions.

- Developmente packages for python and libffi. For example, for python 2.7 on Debian/Raspbian: 

  ``apt-get install python-dev libffi-dev``

Spotify Connect Library
=======================

As Spotify Connect library is not available directly from spotify you should 
grab it from one of the links below depending you Linux version.

- `armel - armv6 <https://github.com/sashahilton00/spotify-connect-resources/raw/master/libs/armel/armv6/release-esdk-1.18.0-v1.18.0-g121b4b2b/libspotify_embedded_shared.so>`_
- `armhf - armv7 <https://github.com/sashahilton00/spotify-connect-resources/raw/master/libs/armhf/armv7/release-esdk-1.20.0-v1.20.0-g594175d4/libspotify_embedded_shared.so>`_

Copy the appropiated library for your architecture to ``/usr/lib``.

Installation
============

Install the dependencies listed above yourself, and then install the
package from PyPI::

    pip install pyspotify-connect


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

.. image:: https://img.shields.io/travis/chukysoria/pyspotify-connect.svg
    :target: https://travis-ci.org/chukysoria/pyspotify-connect

.. image:: https://img.shields.io/coveralls/chukysoria/pyspotify-connect.svg?maxAge=2592000
    :target: https://coveralls.io/github/chukysoria/pyspotify-connect?branch=master
