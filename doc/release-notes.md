Groestlcoin Core version *2.17.2* is now available from:

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

If your node has a txindex, the txindex db will be migrated the first time you
run 2.17.2, which may take up to a few hours. Your node will not be
functional until this migration completes.

The first time you run version 2.16.0 or newer, your chainstate database will be converted to a
new format, which will take anywhere from a few minutes to half an hour,
depending on the speed of your machine.

Downgrading warning
-------------------

The chainstate database for this release is not compatible with previous releases, so if you run 2.16.0 and then decide to switch back to any older version, you will need to run the old release with the -reindex-chainstate option to rebuild the chainstate data structures in the old format.
If your node has pruning enabled, this will entail re-downloading and processing the entire blockchain.

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

Documentation
-------------

- A new document introduces Groestlcoin Core's BIP174
  [Partially-Signed Bitcoin Transactions (PSBT)](https://github.com/bitcoin/bitcoin/blob/0.17/doc/psbt.md)
  interface, which is used to allow multiple programs to collaboratively
  work to create, sign, and broadcast new transactions.  This is useful
  for offline (cold storage) wallets, multisig wallets, coinjoin
  implementations, and many other cases where two or more programs need
  to interact to generate a complete transaction.

When groestlcoin is configured with the `-deprecatedrpc=accounts` setting, specifying
a label/account/dummy argument will return both outgoing and incoming
transactions. Without the `-deprecatedrpc=accounts` setting, it will only return
incoming transactions (because it used to be possible to create transactions
spending from specific accounts, but this is no longer possible with labels).

When `-deprecatedrpc=accounts` is set, it's possible to pass the empty string ""
to list transactions that don't have any label. Without
`-deprecatedrpc=accounts`, passing the empty string is an error because returning
only non-labeled transactions is not generally useful behavior and can cause
confusion.
