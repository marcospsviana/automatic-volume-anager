#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import ctypes
from ctypes import *
from time import sleep
import sys
import os
from Interops import *
from Enums import *
from PGWlib import *




class PayGoPayment:
    def __init__(self):
        self.PWINFO_DESTTCPIP = "app.tpgw.ntk.com.br:17502"
        self.PWINFO_POSID     = "62547"
        self.PWINFO_AUTDEV    = "COOLBAG-SAFE GUARDA BAGAGENS AUTOMATIZADO"
        self.PWINFO_AUTVER = "1.0"
        self.PWINFO_MERCHCNPJCPF = "35223093000106"
        self.PWINFO_AUTHTECHUSER = "314159"
        self.PWINFO_USINGPINPAD =  "1"
        self.PWINFO_AUTNAME = "COOLBAGSAFE-RENTLOCKER"
        self.PWINFO_AUTCAP = "0"
        self.paygoLib = CDLL("./PGWebLib.so")
        self.payment()

    def PW_iExecTransac(self,vstParam, iNumParam):

        self.PW_iExecTransacObj          = self.paygoLib.PW_iExecTransac
        self.PW_iExecTransacObj.restype  = c_short

        
        self.PW_iExecTransacObj.argtypes = [POINTER((PW_GetData *11)),POINTER(c_int)]
        
        
        
        ret = self.PW_iExecTransacObj(byref(vstParam),byref(c_int(iNumParam)))
       

        return ret



    def payment(self):
        directory = os.path.abspath(os.path.dirname(__file__))
        vstParam_11 = (PW_GetData * 11)
        vstParam = vstParam_11()
        iNumParam = 10
        iRet=0
        #__value = value
        pgwLib = CDLL(directory +"/PGWebLib.so")
        paygoLib = CDLL(directory +"/PGWebLib.so")
        #paygoLib = PGWebLibrary()
        #iInit = paygoLib.PW_iInit()
        paygoLib.PW_iInit("./PGWebLib")
        #print("resultado init", iInit)
        ntransac = paygoLib.PW_iNewTransac(E_PWOPER.PWOPER_SALE.value)
        print("resultado ntransac", ntransac)
        #paygoLib.PW_iAddParam(E_PWINFO.PWINFO_POSID.value,"62547")
        paygoLib.PW_iAddParam(0x29,"1") #PWINFO_CARDTYPE
        paygoLib.PW_iAddParam(0x3B,"1") #PWINFO_FINTYPE
        paygoLib.PW_iAddParam(0x35,"BIN") #PWINFO_AUTHSYST
        paygoLib.PW_iAddParam(0x25, "1200") #PWINFO_TOTAMNT
        paygoLib.PW_iAddParam(0x26, "986") # PWINFO_CURRENCY
        paygoLib.PW_iAddParam(0x27, "2")#PWINFO_CURREXP
        #================= mandatory params  ============
        paygoLib.PW_iAddParam(0x17, "COOLBAG-SAFE GUARDA BAGAGENS AUTOMATIZADO") #PWINFO_AUTDEV
        paygoLib.PW_iAddParam(0x16, "1.0") #PWINFO_AUTVER
        paygoLib.PW_iAddParam(0x15, "COOLBAGSAFE-RENTLOCKER") #PWINFO_AUTNAME
        paygoLib.PW_iAddParam(0X24, "0") #PWINFO_AUTCAP
        #paygoLib.PW_iAddParam(E_PWINFO..value, "35223093000106") #PWINFO_MERCHCNPJCPF

        ret = ''
        szDspMsg = create_string_buffer(10000)
        
        ulEvent = c_int32(0)
        """ret = pgwLib.PW_iPPDisplay(b"INSERIR OU PASSE O CARTAO")
        import time
        time.sleep(3)
        if ret == '':
            ret = pgwLib.PW_iPPDisplay(b"INSERIR OU PASSE O CARTAO")
            time.sleep(3)
        else:
            ret = pgwLib.PW_iPPDisplay(b"DIGITE A SENHA")
            print ("ret PW_iPPDisplay", ret)
        ret = '' """
        vstParam_1 = (PW_GetData * 1)
        vstParam1 = vstParam_1()
            


        while ret != 0:
            ret = paygoLib.PW_iPPEventLoop(szDspMsg, 100)
            print("ret PW_iPPEventLoop", ret)
            ret = self.PW_iExecTransac(vstParam, iNumParam)
            print("ret PW_iExecTransac", ret)
            
            card_inf = paygoLib.PW_iNewTransac(0x27)
            print("card_inf", card_inf)
            
            sleep(5)

        ret = ''


        """while ret != 0:
            ret = self.PW_iExecTransac(vstParam, iNumParam)
            print("ret PW_iExecTransac", ret)
            paygoLib.
            time.sleep(20)
                ret = pgwLib.PW_iPPWaitEvent(ulEvent)
            print(" ret PW_GetData", ret)"""



        PrintResultParams()
        print(ret)
        


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
    