import os
import sys
from Interops import *
from Enums import *
from ctypes import *
from CustomObjects import *


class Venda:
    def __init__(self):
        global COMPROVANTE
        COMPROVANTE = ''

        self.szDspMsg = create_string_buffer(100000)

        self.pgWeb = PGWebLibrary()
        # INICIALIZA A BIBLIOTECA
        self.pgWeb.PW_iInit()

        # MANDADATORY PARAMS
        self.PWINFO_AUTNAME = "COOLBAGSAFE-RENTLOCKER"  # 21
        self.PWINFO_AUTVER = "1.0"  # 22
        self.PWINFO_AUTDEV = "COOLBAG-SAFE GUARDA BAGAGENS AUTOMATIZADO LTDA"  # 23
        # self.PWINFO_AUTCAP = "15" #36
        #self.PWINFO_AUTHSYST = "CIELO"

        # PARAMS DEFAULT PARAMS
        self.PWINFO_CURRENCY = "986"
        self.PWINFO_CURREXP = "2"
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
        self.pgWeb.PW_iPPDisplay("APROXIME,INSIRA OU\n PASSE O CARTAO")
        retEventLoop = self.pgWeb.PW_iPPEventLoop(
            self.szDspMsg, sizeof(self.szDspMsg))

        wait = self.pgWeb.PW_iPPWaitEvent(15)

        while retEventLoop == '' and retEventLoop != 0:

            retEventLoop = self.pgWeb.PW_iPPEventLoop(
                self.szDspMsg, sizeof(self.szDspMsg))
            print("retEventLoop", retEventLoop)
            print("wait", wait)
            return retEventLoop

        ret = ''
        # INICIA UMA NOVA TRANSACAO
        self.pgWeb.PW_iNewTransac(0x21)
        # ADICIONA OS PARAMETROS
        self.pgWeb.PW_iAddParam(0x15, "COOLBAGSAFE-RENTLOCKER")
        self.pgWeb.PW_iAddParam(0x16, "1.0")
        self.pgWeb.PW_iAddParam(
            0x17, "COOLBAG-SAFE GUARDA BAGAGENS AUTOMATIZADO")
        self.pgWeb.PW_iAddParam(0x24, "28")
        self.pgWeb.PW_iAddParam(0x26, "986")
        self.pgWeb.PW_iAddParam(0x27, "2")
        self.pgWeb.PW_iAddParam(0x35, "BIN")
        # self.pgWeb.PW_iAddParam(0x29,"1")
        #self.pgWeb.PW_iAddParam(0x3B, "1")
        self.pgWeb.PW_iAddParam(0x25, "1200")
        self.pgWeb.PW_iAddParam(192, "102")
        self.pgWeb.PW_iAddParam(0x1F21, "1")
        self.pgWeb.PW_iAddParam(0x4D, "00")
        self.pgWeb.PW_iAddParam(0x4E, "00")

        ret = self.pgWeb.PW_iExecTransac(vstParam, iNumParam)

        while ret == E_PWRET.PWRET_MOREDATA.value or ret != E_PWRET.PWRET_OK.value or ret == E_PWRET.PWRET_NOTHING.value:
            ret = self.pgWeb.PW_iExecGetData(vstParam, iNumParam)
            print("ret exectransac venda", ret)
            if ret == E_PWRET.PWRET_CANCEL.value:
                print("E_PWRET.PWRET_CANCEL")
                ret = self.pgWeb.PW_iPPAbort()
                retEventLoop = self.pgWeb.PW_iPPEventLoop(
                    self.szDspMsg, sizeof(self.szDspMsg))
                print("retEventLoop", retEventLoop)
                return retEventLoop
            elif ret == E_PWRET.PWRET_HOSTTIMEOUT.value:
                ret = self.pgWeb.PW_iPPAbort()
                retEventLoop = self.pgWeb.PW_iPPEventLoop(
                    self.szDspMsg, sizeof(self.szDspMsg))
                print("retEventLoop", retEventLoop)
                return retEventLoop
            elif ret == E_PWRET.PWRET_REQPARAM.value:
                print("PWRET_REQPARAM", E_PWRET.PWRET_REQPARAM.value)
                ret = self.pgWeb.PW_iPPAbort()
                retEventLoop = self.pgWeb.PW_iPPEventLoop(
                    self.szDspMsg, sizeof(self.szDspMsg))
                print("retEventLoop", retEventLoop)
                return retEventLoop
            elif ret == E_PWRET.PWRET_FROMHOSTPENDTRN.value:
                # PWINFO_PNDAUTHSYST 7F05h até 20 Nome do provedor para o qual existe uma transação
                # pendente.
                # PWINFO_PNDVIRTMERCH 7F06h até 9 Identificador do Estabelecimento para o qual existe uma
                # transação pendente.
                # PWINFO_PNDREQNUM 7F07h até 10 Referência local da transação que está pendente.
                # PWINFO_PNDAUTLOCREF 7F08h até 50 Referência para a infraestrutura Pay&Go Web da transação
                # que está pendente.
                # PWINFO_PNDAUTEXTREF 7F09h até 50 Referência para o Provedor da transação que está pendente.
                ret = 99

                pszReqNum = ''
                pszLocRef = ''
                pszExtRef = ''
                pszVirtMerch = ''
                pszAuthSyst = ''

                for item in transactionResponse:
                    if(item.parameterCode == E_PWINFO.PWINFO_PNDREQNUM.value):
                        pszReqNum = item.parameterValue

                    elif(item.parameterCode == E_PWINFO.PWINFO_PNDAUTLOCREF.value):
                        pszLocRef = item.parameterValue

                    elif(item.parameterCode == E_PWINFO.PWINFO_PNDAUTEXTREF.value):
                        pszExtRef = item.parameterValue

                    elif(item.parameterCode == E_PWINFO.PWINFO_PNDVIRTMERCH.value):
                        pszVirtMerch = item.parameterValue

                    elif(item.parameterCode == E_PWINFO.PWINFO_PNDAUTHSYST.value):
                        pszAuthSyst = item.parameterValue

                # fim do for

                ret = myPGWebLib.PW_iConfirmation(
                    transactionStatus, pszReqNum, pszLocRef, pszLocRef, pszVirtMerch, pszAuthSyst)
                return ret

            elif ret == E_PWRET.PWRET_OK.value:
                ret = self.pgWeb.PW_iExecTransac(vstParam, iNumParam)

                if ret == E_PWRET.PWRET_OK.value:
                    PWINFO_REQNUM = PWINFO_AUTLOCREF = PWINFO_AUTEXTREF = PWINFO_VIRTMERCH = PWINFO_AUTHSYST = ''
                    COMPROVANTE = self.pgWeb.PW_iGetResult()

                    for i in range(iNumParam):

                        if vstParam[i].wIdentificador == E_PWINFO.PWINFO_REQNUM.value:
                            PWINFO_REQNUM = self.pgWeb.PW_iGetResult(
                                vstParam[i].wIdentificador, szAux, sizeof(szAux))
                            print("PWINFO_REQNUM", PWINFO_REQNUM)
                        elif vstParam[i].wIdentificador == E_PWINFO.PWINFO_AUTLOCREF.value:
                            PWINFO_AUTLOCREF = self.pgWeb.PW_iGetResult(
                                vstParam[i].wIdentificador, szAux, sizeof(szAux))
                            print("PWINFO_AUTLOCREF", PWINFO_AUTLOCREF)
                        elif vstParam[i].wIdentificador == E_PWINFO.PWINFO_AUTEXTREF.value:
                            PWINFO_AUTEXTREF = self.pgWeb.PW_iGetResult(
                                vstParam[i].wIdentificador, szAux, sizeof(szAux))
                            print("PWINFO_AUTEXTREF", PWINFO_AUTEXTREF)
                        elif vstParam[i].wIdentificador == E_PWINFO.PWINFO_VIRTMERCH.value:
                            PWINFO_VIRTMERCH = self.pgWeb.PW_iGetResult(
                                vstParam[i].wIdentificador, szAux, sizeof(szAux))
                            print("PWINFO_VIRTMERCH", PWINFO_VIRTMERCH)
                        elif vstParam[i].wIdentificador == E_PWINFO.PWINFO_AUTHSYST.value:
                            PWINFO_AUTHSYST = self.pgWeb.PW_iGetResult(
                                vstParam[i].wIdentificador, szAux, sizeof(szAux))
                            print("PWINFO_AUTHSYST", PWINFO_AUTHSYST)
                        elif vstParam[i].wIdentificador == E_PWINFO.PWINFO_RCPTMERCH.value:
                            COMPROVANTE = self.pgWeb.PW_iGetResult(
                                vstParam[i].wIdentificador, szAux, sizeof(szAux))
                            f = open('/comprovantes/COMPROVANTE Nº %s:%s-%s-%s %s:%s:%s.txt'%(PWINFO_REQNUM, data.day, data.month, data.year, data.hour, data.minute, data.second),'w')
                            f.write(COMPROVANTE)
                            f.close()
                    iRet = self.pgWeb.PW_iConfirmation(
                        E_PWCNF.PWCNF_CNF_AUTO.value,
                        PWINFO_REQNUM,
                        PWINFO_AUTLOCREF,
                        PWINFO_AUTEXTREF,
                        PWINFO_VIRTMERCH,
                        PWINFO_AUTHSYST
                    )
                    print("iRet PW_iConfirmation", iRet)
                    
                    return iRet
                    


if __name__ == "__main__":
    Venda()
