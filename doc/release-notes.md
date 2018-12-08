Groestlcoin Core version 2.17.2 is now available from:

  <https://groestlcoin.org/downloads/>

This is a new major version release, including new features, various bugfixes
and performance improvements, as well as updated translations.

Please report bugs using the issue tracker at GitHub:

  <https://github.com/groestlcoin/groestlcoin/issues>

How to Upgrade
==============

If you are running an older version, shut it down. Wait until it has completely
shut down (which might take a few minutes for older versions), then run the
installer (on Windows) or just copy over `/Applications/Groestlcoin-Qt` (on Mac)
or `groestlcoind`/`groestlcoin-qt` (on Linux).

If your node has a txindex, the txindex db will be migrated the first time you run 2.17.2 or newer, which may take up to a few hours. Your node will not be functional until this migration completes.

The first time you run version 2.16.0 or newer, your chainstate database will be converted to a
new format, which will take anywhere from a few minutes to half an hour,
depending on the speed of your machine.

Note that the block database format also changed in version 2.1.0.6 and there is no
automatic upgrade code from before version 2.1.0.6 to version 2.16.3 or higher.
However, as usual, old wallet versions are still supported.

Downgrading warning
-------------------

Wallets created in 2.16.3 and later are not compatible with versions prior to 2.16.3
and will not work if you try to use newly created wallets in older versions. Existing
wallets that were created with older versions are not affected by this.

Compatibility
==============

Groestlcoin Core is extensively tested on multiple operating systems using
the Linux kernel, macOS 10.10+, and Windows 7 and newer (Windows XP is not supported).

Groestlcoin Core should also work on most other Unix-like systems but is not
frequently tested on them.

From 2.17.2 onwards macOS <10.10 is no longer supported. 2.17.2 is built using Qt 5.9.x, which doesn't
support versions of macOS older than 10.10.

Notable changes
===============

`listtransactions` label support
--------------------------------

The `listtransactions` RPC `account` parameter which was deprecated in 0.17.0
and renamed to `dummy` has been un-deprecated and renamed again to `label`.

When bitcoin is configured with the `-deprecatedrpc=accounts` setting, specifying
a label/account/dummy argument will return both outgoing and incoming
transactions. Without the `-deprecatedrpc=accounts` setting, it will only return
incoming transactions (because it used to be possible to create transactions
spending from specific accounts, but this is no longer possible with labels).

When `-deprecatedrpc=accounts` is set, it's possible to pass the empty string ""
to list transactions that don't have any label. Without
`-deprecatedrpc=accounts`, passing the empty string is an error because returning
only non-labeled transactions is not generally useful behavior and can cause
confusion.
