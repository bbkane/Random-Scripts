# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 20:53:31 2015

@author: Ben
"""

import os
import subprocess

ebook_meta = "E:\Portable Programs\Calibre Portable\Calibre\ebook-meta.exe"

os.chdir(r'E:\Books Not On Kindle\Star Wars')
#for root, dirs, files in os.walk("."):
#    print(dirs)

folders = ['1 - Before the Republic', '2 - Old Galactic Republic Era', '3 - Rise of the Empire Era', '4 - Rebellion Era', '5 - New Republic Era', '6 - New Jedi Order Era', '7 - Legacy Era']
for folder in folders:
    os.chdir(folder)
    for book in os.listdir():
        if book.endswith('epub'):
            arglist = [book, '-t', book.replace('.epub', '')]
            arglist = [book]
    #        print(arglist)
            out = subprocess.run([ebook_meta, *arglist], stdout= subprocess.PIPE)
            out = out.stdout.split(b'\n\t')
            for line in out:
                print(line)
    os.chdir('..')