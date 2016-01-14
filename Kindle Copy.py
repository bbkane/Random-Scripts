# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 10:47:34 2016

@author: Ben
"""

import time
import pyperclip
import re

clipboard_content = pyperclip.paste()
while True:
    new_clipboard_content = pyperclip.paste()
    if new_clipboard_content != clipboard_content and 'Kindle Edition' in new_clipboard_content:
        clipboard_content = new_clipboard_content
        clipboard_content = clipboard_content.replace('\r','')
        try:
            split = clipboard_content.find('\n\n')
            quote = clipboard_content[:split]
            source = clipboard_content[split:].strip()
            page_num = re.findall(r'\(p+\. .*\)', source)[0]
            pyperclip.copy(quote + ' ' + page_num)
        except Exception as e:
            print(str(e), clipboard_content)
    time.sleep(.5)

#print(quote)
#print('==='
#print(page_num)
