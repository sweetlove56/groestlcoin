macOS Build Instructions and Notes
====================================
The commands in this guide should be executed in a Terminal application.
The built-in one is located in `/Applications/Utilities/Terminal.app`.

Preparation
-----------
Install the macOS command line tools:

`xcode-select --install`

When the popup appears, click `Install`.

Then install [Homebrew](https://brew.sh).

Dependencies
----------------------

    brew install automake libtool boost miniupnpc openssl pkg-config protobuf python3 qt libevent qrencode

See [dependencies.md](dependencies.md) for a complete overview.

If you want to build the disk image with `make deploy` (.dmg / optional), you need RSVG

    brew install librsvg

Berkeley DB
It is recommended to use Berkeley DB 5.3

```shell
brew tap zeroc-ice/tap
brew install zeroc-ice/tap/berkeley-db@5.3
```

**Note**: You only need Berkeley DB if the wallet is enabled (see the section *Disable-Wallet mode* below).

Build Groestlcoin Core
------------------------

1. Clone the groestlcoin source code and cd into `groestlcoin`

        git clone https://github.com/Groestlcoin/groestlcoin.git
        cd groestlcoin

2.  Build groestlcoin-core:

    Configure and build the headless Groestlcoin Core binaries as well as the GUI (if Qt is found).

    You can disable the GUI build by passing `--without-gui` to configure.

        ./autogen.sh
        ./configure LDFLAGS=-L/usr/local/opt/berkeley-db@5.3/lib CPPFLAGS=-I/usr/local/opt/berkeley-db@5.3/include
        make

3.  You can also create a .dmg that contains the .app bundle (optional):

        make deploy

Running
-------

Groestlcoin Core is now available at `./src/groestlcoind`

Before running, it's recommended that you create an RPC configuration file.

    echo -e "rpcuser=groestlcoinrpc\nrpcpassword=$(xxd -l 16 -p /dev/urandom)" > "/Users/${USER}/Library/Application Support/Groestlcoin/groestlcoin.conf"

    chmod 600 "/Users/${USER}/Library/Application Support/Groestlcoin/groestlcoin.conf"

The first time you run groestlcoind, it will start downloading the blockchain. This process could take several hours.

You can monitor the download process by looking at the debug.log file:
    tail -f $HOME/Library/Application\ Support/Groestlcoin/debug.log

Once dependencies are compiled, see [doc/release-process.md](release-process.md) for how the Groestlcoin-Qt.app
bundle is packaged and signed to create the .dmg disk image that is distributed.

Other commands:
-------

    ./src/groestlcoind -daemon # Starts the groestlcoin daemon.
    ./src/groestlcoin-cli --help # Outputs a list of command-line options.
    ./src/groestlcoin-cli help # Outputs a list of RPC commands when the daemon is running.

Notes
-----

* Tested on OS X 10.10 Yosemite through macOS 10.13 High Sierra on 64-bit Intel processors only.

* Building with downloaded Qt binaries is not officially supported. See the notes in [#7714](https://github.com/bitcoin/bitcoin/issues/7714)
