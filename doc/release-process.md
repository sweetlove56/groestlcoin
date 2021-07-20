Release Process
====================

## Branch updates

### Before every release candidate

* Update manpages, see [gen-manpages.sh](https://github.com/bitcoin/bitcoin/blob/master/contrib/devtools/README.md#gen-manpagessh).
* Update release candidate version in `configure.ac` (`CLIENT_VERSION_RC`).

### Before every major and minor release

* Update version in `configure.ac` (don't forget to set `CLIENT_VERSION_IS_RELEASE` to `true`) (don't forget to set `CLIENT_VERSION_RC` to `0`)
* Write release notes (see "Write the release notes" below).

### Before every major release

* On both the master branch and the new release branch:
  - update `CLIENT_VERSION_MAJOR` in [`configure.ac`](../configure.ac)
  - update `CLIENT_VERSION_MAJOR`, `PACKAGE_VERSION`, and `PACKAGE_STRING` in [`build_msvc/bitcoin_config.h`](/build_msvc/bitcoin_config.h)
* On the new release branch in [`configure.ac`](../configure.ac) and [`build_msvc/bitcoin_config.h`](/build_msvc/bitcoin_config.h) (see [this commit](https://github.com/bitcoin/bitcoin/commit/742f7dd)):
  - set `CLIENT_VERSION_MINOR` to `0`
  - set `CLIENT_VERSION_BUILD` to `0`
  - set `CLIENT_VERSION_IS_RELEASE` to `true`
* Update hardcoded [seeds](/contrib/seeds/README.md), see [this pull request](https://github.com/bitcoin/bitcoin/pull/7415) for an example.
* Update [`src/chainparams.cpp`](/src/chainparams.cpp) m_assumed_blockchain_size and m_assumed_chain_state_size with the current size plus some overhead (see [this](#how-to-calculate-assumed-blockchain-and-chain-state-size) for information on how to calculate them).
* Update [`src/chainparams.cpp`](/src/chainparams.cpp) chainTxData with statistics about the transaction count and rate. Use the output of the `getchaintxstats` RPC, see
  [this pull request](https://github.com/bitcoin/bitcoin/pull/20263) for an example. Reviewers can verify the results by running `getchaintxstats <window_block_count> <window_final_block_hash>` with the `window_block_count` and `window_final_block_hash` from your output.
* Update `src/chainparams.cpp` nMinimumChainWork and defaultAssumeValid (and the block height comment) with information from the `getblockheader` (and `getblockhash`) RPCs.
  - The selected value must not be orphaned so it may be useful to set the value two blocks back from the tip.
  - Testnet should be set some tens of thousands back from the tip due to reorgs there.
  - This update should be reviewed with a reindex-chainstate with assumevalid=0 to catch any defect
     that causes rejection of blocks in the past history.

#### Tagging a release (candidate)

To tag the version (or release candidate) in git, use the `make-tag.py` script from [groestlcoin-maintainer-tools](https://github.com/groestlcoin/groestlcoin-maintainer-tools). From the root of the repository run:

    ../groestlcoin-maintainer-tools/make-tag.py v(new version, e.g. 2.20.1)

This will perform a few last-minute consistency checks in the build system files, and if they pass, create a signed tag.

## Building

### First time / New builders

Install Guix using one of the installation methods detailed in
[contrib/guix/INSTALL.md](/contrib/guix/INSTALL.md).

Check out the source code in the following directory hierarchy.

    cd /path/to/your/toplevel/build
    git clone https://github.com/groestlcoin/guix.sigs.git
    git clone https://github.com/groestlcoin/groestlcoin-detached-sigs.git
    git clone https://github.com/groestlcoin/groestlcoin.git

### Setup and perform Guix builds

Checkout the Groestlcoin Core version you'd like to build:

```sh
pushd ./groestlcoin
SIGNER='(your builder key, ie jackielove4u, hashengineering, etc)'
VERSION='(new version without v-prefix, e.g. 2.20.1)'
git fetch "v${VERSION}"
git checkout "v${VERSION}"
popd
```

Ensure your guix.sigs are up-to-date if you wish to `guix-verify` your builds
against other `guix-attest` signatures.

```sh
git -C ./guix.sigs pull
```

### Create the macOS SDK tarball: (first time, or when SDK version changes)

Create the macOS SDK tarball, see the [macdeploy
instructions](/contrib/macdeploy/README.md#deterministic-macos-dmg-notes) for
details.

### Build and attest to build outputs:

Follow the relevant Guix README.md sections:
- [Performing a build](/contrib/guix/README.md#performing-a-build)
- [Attesting to build outputs](/contrib/guix/README.md#attesting-to-build-outputs)

### Verify other builders' signatures to your own. (Optional)

Add other builders keys to your gpg keyring, and/or refresh keys: See `../groestlcoin/contrib/builder-keys/README.md`.

Follow the relevant Guix README.md sections:
- [Verifying build output attestations](/contrib/guix/README.md#verifying-build-output-attestations)

### Next steps:

Commit your signature to guix.sigs:

```sh
pushd ./guix.sigs
git add "${VERSION}/${SIGNER}"/noncodesigned.SHA256SUMS{,.asc}
git commit -m "Add attestations by ${SIGNER} for ${VERSION} non-codesigned"
git push  # Assuming you can push to the guix.sigs tree
popd
```

Codesigner only: Create Windows/macOS detached signatures:
- Only one person handles codesigning. Everyone else should skip to the next step.
- Only once the Windows/macOS builds each have 3 matching signatures may they be signed with their respective release keys.

Codesigner only: Sign the macOS binary:

    transfer groestlcoin-osx-unsigned.tar.gz to macOS for signing
    tar xf groestlcoin-osx-unsigned.tar.gz
    ./detached-sig-create.sh -s "Key ID"
    Enter the keychain password and authorize the signature
    Move signature-osx.tar.gz back to the guix-build host

Codesigner only: Sign the windows binaries:

    tar xf groestlcoin-win-unsigned.tar.gz
    ./detached-sig-create.sh -key /path/to/codesign.key
    Enter the passphrase for the key when prompted
    signature-win.tar.gz will be created

Codesigner only: Commit the detached codesign payloads:

```sh
pushd ./groestlcoin-detached-sigs
# checkout the appropriate branch for this release series
rm -rf ./*
tar xf signature-osx.tar.gz
tar xf signature-win.tar.gz
git add -A
git commit -m "point to ${VERSION}"
git tag -s "v${VERSION}" HEAD
git push the current branch and new tag
popd
```

Non-codesigners: wait for Windows/macOS detached signatures:

- Once the Windows/macOS builds each have 3 matching signatures, they will be signed with their respective release keys.
- Detached signatures will then be committed to the [groestlcoin-detached-sigs](https://github.com/groestlcoin/groestlcoin-detached-sigs) repository, which can be combined with the unsigned apps to create signed binaries.

Create (and optionally verify) the codesigned outputs:

- [Codesigning](/contrib/guix/README.md#codesigning)

Commit your signature for the signed macOS/Windows binaries:

```sh
pushd ./guix.sigs
git add "${VERSION}/${SIGNER}"/all.SHA256SUMS{,.asc}
git commit -m "Add attestations by ${SIGNER} for ${VERSION} codesigned"
git push  # Assuming you can push to the guix.sigs tree
popd
```

### After 3 or more people have guix-built and their results match:

Combine `all.SHA256SUMS` and `all.SHA256SUMS.asc` into a clear-signed
`SHA256SUMS.asc` message:

```sh
echo -e "-----BEGIN PGP SIGNED MESSAGE-----\nHash: SHA256\n\n$(cat all.SHA256SUMS)\n$(cat filename.txt.asc)" > SHA256SUMS.asc
```

Here's an equivalent, more readable command if you're confident that you won't
mess up whitespaces when copy-pasting:

```bash
cat << EOF > SHA256SUMS.asc
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA256

$(cat all.SHA256SUMS)
$(cat all.SHA256SUMS.asc)
EOF
```

- Update groestlcoin.org version

- Update other repositories and websites for new version

- Update packaging repo

      - Push the flatpak to flathub, e.g. https://github.com/flathub/org.groestlcoin.groestlcoin-qt/pull/2

      - Push the latest version to master (if applicable), e.g. https://github.com/groestlcoin/packaging/pull/32

      - Create a new branch for the major release "0.xx" from master (used to build the snap package) and request the
        track (if applicable), e.g. https://forum.snapcraft.io/t/track-request-for-groestlcoin-core-snap/17359

      - Notify jackielove4u so that he can start building the snap package

        - https://code.launchpad.net/~groestlcoin/groestlcoin-core-snap/+git/packaging (Click "Import Now" to fetch the branch)
        - https://code.launchpad.net/~groestlcoin/groestlcoin-core-snap/+git/packaging/+ref/0.xx (Click "Create snap package")
        - Name it "groestlcoin-core-snap-0.xx"
        - Leave owner and series as-is
        - Select architectures that are compiled via guix
        - Leave "automatically build when branch changes" unticked
        - Tick "automatically upload to store"
        - Put "groestlcoin-core" in the registered store package name field
        - Tick the "edge" box
        - Put "0.xx" in the track field
        - Click "create snap package"
        - Click "Request builds" for every new release on this branch (after updating the snapcraft.yml in the branch to reflect the latest guix results)
        - Promote release on https://snapcraft.io/groestlcoin-core/releases if it passes sanity checks

- Announce the release:

      - groestlcoin.org/forum post

      - Update title of #groestlcoin on Freenode IRC

      - Twitter, Reddit /r/Groestlcoin, Facebook, Telegram, Discord...

      - Build [the PPAs](https://launchpad.net/~groestlcoin/+archive/ubuntu/groestlcoin)

      - Create a [new GitHub release](https://github.com/groestlcoin/groestlcoin/releases/new) with a link to the archived release notes.

      - Celebrate

### Additional information

#### <a name="how-to-calculate-assumed-blockchain-and-chain-state-size"></a>How to calculate `m_assumed_blockchain_size` and `m_assumed_chain_state_size`

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
