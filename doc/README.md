Groestlcoin Core
=============

Setup
---------------------
Groestlcoin Core is the original Groestlcoin client and it builds the backbone of the network. It downloads and, by default, stores the entire history of Groestlcoin transactions (which is currently more than 2 GB); depending on the speed of your computer and network connection, the synchronization process can take anywhere from a few hours.

To download Groestlcoin Core, visit [groestlcoin.org](https://groestlcoin.org/downloads/).

Running
---------------------
The following are some helpful notes on how to run Groestlcoin on your native platform.

### Unix

Unpack the files into a directory and run:

- `bin/groestlcoin-qt` (GUI) or
- `bin/groestlcoind` (headless)

### Windows

Unpack the files into a directory, and then run groestlcoin-qt.exe.

### macOS

Drag Groestlcoin-Core to your applications folder, and then run Groestlcoin-Core.

### Need Help?

* Ask for help on #groestlcoin on Libera Chat. If you don't have an IRC client, you can use [web.libera.chat](https://web.libera.chat/#groestlcoin).
* Ask for help on the [GroestlTalk](https://groestlcointalk.org/) forum or in in the [Alternate cryptocurrencies board](https://bitcointalk.org/index.php?topic=525926.0).

Building
---------------------
The following are developer notes on how to build Groestlcoin on your native platform. They are not complete guides, but include notes on the necessary libraries, compile flags, etc.

- [Dependencies](dependencies.md)
- [macOS Build Notes](build-osx.md)
- [Unix Build Notes](build-unix.md)
- [Windows Build Notes](build-windows.md)
- [FreeBSD Build Notes](build-freebsd.md)
- [OpenBSD Build Notes](build-openbsd.md)
- [NetBSD Build Notes](build-netbsd.md)
- [Android Build Notes](build-android.md)

Development
---------------------
The Groestlcoin repo's [root README](/README.md) contains relevant information on the development process and automated testing.

- [Developer Notes](developer-notes.md)
- [Productivity Notes](productivity.md)
- [Release Notes](release-notes.md)
- [Release Process](release-process.md)
- [Translation Process](translation_process.md)
- [Translation Strings Policy](translation_strings_policy.md)
- [JSON-RPC Interface](JSON-RPC-interface.md)
- [Unauthenticated REST Interface](REST-interface.md)
- [Shared Libraries](shared-libraries.md)
- [BIPS](bips.md)
- [Dnsseed Policy](dnsseed-policy.md)
- [Benchmarking](benchmarking.md)

### Miscellaneous
- [Assets Attribution](assets-attribution.md)
- [Assumeutxo design](assumeutxo.md)
- [groestlcoin.conf Configuration File](groestlcoin-conf.md)
- [Files](files.md)
- [Fuzz-testing](fuzzing.md)
- [I2P Support](i2p.md)
- [Init Scripts (systemd/upstart/openrc)](init.md)
- [Managing Wallets](managing-wallets.md)
- [PSBT support](psbt.md)
- [Reduce Memory](reduce-memory.md)
- [Reduce Traffic](reduce-traffic.md)
- [Tor Support](tor.md)
- [ZMQ](zmq.md)

License
---------------------
Distributed under the [MIT software license](/COPYING).
