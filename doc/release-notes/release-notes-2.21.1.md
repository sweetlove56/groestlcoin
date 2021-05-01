Groestlcoin Core version 2.21.1 is now available from:

  <https://groestlcoin.org/downloads/>

This release includes new features, various bug fixes and performance
improvements, as well as updated translations.

Please report bugs using the issue tracker at GitHub:

  <https://github.com/groestlcoin/groestlcoin/issues>

How to Upgrade
==============

If you are running an older version, shut it down. Wait until it has completely
shut down (which might take a few minutes in some cases), then run the
installer (on Windows) or just copy over `/Applications/Groestlcoin-Qt` (on Mac)
or `groestlcoind`/`groestlcoin-qt` (on Linux).

Upgrading directly from a version of Groestlcoin Core that has reached its EOL is
possible, but it might take some time if the data directory needs to be migrated.
Old wallet versions of Groestlcoin Core are generally supported.

Compatibility
==============

Groestlcoin Core is supported and extensively tested on operating systems
using the Linux kernel, macOS 10.12+, and Windows 7 and newer. Groestlcoin
Core should also work on most other Unix-like systems but is not as
frequently tested on them.  It is not recommended to use Groestlcoin Core on
unsupported systems.

From Groestlcoin Core 2.20.1 onwards, macOS versions earlier than 10.12 are no
longer supported. Additionally, Groestlcoin Core does not yet change appearance
when macOS "dark mode" is activated.

Notable changes
===============

## Taproot Soft Fork changes

Activation for taproot is now being managed using a variation of BIP9
versionbits called Speedy Trial (described in BIP341). Taproot's
versionbit is bit 2, and nodes will begin tracking which blocks signal
support for taproot at the beginning of the first retarget period after
taproot’s start date of 15 December 2020.  If 90% of blocks within a
2,016-block retarget period (about 1,5 days) signal support for taproot,
the soft fork will be locked in, and taproot will then be active.

Should taproot not be locked in via Speedy Trial activation, it is
expected that a follow-up activation mechanism will be deployed, with
changes to address the reasons the Speedy Trial method failed.

Updated RPCs
------------

- Due to [BIP 350](https://github.com/bitcoin/bips/blob/master/bip-0350.mediawiki)
  being implemented, behavior for all RPCs that accept addresses is changed when
  a native witness version 1 (or higher) is passed. These now require a Bech32m
  encoding instead of a Bech32 one, and Bech32m encoding will be used for such
  addresses in RPC output as well. No version 1 addresses should be created
  for mainnet until consensus rules are adopted that give them meaning
  (e.g. through [BIP 341](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki)).
  Once that happens, Bech32m is expected to be used for them, so this shouldn't
  affect any production systems, but may be observed on other networks where such
  addresses already have meaning (like signet).
