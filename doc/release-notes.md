Groestlcoin Core version *2.18.1* is now available from:

  <https://groestlcoin.org/downloads/>

This is a new major version release, including new features, various bugfixes
and performance improvements, as well as updated translations.

Please report bugs using the issue tracker at GitHub:

  <https://github.com/groestlcoin/groestlcoin/issues>

How to Upgrade
==============

If you are running an older version, shut it down. Wait until it has
completely shut down (which might take a few minutes for older
versions), then run the installer (on Windows) or just copy over
`/Applications/Groestlcoin-Qt` (on Mac) or `groestlcoind`/`groestlcoin-qt` (on
Linux).

The first time you run version 2.16.0 or newer, your chainstate database
will be converted to a new format, which will take anywhere from a few
minutes to half an hour, depending on the speed of your machine.

Note that the block database format also changed in version 2.1.0.6 and
there is no automatic upgrade code from before version 2.1.0.6 to version
2.16.0 or later.

Compatibility
==============

Groestlcoin Core is supported and extensively tested on operating systems
using the Linux kernel, macOS 10.10+, and Windows 7 and newer. It is not
recommended to use Groestlcoin Core on unsupported systems.

Groestlcoin Core should also work on most other Unix-like systems but is not
as frequently tested on them.

From 2.17.2 onwards, macOS <10.10 is no longer supported. 2.17.2 is
built using Qt 5.9.x, which doesn't support versions of macOS older than
10.10. Additionally, Groestlcoin Core does not yet change appearance when
macOS "dark mode" is activated.

Known issues
============

Wallet GUI
----------

For advanced users who have both (1) enabled coin control features, and
(2) are using multiple wallets loaded at the same time: The coin control
input selection dialog can erroneously retain wrong-wallet state when
switching wallets using the dropdown menu. For now, it is recommended
not to use coin control features with multiple wallets loaded.

Notable changes
===============


0.18.x change log
=================
