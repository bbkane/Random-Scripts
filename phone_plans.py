# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 21:36:39 2015

@author: Ben
"""
import collections
from ast import literal_eval as lev

phonedata = """
new_phone 700 30
craigslist 300 30
Galaxy_S5 230 30
# A contract is the cheapest way for ATT
ATT_Galaxy_Note_4 0 60
## ATT_LG_G4 190 60
## ATT_HTC_M8 200 60
# Ting
Ting_300_mid 300 20
Ting_IPhone4_cheap 87 12
Ting_IPhone4_mid 87 20
Ting_LG_G4 547 20
# Republic Wireless
# These phones are NOT reusable with other carriers
# People don't like em on Amazon
RW_Moto_G_Refund 200 16
RW_Moto_G_No_REfund 200 25
"""

class Phone(collections.namedtuple('Phone', 
                                   ['name', 'base_price', 'monthly_bill'])):       
    def price(self, time = 24):
        return int(lev(self.base_price)) + int(lev(self.monthly_bill)) * time

for line in phonedata.split('\n'):
    line = line.strip()
    if line and not line.startswith('##'):
        if line.startswith('#'):
            print(line)
        else:
            p = Phone(*line.split())
            print(p.name, p.price(), sep = ' : ')
    