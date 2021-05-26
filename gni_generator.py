#!/usr/bin/env python3
# Copyright 2021 ZEGO. All rights reserved.

import os
import sys
import argparse
from typing import List, Tuple

CWD_PATH = os.getcwd()
PROJ_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HELP = """
A helper tools for auto collect all source code files
recursively and generate a ".gni" file to list them.

You can run this script directly, or import "generate_gni"
function from other python script.
"""

DEFAULT_TYPE = ['h', 'c', 'cc', 'cpp', 'hpp', 'm', 'mm']

def generate_gni(root_path: str, gni_name: str, include_file_type=DEFAULT_TYPE) -> str:
    """
    Recursive list files under root_path, and generate a .gni
    file which contains a list var names "${gni_name}",
    and the gni file name is same as var

    Args:
        root_path (str): Folder path to be list
        gni_name (str): gni's name

        include_file_type ([type], optional): What type of files need to be collected. Defaults to DEFAULT_TYPE.

    Returns:
        str: gni file path
    """
    filelist: List[str] = []
    filelist_str = ''
    root_path = os.path.realpath(os.path.join(CWD_PATH, root_path))

    for root, _, files in os.walk(root_path):
        for name in files:
            if name.split('.')[-1] not in include_file_type:
                continue
            # Only collect specific type files
            filelist.append(os.path.join(root, name))

    filelist.sort()
    for f in filelist:
        f = f[len(PROJ_ROOT):].lstrip(os.sep)
        # Convert windows style separator to unix style
        f = f.replace('\\', '/')
        file_str = '  "//{}",\n'.format(f)
        filelist_str += file_str

    gni_content = '# WARNING: DO NOT EDIT MANUALLY!\n'
    gni_content += '# GENERATED BY "python3 build/gni_generator.py {0} {1}"\n'.format(root_path[len(PROJ_ROOT)+1:], gni_name)
    gni_content += '\n{0} = [\n{1}]\n'.format(gni_name, filelist_str)
    gni_file_path = os.path.join(root_path, gni_name+'.gni')

    with open(gni_file_path, 'w') as fw:
        fw.write(gni_content)

    return gni_file_path

def main(argv):
    parser = argparse.ArgumentParser(description=HELP)
    parser.add_argument('root_path', type=str, help='The root sources path to perform generating GNI.')
    parser.add_argument('gni_name', type=str, help='The project or module name for the root path dir.')
    parser.add_argument('--include-type', action='store', type=str, nargs='+', choices=DEFAULT_TYPE, default=DEFAULT_TYPE, help='What type of files need to be collected. Defaults to DEFAULT_TYPE.')

    args = parser.parse_args(argv)

    file_path = generate_gni(
        args.root_path,
        args.gni_name,
        include_file_type=args.include_type
    )
    print('[Generate GNI] Ouput: "%s"' % file_path)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
