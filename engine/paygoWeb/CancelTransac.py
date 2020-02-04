from Interops import *
from Enums import *
from CustomObjects import *
import os
import sys
import json
from datetime import datetime, timedelta
from ctypes import *



class CancelTransaction:
    def __init__(self):

        self.szDspMsg = create_string_buffer(100000)

        self.pgWeb = PGWebLibrary()
        # INICIALIZA A BIBLIOTECA
        self.pgWeb.PW_iInit()
        # EXECUTA A FUNÇÃO VENDA
        self.cancel_transac()

    def cancel_transac(self):
        iRet = ''
        vstParam_11 = (PW_GetData * 11)
        vstParam = vstParam_11()
        iNumParam = 10
        ulEvent = 0
        szDspMsg = c_buffer(128)
        szAux = create_string_buffer(10000)
        wait = ''
        retEventLoop = ''
        ret = ''
        ret2 = ''
        data = datetime.now()
        # INICIA UMA NOVA TRANSACAO
        self.pgWeb.PW_iNewTransac(E_PWOPER.PWOPER_SALEVOID.value)
        try:
            f = open('comprovantes/REGISTRO DATA:%s %s %s .json' %(data.day, data.month, data.year), 'r+')
            registro_json = f.read()
            registro_json = registro_json.replace("\n","")
            registro_json = registro_json.replace(" ","")
            registro_json = registro_json.replace("}{","},{")
            registro_json = eval(registro_json)
            PWINFO_TRNORIGDATE = data.strptime("%s%s%s"%(data.day, data.month, data.year),"%d%m%Y").strftime("%d%m%y")
            f.close()   
                            
        except FileNotFoundError:
            data_anterior = data - timedelta(days=1)
            f = open('comprovantes/REGISTRO DATA:%s %s %s .json' %(data.day, data.month, data.year), 'r+')
            registro_json = f.read()
            registro_json = registro_json.replace("\n","")
            registro_json = registro_json.replace(" ","")
            registro_json = registro_json.replace("}{","},{")
            registro_json = eval(registro_json)
            PWINFO_TRNORIGDATE = data_anterior.strptime("%s%s%s"%(data_anterior.day, data_anterior.month, data_anterior.year), "%d%m%Y").strftime("%d%m%y")
            f.close()
            
        print("len registro json",len(registro_json))
        
        if type(registro_json) == dict:
            PWINFO_TRNORIGREQNUM = registro_json["PWINFO_REQNUM"]
            PWINFO_TRNORIGTIME = registro_json["DATA_HORARIO"]
            PWINFO_TRNORIGAUTH = registro_json["PWINFO_AUTHCODE"]
            PWINFO_TRNORIGNSU = registro_json["PWINFO_AUTEXTREF"]
            PWINFO_AUTLOCREF = registro_json["PWINFO_AUTLOCREF"]
            PWINFO_VIRTMERCH = registro_json["PWINFO_VIRTMERCH"]
            PWINFO_AUTHCODE = registro_json["PWINFO_AUTHCODE"]
            
        elif type(registro_json) == tuple:
            PWINFO_TRNORIGREQNUM = registro_json[-1]["PWINFO_REQNUM"]
            PWINFO_TRNORIGTIME = registro_json[-1]["DATA_HORARIO"]
            PWINFO_TRNORIGAUTH = registro_json[-1]["PWINFO_AUTHCODE"]
            PWINFO_TRNORIGNSU = registro_json[-1]["PWINFO_AUTEXTREF"]
            PWINFO_AUTLOCREF = registro_json[-1]["PWINFO_AUTLOCREF"]
            PWINFO_VIRTMERCH = registro_json[-1]["PWINFO_VIRTMERCH"]
            
            
        # MANDADATORY PARAMS
        self.pgWeb.PW_iAddParam( E_PWINFO.PWINFO_AUTNAME.value, "COOLBAGSAFE-RENTLOCKER")
        self.pgWeb.PW_iAddParam( E_PWINFO.PWINFO_AUTVER.value, "1.0")
        self.pgWeb.PW_iAddParam( E_PWINFO.PWINFO_AUTDEV.value, "COOLBAG-SAFE GUARDA BAGAGENS AUTOMATIZADO")
        self.pgWeb.PW_iAddParam( E_PWINFO.PWINFO_AUTCAP.value, "28")
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_CURRENCY.value, "986")  # MOEDA: REAL
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_CURREXP.value, "2")
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_POSID.value, "62547")
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_TRNORIGAMNT.value, "100")
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_TRNORIGDATE.value, PWINFO_TRNORIGDATE)
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_TRNORIGTIME.value, PWINFO_TRNORIGTIME)
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_TRNORIGNSU.value, PWINFO_TRNORIGNSU)
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_AUTLOCREF.value, PWINFO_AUTLOCREF)
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_TRNORIGREQNUM.value, PWINFO_TRNORIGREQNUM)
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_VIRTMERCH.value, PWINFO_VIRTMERCH)
        #self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_AUTHSYST.value, PWINFO_AUTHSYST)
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_AUTHMNGTUSER.value, "1111")
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_AUTHTECHUSER.value, "314159")
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_BOARDINGTAX.value, "00")
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_TIPAMOUNT.value, "00")

        ret = self.pgWeb.PW_iExecTransac(vstParam, iNumParam)
        print("ret admin", ret)

        
        list_errors_pinpad = [
                    -2100, -2101, -2102, -2103, -2104, -2105, -2106, -2107, -2108, -2109, -2110, 
                    -2111, -2112, -2113, -2114, -2115, -2116, -2117, -2118, -2119, -2120, -2121,
                    -2122, -2123, -2124, -2125, -2126, -2127, -2128, -2129, -2130, -2131, -2132,
                    -2133, -2134, -2135, -2136, -2137, -2138, -2139, -2140, -2141, -2142, -2143, 
                    -2144, -2145, -2146, -2147, -2148, -2149, -2150, -2151, -2152, -2153, -2154, 
                    -2155, -2156, -2157, -2158, -2159, -2160, -2161, -2162, -2163, -2164, -2165, 
                    -2166, -2167, -2168, -2169, -2170, -2171, -2172, -2173, -2174, -2175, -2176, 
                    -2177, -2178, -2179, -2180, -2181, -2182, -2183, -2184, -2185, -2186, -2187, 
                    -2188, -2189, -2190, -2191, -2192, -2193, -2194, -2195, -2196, -2197, -2198, 
                    -2199, -2200]
        if ret == E_PWRET.PWRET_MOREDATA.value or ret == E_PWRET.PWRET_NOTHING.value or (ret in list_errors_pinpad):
            print("retorno transacao", ret)

            while ret == -2497 or ret == E_PWRET.PWRET_NOTHING.value or (ret in list_errors_pinpad):
                
                # PERCORRE OS DADOS E RECUPERA OS FALTANTES
                ret = self.pgWeb.PW_iExecGetData(vstParam, iNumParam)
                print("ret exectransac venda", ret)


                if ret == E_PWRET.PWRET_CANCEL.value or (ret in list_errors_pinpad):
                    print("E_PWRET.PWRET_CANCEL")
                    self.pgWeb.PW_iPPAbort()
                    retEventLoop = self.pgWeb.PW_iPPEventLoop(
                        self.szDspMsg, sizeof(self.szDspMsg))
                    print("retEventLoop", retEventLoop)
                    return retEventLoop

                elif ret == E_PWRET.PWRET_HOSTTIMEOUT.value:
                    self.pgWeb.PW_iPPAbort()
                    retEventLoop = self.pgWeb.PW_iPPEventLoop(
                        self.szDspMsg, sizeof(self.szDspMsg))
                    print("retEventLoop", retEventLoop)
                    return retEventLoop
                elif ret == E_PWRET.PWRET_REQPARAM.value:
                    print("PWRET_REQPARAM", E_PWRET.PWRET_REQPARAM.value)
                    self.pgWeb.PW_iPPAbort()
                    retEventLoop = self.pgWeb.PW_iPPEventLoop(
                        self.szDspMsg, sizeof(self.szDspMsg))
                    print("retEventLoop", retEventLoop)
                    return retEventLoop
                elif ret == E_PWRET.PWRET_FROMHOSTPENDTRN.value:
                    print("PWRET_FROMHOSTPENDTRN",
                          E_PWRET.PWRET_FROMHOSTPENDTRN.value)
                    self.confirmPendTransaction(
                        transactionStatus=1, transactionResponse=ret)
                    retEventLoop = self.pgWeb.PW_iPPEventLoop(
                        self.szDspMsg, sizeof(self.szDspMsg))
                    print("retEventLoop", retEventLoop)
                    return retEventLoop

                ret = self.pgWeb.PW_iExecTransac(vstParam, iNumParam)
                print("efetuando a transacao...")
                print("ret ---->", ret)
        self.pgWeb.PW_iGetResult(
            E_PWINFO.PWINFO_TRNORIGAUTH.value, szAux, sizeof(szAux))
        PWINFO_TRNORIGAUTH = szAux.value.decode('utf-8')
        print("PWINFO_TRNORIGAUTH", PWINFO_TRNORIGAUTH)
        sleep(0.1)

        
        self.pgWeb.PW_iGetResult(E_PWINFO.PWINFO_FISCALREF.value, szAux, sizeof(szAux))
        PWINFO_FISCALREF = szAux.value.decode('utf-8')
        print("PWINFO_FISCALREF", PWINFO_FISCALREF)
        sleep(0.1)

        #=========================== ADICIONAIS ===========================

        self.pgWeb.PW_iGetResult(E_PWINFO.PWINFO_AUTMERCHID.value, szAux, sizeof(szAux))
        PWINFO_AUTMERCHID = szAux.value.decode('utf-8')
        print("PWINFO_AUTMERCHID", PWINFO_AUTMERCHID)
        sleep(0.1)

        self.pgWeb.PW_iGetResult(E_PWINFO.PWINFO_PRODUCTID.value, szAux, sizeof(szAux))
        PWINFO_PRODUCTID = szAux.value.decode('utf-8')
        print("PWINFO_AUTMERCHID", PWINFO_AUTMERCHID)
        sleep(0.1)

        self.pgWeb.PW_iGetResult(E_PWINFO.PWINFO_AUTHCODE.value, szAux, sizeof(szAux))
        PWINFO_AUTHCODE = szAux.value.decode('utf-8')
        print("PWINFO_AUTHCODE", PWINFO_AUTHCODE)
        sleep(0.1)

        self.pgWeb.PW_iGetResult(E_PWINFO.PWINFO_AUTRESPCODE.value, szAux, sizeof(szAux))
        PWINFO_AUTRESPCODE = szAux.value.decode('utf-8')
        print("PWINFO_AUTRESPCODE", PWINFO_AUTRESPCODE)
        sleep(0.1)

        self.pgWeb.PW_iGetResult(E_PWINFO.PWINFO_AUTDATETIME.value, szAux, sizeof(szAux))
        PWINFO_AUTDATETIME = szAux.value.decode('utf-8')
        print("PWINFO_AUTRESPCODE", PWINFO_AUTDATETIME)
        sleep(0.1)

        self.pgWeb.PW_iGetResult(E_PWINFO.PWINFO_TRNORIGDATE.value, szAux, sizeof(szAux))
        PWINFO_TRNORIGDATE = szAux.value.decode('utf-8')
        print("PWINFO_AUTRESPCODE", PWINFO_TRNORIGDATE)
        sleep(0.1)

        self.pgWeb.PW_iGetResult(E_PWINFO.PWINFO_TRNORIGNSU.value, szAux, sizeof(szAux))
        PWINFO_TRNORIGNSU = szAux.value.decode('utf-8')
        print("PWINFO_AUTRESPCODE", PWINFO_TRNORIGNSU)
        sleep(0.1)

        self.pgWeb.PW_iGetResult(E_PWINFO.PWINFO_TRNORIGAMNT.value, szAux, sizeof(szAux))
        PWINFO_TRNORIGAMNT = szAux.value.decode('utf-8')
        print("PWINFO_AUTRESPCODE", PWINFO_TRNORIGAMNT)
        sleep(0.1)

        """self.pgWeb.PW_iGetResult(E_PWINFO.PWINFO_TRNORIGREQNUM.value, szAux, sizeof(szAux))
        PWINFO_TRNORIGREQNUM = szAux.value.decode('utf-8')
        print("PWINFO_TRNORIGREQNUM", PWINFO_TRNORIGREQNUM)
        sleep(0.1)"""

        self.pgWeb.PW_iGetResult(E_PWINFO.PWINFO_TRNORIGTIME.value, szAux, sizeof(szAux))
        PWINFO_TRNORIGTIME = szAux.value.decode('utf-8')
        print("PWINFO_TRNORIGTIME", PWINFO_TRNORIGTIME)
        sleep(0.1)        

        # CONFIRMA A TRANSACAO SEJA ELA BEM OU MAL SUCEDIDA
        iRet = self.pgWeb.PW_iConfirmation(
            E_PWCNF.PWCNF_CNF_AUTO.value,
            PWINFO_TRNORIGREQNUM,
            PWINFO_AUTLOCREF,
            PWINFO_TRNORIGNSU,
            PWINFO_VIRTMERCH,
            PWINFO_TRNORIGAUTH
        )
        print("PWINFO_TRNORIGREQNUM", PWINFO_TRNORIGREQNUM)
        print("PWINFO_AUTLOCREF", PWINFO_AUTLOCREF)    
        print("PWINFO_AUTEXTREF",PWINFO_TRNORIGNSU)
        print("PWINFO_VIRTMERCH", PWINFO_VIRTMERCH)
        print("PWINFO_TRNORIGAUTH", PWINFO_TRNORIGAUTH)
        print("iRet PW_iConfirmation", iRet)

        return iRet


if __name__ == "__main__":
    CancelTransaction()
