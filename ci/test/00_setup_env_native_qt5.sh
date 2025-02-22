#!/usr/bin/env bash
#
# Copyright (c) 2019-2021 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

export LC_ALL=C.UTF-8

export CONTAINER_NAME=ci_native_qt5
export DOCKER_NAME_TAG=debian:buster  # Check that buster gcc-8 can compile our C++17 and run our functional tests in python3, see doc/dependencies.md
export PACKAGES="gcc-8 g++-8 python3-zmq qtbase5-dev qttools5-dev-tools libdbus-1-dev libharfbuzz-dev"
export DEP_OPTS="NO_QT=1 NO_UPNP=1 NO_NATPMP=1 DEBUG=1 ALLOW_HOST_PACKAGES=1 CC=gcc-8 CXX=g++-8"
export GOAL="install"
export PREVIOUS_RELEASES_TO_DOWNLOAD="v2.17.2 v2.18.2 v2.19.1 v2.20.1 v2.21.1 v22.0"
export GROESTLCOIN_CONFIG="--enable-zmq --with-libs=no --with-gui=qt5 --enable-reduce-exports \
--enable-debug CFLAGS=\"-g0 -O2 -funsigned-char\" CXXFLAGS=\"-g0 -O2 -funsigned-char\" CC=gcc-8 CXX=g++-8"
