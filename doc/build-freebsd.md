FreeBSD build guide
======================
(updated for FreeBSD 12.0)

This guide describes how to build groestlcoind and command-line utilities on FreeBSD.

This guide does not contain instructions for building the GUI.

## Preparation

You will need the following dependencies, which can be installed as root via pkg:

```shell
pkg install autoconf automake boost-libs git gmake libevent libtool openssl pkgconf

git clone https://github.com/bitcoin/bitcoin.git
```
./contrib/install_db5.sh `pwd`
export BDB_PREFIX="$PWD/db5"
```

See [dependencies.md](dependencies.md) for a complete overview.

Download the source code:
```
git clone https://github.com/groestlcoin/groestlcoin
```

## Building Groestlcoin Core

**Important**: Use `gmake` (the non-GNU `make` will exit with an error):

With wallet:
```shell
./autogen.sh
./configure --with-gui=no
```

Without wallet:
```shell
./autogen.sh
./configure --with-gui=no --disable-wallet
```
