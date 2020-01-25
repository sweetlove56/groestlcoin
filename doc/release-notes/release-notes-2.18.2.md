Groestlcoin Core version *2.18.2* is now available from:

  <https://groestlcoin.org/downloads/>

This is a new major version release, including new features, various bug
fixes and performance improvements, as well as updated translations.

Please report bugs using the issue tracker at GitHub:

  <https://github.com/groestlcoin/groestlcoin/issues>

How to Upgrade
==============

If you are running an older version, shut it down. Wait until it has completely
shut down (which might take a few minutes for older versions), then run the
installer (on Windows) or just copy over `/Applications/Groestlcoin-Qt` (on Mac)
or `groestlcoind`/`groestlcoin-qt` (on Linux).

The first time you run version 2.16.0 or newer, your chainstate database will be converted to a
new format, which will take anywhere from a few minutes to half an hour,
depending on the speed of your machine.

Compatibility
==============

Groestlcoin Core is supported and extensively tested on operating systems
using the Linux kernel, macOS 10.10+, and Windows 7 and newer. It is not
recommended to use Groestlcoin Core on unsupported systems.

Groestlcoin Core should also work on most other Unix-like systems but is not
frequently tested on them.

From 2.17.2 onwards macOS <10.10 is no longer supported. 2.17.2 is built using Qt 5.9.x, which doesn't
support versions of macOS older than 10.10. Additionally, Groestlcoin Core does not yet change appearance when
macOS "dark mode" is activated.

In addition to previously-supported CPU platforms, this release's
pre-compiled distribution also provides binaries for the RISC-V
platform.

If you are using the `systemd` unit configuration file located at
`contrib/init/groestlcoind.service`, it has been changed to use
`/var/lib/groestlcoind` as the data directory instead of
`~groestlcoin/.groestlcoin`. When switching over to the new configuration file,
please make sure that the filesystem on which `/var/lib/groestlcoind` will
exist has enough space (check using `df -h /var/lib/groestlcoind`), and
optionally copy over your existing data directory. See the [systemd init
file section](#systemd-init-file) for more details.

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

Mining
------

- Calls to `getblocktemplate` will fail if the segwit rule is not
  specified.  Calling `getblocktemplate` without segwit specified is
  almost certainly a misconfiguration since doing so results in lower
  rewards for the miner.  Failed calls will produce an error message
  describing how to enable the segwit rule.

Configuration option changes
----------------------------

- A warning is printed if an unrecognized section name is used in the
  configuration file.  Recognized sections are `[test]`, `[main]`, and
  `[regtest]`.

- Four new options are available for configuring the maximum number of
  messages that ZMQ will queue in memory (the "high water mark") before
  dropping additional messages.  The default value is 1,000, the same as
  was used for previous releases.  See the [ZMQ
  documentation](https://github.com/bitcoin/bitcoin/blob/master/doc/zmq.md#usage)
  for details.

- The `rpcallowip` option can no longer be used to automatically listen
  on all network interfaces.  Instead, the `rpcbind` parameter must be
  used to specify the IP addresses to listen on.  Listening for RPC
  commands over a public network connection is insecure and should be
  disabled, so a warning is now printed if a user selects such a
  configuration.  If you need to expose RPC in order to use a tool like
  Docker, ensure you only bind RPC to your localhost, e.g. `docker run
  [...] -p 127.0.0.1:1441:1441` (this is an extra `:1441` over the
  normal Docker port specification).

- The `rpcpassword` option now causes a startup error if the password
  set in the configuration file contains a hash character (#), as it's
  ambiguous whether the hash character is meant for the password or as a
  comment.

- The `whitelistforcerelay` option is used to relay transactions from
  whitelisted peers even when not accepted to the mempool. This option
  now defaults to being off, so that changes in policy and
  disconnect/ban behavior will not cause a node that is whitelisting
  another to be dropped by peers.  Users can still explicitly enable
  this behavior with the command line option (and may want to consider
  [contacting](https://www.groestlcoin.org/#contact) the Groestlcoin Core
  project to let us know about their use-case, as this feature could be
  deprecated in the future).

systemd init file
-----------------

The systemd init file (`contrib/init/groestlcoind.service`) has been changed
to use `/var/lib/groestlcoind` as the data directory instead of
`~groestlcoin/.groestlcoin`. This change makes Bitcoin Core more consistent with
other services, and makes the systemd init config more consistent with
existing Upstart and OpenRC configs.

The configuration, PID, and data directories are now completely managed
by systemd, which will take care of their creation, permissions, etc.
See [`systemd.exec(5)`](https://www.freedesktop.org/software/systemd/man/systemd.exec.html#RuntimeDirectory=)
for more details.

When using the provided init files under `contrib/init`, overriding the
`datadir` option in `/etc/groestlcoin/groestlcoin.conf` will have no effect.
This is because the command line arguments specified in the init files
take precedence over the options specified in
`/etc/groestlcoin/groestlcoin.conf`.


Documentation
-------------

- A new short [document](https://github.com/groestlcoin/groestlcoin/blob/master/doc/JSON-RPC-interface.md)
  about the JSON-RPC interface describes cases where the results of an
  RPC might contain inconsistencies between data sourced from different
  subsystems, such as wallet state and mempool state.  A note is added
  to the [REST interface documentation](https://github.com/groestlcoin/groestlcoin/blob/master/doc/REST-interface.md)
  indicating that the same rules apply.

- Further information is added to the [JSON-RPC
  documentation](https://github.com/groestlcoin/groestlcoin/blob/master/doc/JSON-RPC-interface.md)
  about how to secure this interface.

- A new [document](https://github.com/groestlcoin/groestlcoin/blob/master/doc/groestlcoin-conf.md)
  about the `groestlcoin.conf` file describes how to use it to configure
  Groestlcoin Core.

- A new document introduces Groestlcoin Core's BIP174 [Partially-Signed
  Bitcoin Transactions
  (PSBT)](https://github.com/groestlcoin/groestlcoin/blob/master/doc/psbt.md)
  interface, which is used to allow multiple programs to collaboratively
  work to create, sign, and broadcast new transactions.  This is useful
  for offline (cold storage) wallets, multisig wallets, coinjoin
  implementations, and many other cases where two or more programs need
  to interact to generate a complete transaction.

- The [output script
  descriptor](https://github.com/groestlcoin/groestlcoin/blob/master/doc/descriptors.md)
  documentation has been updated with information about new features in
  this still-developing language for describing the output scripts that
  a wallet or other program wants to receive notifications for, such as
  which addresses it wants to know received payments.  The language is
  currently used in multiple new and updated RPCs described in these
  release notes and is expected to be adapted to other RPCs and to the
  underlying wallet structure.

Build system changes
--------------------

- A new `--disable-bip70` option may be passed to `./configure` to
  prevent Groestlcoin-Qt from being built with support for the BIP70 payment
  protocol or from linking libssl.  As the payment protocol has exposed
  Groestlcoin Core to libssl vulnerabilities in the past, builders who don't
  need BIP70 support are encouraged to use this option to reduce their
  exposure to future vulnerabilities.

- The minimum required version of Qt (when building the GUI) has been
  increased from 5.2 to 5.5.1 (the [depends
  system](https://github.com/bitcoin/bitcoin/blob/master/depends/README.md)
  provides 5.9.7)

New RPCs
--------

- `getnodeaddresses` returns peer addresses known to this node. It may
  be used to find nodes to connect to without using a DNS seeder.

- `listwalletdir` returns a list of wallets in the wallet directory
  (either the default wallet directory or the directory configured by
  the `-walletdir` parameter).

- `getrpcinfo` returns runtime details of the RPC server. At the moment,
  it returns an array of the currently active commands and how long
  they've been running.

- `deriveaddresses` returns one or more addresses corresponding to an
  [output descriptor](https://github.com/groestlcoin/groestlcoin/blob/master/doc/descriptors.md).

- `getdescriptorinfo` accepts a descriptor and returns information about
  it, including its computed checksum.

- `joinpsbts` merges multiple distinct PSBTs into a single PSBT. The
  multiple PSBTs must have different inputs. The resulting PSBT will
  contain every input and output from all of the PSBTs. Any signatures
  provided in any of the PSBTs will be dropped.

- `analyzepsbt` examines a PSBT and provides information about what
  the PSBT contains and the next steps that need to be taken in order
  to complete the transaction. For each input of a PSBT, `analyzepsbt`
  provides information about what information is missing for that
  input, including whether a UTXO needs to be provided, what pubkeys
  still need to be provided, which scripts need to be provided, and
  what signatures are still needed. Every input will also list which
  role is needed to complete that input, and `analyzepsbt` will also
  list the next role in general needed to complete the PSBT.
  `analyzepsbt` will also provide the estimated fee rate and estimated
  virtual size of the completed transaction if it has enough
  information to do so.

- `utxoupdatepsbt` searches the set of Unspent Transaction Outputs
  (UTXOs) to find the outputs being spent by the partial transaction.
  PSBTs need to have the UTXOs being spent to be provided because
  the signing algorithm requires information from the UTXO being spent.
  For segwit inputs, only the UTXO itself is necessary.  For
  non-segwit outputs, the entire previous transaction is needed so
  that signers can be sure that they are signing the correct thing.
  Unfortunately, because the UTXO set only contains UTXOs and not full
  transactions, `utxoupdatepsbt` will only add the UTXO for segwit
  inputs.

Updated RPCs
------------

Note: some low-level RPC changes mainly useful for testing are described
in the Low-level Changes section below.

- `getpeerinfo` now returns an additional `minfeefilter` field set to
  the peer's BIP133 fee filter.  You can use this to detect that you
  have peers that are willing to accept transactions below the default
  minimum relay fee.

- The mempool RPCs, such as `getrawmempool` with `verbose=true`, now
  return an additional "bip125-replaceable" value indicating whether the
  transaction (or its unconfirmed ancestors) opts-in to asking nodes and
  miners to replace it with a higher-feerate transaction spending any of
  the same inputs.

- `settxfee` previously silently ignored attempts to set the fee below
  the allowed minimums.  It now prints a warning.  The special value of
  "0" may still be used to request the minimum value.

- `getaddressinfo` now provides an `ischange` field indicating whether
  the wallet used the address in a change output.

- `importmulti` has been updated to support P2WSH, P2WPKH, P2SH-P2WPKH,
  and P2SH-P2WSH. Requests for P2WSH and P2SH-P2WSH accept an additional
  `witnessscript` parameter.

- `importmulti` now returns an additional `warnings` field for each
  request with an array of strings explaining when fields are being
  ignored or are inconsistent, if there are any.

- `getaddressinfo` now returns an additional `solvable` boolean field
  when Groestlcoin Core knows enough about the address's scriptPubKey,
  optional redeemScript, and optional witnessScript in order for the
  wallet to be able to generate an unsigned input spending funds sent to
  that address.

- The `getaddressinfo`, `listunspent`, and `scantxoutset` RPCs now
  return an additional `desc` field that contains an output descriptor
  containing all key paths and signing information for the address
  (except for the private key).  The `desc` field is only returned for
  `getaddressinfo` and `listunspent` when the address is solvable.

- `importprivkey` will preserve previously-set labels for addresses or
  public keys corresponding to the private key being imported.  For
  example, if you imported a watch-only address with the label "cold
  wallet" in earlier releases of Groestlcoin Core, subsequently importing
  the private key would default to resetting the address's label to the
  default empty-string label ("").  In this release, the previous label
  of "cold wallet" will be retained.  If you optionally specify any
  label besides the default when calling `importprivkey`, the new label
  will be applied to the address.

- See the [Mining](#mining) section for changes to `getblocktemplate`.

- `getmininginfo` now omits `currentblockweight` and `currentblocktx`
  when a block was never assembled via RPC on this node.

- The `getrawtransaction` RPC & REST endpoints no longer check the
  unspent UTXO set for a transaction. The remaining behaviors are as
  follows: 1. If a blockhash is provided, check the corresponding block.
  2. If no blockhash is provided, check the mempool. 3. If no blockhash
  is provided but txindex is enabled, also check txindex.

- `unloadwallet` is now synchronous, meaning it will not return until
  the wallet is fully unloaded.

- `importmulti` now supports importing of addresses from descriptors. A
  "desc" parameter can be provided instead of the "scriptPubKey" in a
  request, as well as an optional range for ranged descriptors to
  specify the start and end of the range to import. Descriptors with key
  origin information imported through `importmulti` will have their key
  origin information stored in the wallet for use with creating PSBTs.
  More information about descriptors can be found
  [here](https://github.com/groestlcoin/groestlcoin/blob/master/doc/descriptors.md).

- `listunspent` has been modified so that it also returns
  `witnessScript`, the witness script in the case of a P2WSH or
  P2SH-P2WSH output.

- `createwallet` now has an optional `blank` argument that can be used
  to create a blank wallet. Blank wallets do not have any keys or HD
  seed.  They cannot be opened in software older than 2.18.2 Once a blank
  wallet has a HD seed set (by using `sethdseed`) or private keys,
  scripts, addresses, and other watch only things have been imported,
  the wallet is no longer blank and can be opened in 2.17.2. Encrypting
  a blank wallet will also set a HD seed for it.

Deprecated or removed RPCs
--------------------------

- `signrawtransaction` is removed after being deprecated and hidden
  behind a special configuration option in version 2.17.2.

- The 'account' API is removed after being deprecated in v2.17.2  The
  'label' API was introduced in v2.17.2 as a replacement for accounts.
  See the [release notes from
  v2.17.2](https://github.com/groestlcoin/groestlcoin/blob/master/doc/release-notes/release-notes-2.17.2.md#label-and-account-apis-for-wallet) for a full description of the changes from the 'account' API to the 'label' API.

- `addwitnessaddress` is removed after being deprecated in version
  2.16.0.

- `generate` is deprecated and will be fully removed in a subsequent
  major version.  This RPC is only used for testing, but its
  implementation reached across multiple subsystems (wallet and mining),
  so it is being deprecated to simplify the wallet-node interface.
  Projects that are using `generate` for testing purposes should
  transition to using the `generatetoaddress` RPC, which does not
  require or use the wallet component. Calling `generatetoaddress` with
  an address returned by the `getnewaddress` RPC gives the same
  functionality as the old `generate` RPC.  To continue using `generate`
  in this version, restart groestlcoind with the `-deprecatedrpc=generate`
  configuration option.

- Be reminded that parts of the `validateaddress` command have been
  deprecated and moved to `getaddressinfo`. The following deprecated
  fields have moved to `getaddressinfo`: `ismine`, `iswatchonly`,
  `script`, `hex`, `pubkeys`, `sigsrequired`, `pubkey`, `embedded`,
  `iscompressed`, `label`, `timestamp`, `hdkeypath`, `hdmasterkeyid`.

- The `addresses` field has been removed from the `validateaddress`
  and `getaddressinfo` RPC methods.  This field was confusing since
  it referred to public keys using their P2PKH address.  Clients
  should use the `embedded.address` field for P2SH or P2WSH wrapped
  addresses, and `pubkeys` for inspecting multisig participants.

REST changes
------------

- A new `/rest/blockhashbyheight/` endpoint is added for fetching the
  hash of the block in the current best blockchain based on its height
  (how many blocks it is after the Genesis Block).

Graphical User Interface (GUI)
------------------------------

- A new Window menu is added alongside the existing File, Settings, and
  Help menus.  Several items from the other menus that opened new
  windows have been moved to this new Window menu.

- In the Send tab, the checkbox for "pay only the required fee" has been
  removed.  Instead, the user can simply decrease the value in the
  Custom Feerate field all the way down to the node's configured minimum
  relay fee.

- In the Overview tab, the watch-only balance will be the only balance
  shown if the wallet was created using the `createwallet` RPC and the
  `disable_private_keys` parameter was set to true.

- The launch-on-startup option is no longer available on macOS if
  compiled with macosx min version greater than 10.11 (use
  CXXFLAGS="-mmacosx-version-min=10.11"
  CFLAGS="-mmacosx-version-min=10.11" for setting the deployment sdk
  version)

Tools
-----

- A new `groestlcoin-wallet` tool is now distributed alongside Groestlcoin
  Core's other executables.  Without needing to use any RPCs, this tool
  can currently create a new wallet file or display some basic
  information about an existing wallet, such as whether the wallet is
  encrypted, whether it uses an HD seed, how many transactions it
  contains, and how many address book entries it has.

Planned changes
===============

This section describes planned changes to Groestlcoin Core that may affect
other Groestlcoin software and services.

- Since version 2.16.0, Groestlcoin Core’s built-in wallet has defaulted to
  generating P2SH-wrapped segwit addresses when users want to receive
  payments. These addresses are backwards compatible with all
  widely-used software.  Starting with Groestlcoin Core 2.20.1 (expected about
  a year after 2.18.2), Groestlcoin Core will default to native segwit
  addresses (bech32) that provide additional fee savings and other
  benefits. Currently, many wallets and services already support sending
  to bech32 addresses, and if the Groestlcoin Core project sees enough
  additional adoption, it will instead default to bech32 receiving
  addresses in Groestlcoin Core 2.19.1.
  P2SH-wrapped segwit addresses will continue to be provided if the user
  requests them in the GUI or by RPC, and anyone who doesn’t want the
  update will be able to configure their default address type.
  (Similarly, pioneering users who want to change their default now may
  set the `addresstype=bech32` configuration option in any Groestlcoin Core
  release from 2.16.0 up.)

Deprecated P2P messages
-----------------------

- BIP 61 reject messages are now deprecated. Reject messages have no use
  case on the P2P network and are only logged for debugging by most
  network nodes. Furthermore, they increase bandwidth and can be harmful
  for privacy and security. It has been possible to disable BIP 61
  messages since v2.17.2 with the `-enablebip61=0` option. BIP 61 messages
  will be disabled by default in a future version, before being removed
  entirely.

Low-level changes
=================

This section describes RPC changes mainly useful for testing, mostly not
relevant in production. The changes are mentioned for completeness.

RPC
---

- The `submitblock` RPC previously returned the reason a rejected block
  was invalid the first time it processed that block, but returned a
  generic "duplicate" rejection message on subsequent occasions it
  processed the same block.  It now always returns the fundamental
  reason for rejecting an invalid block and only returns "duplicate" for
  valid blocks it has already accepted.

- A new `submitheader` RPC allows submitting block headers independently
  from their block.  This is likely only useful for testing.

- The `signrawtransactionwithkey` and `signrawtransactionwithwallet`
  RPCs have been modified so that they also optionally accept a
  `witnessScript`, the witness script in the case of a P2WSH or
  P2SH-P2WSH output. This is compatible with the change to
  `listunspent`.

- For the `walletprocesspsbt` and `walletcreatefundedpsbt` RPCs, if the
  `bip32derivs` parameter is set to true but the key metadata for a
  public key has not been updated yet, then that key will have a
  derivation path as if it were just an independent key (i.e. no
  derivation path and its master fingerprint is itself).

Configuration
-------------

- The `-usehd` configuration option was removed in version 2.16.0 From
  that version onwards, all new wallets created are hierarchical
  deterministic wallets. This release makes specifying `-usehd` an
  invalid configuration option.

Network
-------

- This release allows peers that your node automatically disconnected
  for misbehavior (e.g. sending invalid data) to reconnect to your node
  if you have unused incoming connection slots.  If your slots fill up,
  a misbehaving node will be disconnected to make room for nodes without
  a history of problems (unless the misbehaving node helps your node in
  some other way, such as by connecting to a part of the Internet from
  which you don't have many other peers).  Previously, Groestlcoin Core
  banned the IP addresses of misbehaving peers for a period of time
  (default of 1 day); this was easily circumvented by attackers with
  multiple IP addresses. If you manually ban a peer, such as by using
  the `setban` RPC, all connections from that peer will still be
  rejected.

Wallet
-------

- The key metadata will need to be upgraded the first time that the HD
  seed is available.  For unencrypted wallets this will occur on wallet
  loading.  For encrypted wallets this will occur the first time the
  wallet is unlocked.

- Newly encrypted wallets will no longer require restarting the
  software. Instead such wallets will be completely unloaded and
  reloaded to achieve the same effect.

- A sub-project of Bitcoin Core now provides Hardware Wallet Interaction
  (HWI) scripts that allow command-line users to use several popular
  hardware key management devices with Groestlcoin Core.  See their [project
  page](https://github.com/bitcoin-core/HWI#readme) for details.

Security
--------

- This release changes the Random Number Generator (RNG) used from
  OpenSSL to Groestlcoin Core's own implementation, although entropy
  gathered by Groestlcoin Core is fed out to OpenSSL and then read back in
  when the program needs strong randomness. This moves Groestlcoin Core a
  little closer to no longer needing to depend on OpenSSL, a dependency
  that has caused security issues in the past.  The new implementation
  gathers entropy from multiple sources, including from hardware
  supporting the rdseed CPU instruction.

Changes for particular platforms
--------------------------------

- On macOS, Groestlcoin Core now opts out of application CPU throttling
  ("app nap") during initial blockchain download, when catching up from
  over 100 blocks behind the current chain tip, or when reindexing chain
  data. This helps prevent these operations from taking an excessively
  long time because the operating system is attempting to conserve
  power.
