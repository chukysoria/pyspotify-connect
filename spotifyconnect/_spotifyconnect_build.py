import os
import platform

from distutils.version import StrictVersion

import cffi


if StrictVersion(cffi.__version__) < StrictVersion('1.0.0'):
    raise RuntimeError(
        'pyspotify-connect requires cffi >= 1.0, but found %s' % cffi.__version__)

#Options are armv6l or armv7l
machine = str(platform.machine())
if machine == 'armv6l' or machine == 'armv7l':
    header = '#include "spotify.%s.h"' % machine
    header_processed = 'spotify.processed.%s.h' % machine
else:
    raise RuntimeError('pyspotify-connect not available for platform %s' % machine)   

header_file = os.path.join(os.path.dirname(__file__), header_processed)

with open(header_file) as fh:
    header = fh.read()

ffi = cffi.FFI()
ffi.cdef(header)
ffi.cdef("""
void *malloc(size_t size);
void exit(int status);
""")

ffi.set_source(
    'spotifyconnect._spotifyconnect', header, libraries=['spotify_embedded_shared'], include_dirs=[os.path.dirname(__file__)])

if __name__ == '__main__':
    ffi.compile()
