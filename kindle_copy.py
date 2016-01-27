#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 10:47:34 2016

@author: Ben
"""

import time
import pyperclip
import re

print("Starting Kindle Copy! Press Ctrl-C to stop")
clipboard_content = pyperclip.paste()
while True:
    new_clipboard_content = pyperclip.paste()
    if (new_clipboard_content != clipboard_content and
            'Kindle Edition' in new_clipboard_content):
        clipboard_content = new_clipboard_content
        clipboard_content = clipboard_content.replace('\r', '')
        try:
            quote, source = clipboard_content.partition('\n\n')[::2]
            # remove all extraneous whitespace formatting
            quote = re.sub(r'\s+', ' ', quote)
            source = source.strip()
            page_num = re.findall(r'\(p+\. .*\)', source)[0]
            pyperclip.copy(quote + ' ' + page_num)
        except Exception as e:
            print(str(e), clipboard_content)
    time.sleep(1)
