# Docker container spec for building the develop branch of cpp-ethereum.
#
# The build process it potentially longer running but every effort was made to
# produce a very minimalistic container that can be reused many times without
# needing to constantly rebuild.
#
# This image is based on
# https://github.com/ethereum/cpp-ethereum/blob/ccac1dd777c5b25de1c0bacc72dbecb6b376689e/scripts/docker/eth-alpine/Dockerfile

FROM ethereum/cpp-build-env

USER root

# Make sure bash, bc and jq is available for easier wrapper implementation
RUN URL=https://github.com/ethereum/cpp-ethereum/releases/download/v1.4.0.dev1/cpp-ethereum-1.4.0.dev1-linux.tar.gz && curl -L $URL | tar xz -C /usr/local \
    && curl https://raw.githubusercontent.com/ethereum/cpp-ethereum/develop/scripts/jsonrpcproxy.py > /usr/local/bin/jsonrpcproxy.py

RUN git clone https://github.com/ewasm/hera && \
		cd hera && \
		git submodule update --init --recursive && \
		cmake -DBUILD_SHARED_LIBS=ON . && \
		make -j8 && \
    cp src/libhera.so /usr/local/lib/libhera.so

RUN curl http://ftp.us.debian.org/debian/pool/main/n/netcat-openbsd/netcat-openbsd_1.105-7_amd64.deb > netcat-openbsd_1.105-7_amd64.deb
RUN dpkg -i netcat-openbsd_1.105-7_amd64.deb

RUN mkdir -p /opt/ewasm-testnet
WORKDIR /opt/ewasm-testnet

ADD cpp-eth.sh cpp-eth.sh

EXPOSE 8545 30303

ENTRYPOINT ["./cpp-eth.sh"]
