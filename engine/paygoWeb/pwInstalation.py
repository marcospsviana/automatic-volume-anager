from ctypes import *
from Interops import *

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
        self.PWINFO_DESTTCPIP = "app.tpgw.ntk.com.br:17502"
        self.PWINFO_POSID     = "62547"
        self.PWINFO_AUTDEV    = "COOLBAG-SAFE GUARDA BAGAGENS AUTOMATIZADO"
        self.PWINFO_AUTVER = "1.0"
        self.PWINFO_MERCHCNPJCPF = "35223093000106"
        self.PWINFO_AUTHTECHUSER = "314159"
        self.PWINFO_USINGPINPAD =  "1"
        self.PWINFO_AUTNAME = "COOLBAGSAFE-RENTLOCKER"
        self.PWINFO_AUTCAP = "15"
        self.install()
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

    def PW_iExecTransac(self,vstParam, iNumParam):
        self.PW_iExecTransacObj          = self.PGWebLib_dll.PW_iExecTransac
        self.PW_iExecTransacObj.restype  = c_short


        self.PW_iExecTransacObj.argtypes = [POINTER((PW_GetData *9)),POINTER(c_int)]



        ret = self.PW_iExecTransacObj(byref(vstParam),byref(c_int(iNumParam)))

        print(ret)


        return ret

    def install(self):
        ret = ''
        vstParam_install = (PW_GetData * 9)
        vstParam = vstParam_install()
        iNumParam = 1
        self.PW_iInit()
        self.PGWebLib_dll.PW_iNewTransac(0x01)
        self.PGWebLib_dll.PW_iAddParam(0x11, self.PWINFO_POSID)
        self.PGWebLib_dll.PW_iAddParam(0x15, self.PWINFO_AUTNAME)
        self.PGWebLib_dll.PW_iAddParam(0x16, self.PWINFO_AUTVER)
        self.PGWebLib_dll.PW_iAddParam(0x17, self.PWINFO_AUTDEV)
        self.PGWebLib_dll.PW_iAddParam(0x1B, self.PWINFO_DESTTCPIP)
        self.PGWebLib_dll.PW_iAddParam(0x1C, self.PWINFO_MERCHCNPJCPF)
        self.PGWebLib_dll.PW_iAddParam(0xF6, self.PWINFO_AUTHTECHUSER)
        self.PGWebLib_dll.PW_iAddParam(0x7F01, self.PWINFO_USINGPINPAD)
        self.PGWebLib_dll.PW_iAddParam(0x24, self.PWINFO_AUTCAP)
        self.PGWebLib_dll.PW_iAddParam(0x7F02, "0")

        
        

        ret = self.PW_iExecTransac(vstParam, iNumParam)

        return ret
        retEventLoop = ''
        szDspMsg = create_string_buffer(100000)
        retEventLoop = self.PW_iPPEventLoop(szDspMsg, 1000)
        print("retEventLoop szDspMsg", retEventLoop, szDspMsg)

        

if __name__ == '__main__':
    PgwInstall()





