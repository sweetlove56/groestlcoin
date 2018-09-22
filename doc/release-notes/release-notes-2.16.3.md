Groestlcoin Core version *2.16.3* is now available from:

  <https://groestlcoin.org/downloads/>

This is a new minor version release, including various bugfixes and performance improvements, as well as updated translations.

Please report bugs using the issue tracker at GitHub:

  <https://github.com/groestlcoin/groestlcoin/issues>

How to Upgrade
==============

If you are running an older version, shut it down. Wait until it has completely
shut down (which might take a few minutes for older versions), then run the
installer (on Windows) or just copy over `/Applications/Groestlcoin-Qt` (on Mac)
or `groestlcoind`/`groestlcoin-qt` (on Linux).

The first time you run version 2.16.x, your chainstate database will
be converted to a new format, which will take anywhere from a few minutes to
half an hour, depending on the speed of your machine.

The file format of `fee_estimates.dat` changed in version 2.16.0. Hence, a
downgrade from version 2.16.x or upgrade to version 2.16.x will cause all fee
estimates to be discarded.

Downgrading warning
-------------------

Wallets created in 2.16.x and later are not compatible with versions prior to 2.16.x and will not work if you try to use newly created wallets in older versions. Existing wallets that were created with older versions are not affected by this.

Compatibility
==============

Groestlcoin Core is extensively tested on multiple operating systems using
the Linux kernel, macOS 10.8+, and Windows Vista and later. Windows XP is not supported.

Groestlcoin Core should also work on most other Unix-like systems but is not
frequently tested on them.


Notable changes
===============

Miner block size removed
------------------------

The `-blockmaxsize` option for miners to limit their blocks' sizes has been removed.
Miners should use the `-blockmaxweight` option if they want to limit the weight of their blocks' weights.

Denial-of-Service vulnerability
-------------------------------

A denial-of-service vulnerability (CVE-2018-17144) exploitable by miners has
been discovered in Groestlcoin Core versions 2.13.3 up to 2.16.0. It is recommended
to upgrade any of the vulnerable versions to 2.16.3 as soon as possible.
