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

        #self.valor = sys.argv[1]
           
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
    
    def PW_iExecGetData(self, vstParam, iNumParam):
        iKey = ''
        ikeydisplay = ''
        iKeyGetData = ''
        getcard = ''
        
        for i in range(0, iNumParam):
            ret = vstParam[i].wIdentificador
            #getcard = self.PGWebLib_dll.PW_iPPGetCard(c_short(i))
            #print("getcard", getcard)
            print("vstParam identificador", vstParam[i].wIdentificador)
            print("ret getdata", ret)
            #msgMenu = create_string_buffer(100000)
            if ret == E_PWINFO.PWINFO_LOCALINFO1.value:
                #vstParam[i].bTeclasDeAtalho = 1
                vstParam[i].bTipoDeDado = E_PWDAT.PWDAT_MENU.value
                vstParam[i].bNumOpcoesMenu = 2
                vstParam[i].vszValorMenu[0] = create_string_buffer(b"F1 - CREDITO", 256)
                vstParam[i].vszValorMenu[1] = create_string_buffer(b"F2 - DEBITO", 256)
                vstParam[i].szPrompt = b"F1 - CREDITO\nF2 - DEBITO"
                iKey = ''

                while iKey != 0:
                    ulEvent = 0

                    ikeydisplay = self.PW_iPPDisplay("F1 - CREDITO\nF2 - DEBITO")
                    print("ikeydisplay", ikeydisplay)
                    iKey = self.PW_iPPWaitEvent(15)
                    if iKey:
                        szDspMsg = create_string_buffer(100000)
                        retEventLoop = self.PW_iPPEventLoop(szDspMsg, 1000)
                        print("retEventLoop szDspMsg", retEventLoop, szDspMsg)
                        print("iKey wait", iKey)
                        return retEventLoop

                    retEventLoop = ''
                    szDspMsg = create_string_buffer(100000)
                    retEventLoop = self.PW_iPPEventLoop(szDspMsg, 1000)
                    print("retEventLoop szDspMsg", retEventLoop, szDspMsg)
                    retTransac = self.PW_iExecTransac(vstParam, iNumParam)
                    print("retTransac getdata", retTransac)

                    iKey = ''
                    if iKey == 0:
                        
                        retEventLoop = self.PW_iPPEventLoop(szDspMsg, 1000)
                        print("retEventLoop szDspMsg", retEventLoop, szDspMsg)
                        #iKey = self.PW_iPPGetData(i)
                        #print("iKey GetData", iKey)

                        self.PW_iAddParam(0x29, "1")
                        self.PGWebLib_dll.PW_iAddParam(vstParam[i].wIdentificador, vstParam[i].vszValorMenu[0])
                        print("vstParam vszvalormenu", vstParam[i].wIdentificador , vstParam[i].vszValorMenu[0])
                        self.PW_iAddParam(0x7F0A, "CREDITO")
                        #self.PW_iPPDisplay("CREDITO")
                        
                        sleep(2)
                    elif iKey == 34:
                        self.PW_iAddParam(0x29, "2")
                        self.PW_iAddParam(0x7F0A, "DEBITO")
                        #self.PW_iPPDisplay("DEBITO")
                        sleep(2)
                    else:
                        return "valor escolhido indisponivel"

                    
                    
                    self.PGWebLib_dll.PW_iAddParam(vstParam[i].wIdentificador, vstParam[i].szPrompt )#vszValorMenu[key])

            elif ret == E_PWINFO.PWINFO_AUTHTECHUSER.value:
                result = ''
                result = self.PW_iAddParam(0xF6, "314159")
                return result
            elif ret == E_PWINFO.PWINFO_MERCHCNPJCPF.value:
                result = self.PW_iAddParam(0x1C, "35223093000106")
                return result    
        
        return ret
    

    def PW_iGetResult(self,cod, szAux, szAuxSize):
        self.PW_iGetResultObj          = self.PGWebLib_dll.PW_iGetResult
        self.PW_iGetResultObj.restype  = c_short

        #steste = create_string_buffer(10000)
        self.PW_iGetResultObj.argtypes = [c_int16, c_char_p, c_uint32]


        #ret = self.PW_iGetResultObj(c_int16(cod),steste,sizeof(steste))
        return self.PW_iGetResultObj(c_int16(cod),szAux,szAuxSize)
        #saida = steste.value
        #print("stest = ",saida)
        #return ret
    def PW_iConfirmation(self,ulResult,pszReqNum, pszLocRef,pszExtRef,pszVirtMerch,pszAuthSyst):
        self.PW_iConfirmationObj          = self.PGWebLib_dll.PW_iConfirmation
        self.PW_iConfirmationObj.restype  = c_short
        self.PW_iConfirmationObj.argtypes = [c_uint32,POINTER(c_byte),POINTER(c_byte),POINTER(c_byte),POINTER(c_byte),POINTER(c_byte)]

        """pszReqNumAux    = pszReqNum.encode('utf-8')
        pszLocRefAux    = pszLocRef.encode('utf-8')
        pszExtRefAux    = pszExtRef.encode('utf-8')
        pszVirtMerchAux = pszVirtMerch.encode('utf-8')
        pszAuthSystAux  = pszAuthSyst.encode('utf-8')"""
    
        return self.PW_iConfirmationObj(c_uint32(ulResult),byref(c_byte(pszReqNum)),byref(c_byte(pszLocRef)),byref(c_byte(pszExtRef)),
                                    byref(c_byte(pszVirtMerch)),byref(c_byte(pszAuthSyst)))

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
    """def PW_iPPWaitEvent(self,vstParam, iNumParam):
        self.PW_iPPWaitEventObj          = self.PGWebLib_dll.PW_iPPWaitEvent
        self.PW_iPPWaitEventObj.restype  = c_short
        self.PW_iPPWaitEventObj.argtypes = [POINTER(c_int)]
        ret = self.PW_iPPWaitEventObj(byref(c_int(iNumParam)))
        return ret"""
    def PW_iPPWaitEvent(self, ulEvent):
        self.PW_iPPWaitEventObj          = self.PGWebLib_dll.PW_iPPWaitEvent
        self.PW_iPPWaitEventObj.restype  = c_short
        self.PW_iPPWaitEventObj.argtypes = [POINTER(c_int)]
        ret =  self.PW_iPPWaitEventObj(byref(c_int(ulEvent)))
        return ret
    
    def PW_iPPGetData(self, uiIndex):
      self.PW_iPPGetDataObj          = self.PGWebLib_dll.PW_iPPGetData
      self.PW_iPPGetDataObj.restype  = c_short
      self.PW_iPPGetDataObj.argtypes = [c_uint16]
      ret = self.PW_iPPGetDataObj(c_uint16(uiIndex))
      return ret
        
    def PW_iPPDisplay(self,pszMsg):
      self.PW_iPPDisplayObj          = self.PGWebLib_dll.PW_iPPDisplay
      self.PW_iPPDisplayObj.restype  = c_short
      self.PW_iPPDisplayObj.argtypes = [c_char_p]
      pszMsgAux = pszMsg.encode('utf-8')
      return self.PW_iPPDisplayObj(c_char_p(pszMsgAux))
    
    def PW_iPPGetUserData(self,uiMessageId, bMinLen, bMaxLen,  iToutSec, pszData):
      self.PW_iPPGetUserDataObj          = self.PGWebLib_dll.PW_iPPGetUserData
      self.PW_iPPGetUserDataObj.restype  = c_short
      self.PW_iPPGetUserDataObj.argtypes = [c_short, c_short, c_short, c_short, POINTER(c_char)]
      
      ret = self.PW_iPPGetUserDataObj(c_short(uiMessageId), c_short(bMinLen), c_short(bMaxLen), c_short(iToutSec),pszData)
      
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
        self.PW_iNewTransac(0x21)
        params = []
        #self.PW_iAddParam(0x29,"1") #PWINFO_CARDTYPE 1: crédito 2: débito 4: voucher/PAT 8: outros
        #sleep(0.1)
        self.PW_iAddParam(0x3B,"1") #PWINFO_FINTYPE
        sleep(0.1)
        self.PW_iAddParam(0x35,"REDE") #PWINFO_AUTHSYST
        sleep(0.1)
        self.PW_iAddParam(0x36, "0")
        sleep(0.1)
        #self.PGWebLib_dll.PW_iAddParam(0x3C, "3")#PWINFO_INSTALLMENTS
        self.PW_iAddParam(0x25, "1200")#str(self.valor)) #PWINFO_TOTAMNT valor total da compra
        sleep(0.1)
        self.PW_iAddParam(0x26, "986") # PWINFO_CURRENCY
        sleep(0.1)
        self.PW_iAddParam(0x27, "2")#PWINFO_CURREXP
        sleep(0.1)
        #================= mandatory params  ============
        self.PW_iAddParam(0x17, "COOLBAG-SAFE GUARDA BAGAGENS AUTOMATIZADO LTDA") #"SETIS AUTOMACAO E SISTEMA LTDA")# PWINFO_AUTDEV
        sleep(0.1)
        self.PW_iAddParam(0x16, "1.0") #PWINFO_AUTVER
        sleep(0.1)
        self.PW_iAddParam(0x15, "COOLBAGSAFE-RENTLOCKER") #"PGWEBLIBTEST")##PWINFO_AUTNAME
        sleep(0.1)
        self.PW_iAddParam(0X24, "4") #PWINFO_AUTCAP Capacidades da Automação (soma dos valores abaixo): 1: funcionalidade de troco/saque; 2: funcionalidade de desconto; 4: valor fixo, sempre incluir; 8: impressão das vias diferenciadas do comprovante para Cliente/Estabelecimento; 16: impressão do cupom reduzido. 32: utilização de saldo total do voucher para abatimento do valor da compra.
        sleep(0.1)
        self.PW_iAddParam(0x6C, "0")
        sleep(0.1)
        self.PW_iAddParam(0x6F, "PROCESSANDO...") #PWINFO_PROCESSMSG
        sleep(0.1)
        #self.PW_iAddParam(0xC0, "375")
        #sleep(0.1)
        
        self.PW_iAddParam(0xF4, "0") #PWINFO_RCPTPRN 0: não há comprovante 1: imprimir somente a via do Cliente 2: imprimir somente a via do Estabelecimento 3: imprimir ambas as vias do Cliente e do Estabelecimento
        sleep(0.1)
        self.PW_iAddParam(0x1F21, "1")
        sleep(0.1)
        self.PW_iAddParam(0xF6, "314159")
        sleep(0.1)
        self.PW_iAddParam(0x1C, "35223093000106")
        
        
        params = [
            0x29,0x3B,0x35, 0x3C, 0x25,0x26,0x27,0x17,0x16,0x15,0X24,0x1F21, 0xF6, 0x1C
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
        keyF = ''
        ppEvent = ''
        ppEventRemove = ''
        pzData = szDspMsg = create_string_buffer(100000)
        ulEvent = 0
        


        while ppEvent != 0:
            ppEvent = self.PW_iPPWaitEvent(15)#(byref(c_int(15)))
            print("ppEvent", ppEvent)
            sleep(3)
            retEventLoop = self.PW_iPPEventLoop(szDspMsg, 1000)
            print("retEventLoop szDspMsg", retEventLoop, szDspMsg.value)
        
        
       

        key = ''
        while key != 0:
            self.PW_iPPDisplay("DIGITE A PALAVRA PASSE\r")
            self.PW_iPPWaitEvent(6)#(byref(c_int(6)))
            
            sleep(5)
            key = self.PW_iPPWaitEvent(0x13)#(byref(c_int(0x13)))
            
            sleep(2)
            retEventLoop = self.PW_iPPEventLoop(szDspMsg, 1000)
            print("retEventLoop szDspMsg", retEventLoop, szDspMsg.value)
        retTransac = self.PGWebLib_dll.PW_iExecTransac(byref(vstParam), byref(c_int(iNumParam)))
        
        #ret = self.PW_iExecTransacObj(byref(vstParam),byref(c_int(iNumParam)))
        print("retTransac", retTransac)
        retiGetResult = ''
        
        
                
        PWINFO_REQNUM = create_string_buffer(100000)
        PWINFO_AUTLOCREF = create_string_buffer(100000)
        PWINFO_AUTEXTREF = create_string_buffer(100000)
        PWINFO_VIRTMERCH = create_string_buffer(100000)
        PWINFO_AUTHSYST = create_string_buffer(100000)
        retPWINFO_REQNUM = self.PGWebLib_dll.PW_iGetResult(c_int16(0x32), PWINFO_REQNUM, c_uint32(10000))
                    
        print("retPWINFO_REQNUM", retPWINFO_REQNUM)
        retPWINFO_AUTLOCREF = self.PW_iGetResult(0x44, PWINFO_AUTLOCREF,  10000)
        print("retPWINFO_AUTLOCREF", retPWINFO_AUTLOCREF)
        retPWINFO_AUTEXTREF = self.PW_iGetResult(0x45, PWINFO_AUTEXTREF,  10000)
        print("retPWINFO_AUTEXTREF", retPWINFO_AUTEXTREF)
        retPWINFO_VIRTMERCH = self.PW_iGetResult(0x36, PWINFO_VIRTMERCH,  10000)
        print("retPWINFO_VIRTMERCH", retPWINFO_VIRTMERCH)
        retPWINFO_AUTHSYST = self.PW_iGetResult(0x35, PWINFO_AUTHSYST,  10000)
        print("retPWINFO_AUTHSYST", retPWINFO_AUTHSYST)
        retConfirm = ''
        

        retConfirm = self.PW_iConfirmation(1, retPWINFO_REQNUM, retPWINFO_AUTLOCREF,
                                retPWINFO_VIRTMERCH, retPWINFO_VIRTMERCH, retPWINFO_AUTHSYST)
        print("retIget result" , retConfirm)
        
        ret = ''
        

        
            
            
        retTransac = self.PW_iExecTransac(vstParam,iNumParam)
        print("retTransac", retTransac)
        while retTransac == -2497:
            retExecGetData = self.PW_iExecGetData(vstParam, iNumParam)
            print("retExecGetData", retExecGetData)
            sleep(10)
            retTransac = self.PW_iExecTransac(vstParam,iNumParam)
            print("retTransac", retTransac)
            if retTransac == 0:
                retEventLoop = self.PW_iPPEventLoop(szDspMsg, 1000)
                print("retEventLoop szDspMsg", retEventLoop, szDspMsg.value)
                retRemoveCard = ''
                print("remove card ....")
                self.PW_iPPDisplay(" RETIRE O CARTAO ")
                sleep(2)
                self.PW_iPPRemoveCard()
                return "PWRET_OK"

        #print("iRet",i, " = ", iRet)
        print("szDspMsg", szDspMsg.value)            
        print("retEventLoop", retEventLoop)
        """if retEventLoop == 0 and retTransac == 0:
            return retEventLoop , retTransac"""
        #retTransac = self.PGWebLib_dll.PW_iExecTransac(byref(vstParam), byref(c_int(iNumParam)))
        """for i in range(len(params)):
            retiGetResult = self.PW_iPPGetData(vstParam[i])#self.PGWebLib_dll.PW_iGetResult(c_int16(i), szDspMsg, c_uint32(10000))
            print("retiGetResult", retiGetResult)
            sleep(0.3)"""
        
        


            

           
             
            
        
           

if __name__ == '__main__':
    PayGoPayment()
    
