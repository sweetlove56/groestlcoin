NetBSD build guide
======================
(updated for NetBSD 8.0)

This guide describes how to build groestlcoind and command-line utilities on NetBSD.

This guide does not contain instructions for building the GUI.

Preparation
-------------

You will need the following modules, which can be installed via pkgsrc or pkgin:

```
autoconf
automake
boost
git
gmake
libevent
libtool
pkg-config
python37

git clone https://github.com/groestlcoin/groestlcoin
```

See [dependencies.md](dependencies.md) for a complete overview.

### Building Groestlcoin Core

**Important**: Use `gmake` (the non-GNU `make` will exit with an error).

With wallet:
```
./autogen.sh
./configure --with-gui=no CPPFLAGS="-I/usr/pkg/include" \
    LDFLAGS="-L/usr/pkg/lib" \
    BOOST_CPPFLAGS="-I/usr/pkg/include" \
    BOOST_LDFLAGS="-L/usr/pkg/lib"
```

Without wallet:
```
./autogen.sh
./configure --with-gui=no --disable-wallet \
    CPPFLAGS="-I/usr/pkg/include" \
    LDFLAGS="-L/usr/pkg/lib" \
    BOOST_CPPFLAGS="-I/usr/pkg/include" \
    BOOST_LDFLAGS="-L/usr/pkg/lib"
```

Build and run the tests:
```bash
gmake # use -jX here for parallelism
gmake check
```
