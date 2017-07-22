#!/usr/bin/env python3

import argparse
import datetime
import json
import os
import pprint
import sys

DESCRIPTION = """\
Print file stats (similar to `stat`) for all
directories and files under a folder.
Useful for diffs before and after an action
"""


def parse_args():
    parser = argparse.ArgumentParser(DESCRIPTION)
    parser.add_argument('topdir', help="directory to start at")
    return parser.parse_args()


def main():
    topdir = parse_args().topdir
    topdir = os.path.expanduser(topdir)
    topdir = os.path.expandvars(topdir)
    infos = []
    for dirpath, dirnames, filenames in os.walk(topdir, topdown=True):
        dir_infos = [{'type': 'dir', 'path': os.path.join(dirpath, dirname)}
                     for dirname in dirnames]
        file_infos = [{'type': 'file', 'path': os.path.join(dirpath, filename)}
                      for filename in filenames]
        infos.extend(dir_infos)
        infos.extend(file_infos)
    infos.sort(key=lambda i: i['path'])
    results = []
    for info in infos:
        # get stat information (really wish I could just call vars() on the stat_info)
        # Get the info on the symlink (otherwise I can get errors)
        # NOTE: does this make me miss info?
        # this can fail so that's why I'm trying and excepting
        try:
            stat_info = os.lstat(info['path'])
        except FileNotFoundError as e:
            print(info, file=sys.stderr)
            print(repr(e), file=sys.stderr)
            print(file=sys.stderr)
            continue
        info['st_mode'] = stat_info.st_mode
        info['st_size'] = stat_info.st_size
        info['st_atime'] = stat_info.st_atime
        info['st_mtime'] = stat_info.st_mtime
        info['st_ctime'] = stat_info.st_ctime
        results.append(info)

    answer = dict(top_dir=topdir,
                  launch_time=datetime.datetime.now().isoformat(),
                  results=results)
    print(json.dumps(answer, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
