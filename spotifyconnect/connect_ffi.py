import os

from cffi import FFI


ffi = FFI()

# Header generated with cpp spotify.h > spotify.processed.h && sed -i 's/__extension__//g' spotify.processed.h
with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "spotify.processed.h")) as header_file:
    header = header_file.read()

ffi.cdef(header)
ffi.cdef("""
void *malloc(size_t size);
void exit(int status);
""")

C = ffi.dlopen(None)
lib = ffi.verify("""
    #include "spotify.h"
""", include_dirs=['./'],
    library_dirs=['./'],
    libraries=[str('spotify_embedded_shared')])
