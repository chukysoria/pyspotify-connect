FROM chukysoria/armhf-python:latest
MAINTAINER Carlos Sánchez

RUN pip install tox
ADD https://github.com/sashahilton00/spotify-connect-resources/raw/master/libs/armhf/armv7/release-esdk-1.20.0-v1.20.0-g594175d4/libspotify_embedded_shared.so /usr/lib/

WORKDIR /usr/src/pyspotify-connect

ENTRYPOINT ["/bin/bash"]
