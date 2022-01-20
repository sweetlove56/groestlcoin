#!/usr/bin/env bash
#
# Copyright (c) 2018-2021 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

export LC_ALL=C.UTF-8

if [[ $HOST = *-mingw32 ]]; then
  # Generate all binaries, so that they can be wrapped
  DOCKER_EXEC make "$MAKEJOBS" -C src/secp256k1 VERBOSE=1
  DOCKER_EXEC "${BASE_ROOT_DIR}/ci/test/wrap-wine.sh"
fi

if [ -n "$QEMU_USER_CMD" ]; then
  # Generate all binaries, so that they can be wrapped
  DOCKER_EXEC make "$MAKEJOBS" -C src/secp256k1 VERBOSE=1
  DOCKER_EXEC "${BASE_ROOT_DIR}/ci/test/wrap-qemu.sh"
fi

if [ "$RUN_SECURITY_TESTS" = "true" ]; then
  DOCKER_EXEC make test-security-check
fi
