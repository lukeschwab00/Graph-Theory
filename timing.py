# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 15:37:46 2022

@author: Luke
"""
import time

def aprilTag0():
    for i in range(10000):
        yield 0

function = aprilTag0()
c = 0
for i in function:
    c = c + 1
print(c)
