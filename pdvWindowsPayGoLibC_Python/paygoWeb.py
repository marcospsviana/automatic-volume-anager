#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import ctypes
from ctypes import *

import sys
import os
from Interops import *
from Enums import *
import MainWindow



class PayGoPayment:
    def __init__(self):
        self.directory = os.path.abspath(os.path.dirname(__file__))



    def payment(value):
        __value = value
        __library = PGWebLibrary()
        iInit = __library.PW_iInit()
        print("resultado init", iInit)
        ntransac = __library.PW_iNewTransac(21)
        print("resultado ntransac", ntransac)
        __library.PW_iAddParam()
        
        
    def main_window():
        MainWindow()
        
    main_window()


    # ====================     IADD_PARAM  ========================  

    """
    PWINFO_CARDTYPE (41, 1)
    PWINFO_FINTYPE(59, 1)
    PWINFO_AUTHSYST(53, REDE)
    PWINFO_AUTNAME(21,);
    PWINFO_AUTVER(22,);
    PWINFO_AUTDEV(23,);
    PWINFO_AUTCAP (36,);
    PWINFO_TOTAMNT (37, 1200);
    PWINFO_CURRENCY (38, 986);
    PWINFO_CURREXP (39, 2).
    
    PARAMS = (
    libtest.PW_iAddParam(0x29,"1"), 
    libtest.PW_iAddParam(0x3B,"1"),
    libtest.PW_iAddParam(0x35,"BIN"),
    libtest.PW_iAddParam(0x15, "21"),
    libtest.PW_iAddParam(0x16, "22"),
    libtest.PW_iAddParam(0x17, "23"),
    libtest.PW_iAddParam(0x24, "36"),
    libtest.PW_iAddParam(0x25, "1200"),
    libtest.PW_iAddParam(0x26, "986"),
    libtest.PW_iAddParam(0x27, "2")
    )

    p=''

    import time
    for p in PARAMS:
        result = p
        print(result)
        time.sleep(0.3)
    """
if __name__ == '__main__':
	PayGoPayment()