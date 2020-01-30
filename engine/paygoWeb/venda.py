from Interops import *
from Enums import *
from CustomObjects import *
import os
import sys
import json
import datetime
from ctypes import *



class Venda:
    def __init__(self):

        self.szDspMsg = create_string_buffer(100000)

        self.pgWeb = PGWebLibrary()
        # INICIALIZA A BIBLIOTECA
        self.pgWeb.PW_iInit()
        # EXECUTA A FUNÇÃO VENDA
        self.venda()

    def venda(self):
        """Função responsavel por efetuar a transacao adicionando os parametros obrigatorios com a 
        funcao PW_iAddParam e aguardando o retorno do PIN PAD, caso haja parametros faltantes com 
        retorno PWRET_MOREDATA a aplicacao chama a funcao PW_iExecGetData para percorrer todos os 
        parametros e verificar qual parametro está faltando fazendo  o tratamento do mesmo conforme
        documentacao PayGoWeb"""
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

        # VERIFICA O IDIOMA ESCOLHIDO PELO CLIENTE , APENAS PORTUGUES OU INGLES
        """if dados['LANGUAGE'] == 'pt_BR':
            self.language = "0"
        else:
            self.language = "1"
        tipo_cartao = dados['PWINFO_CARDTYPE']
        if tipo_cartao == "CREDITO":
            self.tipo_cartao = "1"
        elif tipo_cartao == "DEBITO":
            self.tipo_cartao = "2"
        print("tipo_cartao", tipo_cartao)"""

        # INICIA UMA NOVA TRANSACAO
        self.pgWeb.PW_iNewTransac(E_PWOPER.PWOPER_SALE.value)

        # MANDADATORY PARAMS
        self.pgWeb.PW_iAddParam(
            E_PWINFO.PWINFO_AUTNAME.value, "COOLBAGSAFE-RENTLOCKER")
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_AUTVER.value, "1.0")
        self.pgWeb.PW_iAddParam(
            E_PWINFO.PWINFO_AUTDEV.value, "COOLBAG-SAFE GUARDA BAGAGENS AUTOMATIZADO")
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_AUTCAP.value, "28")

        # ADICIONA O PARAMETRO DO IDIOMA ESTABELECIDO NA APLICACAO
        #self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_LANGUAGE.value, self.language)

        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_CURRENCY.value, "986")  # MOEDA: REAL
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_CURREXP.value, "2")
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_AUTHSYST.value, "REDE")  # ADQUIRENTE
        # 1 - CREDITO 2 - DEBITO
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_CARDTYPE.value, "1") #self.tipo_cartao)
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_FINTYPE.value, "1")  # 1 A VISTA
        #self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_INSTALLMENTS.value, "3") # QUANTIDADE DE PARCELAS
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_TOTAMNT.value, "1200")#self.total)
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_PAYMNTTYPE.value, "1")  # 1 SOMENTE CARTAO
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_BOARDINGTAX.value, "00")
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_TIPAMOUNT.value, "00")

        ret = self.pgWeb.PW_iExecTransac(vstParam, iNumParam)
        
        PWINFO_REQNUM = PWINFO_AUTLOCREF = PWINFO_AUTEXTREF = PWINFO_VIRTMERCH = PWINFO_AUTHSYST = ''
        PWINFO_PNDAUTHSYST = PWINFO_PNDVIRTMERCH = PWINFO_PNDREQNUM = PWINFO_PNDAUTLOCREF = PWINFO_PNDAUTEXTREF = ''

        #DATA E HORA ATUAL
        data = datetime.datetime.now()

        # OBTENDO INFORMACOES DA TRANSACAO
        self.pgWeb.PW_iGetResult(
            E_PWINFO.PWINFO_REQNUM.value, szAux, sizeof(szAux))
        PWINFO_REQNUM = szAux.value.decode('utf-8')
        print("PWINFO_REQNUM", PWINFO_REQNUM)
        sleep(0.1)
        self.pgWeb.PW_iGetResult(
            E_PWINFO.PWINFO_AUTLOCREF.value, szAux, sizeof(szAux))
        PWINFO_AUTLOCREF = szAux.value.decode('utf-8')
        print("PWINFO_AUTLOCREF", PWINFO_AUTLOCREF)
        sleep(0.1)
        self.pgWeb.PW_iGetResult(
            E_PWINFO.PWINFO_AUTEXTREF.value, szAux, sizeof(szAux))
        PWINFO_AUTEXTREF = szAux.value.decode('utf-8')
        print("PWINFO_AUTEXTREF", PWINFO_AUTEXTREF)
        if PWINFO_AUTEXTREF == None or PWINFO_AUTEXTREF == '':
            PWINFO_AUTEXTREF = '0'
        sleep(0.1)
        self.pgWeb.PW_iGetResult(
            E_PWINFO.PWINFO_VIRTMERCH.value, szAux, sizeof(szAux))
        PWINFO_VIRTMERCH = szAux.value.decode('utf-8')
        print("PWINFO_VIRTMERCH", PWINFO_VIRTMERCH)
        sleep(0.1)
        self.pgWeb.PW_iGetResult(
            E_PWINFO.PWINFO_AUTHSYST.value, szAux, sizeof(szAux))
        PWINFO_AUTHSYST = szAux.value.decode('utf-8')
        print("PWINFO_AUTHSYST", PWINFO_AUTHSYST)
        sleep(0.1)
        registro_json = open('comprovantes/REGISTRO DATA:%s %s %s .json' %
                             (data.day, data.month, data.year), 'a+')
        registro_json.write('\n{  \n')
        registro_json.write('     "DATA HORARIO"    : "%s:%s",\n' %
                            (data.hour, data.minute))
        registro_json.write(
            '     "PWINFO_REQNUM"    : "%s",\n' % (PWINFO_REQNUM))
        registro_json.write(
            '     "PWINFO_AUTLOCREF" : "%s",\n' % (PWINFO_AUTLOCREF))
        registro_json.write(
            '     "PWINFO_AUTEXTREF" : "%s",\n' % (PWINFO_AUTEXTREF))
        registro_json.write(
            '     "PWINFO_VIRTMERCH" : "%s",\n' % (PWINFO_VIRTMERCH))
        registro_json.write(
            '     "PWINFO_AUTHSYST"  : "%s",\n' % (PWINFO_AUTHSYST))
        registro_json.write('\n}  \n')
        registro_json.close()

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

            while ret == -2497 or ret == E_PWRET.PWRET_NOTHING.value or (2100 <= ret <= 2200):
                
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
                #SE HÁ TRANSACAO PENDENTE  CONFIRMAR A TRANSACAO 
                if ret == E_PWRET.PWRET_FROMHOSTPENDTRN.value:
                    (print("esta em pendencia"))
                    self.pgWeb.PW_iGetResult(
                        E_PWINFO.PWINFO_PNDAUTHSYST.value, szAux, sizeof(szAux)
                    )
                    PWINFO_PNDAUTHSYST = szAux.value.decode('utf-8')
                    print("PWINFO_PNDAUTHSYST = ", PWINFO_PNDAUTHSYST)
                    sleep(0.1)

                    self.pgWeb.PW_iGetResult(
                        E_PWINFO.PWINFO_PNDVIRTMERCH.value, szAux, sizeof(szAux)
                    )
                    PWINFO_PNDVIRTMERCH = szAux.value.decode('utf-8')
                    print("PWINFO_PNDVIRTMERCH = ", PWINFO_PNDVIRTMERCH )
                    sleep(0.1)

                    self.pgWeb.PW_iGetResult(
                        E_PWINFO.PWINFO_PNDREQNUM.value, szAux, sizeof(szAux)
                    )
                    PWINFO_PNDREQNUM = szAux.value.decode('utf-8')
                    print("PWINFO_PNDREQNUM = ", PWINFO_PNDREQNUM )
                    sleep(0.1)

                    self.pgWeb.PW_iGetResult(
                        E_PWINFO.PWINFO_PNDAUTLOCREF.value, szAux, sizeof(szAux)
                    )
                    PWINFO_PNDAUTLOCREF = szAux.value.decode('utf-8')
                    print("PWINFO_PNDAUTLOCREF = ", PWINFO_PNDAUTLOCREF )
                    sleep(0.1)

                    self.pgWeb.PW_iGetResult(
                        E_PWINFO.PWINFO_PNDAUTEXTREF.value, szAux, sizeof(szAux)
                    )
                    PWINFO_PNDAUTEXTREF = szAux.value.decode('utf-8')
                    print("PWINFO_PNDAUTEXTREF = ", PWINFO_PNDAUTEXTREF )
                    sleep(0.1)

                    iPndRet = self.pgWeb.PW_iConfirmation(
                        E_PWCNF.PWCNF_CNF_AUTO.value,
                        PWINFO_PNDREQNUM,
                        PWINFO_PNDAUTLOCREF,
                        PWINFO_PNDAUTEXTREF,
                        PWINFO_PNDVIRTMERCH,
                        PWINFO_PNDAUTHSYST
                    )
                    print("iRet PENDENTE PW_iConfirmation", iPndRet)

                    return iPndRet

        
        elif ret <= E_PWRET.PWRET_FROMHOSTPOSAUTHERR.value and ret >= E_PWRET.PWRET_INVALIDTRN.value and ret != E_PWRET.PWRET_MOREDATA.value:
            self.pgWeb.PW_iGetResult(
                E_PWINFO.PWINFO_RESULTMSG.value, szAux, sizeof(szAux))
            PWINFO_RESULTMSG = szAux.value.decode('utf-8')
            self.PW_iPPAbort()
            retEventLoop = self.pgWeb.PW_iPPEventLoop(
                        self.szDspMsg, sizeof(self.szDspMsg))
            print("retEventLoop", retEventLoop)
            return retEventLoop
        
        

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

        sleep(0.1)

        # GUARDA AS INFORMACOES NAO SENSIVEIS DA TRANSACAO EM JSON PARA CONSULTA FUTURA
        result_json = open('comprovantes/RESULT DATA:%s %s %s .json' %(data.day, data.month, data.year), 'a+')
        result_json.write('\n{  \n')
        result_json.write('     "PWINFO_REQNUM"    : "%s",\n' %(PWINFO_REQNUM))
        result_json.write('     "PWINFO_AUTLOCREF" : "%s",\n' %(PWINFO_AUTLOCREF))
        result_json.write('     "PWINFO_AUTEXTREF" : "%s",\n' %(PWINFO_AUTEXTREF))
        result_json.write('     "PWINFO_VIRTMERCH" : "%s",\n' %(PWINFO_VIRTMERCH))
        result_json.write('     "PWINFO_AUTHSYST"  : "%s",\n' %(PWINFO_AUTHSYST))
        result_json.write('     "PWINFO_RESULTMSG" : "%s",\n' %(PWINFO_RESULTMSG))
        result_json.write('\n}  \n')
        result_json.close()

        # GRAVA EM JSON O RETORNO DA TRANSACAO SEJA ELA BEM OU MAL SUCEDIDA
        retorno_transacao = open('comprovantes/retornotransacao.json', 'w+')
        retorno_transacao.write('\n{  \n')
        retorno_transacao.write('  "DATA" : "%s %s %s %s %s",\n' % (data.day, data.month, data.year, data.hour, data.minute))
        retorno_transacao.write('  "PWINFO_RESULTMSG" : "%s"' % (PWINFO_RESULTMSG))
        retorno_transacao.write('\n}  \n')
        retorno_transacao.close()

        self.pgWeb.PW_iGetResult(
            E_PWINFO.PWINFO_RCPTMERCH.value, szAux, sizeof(szAux))
        print("PWINFO_RCPTMERCH", E_PWINFO.PWINFO_RCPTMERCH.value)
        COMPROVANTE = szAux.value.decode('utf-8')
        print("result transacao nota")
        f = open('comprovantes/COMPROVANTE DATA:%s %s %s .txt' %(data.day, data.month, data.year), 'a+')
        f.write("==============================================\n\n")
        f.write(COMPROVANTE)
        f.write("==============================================\n\n")
        f.close()

        sleep(0.1)
        self.pgWeb.PW_iGetResult(
            E_PWINFO.PWINFO_RCPTCHOLDER.value, szAux, sizeof(szAux))
        print("PWINFO_RCPTMERCH", E_PWINFO.PWINFO_RCPTCHOLDER.value)
        COMPROVANTE_CLIENTE = szAux.value.decode('utf-8')
        f = open('comprovantes/COMPROVANTE CLIENTE DATA:%s %s %s .txt' %
                 (data.day, data.month, data.year), 'a+')
        f.write("\n\n\==============================================\n\n")
        f.write(COMPROVANTE_CLIENTE)
        f.write("\n\n==============================================\n\n")
        f.close()

        envio_email = open('comprovantes/COMPROVANTE CLIENTE EMAIL.txt', 'w+')
        envio_email.write(COMPROVANTE_CLIENTE)
        envio_email.close()

        # CONFIRMA A TRANSACAO SEJA ELA BEM OU MAL SUCEDIDA
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

        

        # zera todos os parametros
        iRet = vstParam_11 = vstParam = iNumParam = ulEvent = szDspMsg = szAux = wait = retEventLoop = ret = ''
        PWINFO_REQNUM = PWINFO_AUTLOCREF = PWINFO_AUTEXTREF = PWINFO_VIRTMERCH = PWINFO_AUTHSYST


if __name__ == "__main__":
    Venda()
