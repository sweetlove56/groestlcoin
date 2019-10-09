Release Process
====================

## Branch updates

* Update manpages, see [gen-manpages.sh](https://github.com/bitcoin/bitcoin/blob/master/contrib/devtools/README.md#gen-manpagessh).
* Update release candidate version in `configure.ac` (`CLIENT_VERSION_RC`).

### Before every major and minor release

* Update version in `configure.ac` (don't forget to set `CLIENT_VERSION_IS_RELEASE` to `true`) (don't forget to set `CLIENT_VERSION_RC` to `0`)
* Write release notes (see "Write the release notes" below).
* Update `src/chainparams.cpp` nMinimumChainWork with information from the getblockchaininfo rpc.
* Update `src/chainparams.cpp` defaultAssumeValid with information from the getblockhash rpc.
  - The selected value must not be orphaned so it may be useful to set the value two blocks back from the tip.
  - Testnet should be set some tens of thousands back from the tip due to reorgs there.
  - This update should be reviewed with a reindex-chainstate with assumevalid=0 to catch any defect
     that causes rejection of blocks in the past history.

### Before every major release

* Update hardcoded [seeds](/contrib/seeds/README.md), see [this pull request](https://github.com/bitcoin/bitcoin/pull/7415) for an example.
* Update [`src/chainparams.cpp`](/src/chainparams.cpp) m_assumed_blockchain_size and m_assumed_chain_state_size with the current size plus some overhead (see [this](#how-to-calculate-m_assumed_blockchain_size-and-m_assumed_chain_state_size) for information on how to calculate them).
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

  - Create a [new GitHub release](https://github.com/groestlcoin/groestlcoin/releases/new) with a link to the archived release notes.

  - Celebrate

### Additional information

#### How to calculate `m_assumed_blockchain_size` and `m_assumed_chain_state_size`

Both variables are used as a guideline for how much space the user needs on their drive in total, not just strictly for the blockchain.
Note that all values should be taken from a **fully synced** node and have an overhead of 5-10% added on top of its base value.

To calculate `m_assumed_blockchain_size`:
- For `mainnet` -> Take the size of the data directory, excluding `/regtest` and `/testnet3` directories.
- For `testnet` -> Take the size of the `/testnet3` directory.


To calculate `m_assumed_chain_state_size`:
- For `mainnet` -> Take the size of the `/chainstate` directory.
- For `testnet` -> Take the size of the `/testnet3/chainstate` directory.

Notes:
- When taking the size for `m_assumed_blockchain_size`, there's no need to exclude the `/chainstate` directory since it's a guideline value and an overhead will be added anyway.
- The expected overhead for growth may change over time, so it may not be the same value as last release; pay attention to that when changing the variables.
