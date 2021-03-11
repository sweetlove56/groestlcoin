# macOS Build Instructions and Notes

The commands in this guide should be executed in a Terminal application.
The built-in one is located in
```
/Applications/Utilities/Terminal.app
```

## Preparation
Install the macOS command line tools:

```shell
xcode-select --install
```

When the popup appears, click `Install`.

Then install [Homebrew](https://brew.sh).

## Dependencies
```shell
brew install automake libtool boost miniupnpc libnatpmp pkg-config python qt@5 libevent qrencode
```

If you run into issues, check [Homebrew's troubleshooting page](https://docs.brew.sh/Troubleshooting).
See [dependencies.md](dependencies.md) for a complete overview.

If you want to build the disk image with `make deploy` (.dmg / optional), you need RSVG:
```shell
brew install librsvg
```

and [`macdeployqtplus`](../contrib/macdeploy/README.md) dependencies:
```shell
pip3 install ds_store mac_alias
```

The wallet support requires one or both of the dependencies ([*SQLite*](#sqlite) and [*Berkeley DB*](#berkeley-db)) in the sections below.
To build Groestlcoin Core without wallet, see [*Disable-wallet mode*](#disable-wallet-mode).

#### SQLite

Usually, macOS installation already has a suitable SQLite installation.
Also, the Homebrew package could be installed:

```shell
brew install sqlite
```

In that case the Homebrew package will prevail.

#### Berkeley DB

It is recommended to use Berkeley DB 5.3. If you have to build it yourself,
you can use [this](/contrib/install_db5.sh) script to install it
like so:

```shell
./contrib/install_db5.sh .
```

**Note**: You only need Berkeley DB if the wallet is enabled (see the section *Disable-Wallet mode* below).

Also, the Homebrew package could be installed:

```shell
brew tap zeroc-ice/tap
brew install zeroc-ice/tap/berkeley-db@5.3
```

## Build Groestlcoin Core

1. Clone the Groestlcoin Core source code:
    ```shell
    git clone https://github.com/groestlcoin/groestlcoin
    cd groestlcoin
    ```

2.  Build Groestlcoin Core:

    Configure and build the headless Groestlcoin Core binaries as well as the GUI (if Qt is found).

    You can disable the GUI build by passing `--without-gui` to configure.
    ```shell
    ./autogen.sh
    ./configure LDFLAGS=-L/usr/local/opt/berkeley-db@5.3/lib CPPFLAGS=-I/usr/local/opt/berkeley-db@5.3/include
    make
    ```

3.  You can also create a  `.dmg` that contains the `.app` bundle (optional):
    ```shell
    make deploy
    ```

## Disable-wallet mode
When the intention is to run only a P2P node without a wallet, Groestlcoin Core may be
compiled in disable-wallet mode with:
```shell
./configure --disable-wallet
```

In this case there is no dependency on [*Berkeley DB*](#berkeley-db) and [*SQLite*](#sqlite).

Mining is also possible in disable-wallet mode using the `getblocktemplate` RPC call.

## Running
Groestlcoin Core is now available at `./src/groestlcoind`

Before running, you may create an empty configuration file:
```shell
mkdir -p "/Users/${USER}/Library/Application Support/Groestlcoin"

touch "/Users/${USER}/Library/Application Support/Groestlcoin/groestlcoin.conf"

chmod 600 "/Users/${USER}/Library/Application Support/Groestlcoin/groestlcoin.conf"
```

The first time you run groestlcoind, it will start downloading the blockchain. This process could
take several hours.

You can monitor the download process by looking at the debug.log file:
```shell
tail -f $HOME/Library/Application\ Support/Groestlcoin/debug.log
```

## Other commands:
```shell
./src/groestlcoind -daemon      # Starts the groestlcoin daemon.
./src/groestlcoin-cli --help    # Outputs a list of command-line options.
./src/groestlcoin-cli help      # Outputs a list of RPC commands when the daemon is running.
```

## Notes
* Tested on OS X 10.14 Mojave through macOS 11 Big Sur on 64-bit Intel
processors only.
* Building with downloaded Qt binaries is not officially supported. See the notes in [#7714](https://github.com/bitcoin/bitcoin/issues/7714).
