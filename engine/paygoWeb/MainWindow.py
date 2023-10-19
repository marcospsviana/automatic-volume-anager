import os

# import ctypes.
from ctypes import *
from time import *

from CustomObjects import *
from Enums import *
from Interops import *
from PGWlib import *

#######################################################################
# execução da inicialização e instalação

# inicializa DLL
ret = myPGWebLib.PW_iInit()
print('ret PW_iInit() =')


print(ret)

# faz instalação
# dados de entrada e saida na aba TERMINAL do Ambiente

TesteInstalacaoJan()
# ret = TesteIsNull()
# TesteManutencao()
# TesteVersion()
# PrintResultParams()
getTransactionResult()
