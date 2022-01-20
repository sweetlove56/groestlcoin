#!/usr/bin/env python3
#
# Copyright (c) 2018-2021 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
#
# Download or build previous releases.
# Needs curl and tar to download a release, or the build dependencies when
# building a release.

import argparse
import contextlib
from fnmatch import fnmatch
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import hashlib


SHA256_SUMS = {
    "e83406ebf473c7d69da02d2f09539a710cb82b090116ff8f9b63e35a41608577": "groestlcoin-2.17.2-aarch64-linux-gnu.tar.gz",
    "5db693a615ce60e817af16cdcae51c4ac03e31f9588ed63447a57c343e1e4c7c": "groestlcoin-2.17.2-arm-linux-gnueabihf.tar.gz",
    "5db065045115a0bc5d02e46d591dfac9fb98e028dd3933d42c16712e5c29925d": "groestlcoin-2.17.2-i686-pc-linux-gnu.tar.gz",
    "b3fe245752a445ce56cac265af7ed63906c7c1c8e2c932891369be72c290307d": "groestlcoin-2.17.2-x86_64-apple-darwin14.tar.gz",
    "e90f6ceb56fbc86ae17ee3c5d6d3913c422b7d98aa605226adb669acdf292e9e": "groestlcoin-2.17.2-x86_64-linux-gnu.tar.gz",
    #
    "99f7a11f9f59c09f44b64f5631b73b7e98cb27a8fc35ba67c85310001b644e43": "groestlcoin-2.18.2-aarch64-linux-gnu.tar.gz",
    "93c093b7684623c1cdf864cfacdec653ac6808d01f48ec9d1ffe26479623c6f5": "groestlcoin-2.18.2-arm-linux-gnueabihf.tar.gz",
    "82cbeac6615bf9482da11b9d6a6aadc08424b78f3667b4331455264b5fbb06c5": "groestlcoin-2.18.2-i686-pc-linux-gnu.tar.gz",
    "fdb722b326433501b179a33ac20e88b5fd587a249878eb94a9981da2097c42a5": "groestlcoin-2.18.2-osx64.tar.gz",
    "08472eb96cb12b6ff6bebf18237ed05e0c236376446655bdb5901a42d781f75a": "groestlcoin-2.18.2-riscv64-linux-gnu.tar.gz",
    "9ee26e1cd7967d0dc88670dbbdb99f95236ebc218f75977efb23f03ad8b74250": "groestlcoin-2.18.2-x86_64-linux-gnu.tar.gz",
    #
    "f151cfada51e981db2cb90e78f50e13ba3c64640339f41d4f212d428df8ca1bf": "groestlcoin-2.19.1-aarch64-linux-gnu.tar.gz",
    "218218b18b49d924fc4085545ed71a59a985dbecdc2dab48c401d3ac622f10d4": "groestlcoin-2.19.1-arm-linux-gnueabihf.tar.gz",
    "051274a3de9877b790be713d6141916ed2f25d7f9c3b7d16603fa3e3ed4d5ee9": "groestlcoin-2.19.1-i686-pc-linux-gnu.tar.gz",
    "902d38bea03fded2762acd1855cddd4a7b210acac9921ea56d816e622c4244ba": "groestlcoin-2.19.1-osx64.tar.gz",
    "624f8d6a442557a87aed8f84c5949bd3b424f87a0f7cccb927ba8ade99768a78": "groestlcoin-2.19.1-riscv64-linux-gnu.tar.gz",
    "0646cae023a0be0821f357d33bdbf81fc05fc9a9e3e9d4e5936d5053f1a988d4": "groestlcoin-2.19.1-x86_64-linux-gnu.tar.gz",
    #
    "989a626db8178f9d26181fc4c38ba920b5a27ad236ab9d7035f59d291ad8ed6b": "groestlcoin-2.20.1-aarch64-linux-gnu.tar.gz",
    "4c5915aed6e3c7aabc77040c91c133d29bc757a1f9f19477204f5aa75a485444": "groestlcoin-2.20.1-arm-linux-gnueabihf.tar.gz",
    "16564cf6df5f4edead0f8a807f285e34e9f20b2770c2f66ab803de5152e38d3b": "groestlcoin-2.20.1-osx64.tar.gz",
    "d1b8cbc23dc4a7c068df92fe1a470d293ec098d80492ddf253868ead94deb3ad": "groestlcoin-2.20.1-osx-unsigned.dmg",
    "b0e7a1a18d29975b76281450dc744a64461aa4660fa8a09fafa7582e9c7b386b": "groestlcoin-2.20.1-riscv64-linux-gnu.tar.gz",
    "0a877be9dac14f4d9aab95d6bfd51547275acbcc3e6553f0cb82c5c9f35f333c": "groestlcoin-2.20.1-x86_64-linux-gnu.tar.gz",
}


@contextlib.contextmanager
def pushd(new_dir) -> None:
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(previous_dir)


def download_binary(tag, args) -> int:
    if Path(tag).is_dir():
        if not args.remove_dir:
            print('Using cached {}'.format(tag))
            return 0
        shutil.rmtree(tag)
    Path(tag).mkdir()
    bin_path = 'Groestlcoin/groestlcoin/releases/download/v{}'.format(tag[1:])
    match = re.compile('v(.*)(rc[0-9]+)$').search(tag)
    if match:
        bin_path = 'Groestlcoin/groestlcoin/releases/download/v{}/test.{}'.format(
            match.group(1), match.group(2))
    tarball = 'groestlcoin-{tag}-{platform}.tar.gz'.format(
        tag=tag[1:], platform=args.platform)
    tarballUrl = 'https://github.com/{bin_path}/{tarball}'.format(
        bin_path=bin_path, tarball=tarball)

    print('Fetching: {tarballUrl}'.format(tarballUrl=tarballUrl))

    header, status = subprocess.Popen(
        ['curl', '-L', '--head', tarballUrl], stdout=subprocess.PIPE).communicate()
    if re.search("404 Not Found", header.decode("utf-8")):
        print("Binary tag was not found")
        return 1

    curlCmds = [
        ['curl', '-L', '--remote-name', tarballUrl]
    ]

    for cmd in curlCmds:
        ret = subprocess.run(cmd).returncode
        if ret:
            return ret

    hasher = hashlib.sha256()
    with open(tarball, "rb") as afile:
        hasher.update(afile.read())
    tarballHash = hasher.hexdigest()

    if tarballHash not in SHA256_SUMS or SHA256_SUMS[tarballHash] != tarball:
        if tarball in SHA256_SUMS.values():
            print("Checksum did not match")
            return 1

        print("Checksum for given version doesn't exist")
        return 1
    print("Checksum matched")

    # Extract tarball
    ret = subprocess.run(['tar', '-zxf', tarball, '-C', tag,
                          '--strip-components=1',
                          'groestlcoin-{tag}'.format(tag=tag[1:])]).returncode
    if ret:
        return ret

    Path(tarball).unlink()
    return 0


def build_release(tag, args) -> int:
    githubUrl = "https://github.com/groestlcoin/groestlcoin"
    if args.remove_dir:
        if Path(tag).is_dir():
            shutil.rmtree(tag)
    if not Path(tag).is_dir():
        # fetch new tags
        subprocess.run(
            ["git", "fetch", githubUrl, "--tags"])
        output = subprocess.check_output(['git', 'tag', '-l', tag])
        if not output:
            print('Tag {} not found'.format(tag))
            return 1
    ret = subprocess.run([
        'git', 'clone', githubUrl, tag
    ]).returncode
    if ret:
        return ret
    with pushd(tag):
        ret = subprocess.run(['git', 'checkout', tag]).returncode
        if ret:
            return ret
        host = args.host
        if args.depends:
            with pushd('depends'):
                ret = subprocess.run(['make', 'NO_QT=1']).returncode
                if ret:
                    return ret
                host = os.environ.get(
                    'HOST', subprocess.check_output(['./config.guess']))
        config_flags = '--prefix={pwd}/depends/{host} '.format(
            pwd=os.getcwd(),
            host=host) + args.config_flags
        cmds = [
            './autogen.sh',
            './configure {}'.format(config_flags),
            'make',
        ]
        for cmd in cmds:
            ret = subprocess.run(cmd.split()).returncode
            if ret:
                return ret
        # Move binaries, so they're in the same place as in the
        # release download
        Path('bin').mkdir(exist_ok=True)
        files = ['groestlcoind', 'groestlcoin-cli', 'groestlcoin-tx']
        for f in files:
            Path('src/'+f).rename('bin/'+f)
    return 0


def check_host(args) -> int:
    args.host = os.environ.get('HOST', subprocess.check_output(
        './depends/config.guess').decode())
    if args.download_binary:
        platforms = {
            'aarch64-*-linux*': 'aarch64-linux-gnu',
            'x86_64-*-linux*': 'x86_64-linux-gnu',
            'x86_64-apple-darwin*': 'osx64',
            'aarch64-apple-darwin*': 'osx64',
        }
        args.platform = ''
        for pattern, target in platforms.items():
            if fnmatch(args.host, pattern):
                args.platform = target
        if not args.platform:
            print('Not sure which binary to download for {}'.format(args.host))
            return 1
    return 0


def main(args) -> int:
    Path(args.target_dir).mkdir(exist_ok=True, parents=True)
    print("Releases directory: {}".format(args.target_dir))
    ret = check_host(args)
    if ret:
        return ret
    if args.download_binary:
        with pushd(args.target_dir):
            for tag in args.tags:
                ret = download_binary(tag, args)
                if ret:
                    return ret
        return 0
    args.config_flags = os.environ.get('CONFIG_FLAGS', '')
    args.config_flags += ' --without-gui --disable-tests --disable-bench'
    with pushd(args.target_dir):
        for tag in args.tags:
            ret = build_release(tag, args)
            if ret:
                return ret
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-r', '--remove-dir', action='store_true',
                        help='remove existing directory.')
    parser.add_argument('-d', '--depends', action='store_true',
                        help='use depends.')
    parser.add_argument('-b', '--download-binary', action='store_true',
                        help='download release binary.')
    parser.add_argument('-t', '--target-dir', action='store',
                        help='target directory.', default='releases')
    parser.add_argument('tags', nargs='+',
                        help="release tags. e.g.: v2.18.2 v2.20.1")
    args = parser.parse_args()
    sys.exit(main(args))
