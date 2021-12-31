#!/usr/bin/env bash
# Copyright (c) 2016-2021 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

export LC_ALL=C
TOPDIR=${TOPDIR:-$(git rev-parse --show-toplevel)}
BUILDDIR=${BUILDDIR:-$TOPDIR}

BINDIR=${BINDIR:-$BUILDDIR/src}
MANDIR=${MANDIR:-$TOPDIR/doc/man}

BITCOIND=${GROESTLCOIND:-$BINDIR/groestlcoind}
BITCOINCLI=${GROESTLCOINCLI:-$BINDIR/groestlcoin-cli}
BITCOINTX=${GROESTLCOINTX:-$BINDIR/groestlcoin-tx}
WALLET_TOOL=${WALLET_TOOL:-$BINDIR/groestlcoin-wallet}
BITCOINUTIL=${GROESTLCOINQT:-$BINDIR/groestlcoin-util}
BITCOINQT=${GROESTLCOINQT:-$BINDIR/qt/groestlcoin-qt}

[ ! -x "$BITCOIND" ] && echo "$BITCOIND not found or not executable." && exit 1

# Don't allow man pages to be generated for binaries built from a dirty tree
DIRTY=""
for cmd in $BITCOIND $BITCOINCLI $BITCOINTX $WALLET_TOOL $BITCOINUTIL $BITCOINQT; do
  VERSION_OUTPUT=$($cmd --version)
  if [[ $VERSION_OUTPUT == *"dirty"* ]]; then
    DIRTY="${DIRTY}${cmd}\n"
  fi
done
if [ -n "$DIRTY" ]
then
  echo -e "WARNING: the following binaries were built from a dirty tree:\n"
  echo -e "$DIRTY"
  echo "man pages generated from dirty binaries should NOT be committed."
  echo "To properly generate man pages, please commit your changes to the above binaries, rebuild them, then run this script again."
fi

# The autodetected version git tag can screw up manpage output a little bit
read -r -a GRSVER <<< "$($BITCOINCLI --version | head -n1 | awk -F'[ -]' '{ print $6, $7 }')"

# Create a footer file with copyright content.
# This gets autodetected fine for groestlcoind if --version-string is not set,
# but has different outcomes for groestlcoin-qt and groestlcoin-cli.
echo "[COPYRIGHT]" > footer.h2m
$BITCOIND --version | sed -n '1!p' >> footer.h2m

for cmd in $BITCOIND $BITCOINCLI $BITCOINTX $WALLET_TOOL $BITCOINUTIL $BITCOINQT; do
  cmdname="${cmd##*/}"
  help2man -N --version-string="${GRSVER[0]}" --include=footer.h2m -o "${MANDIR}/${cmdname}.1" "${cmd}"
  sed -i "s/\\\-${GRSVER[1]}//g" "${MANDIR}/${cmdname}.1"
done

rm -f footer.h2m
