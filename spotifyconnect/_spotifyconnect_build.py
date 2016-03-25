import os

from distutils.version import StrictVersion

import cffi


if StrictVersion(cffi.__version__) < StrictVersion('1.0.0'):
    raise RuntimeError(
        'pyspotifyconnect requires cffi >= 1.0, but found %s' % cffi.__version__)


header_file = os.path.join(os.path.dirname(__file__), 'spotify.processed.h')

with open(header_file) as fh:
    header = fh.read()

ffi = cffi.FFI()
ffi.cdef(header)
ffi.cdef("""
void *malloc(size_t size);
void exit(int status);
""")

ffi.set_source(
    'spotifyconnect._spotifyconnect', '#include "spotify.h"', libraries=['spotify_embedded_shared'], include_dirs=[os.path.dirname(__file__)])

if __name__ == '__main__':
    ffi.compile()
