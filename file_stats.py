#!/usr/bin/env python3

import argparse
import datetime
import json
import os
import sys


DESCRIPTION = """\
Print file stats (similar to `stat`) for all directories and files under a
folder in a JSON format.  Useful for diffs before and after an action. Somewhat
surprisingly, it's fast enough to use from the root directory without being
annoying.

Outputs:
- launch_datetime
- comment (optional)
- top_dir (always absolute path)
- file_stats (can have relative paths)

NOTE: there will usually be a couple of "FileNotFound" errors. These are the
result of files disappearing between finding them and statting them. As long as
they are files you don't care about, this is fine.

Example:

    {exe} -c 'About to install blah' / > ~/before_blah.json
    curl install.blah.io | bash  # or some install process
    {exe} -c 'After installing blah' / > ~/after_blah.json
    vimdiff ~/before_blah.json ~/after_blah.json
""".format(exe=sys.argv[0])


def parse_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-c', '--comment',
                        help="Comment for the output file")
    parser.add_argument('topdir', help="directory to start at")
    return parser.parse_args()


def main():
    args = parse_args()
    comment = args.comment
    topdir = args.topdir
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

    answer = dict(top_dir=os.path.realpath(topdir),
                  comment=comment,
                  launch_datetime=datetime.datetime.now().isoformat(),
                  file_stats=results)
    print(json.dumps(answer, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
