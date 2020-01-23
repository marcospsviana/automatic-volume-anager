import os , sys
import json
from Interops import *
from Enums import *
import datetime
from ctypes import *
from CustomObjects import *

class Venda:
    def __init__(self):
        
        self.szDspMsg = create_string_buffer(100000)
        
        self.pgWeb = PGWebLibrary()
        # INICIALIZA A BIBLIOTECA 
        self.pgWeb.PW_iInit()     
        # EXECUTA A FUNÇÃO VENDA
        self.venda()
    



    def venda(self):
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
        with open('comprovantes/valor_venda.json', 'r') as f:
            dados = json.load(f)
        self.total = dados['TOTAL']
        print("type(total)", type(self.total))
        print(self.total)
        if dados['LANGUAGE'] == 'pt_BR':
            language = "0"
        else:
            language = "1"
        tipo_cartao = dados['PWINFO_CARDTYPE']
        if tipo_cartao == "CREDITO":
            self.tipo_cartao = "1"
        elif tipo_cartao == "DEBITO":
            self.tipo_cartao = "2"
        print("tipo_cartao", tipo_cartao)
        # INICIA UMA NOVA TRANSACAO
        self.pgWeb.PW_iNewTransac(E_PWOPER.PWOPER_SALE.value)
        #MANDADATORY PARAMS
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_AUTNAME.value, "COOLBAGSAFE-RENTLOCKER")
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_AUTVER.value, "1.0")
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_AUTDEV.value, "COOLBAG-SAFE GUARDA BAGAGENS AUTOMATIZADO")
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_AUTCAP.value, "28")
        #self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_LANGUAGE.value, language)
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_CURRENCY.value, "986") # MOEDA: REAL
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_CURREXP.value, "2") 
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_AUTHSYST.value, "CIELO") #ADQUIRENTE
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_CARDTYPE.value,self.tipo_cartao) # 1 - CREDITO 2 - DEBITO
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_FINTYPE.value, "1") # 1 A VISTA
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_TOTAMNT.value, self.total)
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_PAYMNTTYPE.value, "1") # 1 SOMENTE CARTAO
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_BOARDINGTAX.value, "00")
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_TIPAMOUNT.value, "00")
        
        
        
        
        ret = self.pgWeb.PW_iExecTransac(vstParam, iNumParam)
        
        while ret == -2497 or ret == E_PWRET.PWRET_NOTHING.value:
            #ret = self.pgWeb.PW_iExecTransac(vstParam, iNumParam)
            ret = self.pgWeb.PW_iExecGetData(vstParam, iNumParam)
            print("ret exectransac venda", ret)
            
            
            if ret == E_PWRET.PWRET_CANCEL.value:
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
                print("PWRET_FROMHOSTPENDTRN", E_PWRET.PWRET_FROMHOSTPENDTRN.value)
                self.confirmPendTransaction(transactionStatus=1, transactionResponse=ret)
                retEventLoop = self.pgWeb.PW_iPPEventLoop(
                    self.szDspMsg, sizeof(self.szDspMsg))
                print("retEventLoop", retEventLoop)
                return retEventLoop
            ret = self.pgWeb.PW_iExecTransac(vstParam, iNumParam)
            print("efetuando a transacao...")
            print("ret ---->", ret)
        

        
        PWINFO_REQNUM = PWINFO_AUTLOCREF = PWINFO_AUTEXTREF = PWINFO_VIRTMERCH = PWINFO_AUTHSYST = ''
        data = datetime.datetime.now()
        self.pgWeb.PW_iGetResult(
                    E_PWINFO.PWINFO_REQNUM.value, szAux, sizeof(szAux))
        PWINFO_REQNUM = szAux.value.decode('utf-8')
        print("PWINFO_REQNUM", PWINFO_REQNUM)
        sleep(0.3)
        self.pgWeb.PW_iGetResult(
                    E_PWINFO.PWINFO_AUTLOCREF.value, szAux, sizeof(szAux))
        PWINFO_AUTLOCREF = szAux.value.decode('utf-8')
        print("PWINFO_AUTLOCREF", PWINFO_AUTLOCREF)
        sleep(0.3)
        self.pgWeb.PW_iGetResult(
                    E_PWINFO.PWINFO_AUTEXTREF.value, szAux, sizeof(szAux))
        PWINFO_AUTEXTREF = szAux.value.decode('utf-8')
        print("PWINFO_AUTEXTREF", PWINFO_AUTEXTREF)
        if PWINFO_AUTEXTREF == None or PWINFO_AUTEXTREF == '':
            PWINFO_AUTEXTREF = '0'
        sleep(0.3)
        self.pgWeb.PW_iGetResult(
                    E_PWINFO.PWINFO_VIRTMERCH.value, szAux, sizeof(szAux))
        PWINFO_VIRTMERCH = szAux.value.decode('utf-8')
        print("PWINFO_VIRTMERCH", PWINFO_VIRTMERCH)
        sleep(0.3)
        self.pgWeb.PW_iGetResult(
                    E_PWINFO.PWINFO_AUTHSYST.value, szAux, sizeof(szAux))
        PWINFO_AUTHSYST = szAux.value.decode('utf-8')
        print("PWINFO_AUTHSYST", PWINFO_AUTHSYST)
        sleep(0.3)
        iRet = self.pgWeb.PW_iConfirmation(
            E_PWCNF.PWCNF_CNF_AUTO.value,
            PWINFO_REQNUM,
            PWINFO_AUTLOCREF,
            PWINFO_AUTEXTREF,
            PWINFO_VIRTMERCH,
            PWINFO_AUTHSYST
        )
        print("iRet PW_iConfirmation", iRet)

        self.pgWeb.PW_iGetResult(
                    E_PWINFO.PWINFO_RESULTMSG.value, szAux, sizeof(szAux))
        PWINFO_RESULTMSG = szAux.value.decode('utf-8')
        print("PWINFO_AUTHSYST", PWINFO_RESULTMSG)
        texto = ''
        for i in PWINFO_RESULTMSG:
            if i == '\n':
                i = i.replace('\n', ' ')
                texto += i
            elif i == '\r':
                i = i.replace('\r', ' ')
                texto += i
            else:
                texto += i
        PWINFO_RESULTMSG = texto
            
        sleep(0.3)
        

        result_json =  open('comprovantes/RESULT DATA:%s %s %s .json'%(data.day, data.month, data.year),'a+')
        result_json.write('\n{  \n')
        result_json.write('     "PWINFO_REQNUM"    : "%s",\n'%(PWINFO_REQNUM))
        result_json.write('     "PWINFO_AUTLOCREF" : "%s",\n'%(PWINFO_AUTLOCREF))
        result_json.write('     "PWINFO_AUTEXTREF" : "%s",\n'%(PWINFO_AUTEXTREF))
        result_json.write('     "PWINFO_VIRTMERCH" : "%s",\n'%(PWINFO_VIRTMERCH))
        result_json.write('     "PWINFO_AUTHSYST"  : "%s",\n'%(PWINFO_AUTHSYST))
        result_json.write('     "PWINFO_RESULTMSG" : "%s",\n'%(PWINFO_RESULTMSG))
        result_json.write('\n}  \n')
        result_json.close()

        retorno_transacao =  open('comprovantes/retornotransacao.json','w+')
        retorno_transacao.write('\n{  \n')
        retorno_transacao.write('     "PWINFO_RESULTMSG" : "%s"'%(PWINFO_RESULTMSG))
        retorno_transacao.write('\n}  \n')
        retorno_transacao.close()
        

        

        self.pgWeb.PW_iGetResult(
            E_PWINFO.PWINFO_RCPTMERCH.value, szAux, sizeof(szAux))
        print("PWINFO_RCPTMERCH", E_PWINFO.PWINFO_RCPTMERCH.value)
        COMPROVANTE = szAux.value.decode('utf-8')
        print("result transacao nota")
        f = open('comprovantes/COMPROVANTE DATA:%s %s %s .txt'%(data.day, data.month, data.year),'a+')
        f.write("==============================================\n\n")
        f.write(COMPROVANTE)
        f.write("==============================================\n\n")
        f.close()

        sleep(0.3)
        self.pgWeb.PW_iGetResult(
            E_PWINFO.PWINFO_RCPTCHOLDER.value, szAux, sizeof(szAux))
        print("PWINFO_RCPTMERCH", E_PWINFO.PWINFO_RCPTCHOLDER.value)
        COMPROVANTE_CLIENTE = szAux.value.decode('utf-8')
        f = open('comprovantes/COMPROVANTE CLIENTE DATA:%s %s %s .txt'%(data.day, data.month, data.year),'a+')
        f.write("\n\n\==============================================\n\n")
        f.write(COMPROVANTE_CLIENTE)
        f.write("\n\n==============================================\n\n")
        f.close()

        envio_email = open('comprovantes/COMPROVANTE CLIENTE EMAIL.txt','w+')
        envio_email.write(COMPROVANTE_CLIENTE)
        envio_email.close()


        return iRet
    
            
                
        

if __name__ == "__main__":
    Venda()