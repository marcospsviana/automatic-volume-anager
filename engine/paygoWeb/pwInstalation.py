from ctypes import *
from Interops import *
from Enums import *
from CustomObjects import *

class PW_GetData(Structure):
   _fields_=[   
               ("wIdentificador",c_ushort),
               ("bTipoDeDado",c_ubyte),
               ("szPrompt",c_char * 84),
               ("bNumOpcoesMenu",c_ubyte),     
               ("vszTextoMenu",(c_char * 41) * PWMENU_MAXINTENS),
               ("vszValorMenu",(c_char * 256) * PWMENU_MAXINTENS),
               ("szMascaraDeCaptura",c_char * 41),
               ("bTiposEntradaPermitidos",c_ubyte),
               ("bTamanhoMinimo",c_ubyte),
               ("bTamanhoMaximo",c_ubyte),
               ("ulValorMinimo",c_ulong),
               ("ulValorMaximo",c_ulong),
               ("bOcultarDadosDigitados",c_ubyte),
               ("bValidacaoDado",c_ubyte),
               ("bAceitaNulo",c_ubyte),
               ("szValorInicial",c_char * 41),
               ("bTeclasDeAtalho",c_ubyte),
               ("szMsgValidacao",c_char   * 84),
               ("szMsgConfirmacao",c_char * 84),
               ("szMsgDadoMaior",c_char   * 84),    
               ("szMsgDadoMenor",c_char   * 84),
               ("bCapturarDataVencCartao",c_ubyte),
               ("ulTipoEntradaCartao",c_ulong),
               ("bItemInicial",c_ubyte),
               ("bNumeroCapturas",c_ubyte),
               ("szMsgPrevia",c_char * 84),
               ("bTipoEntradaCodigoBarras",c_ubyte),
               ("bOmiteMsgAlerta",c_ubyte),
               ("bIniciaPelaEsquerda",c_ubyte),
               ("bNotificarCancelamento",c_ubyte),
               ("bAlinhaPelaDireita",c_ubyte)
            ]

class PgwInstall():
    def __init__(self):
        self.pgWeb = PGWebLibrary()
        self.pgWeb.PW_iInit()
        self.PWINFO_DESTTCPIP = "app.tpgw.ntk.com.br:17502"
        self.PWINFO_POSID     = "62547"
        self.PWINFO_AUTDEV    = "COOLBAG-SAFE GUARDA BAGAGENS AUTOMATIZADO LTDA"
        self.PWINFO_AUTVER = "1.0"
        self.PWINFO_MERCHCNPJCPF = "35223093000106"
        self.PWINFO_AUTHTECHUSER = "314159"
        self.PWINFO_USINGPINPAD =  "1"
        self.PWINFO_AUTNAME = "COOLBAGSAFE-RENTLOCKER"
        self.PWINFO_AUTCAP = "28"
        self.PWINFO_PPCOMMPORT = "0"
        self.install()
    

   
    def install(self):
        
        ret = ''
        vstParam_11 = PW_GetData
        vstParam = vstParam_11()
        iNumParam = 10
        
        self.pgWeb.PW_iNewTransac(0x01)
        self.pgWeb.PW_iAddParam(0x11, self.PWINFO_POSID)
        self.pgWeb.PW_iAddParam(0x15, self.PWINFO_AUTNAME)
        self.pgWeb.PW_iAddParam(0x16, self.PWINFO_AUTVER)
        self.pgWeb.PW_iAddParam(0x17, self.PWINFO_AUTDEV)
        self.pgWeb.PW_iAddParam(0x1B, self.PWINFO_DESTTCPIP)
        self.pgWeb.PW_iAddParam(0x1C, self.PWINFO_MERCHCNPJCPF)
        self.pgWeb.PW_iAddParam(0xF6, self.PWINFO_AUTHTECHUSER)
        self.pgWeb.PW_iAddParam(0x7F01, self.PWINFO_USINGPINPAD)
        self.pgWeb.PW_iAddParam(0x24, self.PWINFO_AUTCAP)
        self.pgWeb.PW_iAddParam(0x7F02, self.PWINFO_PPCOMMPORT)

        
        

        ret = self.pgWeb.PW_iExecTransac(vstParam, iNumParam)

        
        retEventLoop = ''
        szDspMsg = create_string_buffer(100000)
        retEventLoop = self.pgWeb.PW_iPPEventLoop(szDspMsg, 1000)
        print("retEventLoop szDspMsg", retEventLoop, szDspMsg)
        return retEventLoop

        

if __name__ == '__main__':
    PgwInstall()





