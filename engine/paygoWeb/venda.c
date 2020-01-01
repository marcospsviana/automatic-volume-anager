#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdarg.h>
#include <dlfcn.h>
#include <termios.h>
#include <fcntl.h>
#include <stdio_ext.h>
#include "PGWebLib.h"

// Definição da versão do aplicativo
#define  COOLBAGSAFE_RENTLOCKER_VERSION "1.0"
//MANDADATORY PARAMS
// 21
#define        PWINFO_AUTNAME "COOLBAGSAFE-RENTLOCKER" 
// 22
#define        PWINFO_AUTVER  "1.0" 
// 23
#define        PWINFO_AUTDEV  "COOLBAG-SAFE GUARDA BAGAGENS AUTOMATIZADO LTDA" 
//36
#define        PWINFO_AUTCAP "4" 
#define        PWINFO_AUTHSYST "REDE"
//PARAMS DEFAULT PARAMS
#define        PWINFO_CURRENCY  "986"
#define        PWINFO_CURREXP "2" 
// DEBITO E CREDITO
#define        PWINFO_CARDTYPE "3" 

// Estrutura para importação das funções da DLL "PGWebLib.dll"
typedef struct {
    Int16 (PW_EXPORT *pPW_iInit)              (const char* pszWorkingDir);
    Int16 (PW_EXPORT *pPW_iNewTransac)        (Int16 iOper);
    Int16 (PW_EXPORT *pPW_iAddParam)          (Int16 iParam, const char *szValue);
    Int16 (PW_EXPORT *pPW_iExecTransac)       (PW_GetData vstParam[], Int16 *piNumParam);
    Int16 (PW_EXPORT *pPW_iGetResult)         (Int16 iInfo, char *pszData, Uint32 ulDataSize);
    Int16 (PW_EXPORT *pPW_iConfirmation)      (Uint32 ulResult, const char* pszReqNum, const char* pszLocRef, const char* pszExtRef,
                                               const char* pszVirtMerch, const char* pszAuthSyst);
    Int16 (PW_EXPORT *pPW_iIdleProc)          (void);
    Int16 (PW_EXPORT *pPW_iPPAbort)           (void);
    Int16 (PW_EXPORT *pPW_iPPEventLoop)       (char *pszDisplay, Uint32 ulDisplaySize);
    Int16 (PW_EXPORT *pPW_iPPGetCard)         (Uint16 uiIndex);
    Int16 (PW_EXPORT *pPW_iPPGetPIN)          (Uint16 uiIndex);
    Int16 (PW_EXPORT *pPW_iPPGetData)         (Uint16 uiIndex);
    Int16 (PW_EXPORT *pPW_iPPGoOnChip)        (Uint16 uiIndex);
    Int16 (PW_EXPORT *pPW_iPPFinishChip)      (Uint16 uiIndex);
    Int16 (PW_EXPORT *pPW_iPPConfirmData)     (Uint16 uiIndex);
    Int16 (PW_EXPORT *pPW_iPPRemoveCard)      (void);
    Int16 (PW_EXPORT *pPW_iPPDisplay)         (const char* pszMsg);
    Int16 (PW_EXPORT *pPW_iPPWaitEvent)       (Uint32 *pulEvent);
    Int16 (PW_EXPORT *pPW_iPPGenericCMD)      (Uint16 uiIndex);
} HwFuncs;

// Estrutura para armazenamento de dados para confirmação de transação
typedef struct {
   char szReqNum[11];
   char szHostRef[51];
   char szLocRef[51];
   char szVirtMerch[19];
   char szAuthSyst[21];
} ConfirmData;

// Variáveis globais
static void*         ghHwLib;
static HwFuncs       gstHwFuncs;
static ConfirmData   gstConfirmData;
static Bool          gfAutoAtendimento;

/******************************************/
/* FUNÇÕES LOCAIS AUXILIARES              */
/******************************************/
int kbhit(void)
{
  struct termios oldt, newt;
  int ch;
  int oldf;
 
  tcgetattr(STDIN_FILENO, &oldt);
  newt = oldt;
  newt.c_lflag &= ~(ICANON | ECHO);
  tcsetattr(STDIN_FILENO, TCSANOW, &newt);
  oldf = fcntl(STDIN_FILENO, F_GETFL, 0);
  fcntl(STDIN_FILENO, F_SETFL, oldf | O_NONBLOCK);
 
  ch = getchar();
 
  tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
  fcntl(STDIN_FILENO, F_SETFL, oldf);
 
  if(ch != EOF)
  {
    ungetc(ch, stdin);
    return 1;
  }
 
  return 0;
}

/*=====================================================================================*\
 Funcao     :  InputCR

 Descricao  :  Esta função é utilizada para substituir o caractere utilizado pelo 
               Pay&Go Web para a quebra de linha ('\r') para o padrão utilizado 
               pelos aplicativos console Linux ("\r\n").
 
 Entradas   :  pszSourceStr   :  String a ser alterada.

 Saidas     :  pszSourceStr   :  String com o caractere de quebra de linha substituído.
 
 Retorno    :  nao ha.
\*=====================================================================================*/
static void InputCR(char* pszSourceStr)
{
   int i, j, iSourceLen;
   char cAux, cTemp;

   iSourceLen = strlen(pszSourceStr);

   for( i = 0; i < iSourceLen; i++)
   {
      if( pszSourceStr[i] == '\r' && pszSourceStr[i+1] != '\n')
      {
         cAux = pszSourceStr[i+1];
         pszSourceStr[i+1] = '\n';
         for( j = i+1; j <= iSourceLen; j++)
         {
            cTemp = pszSourceStr[j+1];
            pszSourceStr[j+1] = cAux;
            cAux = cTemp;
         }
         iSourceLen++;
      }
   }
}

/*=====================================================================================*\
 Funcao     :  pszGetInfoDescription

 Descricao  :  Esta função recebe um código PWINFO_XXX e retorna uma string com a 
               descrição da informação representada por aquele código.
 
 Entradas   :  wIdentificador :  Código da informação (PWINFO_XXX).

 Saidas     :  nao ha.
 
 Retorno    :  String representando o código recebido como parâmetro.
\*=====================================================================================*/
static const char* pszGetInfoDescription(Int16 wIdentificador)
{
   switch(wIdentificador)
   {
      case(PWINFO_OPERATION        ): return "PWINFO_OPERATION";
      case(PWINFO_POSID            ): return "PWINFO_POSID";
      case(PWINFO_AUTNAME          ): return "PWINFO_AUTNAME";
      case(PWINFO_AUTVER           ): return "PWINFO_AUTVER";
      case(PWINFO_AUTDEV           ): return "PWINFO_AUTDEV";
      case(PWINFO_DESTTCPIP        ): return "PWINFO_DESTTCPIP";
      case(PWINFO_MERCHCNPJCPF     ): return "PWINFO_MERCHCNPJCPF";
      case(PWINFO_AUTCAP           ): return "PWINFO_AUTCAP";
      case(PWINFO_TOTAMNT          ): return "PWINFO_TOTAMNT";
      case(PWINFO_CURRENCY         ): return "PWINFO_CURRENCY";
      case(PWINFO_CURREXP          ): return "PWINFO_CURREXP";
      case(PWINFO_FISCALREF        ): return "PWINFO_FISCALREF";
      case(PWINFO_CARDTYPE         ): return "PWINFO_CARDTYPE";
      case(PWINFO_PRODUCTNAME      ): return "PWINFO_PRODUCTNAME";
      case(PWINFO_DATETIME         ): return "PWINFO_DATETIME";
      case(PWINFO_REQNUM           ): return "PWINFO_REQNUM";
      case(PWINFO_AUTHSYST         ): return "PWINFO_AUTHSYST";
      case(PWINFO_VIRTMERCH        ): return "PWINFO_VIRTMERCH";
      case(PWINFO_AUTMERCHID       ): return "PWINFO_AUTMERCHID";
      case(PWINFO_PHONEFULLNO      ): return "PWINFO_PHONEFULLNO";
      case(PWINFO_FINTYPE          ): return "PWINFO_FINTYPE";
      case(PWINFO_INSTALLMENTS     ): return "PWINFO_INSTALLMENTS";
      case(PWINFO_INSTALLMDATE     ): return "PWINFO_INSTALLMDATE";
      case(PWINFO_PRODUCTID        ): return "PWINFO_PRODUCTID";
      case(PWINFO_RESULTMSG        ): return "PWINFO_RESULTMSG";
      case(PWINFO_CNFREQ           ): return "PWINFO_CNFREQ";
      case(PWINFO_AUTLOCREF        ): return "PWINFO_AUTLOCREF";
      case(PWINFO_AUTEXTREF        ): return "PWINFO_AUTEXTREF";
      case(PWINFO_AUTHCODE         ): return "PWINFO_AUTHCODE";
      case(PWINFO_AUTRESPCODE      ): return "PWINFO_AUTRESPCODE";
      case(PWINFO_DISCOUNTAMT      ): return "PWINFO_DISCOUNTAMT";
      case(PWINFO_CASHBACKAMT      ): return "PWINFO_CASHBACKAMT";
      case(PWINFO_CARDNAME         ): return "PWINFO_CARDNAME";
      case(PWINFO_ONOFF            ): return "PWINFO_ONOFF";
      case(PWINFO_BOARDINGTAX      ): return "PWINFO_BOARDINGTAX";
      case(PWINFO_TIPAMOUNT        ): return "PWINFO_TIPAMOUNT";
      case(PWINFO_INSTALLM1AMT     ): return "PWINFO_INSTALLM1AMT";
      case(PWINFO_INSTALLMAMNT     ): return "PWINFO_INSTALLMAMNT";
      case(PWINFO_RCPTFULL         ): return "PWINFO_RCPTFULL";
      case(PWINFO_RCPTMERCH        ): return "PWINFO_RCPTMERCH";
      case(PWINFO_RCPTCHOLDER      ): return "PWINFO_RCPTCHOLDER";
      case(PWINFO_RCPTCHSHORT      ): return "PWINFO_RCPTCHSHORT";
      case(PWINFO_TRNORIGDATE      ): return "PWINFO_TRNORIGDATE";
      case(PWINFO_TRNORIGNSU       ): return "PWINFO_TRNORIGNSU";
      case(PWINFO_TRNORIGAMNT      ): return "PWINFO_TRNORIGAMNT";
      case(PWINFO_TRNORIGAUTH      ): return "PWINFO_TRNORIGAUTH";
      case(PWINFO_TRNORIGREQNUM    ): return "PWINFO_TRNORIGREQNUM";
      case(PWINFO_TRNORIGTIME      ): return "PWINFO_TRNORIGTIME";
      case(PWINFO_CARDFULLPAN      ): return "PWINFO_CARDFULLPAN";
      case(PWINFO_CARDEXPDATE      ): return "PWINFO_CARDEXPDATE";
      case(PWINFO_CARDPARCPAN      ): return "PWINFO_CARDPARCPAN";
      case(PWINFO_BARCODENTMODE    ): return "PWINFO_BARCODENTMODE";
      case(PWINFO_BARCODE          ): return "PWINFO_BARCODE";
      case(PWINFO_MERCHADDDATA1    ): return "PWINFO_MERCHADDDATA1";
      case(PWINFO_MERCHADDDATA2    ): return "PWINFO_MERCHADDDATA2";
      case(PWINFO_MERCHADDDATA3    ): return "PWINFO_MERCHADDDATA3";
      case(PWINFO_MERCHADDDATA4    ): return "PWINFO_MERCHADDDATA4";
      case(PWINFO_PAYMNTTYPE       ): return "PWINFO_PAYMNTTYPE";
      case(PWINFO_USINGPINPAD      ): return "PWINFO_USINGPINPAD";
      case(PWINFO_PPCOMMPORT       ): return "PWINFO_PPCOMMPORT";
      case(PWINFO_IDLEPROCTIME     ): return "PWINFO_IDLEPROCTIME";
      case(PWINFO_PNDAUTHSYST		  ): return "PWINFO_PNDAUTHSYST";	      
      case(PWINFO_PNDVIRTMERCH     ): return "PWINFO_PNDVIRTMERCH";
      case(PWINFO_PNDREQNUM        ): return "PWINFO_PNDREQNUM";   
      case(PWINFO_PNDAUTLOCREF     ): return "PWINFO_PNDAUTLOCREF";
      case(PWINFO_PNDAUTEXTREF     ): return "PWINFO_PNDAUTEXTREF";
      default                       : return "PWINFO_XXX";
   }
}

/*=====================================================================================*\
 Funcao     :  PrintResultParams

 Descricao  :  Esta função exibe na tela todas as informações de resultado disponíveis 
               no momento em que foi chamada.
 
 Entradas   :  nao ha.

 Saidas     :  nao ha.
 
 Retorno    :  nao ha.
\*=====================================================================================*/
static void PrintResultParams()
{
   char szAux[10000];
   Int16 iRet=0, i;

   // Percorre todos os números inteiros, exibindo o valor do parâmetro PWINFO_XXX
   // sempre que o retorno for de dados disponível
   // Essa implementação foi feita desta forma para facilitar o exemplo, a função
   // PW_iGetResult() deve ser chamada somente para informações documentadas, as
   // chamadas adicionais causarão lentidão no sistema como um todo.
   for( i=1; i<MAXINT16; i++)
   {
      if(i==PWINFO_PPINFO)
         continue;

      iRet = gstHwFuncs.pPW_iGetResult( i, szAux, sizeof(szAux));
      if( iRet == PWRET_OK)
      {
         InputCR(szAux);
         printf( "\n\n%s<0x%X> =\n%s", pszGetInfoDescription(i), i, szAux);

         // Caso seja um parâmetro necessário para a confirmação da transação
         // o armazena na estrutura existente para essa finalidade.
         switch(i)
         {
            case(PWINFO_REQNUM):
               strcpy( gstConfirmData.szReqNum, szAux);
               break;

            case(PWINFO_AUTEXTREF):
               strcpy( gstConfirmData.szHostRef, szAux);
               break;

            case(PWINFO_AUTLOCREF):
               strcpy( gstConfirmData.szLocRef, szAux);
               break;

            case(PWINFO_VIRTMERCH):
               strcpy( gstConfirmData.szVirtMerch, szAux);
               break;

            case(PWINFO_AUTHSYST):
               strcpy( gstConfirmData.szAuthSyst, szAux);
               break;
         }
      }
   }
   printf("\n"); // Flushing display
}

/*=====================================================================================*\
 Funcao     :  PrintReturnDescription

 Descricao  :  Esta função recebe um código PWRET_XXX e imprime na tela a sua descrição.
 
 Entradas   :  iResult :   Código de resultado da transação (PWRET_XXX). 

 Saidas     :  nao ha.
 
 Retorno    :  nao ha.
\*=====================================================================================*/
static void PrintReturnDescription(Int16 iReturnCode, char* pszDspMsg)
{
   switch( iReturnCode)
   {
      case(PWRET_OK):
         printf("\nRetorno = PWRET_OK");
         break;

      case(PWRET_INVCALL):
         printf("\nRetorno = PWRET_INVCALL");
         break;

      case(PWRET_INVPARAM):
         printf("\nRetorno = PWRET_INVPARAM");
         break;

      case(PWRET_NODATA):
         printf("\nRetorno = PWRET_NODATA");
         break;
      
      case(PWRET_BUFOVFLW):
         printf("\nRetorno = PWRET_BUFOVFLW");
         break;

      case(PWRET_MOREDATA):
         printf("\nRetorno = PWRET_MOREDATA");
         break;

      case(PWRET_DLLNOTINIT):
         printf("\nRetorno = PWRET_DLLNOTINIT");
         break;

      case(PWRET_NOTINST):
         printf("\nRetorno = PWRET_NOTINST");
         break;

      case(PWRET_TRNNOTINIT):
         printf("\nRetorno = PWRET_TRNNOTINIT");
         break;

      case(PWRET_NOMANDATORY):
         printf("\nRetorno = PWRET_NOMANDATORY");
         break;

      case(PWRET_TIMEOUT):
         printf("\nRetorno = PWRET_TIMEOUT");
         break;

      case(PWRET_CANCEL):
         printf("\nRetorno = PWRET_CANCEL");
         break;;

      case(PWRET_FALLBACK):
         printf("\nRetorno = PWRET_FALLBACK");
         break;

      case(PWRET_DISPLAY):
         printf("\nRetorno = PWRET_DISPLAY");
         InputCR(pszDspMsg);
         printf("\n%s", pszDspMsg);
         break;

      case(PWRET_NOTHING):
         printf(".");
         break;

      case(PWRET_FROMHOST):
         printf("\nRetorno = ERRO DO HOST");
         break;

      case(PWRET_SSLCERTERR):
         printf("\nRetorno = PWRET_SSLCERTERR");
         break;

      case(PWRET_SSLNCONN):
         printf("\nRetorno = PWRET_SSLNCONN");
         break;

      default:
         printf("\nRetorno = OUTRO ERRO <%d>", iReturnCode);
         break;
   }

   // Imprime os resultados disponíveis na tela caso seja fim da transação
   if( iReturnCode!=PWRET_MOREDATA && iReturnCode!=PWRET_DISPLAY && 
       iReturnCode!=PWRET_NOTHING && iReturnCode!=PWRET_FALLBACK)
      PrintResultParams();
}
/*=====================================================================================*\
 Funcao     :  TesteAdmin

 Descricao  :  Esta função inicia uma transação administrativa genérica através de 
               PW_iNewTransac, adiciona os parâmetros obrigatórios através de PW_iAddParam 
               e em seguida se comporta de forma idêntica a ExecTransac.
 
 Entradas   :  nao ha.

 Saidas     :  nao ha.
 
 Retorno    :  nao ha.
\*=====================================================================================*/
static void TesteAA()
{
   PW_GetData vstParam[10];
   Int16   iNumParam = 10, iRet;
   Uint32 ulEvent=0;
   char szDspMsg[128];

   // Aguarda a inserção ou passagem do cartão pelo usuário para iniciar a transação
   for(;;)
   {
      // Exibe a mensagem no PIN-pad
      printf("\nAGUARDANDO CARTAO PARA INICIAR OPERACAO!!!");
      iRet = gstHwFuncs.pPW_iPPDisplay(" INSIRA OU PASSE    O CARTAO    ");
      if(iRet)
      {
         printf("\nErro em PW_iPPDisplay <%d>", iRet);
         return;
      }
      do
      {
         iRet =gstHwFuncs.pPW_iPPEventLoop(szDspMsg, sizeof(szDspMsg));
         if(iRet!=PWRET_OK && iRet!=PWRET_DISPLAY && iRet!=PWRET_NOTHING)
            return;
         usleep(1000*100);
      } while(iRet!=PWRET_OK);

      // Aguarda o cartão do cliente
      iRet = gstHwFuncs.pPW_iPPWaitEvent(&ulEvent);
      if(iRet)
      {
         printf("\nErro em PPWaitEvent <%d>", iRet);
         return;
      }
      do
      {
         iRet =gstHwFuncs.pPW_iPPEventLoop(szDspMsg, sizeof(szDspMsg));
         if(iRet!=PWRET_OK && iRet!=PWRET_DISPLAY && iRet!=PWRET_NOTHING)
         {
            printf("\nErro em PW_iPPEventLoop <%d>", iRet);
            return;
         }
         usleep(1000*500);
         printf(".");
      } while(iRet!=PWRET_OK);

      if( ulEvent==PWPPEVT_ICC || ulEvent==PWPPEVT_MAGSTRIPE)                  
         break;
   }

   // Exibe mensagem processando no PIN-pad
   iRet = gstHwFuncs.pPW_iPPDisplay(" PROCESSANDO...                 ");
   if(iRet)
   {
      printf("\nErro em PPDisplay <%d>", iRet);
      return;
   }
   do
   {
      iRet =gstHwFuncs.pPW_iPPEventLoop(szDspMsg, sizeof(szDspMsg));
      if(iRet!=PWRET_OK && iRet!=PWRET_DISPLAY && iRet!=PWRET_NOTHING)
         return;
      usleep(1000*100);
   } while(iRet!=PWRET_OK);

   /// Inicializa a transação de venda
   iRet = gstHwFuncs.pPW_iNewTransac(PWOPER_SALE);
   if( iRet)
      printf("\nErro PW_iNewTransacr <%d>", iRet);

   // Adiciona os parâmetros obrigatórios
   AddMandatoryParams();
   gstHwFuncs.pPW_iAddParam(PWINFO_TOTAMNT, "100");
   
   // Loop até que ocorra algum erro ou a transação seja aprovada, capturando dados
   // do usuário caso seja necessário
   for(;;)
   {
      // Coloca o valor 10 (tamanho da estrutura de entrada) no parâmetro iNumParam
      iNumParam = 10;

      printf("\n\nPROCESSANDO...\n");
      iRet = gstHwFuncs.pPW_iExecTransac(vstParam, &iNumParam);
      PrintReturnDescription(iRet, NULL);
      if(iRet == PWRET_MOREDATA)
      {
          printf("\nNumero de parametros ausentes:%d", iNumParam);
         
          // Tenta capturar os dados faltantes, caso ocorra algum erro retorna
         if (iExecGetData(vstParam, iNumParam))
            return;
         continue;
      }
      break;
   }

   // Caso a transação tenha ocorrido com sucesso, confirma
   if( iRet == PWRET_OK)
   {
      printf("\n\nCONFIRMANDO TRANSACAO...\n");
      iRet = gstHwFuncs.pPW_iConfirmation(PWCNF_CNF_AUTO, gstConfirmData.szReqNum, 
      gstConfirmData.szLocRef, gstConfirmData.szHostRef, gstConfirmData.szVirtMerch, 
      gstConfirmData.szAuthSyst);
      if( iRet)
         printf("\nERRO AO CONFIRMAR TRANSAÇÃO");
   }

}