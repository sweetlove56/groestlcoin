Release Process
====================

Before every release candidate:

* Update manpages, see [gen-manpages.sh](https://github.com/groestlcoin/groestlcoin/blob/master/contrib/devtools/README.md#gen-manpagessh).

Before every minor and major release:

* Update version in `configure.ac` (don't forget to set `CLIENT_VERSION_IS_RELEASE` to `true`)
* Write release notes (see below)
* Update `src/chainparams.cpp` nMinimumChainWork with information from the getblockchaininfo rpc.
* Update `src/chainparams.cpp` defaultAssumeValid with information from the getblockhash rpc.
  - The selected value must not be orphaned so it may be useful to set the value two blocks back from the tip.
  - Testnet should be set some tens of thousands back from the tip due to reorgs there.
  - This update should be reviewed with a reindex-chainstate with assumevalid=0 to catch any defect
     that causes rejection of blocks in the past history.

Before every major release:

* Update hardcoded [seeds](/contrib/seeds/README.md)
* Update [`BLOCK_CHAIN_SIZE`](/src/qt/intro.cpp) to the current size plus some overhead.
* Update `src/chainparams.cpp` chainTxData with statistics about the transaction count and rate. Use the output of the RPC `getchaintxstats`, see
  [this pull request](https://github.com/bitcoin/bitcoin/pull/12270) for an example. Reviewers can verify the results by running `getchaintxstats <window_block_count> <window_last_block_hash>` with the `window_block_count` and `window_last_block_hash` from your output.

The list of files should be:
```
groestlcoin-${VERSION}-aarch64-linux-gnu.tar.gz
groestlcoin-${VERSION}-arm-linux-gnueabihf.tar.gz
groestlcoin-${VERSION}-i686-pc-linux-gnu.tar.gz
groestlcoin-${VERSION}-x86_64-linux-gnu.tar.gz
groestlcoin-${VERSION}-osx64.tar.gz
groestlcoin-${VERSION}-osx.dmg
groestlcoin-${VERSION}.tar.gz
groestlcoin-${VERSION}-win32-setup.exe
groestlcoin-${VERSION}-win32.zip
groestlcoin-${VERSION}-win64-setup.exe
groestlcoin-${VERSION}-win64.zip
```

- Update groestlcoin.org version
- Announce the release:

  - groestlcoin.org/forum post

  - Update title of #groestlcoin on Freenode IRC

  - Twitter, Reddit /r/Groestlcoin, Facebook, Telegram, Discord...

  - Notify Jbisch so that he can start building [the PPAs](https://launchpad.net/~groestlcoin/+archive/ubuntu/groestlcoin)

  - Create a [new GitHub release](https://github.com/bitcoin/bitcoin/releases/new) with a link to the archived release notes.

  - Celebrate
