#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import ctypes
from ctypes import *
from time import sleep
import sys
import os
#from Interops import *
from Enums import *
from CustomObjects import *




class PayGoPayment:
    def __init__(self):
           
        #busca o diretório onde está o executavel 
        self.me = os.path.abspath(os.path.dirname(__file__))
        
        #cria o diretório PGWebLib
        directory = "."
    
        # Parent Directory path 
        parent_dir = self.me
        
        # Path 
        path = os.path.join(parent_dir, directory) 
        
        # Create the directory 
        # 'GeeksForGeeks' in 
        # '/home / User / Documents' 
        if(os.path.exists(path) != True):
            os.mkdir(path) 

        self.aux_path  = os.path.join(self.me,  "PGWebLib.so")
        self.path_init = os.path.join(self.me,  "PGWebLib")
        self.PGWebLib_dll = CDLL(self.aux_path)
        self.payment()

    def PW_iInit(self):
        self.PW_iInitObj          = self.PGWebLib_dll.PW_iInit
        self.PW_iInitObj.restype  = c_short
        self.PW_iInitObj.argtypes = [c_char_p]
        self.b_path_init = self.path_init.encode('utf-8')
        
        return self.PW_iInitObj(c_char_p(self.b_path_init))

    
    def PW_iNewTransac(self,bOper):
        self.PW_iNewTransactObj          = self.PGWebLib_dll.PW_iNewTransac
        self.PW_iNewTransactObj.restype  = c_short
        self.PW_iNewTransactObj.argtypes = [c_byte]
        return self.PW_iNewTransactObj(c_byte(bOper))


    def PW_iAddParam(self,wParam,pszValue):
        self.PW_iAddParamObj          = self.PGWebLib_dll.PW_iAddParam
        self.PW_iAddParamObj.restype  = c_short
        self.PW_iAddParamObj.argtypes = [c_int16,c_char_p]
        pszValueAux = pszValue.encode('utf-8')
        #print("add parametro", self.PW_iAddParamObj(c_int16(wParam),c_char_p(pszValueAux)))
        return self.PW_iAddParamObj(c_int16(wParam),c_char_p(pszValueAux))


    def PW_iExecTransac(self,vstParam, iNumParam):
            self.PW_iExecTransacObj          = self.PGWebLib_dll.PW_iExecTransac
            self.PW_iExecTransacObj.restype  = c_short

            
            self.PW_iExecTransacObj.argtypes = [POINTER((PW_GetData *11)),POINTER(c_int)]
            
            
            
            ret = self.PW_iExecTransacObj(byref(vstParam),byref(c_int(iNumParam)))
        

            return ret
    def PW_iExecGetData(self,vstParam, iNumParam):
        self.PW_iExecGetDataObj  = self.PGWebLib_dll.PW_iPPGetData
        self.PW_iExecGetDataObj.restype = c_short
        self.PW_iExecTransacObj.argtypes = [POINTER(PW_GetData * 11), POINTER(c_int)]
        ret = self.PW_iExecTransacObj(byref(vstParam), byref(c_int(iNumParam)))
        return ret
    

    def PW_iGetResult(self,cod, szAux, szAuxSize):
        self.PW_iGetResultObj          = self.PGWebLib_dll.PW_iGetResult
        self.PW_iGetResultObj.restype  = c_short

        #steste = create_string_buffer(10000)
        self.PW_iGetResultObj.argtypes = [c_int16, c_char_p, c_uint32]


        #ret = self.PW_iGetResultObj(c_int16(cod),steste,sizeof(steste))
        ret = self.PW_iGetResultObj(c_int16(cod),szAux,szAuxSize)
        #saida = steste.value
        #print("stest = ",saida)
        return ret

    def PW_iPPRemoveCard(self):
        self.PW_iPPRemoveCardObj          = self.PGWebLib_dll.PW_iPPRemoveCard
        self.PW_iPPRemoveCardObj.restype  = c_short
        self.PW_iPPRemoveCardObj.argtypes = []

        ret = self.PW_iPPRemoveCardObj()
        return ret
    
    def PW_iPPEventLoop(self, pszDisplay, ulDisplaySize):
        self.PW_iPPEventLoopObj          = self.PGWebLib_dll.PW_iPPEventLoop
        self.PW_iPPEventLoopObj.restype  = c_short
        self.PW_iPPEventLoopObj.argtypes = [c_char_p,c_uint32]

        ret = self.PW_iPPEventLoopObj(pszDisplay,c_uint32(ulDisplaySize))
        return ret
    def PW_iPPWaitEvent(self, iNumParam):
        self.PW_iPPWaitEventObj          = self.PGWebLib_dll.PW_iPPWaitEvent
        self.PW_iPPWaitEventObj.restype  = c_short
        self.PW_iPPWaitEventObj.argtypes = [POINTER(c_int)]
        ret = self.PW_iPPWaitEventObj(byref(c_int(iNumParam)))
        return ret
    
    def PW_iPPGetData(self, uiIndex):
        self.PW_iPPGetDataObj          = self.PGWebLib_dll.PW_iPPGetData
        self.PW_iPPGetDataObj.restype  = c_short
        self.PW_iPPGetDataObj.argtypes = [c_int]
        ret = self.PW_iPPGetDataObj(c_int(uiIndex))
        return ret
    
    


    def payment(self):
        directory = os.path.abspath(os.path.dirname(__file__))
        vstParam_11 = (PW_GetData * 11)
        vstParam = vstParam_11()
        iNumParam = 10
        iRet=0
        
        
        ulEvent = 0
        
        self.PW_iInit()
        #print("resultado init", iInit)
        ntransac = self.PW_iNewTransac(0x21)
        print("resultado ntransac", ntransac)
        params = []
        #self.PW_iAddParam(0X11,"62547") #PWINFO_POSID
        self.PW_iAddParam(0x29,"1") #PWINFO_CARDTYPE
        sleep(0.1)
        self.PW_iAddParam(0x3B,"1") #PWINFO_FINTYPE
        sleep(0.1)
        self.PW_iAddParam(0x35,"CIELO") #PWINFO_AUTHSYST
        sleep(0.1)
        #self.PGWebLib_dll.PW_iAddParam(0x3C, "3")#PWINFO_INSTALLMENTS
        self.PW_iAddParam(0x25, "1200") #PWINFO_TOTAMNT
        sleep(0.1)
        self.PW_iAddParam(0x26, "986") # PWINFO_CURRENCY
        sleep(0.1)
        self.PW_iAddParam(0x27, "2")#PWINFO_CURREXP
        sleep(0.1)
        #================= mandatory params  ============
        self.PW_iAddParam(0x17, "COOLBAG-SAFE GUARDA BAGAGENS AUTOMATIZADO") #"SETIS AUTOMACAO E SISTEMA LTDA")# PWINFO_AUTDEV
        sleep(0.1)
        self.PW_iAddParam(0x16, "1.0") #PWINFO_AUTVER
        sleep(0.1)
        self.PW_iAddParam(0x15, "COOLBAGSAFE-RENTLOCKER") #"PGWEBLIBTEST")##PWINFO_AUTNAME
        sleep(0.1)
        self.PW_iAddParam(0X24, "4") #PWINFO_AUTCAP
        sleep(0.1)
        #self.PGWebLib_dll.PWCNF_CNF_AUTO()
        
        #self.PW_iAddParam()
        """
        self.PW_iAddParam(0x1C, "35223093000106") #PWINFO_MERCHCNPJCPF
        sleep(0.1)
        self.PW_iAddParam(0x36, "0")
        sleep(0.1)
        self.PW_iAddParam(0x6C, "0")
        sleep(0.1)
        self.PW_iAddParam(0x6F, "PROCESSANDO....")
        sleep(0.1)
        self.PW_iAddParam(0xC0, "4")
        sleep(0.1)
        self.PW_iAddParam(0xCF, "8")
        sleep(0.1)
        self.PW_iAddParam(0xF4, "0")
        sleep(0.1)
        self.PW_iAddParam(0x1F21, "1")
        sleep(0.1)
        self.PW_iAddParam(0xF6, "PGWEBLIBTEST")
        sleep(0.1)
        self.PW_iAddParam(0x1B, self.PWINFO_DESTTCPIP)
        sleep(0.1)
        self.PW_iAddParam(0x43, "1")
        sleep(0.1)
        self.PW_iAddParam(0x1F21, "1")
        sleep(0.3)
        
        #self.PW_iAddParam(0x7F01, "1")
        #sleep(0.1)
        #self.PW_iAddParam(0x7F02, "0")"""
        params = [
            0x29,0x3B,0x35, 0x3C, 0x25,0x26,0x27,0x17,0x16,0x15,0X24 
                ]

        ret = ''
        retEventLoop = -2493
        retGetResult = ''
        retGetPin = ''
        retTransac = ''
        retExecGetData = ''
        retExecGetCard = ''
        retWait = ''
        iRet = ''
        key = ''
        ppEvent = ''
        ppEventRemove = ''
        szDspMsg = create_string_buffer(100000)
        
        
        
        while retEventLoop != 0:
            
            retEventLoop = self.PW_iPPEventLoop( szDspMsg, 1000 )
            retTransac = self.PGWebLib_dll.PW_iExecTransac(byref(vstParam), byref(c_int(iNumParam)))
            #ret = self.PW_iExecTransacObj(byref(vstParam),byref(c_int(iNumParam)))
            print("retTransac", retTransac)
            while ppEvent != 0:
                        ppEvent = self.PGWebLib_dll.PW_iPPWaitEvent(byref(c_int(4)))
                        print("ppEvent", ppEvent)
                        sleep(0.3)
            while key != 0:
                self.PGWebLib_dll.PW_iPPDisplay(b"DIGITE A SENHA\r\r")
                key = self.PGWebLib_dll.PW_iPPWaitEvent(byref(c_int(6)))
                print("key", key)
                sleep(5)
                keyOk = key = self.PGWebLib_dll.PW_iPPWaitEvent(byref(c_byte(0x13)))
                print("keyOk", keyOk)
                sleep(2)
            #ntransac = self.PW_iNewTransac(0x27)
            if retTransac == -2497:
            
                for i in range(0, len(params)):
                    
                    #retExecGetCard =  self.PGWebLib_dll.PW_iPPGetCard(c_int(params[i]))
                    #print("retExecGetCard", retExecGetCard)
                    iRet = self.PGWebLib_dll.PW_iGetResult(params[i], szDspMsg,  1000)
                    print("iRet",i, " = ", iRet)
                    sleep(0.3)
                    retExecGetData = self.PGWebLib_dll.PW_iPPGetData(params[i])
                    print("retExecGetData",i, " = ", retExecGetData)
                    sleep(0.3)
                    
            PWINFO_REQNUM = PWINFO_AUTLOCREF = PWINFO_AUTEXTREF = PWINFO_VIRTMERCH = PWINFO_AUTHSYST = create_string_buffer(100000)
            retPWINFO_REQNUM = self.PGWebLib_dll.PW_iGetResult(0x32, "PWINFO_REQNUM",  1000)
            print("retPWINFO_REQNUM", retPWINFO_REQNUM)
            retPWINFO_AUTLOCREF = self.PGWebLib_dll.PW_iGetResult(0x44, "PWINFO_AUTLOCREF",  1000)
            print("retPWINFO_AUTLOCREF", retPWINFO_AUTLOCREF)
            retPWINFO_AUTEXTREF = self.PGWebLib_dll.PW_iGetResult(0x45, "PWINFO_AUTEXTREF",  1000)
            print("retPWINFO_AUTEXTREF", retPWINFO_AUTEXTREF)
            retPWINFO_VIRTMERCH = self.PGWebLib_dll.PW_iGetResult(0x36, "PWINFO_VIRTMERCH",  1000)
            print("retPWINFO_VIRTMERCH", retPWINFO_VIRTMERCH)
            retPWINFO_AUTHSYST = self.PGWebLib_dll.PW_iGetResult(0x36, "PWINFO_AUTHSYST",  1000)
            print("retPWINFO_AUTHSYST", retPWINFO_AUTHSYST)

            ret = self.PGWebLib_dll.PW_iConfirmation(1, PWINFO_REQNUM, PWINFO_AUTLOCREF,
                                 PWINFO_AUTEXTREF, PWINFO_VIRTMERCH, PWINFO_AUTHSYST)
            print("retIget result" , ret)
            retEventLoop = self.PW_iPPEventLoop( szDspMsg, 1000 )

            print("iRet",i, " = ", iRet)
            print("szDspMsg", szDspMsg.value)
            print("retEventLoop", retEventLoop)

           
             
            
        
           

if __name__ == '__main__':
    PayGoPayment()
    
