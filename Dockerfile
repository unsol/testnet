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

ADD setup.sh setup.sh
RUN ./setup.sh

RUN mkdir -p /opt/ewasm-testnet
WORKDIR /opt/ewasm-testnet

ADD cpp-eth.sh cpp-eth.sh

EXPOSE 8545 30303

ENTRYPOINT ["./cpp-eth.sh"]
