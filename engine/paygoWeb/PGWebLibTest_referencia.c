/*********************** SETIS - Automação e Sistemas ************************

 Arquivo          : PGWebLibTest.c
 Projeto          : Pay&Go WEB
 Plataforma       : Linux
 Data de criação  : 19/02/2014
 Autor            : Guilherme Eduardo Leite
 Descrição        : Console de testes extendido para a simulação de um cliente
                    para a so de integração com a solução Pay&Go WEB.
 ================================= HISTÓRICO =================================
 Data      Responsável Modificação
 --------  ----------- -------------------------------------------------------
\*****************************************************************************/
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
#define  PGWEBLIBTEST_VERSION "1.1.0.0"

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
 Funcao     :  iExecGetData

 Descricao  :  Esta função obtém dos usuários os dados requisitado pelo Pay&Go Web.
 
 Entradas   :  vstGetData  :  Vetor com as informações dos dados a serem obtidos.
               iNumParam   :  Número de dados a serem obtidos.

 Saidas     :  nao ha.
 
 Retorno    :  Código de resultado da operação.
\*=====================================================================================*/
static Int16 iExecGetData(PW_GetData vstGetData[], Int16 iNumParam)
{
   Int16 i,j, iKey, iRet;
   char szAux[1024], szDspMsg[128], szMsgPinPad[34];
   Uint32 ulEvent=0;

   // Caso exista uma mensagem a ser exibida antes da captura do próximo dado, a exibe
   if(vstGetData[0].szMsgPrevia != NULL && vstGetData[0].szMsgPrevia[0])
   {
      InputCR(vstGetData[0].szMsgPrevia);
      printf("\nMensagem = \n%s", vstGetData[0].szMsgPrevia);
   }
   
   // Enquanto houverem dados para capturar
   for( i=0; i < iNumParam; i++)
   {
      // Imprime na tela qual informação está sendo capturada
      printf("\nDado a capturar = %s<0x%X>", pszGetInfoDescription(vstGetData[i].wIdentificador), 
         vstGetData[i].wIdentificador);

      // Captura de acordo com o tipo de captura
      switch( vstGetData[i].bTipoDeDado)
      {
         // Menu de opções
         case(PWDAT_MENU):
            printf("\nTipo de dados = MENU");
            InputCR(vstGetData[i].szPrompt);
            printf("\n%s\n", vstGetData[i].szPrompt);

            // Caso só tenha uma opção, escolhe automaticamente
            if( vstGetData[i].bNumOpcoesMenu == 1)
            {
               printf("\nMENU COM 1 OPCAO... ADICIONANDO AUTOMATICAMENTE...");
               iRet = gstHwFuncs.pPW_iAddParam(vstGetData[i].wIdentificador, vstGetData[i].vszValorMenu[0]);
               if(iRet)
                  printf("\nERRO AO ADICIONAR PARAMETRO...");
               break;
            }

            // Caso o modo autoatendimento esteja ativado, faz o menu no PIN-pad
            if(gfAutoAtendimento)
            {
               if( vstGetData[i].bNumOpcoesMenu > 2)
                  printf("\nMENU NAO PODE SER FEITO NO PINPAD!!!");
               else
                  printf("\nEXECUTANDO MENU NO PINPAD");

               // Garante que as opções de menu não terão mais do que 13 caracteres
               vstGetData[i].vszTextoMenu[0][13] = '\0';
               vstGetData[i].vszTextoMenu[1][13] = '\0';

               sprintf(szMsgPinPad, "F1-%s\rF2-%s",vstGetData[i].vszTextoMenu[0], vstGetData[i].vszTextoMenu[1]);

               for(;;)
               {
                  // Exibe a mensagem no PIN-pad
                  iRet = gstHwFuncs.pPW_iPPDisplay(szMsgPinPad);
                  if(iRet)
                  {
                     printf("\nErro em PW_iPPDisplay <%d>", iRet);
                     return iRet;
                  }
                  do
                  {
                     iRet =gstHwFuncs.pPW_iPPEventLoop(szDspMsg, sizeof(szDspMsg));
                     if(iRet!=PWRET_OK && iRet!=PWRET_DISPLAY && iRet!=PWRET_NOTHING)
                        return iRet;
                     usleep(1000*100);
                  } while(iRet!=PWRET_OK);

                  // Aguarda a seleção da opção pelo cliente
                  iRet = gstHwFuncs.pPW_iPPWaitEvent(&ulEvent);
                  if(iRet)
                  {
                     printf("\nErro em PPWaitEvent <%d>", iRet);
                     return iRet;
                  }
                  do
                  {
                     iRet =gstHwFuncs.pPW_iPPEventLoop(szDspMsg, sizeof(szDspMsg));
                     if(iRet!=PWRET_OK && iRet!=PWRET_DISPLAY && iRet!=PWRET_NOTHING)
                     {
                        printf("\nErro em PW_iPPEventLoop <%d>", iRet);
                        return iRet;
                     }
                     usleep(1000*500);
                     printf(".");
                  } while(iRet!=PWRET_OK);

                  if( ulEvent==PWPPEVT_KEYF1)
                  {
                     iKey = 0x30;                    
                     break;
                  }
                  else if( ulEvent==PWPPEVT_KEYF2)
                  {
                     iKey = 0x31;
                     break;
                  }
                  else if(ulEvent==PWPPEVT_KEYCANC)
                  {
                     iRet = gstHwFuncs.pPW_iPPDisplay("    OPERACAO        CANCELADA   ");
                     if(iRet)
                     {
                        printf("\nErro em PPDisplay <%d>", iRet);
                        return iRet;
                     }
                     do
                     {
                        iRet =gstHwFuncs.pPW_iPPEventLoop(szDspMsg, sizeof(szDspMsg));
                        if(iRet!=PWRET_OK && iRet!=PWRET_DISPLAY && iRet!=PWRET_NOTHING)
                           return iRet;
                        usleep(1000*100);
                     } while(iRet!=PWRET_OK);

                     return PWRET_CANCEL;
                  }
                  else
                  {
                     iRet = gstHwFuncs.pPW_iPPDisplay("   UTILIZE AS   TECLAS F1 OU F2");
                     if(iRet)
                     {
                        printf("\nErro em PPDisplay <%d>", iRet);
                        return iRet;
                     }
                     do
                     {
                        iRet =gstHwFuncs.pPW_iPPEventLoop(szDspMsg, sizeof(szDspMsg));
                        if(iRet!=PWRET_OK && iRet!=PWRET_DISPLAY && iRet!=PWRET_NOTHING)
                           return iRet;
                        usleep(1000*100);
                     } while(iRet!=PWRET_OK);
                     usleep(1000*1000);
                  }
               }
            }
            else
            {
               for(j=0; j < vstGetData[i].bNumOpcoesMenu; j++) 
                  printf("\n%d - %s", j, vstGetData[i].vszTextoMenu[j]);

               printf("\n\nSELECIONE A OPCAO:");

               __fpurge(stdin);
               do 
               {
                  iKey = getchar ();

                  if( iKey-0x30 > vstGetData[i].bNumOpcoesMenu )
                     continue;
                  else
                     break;
               } while (TRUE);
               printf ("%c\n", iKey);
            }

            iRet = gstHwFuncs.pPW_iAddParam(vstGetData[i].wIdentificador, vstGetData[i].vszValorMenu[iKey-0x30]);
            if(iRet)
               printf("\nERRO AO ADICIONAR PARAMETRO...");

            break;

         // Captura de dado digitado
         case(PWDAT_TYPED):
            if(gfAutoAtendimento)
            {
               gstHwFuncs.pPW_iPPAbort();
               printf("\n\nNAO E POSSIVEL CAPTURAR UM DADO DIGITADO NO AUTOATENDIMENTO\n");
               return PWRET_CANCEL;
            }

            printf("\nTipo de dados = DIGITADO");
            printf("\nTamanho minimo = %d", vstGetData[i].bTamanhoMinimo );
            printf("\nTamanho maximo = %d", vstGetData[i].bTamanhoMaximo);
            printf("\nValor atual:%s\n", vstGetData[i].szValorInicial);
            
            for(;;)
            {
               InputCR(vstGetData[i].szPrompt);
               printf("\n%s\n", vstGetData[i].szPrompt);
               scanf("%s", szAux);
               if( strlen(szAux) > vstGetData[i].bTamanhoMaximo)            
               {
                  printf("\nTamanho maior que o maximo permitido");
                  printf("\nTente novamente...\n");
                  continue;
               }
               else if ( strlen(szAux) < vstGetData[i].bTamanhoMinimo)
               {
                  printf("\nTamanho menor que o minimo permitido");
                  printf("\nTente novamente...\n");
                  continue;
               }
               else
                  break;
            }

            iRet = gstHwFuncs.pPW_iAddParam(vstGetData[i].wIdentificador, szAux);
            if(iRet)
               printf("\nERRO AO ADICIONAR PARAMETRO...");

            break;

         // Captura de dados do cartão
         case(PWDAT_CARDINF):
            printf("\nTipo de dados = DADOS DO CARTAO");

            if(vstGetData[i].ulTipoEntradaCartao == 1/*1=ENTRADA DIGITADA*/ )
            {
               printf(" ***SOMENTE DIGITADO***");
               InputCR(vstGetData[i].szPrompt);
               printf("\n%s\n", vstGetData[i].szPrompt);
               scanf("%s", szAux);

               iRet = gstHwFuncs.pPW_iAddParam(PWINFO_CARDFULLPAN, szAux);
               if(iRet)
                  printf("\nERRO AO ADICIONAR PARAMETRO...");
            }
            else
            {
               iRet = gstHwFuncs.pPW_iPPGetCard(i);
               PrintReturnDescription(iRet, szDspMsg);
               if(iRet)
                  return iRet;
               __fpurge(stdin);
               do
               {
                  iRet = gstHwFuncs.pPW_iPPEventLoop(szDspMsg, sizeof(szDspMsg));
                  PrintReturnDescription(iRet, szDspMsg);
                  if(iRet!=PWRET_OK && iRet!=PWRET_DISPLAY && iRet!=PWRET_NOTHING)
                     return iRet;
                  if( (vstGetData[i].ulTipoEntradaCartao&1/*1=ENTRADA DIGITADA*/) && kbhit() )
                  {
                     gstHwFuncs.pPW_iPPAbort();
                     printf("\n");
                     scanf("%s", szAux);
                     iRet = gstHwFuncs.pPW_iAddParam(PWINFO_CARDFULLPAN, szAux);
                     if(iRet)
                        printf("\nERRO AO ADICIONAR PARAMETRO...");
                     break;
                  }
                  usleep(1000*500);
               } while(iRet!=PWRET_OK);
            }
            break;

         // Captura de dado digitado no PIN-pad
         case(PWDAT_PPENTRY):
            printf("\nTipo de dados = DADO DIG. NO PINPAD");
            iRet = gstHwFuncs.pPW_iPPGetData(i);
            PrintReturnDescription(iRet, szDspMsg);
            if(iRet)
               return iRet;

            do
            {
               iRet =gstHwFuncs.pPW_iPPEventLoop(szDspMsg, sizeof(szDspMsg));
               PrintReturnDescription(iRet, szDspMsg);
               if(iRet!=PWRET_OK && iRet!=PWRET_DISPLAY && iRet!=PWRET_NOTHING)
                  return iRet; 
               usleep(1000*500);
            } while(iRet!=PWRET_OK);
            break;

         // Captura da senha criptografada
         case(PWDAT_PPENCPIN):
            printf("\nTipo de dados = SENHA");
            iRet = gstHwFuncs.pPW_iPPGetPIN(i);
            PrintReturnDescription(iRet, szDspMsg);
            if(iRet)
               return iRet;

            do
            {
               iRet =gstHwFuncs.pPW_iPPEventLoop(szDspMsg, sizeof(szDspMsg));
               PrintReturnDescription(iRet, szDspMsg);
               if(iRet!=PWRET_OK && iRet!=PWRET_DISPLAY && iRet!=PWRET_NOTHING)
                  return iRet;
               usleep(1000*500);
            } while(iRet!=PWRET_OK);
            break;

         // Processamento offline do cartão com chip
         case(PWDAT_CARDOFF):
            printf("\nTipo de dados = CHIP OFFLINE");
            iRet = gstHwFuncs.pPW_iPPGoOnChip(i);
            PrintReturnDescription(iRet, szDspMsg);
            if(iRet)
               return iRet;

            do
            {
               iRet =gstHwFuncs.pPW_iPPEventLoop(szDspMsg, sizeof(szDspMsg));
               PrintReturnDescription(iRet, szDspMsg);
               if(iRet!=PWRET_OK && iRet!=PWRET_DISPLAY && iRet!=PWRET_NOTHING)
                  return iRet;
               usleep(1000*500);
            } while(iRet!=PWRET_OK);
            break;

         // Processamento online do cartão com chip
         case(PWDAT_CARDONL):
            printf("\nTipo de dados = CHIP ONLINE");
            iRet = gstHwFuncs.pPW_iPPFinishChip(i);
            PrintReturnDescription(iRet, szDspMsg);
            if(iRet)
               return iRet;

            do
            {
               iRet =gstHwFuncs.pPW_iPPEventLoop(szDspMsg, sizeof(szDspMsg));
               PrintReturnDescription(iRet, szDspMsg);
               if(iRet!=PWRET_OK && iRet!=PWRET_DISPLAY && iRet!=PWRET_NOTHING)
                  return iRet;
               usleep(1000*500);
            } while(iRet!=PWRET_OK);
            break;

         // Confirmação de dado no PIN-pad
         case(PWDAT_PPCONF):
            printf("\nTipo de dados = PPCONFIRMDATA");
            iRet = gstHwFuncs.pPW_iPPConfirmData(i);
            PrintReturnDescription(iRet, szDspMsg);
            if(iRet)
               return iRet;

            do
            {
               iRet =gstHwFuncs.pPW_iPPEventLoop(szDspMsg, sizeof(szDspMsg));
               PrintReturnDescription(iRet, szDspMsg);
               if(iRet!=PWRET_OK && iRet!=PWRET_DISPLAY && iRet!=PWRET_NOTHING)
                  return iRet;
               usleep(1000*500);
            } while(iRet!=PWRET_OK);
            break;

         // Remoção de cartão do PIN-pad
         case(PWDAT_PPREMCRD):
            printf("\nTipo de dados = PWDAT_PPREMCRD");
            iRet = gstHwFuncs.pPW_iPPRemoveCard();
            PrintReturnDescription(iRet, szDspMsg);
            if(iRet)
               return iRet;

            do
            {
               iRet =gstHwFuncs.pPW_iPPEventLoop(szDspMsg, sizeof(szDspMsg));
               PrintReturnDescription(iRet, szDspMsg);
               if(iRet!=PWRET_OK && iRet!=PWRET_DISPLAY && iRet!=PWRET_NOTHING)
                  return iRet;
               usleep(1000*500);
            } while(iRet!=PWRET_OK);
            break;

         case (PWDAT_PPGENCMD):
            printf ("\nTipo de dados = PWDAT_PPGENCMD");
            
            // Executa a operação
            iRet = gstHwFuncs.pPW_iPPGenericCMD (i);
            PrintReturnDescription (iRet, szDspMsg);

            if (iRet) 
               return iRet;

            // Caso a operação tenha sido executada com sucesso, inicia o loop e trata os
            // retornos possíveis
            do {
               iRet = gstHwFuncs.pPW_iPPEventLoop (szDspMsg, sizeof (szDspMsg));
               PrintReturnDescription (iRet, szDspMsg);
               if (iRet != PWRET_OK && iRet != PWRET_DISPLAY && iRet != PWRET_NOTHING) {
                  return iRet;
               }

               usleep (1000 * 500);
            } while (iRet != PWRET_OK);

            break;

         // Tipo de captura desconhecido
         default:
            printf("\nCAPTURA COM TIPO DE DADOS DESCONHECIDO<%d>", vstGetData[i].bTipoDeDado);
      }
   }
   return PWRET_OK;
}

/*=====================================================================================*\
 Funcao     :  AddMandatoryParams

 Descricao  :  Esta função adiciona os parâmetros obrigatórios de toda mensagem para o
               Pay&Go Web.
 
 Entradas   :  nao ha.

 Saidas     :  nao ha.
 
 Retorno    :  nao ha.
\*=====================================================================================*/
static void AddMandatoryParams()
{
   // Adiciona os parâmetros obrigatórios
   gstHwFuncs.pPW_iAddParam(PWINFO_AUTDEV, "SETIS AUTOMACAO E SISTEMA LTDA");
   gstHwFuncs.pPW_iAddParam(PWINFO_AUTVER, PGWEBLIBTEST_VERSION);
   gstHwFuncs.pPW_iAddParam(PWINFO_AUTNAME, "PGWEBLIBTEST");
   gstHwFuncs.pPW_iAddParam(PWINFO_AUTCAP, "15");
   gstHwFuncs.pPW_iAddParam(PWINFO_AUTHTECHUSER, "PGWEBLIBTEST");
}

/*=====================================================================================*\
 Funcao     :  Init

 Descricao  :  Esta função captura os dados necesários e executa PW_iInit.
 
 Entradas   :  nao ha.

 Saidas     :  nao ha.
 
 Retorno    :  nao ha.
\*=====================================================================================*/
static void Init()
{
   char szWorkingDir[256];
   Int16 iRet=0;

   printf("\nDigite a pasta de trabalho: ");
   scanf(" %[^\n]", szWorkingDir);

   iRet = gstHwFuncs.pPW_iInit(szWorkingDir);
   PrintReturnDescription(iRet, NULL);
}

/*=====================================================================================*\
 Funcao     :  NewTransac

 Descricao  :  Esta função captura os dados necesários e executa PW_iNewTransac.
 
 Entradas   :  nao ha.

 Saidas     :  nao ha.
 
 Retorno    :  nao ha.
\*=====================================================================================*/
static void NewTransac()
{
   Int16 iOper = 0, iRet = 0;
  
   // Exibe na tela as opções de operação existentes e captura a escolhida
   printf("\n0x00 - PWOPER_NULL       - Testa comunicacao");
   printf("\n0x01 - PWOPER_INSTALL    - Instalacao");
   printf("\n0x02	- PWOPER_PARAMUPD	  - Atualizacao de parametros");
   printf("\n0x10 - PWOPER_REPRINT    - Reimpressao");
   printf("\n0x11 - PWOPER_RPTTRUNC   - Relatorio");
   printf("\n0x20 - PWOPER_ADMIN      - Operacao administrativa");
   printf("\n0x21 - PWOPER_SALE       - Venda");
   printf("\n0x22 - PWOPER_SALEVOID   - Cancelamento de venda");
   printf("\n0x23 - PWOPER_PREPAID    - Aquisicao de creditos pre-pagos");
   printf("\n0x24 - PWOPER_CHECKINQ   - Consulta a validade de um cheque papel");
   printf("\n0x25 - PWOPER_RETBALINQ  - Consulta o saldo/limite do Estabelecimento");
   printf("\n0x26 - PWOPER_CRDBALINQ  - Consulta o saldo do cartao do Cliente");
   printf("\n0x27 - PWOPER_INITIALIZ  - Inicializacao/abertura");
   printf("\n0x28 - PWOPER_SETTLEMNT  - Fechamento/finalizacao");
   printf("\n0x29 - PWOPER_PREAUTH    - Pre-autorizacao");
   printf("\n0x2A - PWOPER_PREAUTVOID - Cancelamento de pre-autorizacao");
   printf("\n0x2B - PWOPER_CASHWDRWL  - Saque");
   printf("\n0x2C - PWOPER_LOCALMAINT - Baixa tecnica");
   printf("\n0x2D - PWOPER_FINANCINQ  - Consulta as taxas de financiamento");
   printf("\n0x2E - PWOPER_ADDRVERIF  - Verifica junto ao Provedor o endereço do Cliente");
   printf("\n0x2F - PWOPER_SALEPRE    - Efetiva uma pre-autorizacao (PWOPER_PREAUTH)");
   printf("\n0x30 - PWOPER_LOYCREDIT  - Registra o acumulo de pontos pelo Cliente");
   printf("\n0x31 - PWOPER_LOYCREDVOID- Cancela uma transacao PWOPER_LOYCREDIT");
   printf("\n0x32 - PWOPER_LOYDEBIT   - Registra o resgate de pontos/premio pelo Cliente");
   printf("\n0x33 - PWOPER_LOYDEBVOID - Cancela uma transacao PWOPER_LOYDEBIT");
   printf("\n0x39 - PWOPER_VOID       - Menu de cancelamentos, se so 1 seleciona automaticamente");
   printf("\n0xFC - PWOPER_VERSION    - Versao");
   printf("\n0xFD - PWOPER_CONFIG     - Configuracao");
   printf("\n0xFE - PWOPER_MAINTENANCE- Manutencao");
   printf("\n SELECIONE A OPCAO:");
   scanf("%hx", &iOper);

   // Executa a operação
   iRet = gstHwFuncs.pPW_iNewTransac(iOper);
   PrintReturnDescription(iRet, NULL);

   __fpurge(stdin);
   printf ("\n <tecle algo>\n\n");
   getchar();
}

/*=====================================================================================*\
 Funcao     :  AddParam

 Descricao  :  Esta função captura os dados necesários e executa PW_iAddParam.
 
 Entradas   :  nao ha.

 Saidas     :  nao ha.
 
 Retorno    :  nao ha.
\*=====================================================================================*/
static void AddParam()
{
   Int16 iParam = 0, iRet = 0;
   char szValue[129];

   // Exibe na tela as opções de informação existentes e captura a escolhida
   printf("\nEscolha o codigo do parametro a ser adicionado: ");
   printf("\n0x11 - PWINFO_POSID		");	
   printf("\n0x15 - PWINFO_AUTNAME		");	
   printf("\n0x16 - PWINFO_AUTVER		");	
   printf("\n0x17 - PWINFO_AUTDEV		");	
   printf("\n0x1B - PWINFO_DESTTCPIP	");	
   printf("\n0x1C - PWINFO_MERCHCNPJCPF");	
   printf("\n0x24 - PWINFO_AUTCAP		");	
   printf("\n0x25 - PWINFO_TOTAMNT		");	
   printf("\n0x26 - PWINFO_CURRENCY	");	
   printf("\n0x27 - PWINFO_CURREXP		");	
   printf("\n0x28 - PWINFO_FISCALREF	");	
   printf("\n0x29 - PWINFO_CARDTYPE	");	
   printf("\n0x2A - PWINFO_PRODUCTNAME	");	
   printf("\n0x31 - PWINFO_DATETIME	");	
   printf("\n0x32 - PWINFO_REQNUM		");	
   printf("\n0x35 - PWINFO_AUTHSYST	");	
   printf("\n0x36 - PWINFO_VIRTMERCH	");	
   printf("\n0x38 - PWINFO_AUTMERCHID	");	
   printf("\n0x3A - PWINFO_PHONEFULLNO	");	
   printf("\n0x3B - PWINFO_FINTYPE		");	
   printf("\n0x3C - PWINFO_INSTALLMENTS");	
   printf("\n0x3D - PWINFO_INSTALLMDATE");	
   printf("\n0x3E - PWINFO_PRODUCTID	");	
   printf("\n0x42 - PWINFO_RESULTMSG	");	
   printf("\n0x43 - PWINFO_CNFREQ		");	
   printf("\n0x44 - PWINFO_AUTLOCREF	");	
   printf("\n0x45 - PWINFO_AUTEXTREF	");	
   printf("\n0x46 - PWINFO_AUTHCODE	");	
   printf("\n0x47 - PWINFO_AUTRESPCODE	");	
   printf("\n0x48 - PWINFO_AUTDATETIME	");	
   printf("\n0x49 - PWINFO_DISCOUNTAMT	");	
   printf("\n0x4A - PWINFO_CASHBACKAMT	");	
   printf("\n0x4B - PWINFO_CARDNAME	");	
   printf("\n0x4C - PWINFO_ONOFF		");	
   printf("\n0x4D - PWINFO_BOARDINGTAX	");	
   printf("\n0x4E - PWINFO_TIPAMOUNT	");	
   printf("\n0x4F - PWINFO_INSTALLM1AMT");	
   printf("\n0x50 - PWINFO_INSTALLMAMNT");	
   printf("\n0x52 - PWINFO_RCPTFULL	");	
   printf("\n0x53 - PWINFO_RCPTMERCH	");	
   printf("\n0x54 - PWINFO_RCPTCHOLDER	");	
   printf("\n0x55 - PWINFO_RCPTCHSHORT	");	
   printf("\n0x57 - PWINFO_TRNORIGDATE	");	
   printf("\n0x58 - PWINFO_TRNORIGNSU	");	
   printf("\n0x60 - PWINFO_TRNORIGAMNT	");	
   printf("\n0x62 - PWINFO_TRNORIGAUTH	");	
   printf("\n0x72 - PWINFO_TRNORIGREQNUM");	
   printf("\n0x73 - PWINFO_TRNORIGTIME	");	
   printf("\n0xC1 - PWINFO_CARDFULLPAN	");	
   printf("\n0xC2 - PWINFO_CARDEXPDATE	");	
   printf("\n0xC8 - PWINFO_CARDPARCPAN	");	
   printf("\n0xE9 - PWINFO_BARCODENTMODE");
   printf("\n0xEA - PWINFO_BARCODE		");	
   printf("\n0xF0 - PWINFO_MERCHADDDATA1");	
   printf("\n0xF1 - PWINFO_MERCHADDDATA2");	
   printf("\n0xF2 - PWINFO_MERCHADDDATA3");
   printf("\n0xF3 - PWINFO_MERCHADDDATA4");
   printf("\n0xF5 - PWINFO_AUTHMNGTUSER");      
   printf("\n0xF6 - PWINFO_AUTHTECHUSER");
   printf("\n0x1F21 - PWINFO_PAYMNTTYPE");		
   printf("\n0x7F01 - PWINFO_USINGPINPAD");		
   printf("\n0x7F02 - PWINFO_PPCOMMPORT");		
   printf("\n0x7F04 - PWINFO_IDLEPROCTIME");  
   printf("\nCódigo = ");
   scanf("%hx", &iParam);

   printf("\nDigite o valor do parametro: ");
   scanf(" %[^\n]",szValue);

   // Executa a operação
   iRet = gstHwFuncs.pPW_iAddParam(iParam, szValue);
   PrintReturnDescription(iRet, NULL);

   __fpurge(stdin);
   printf ("\n <tecle algo>\n\n");
   getchar();
}

/*=====================================================================================*\
 Funcao     :  ExecTransac

 Descricao  :  Esta função executa PW_iExecTransac, caso falte algum dado para executar
               a transação, faz a captura dos dados faltantes do usuário e executa 
               PW_iExecTransac novamente, até que seja possível aprovar/negar a transação.
 
 Entradas   :  nao ha.

 Saidas     :  nao ha.
 
 Retorno    :  nao ha.
\*=====================================================================================*/
static void ExecTransac()
{
   PW_GetData vstParam[10];
   Int16   iNumParam = 10, iRet;
   
   // Loop até que ocorra algum erro ou a transação seja aprovada, capturando dados
   // do usuário caso seja necessário
   for(;;)
   {
      // Coloca o valor 10 (tamanho da estrutura de entrada) no parâmetro iNumParam
      iNumParam = 10;

      // Tenta executar a transação
      printf("\n\nPROCESSANDO...\n");
      iRet = gstHwFuncs.pPW_iExecTransac(vstParam, &iNumParam);
      PrintReturnDescription(iRet, NULL);
      if(iRet == PWRET_MOREDATA)
      {
          printf("\nNumero de parametros ausentes = %d", iNumParam);
         
          // Tenta capturar os dados faltantes, caso ocorra algum erro retorna
         if (iExecGetData(vstParam, iNumParam))
            return;
         continue;
      }
      break;     
   }

   __fpurge(stdin);
   printf ("\n <tecle algo>\n\n");
   getchar();
}

/*=====================================================================================*\
 Funcao     :  GetResult

 Descricao  :  Esta função obtém um dado da transação através de PW_iGetResult.
 
 Entradas   :  nao ha.

 Saidas     :  nao ha.
 
 Retorno    :  nao ha.
\*=====================================================================================*/
static void GetResult()
{
   Int16 iParam = 0, iRet = 0;
   char szAux[10000];

   // Exibe na tela as opções de informação existentes e captura a escolhida
   printf("\nEscolha o codigo do parametro a ser obtido: ");
   printf("\n0x11 - PWINFO_POSID		");	
   printf("\n0x15 - PWINFO_AUTNAME		");	
   printf("\n0x16 - PWINFO_AUTVER		");	
   printf("\n0x17 - PWINFO_AUTDEV		");	
   printf("\n0x1B - PWINFO_DESTTCPIP	");	
   printf("\n0x1C - PWINFO_MERCHCNPJCPF");	
   printf("\n0x24 - PWINFO_AUTCAP		");	
   printf("\n0x25 - PWINFO_TOTAMNT		");	
   printf("\n0x26 - PWINFO_CURRENCY	");	
   printf("\n0x27 - PWINFO_CURREXP		");	
   printf("\n0x28 - PWINFO_FISCALREF	");	
   printf("\n0x29 - PWINFO_CARDTYPE	");	
   printf("\n0x2A - PWINFO_PRODUCTNAME	");	
   printf("\n0x31 - PWINFO_DATETIME	");	
   printf("\n0x32 - PWINFO_REQNUM		");	
   printf("\n0x35 - PWINFO_AUTHSYST	");	
   printf("\n0x36 - PWINFO_VIRTMERCH	");	
   printf("\n0x38 - PWINFO_AUTMERCHID	");	
   printf("\n0x3A - PWINFO_PHONEFULLNO	");	
   printf("\n0x3B - PWINFO_FINTYPE		");	
   printf("\n0x3C - PWINFO_INSTALLMENTS");	
   printf("\n0x3D - PWINFO_INSTALLMDATE");	
   printf("\n0x3E - PWINFO_PRODUCTID	");	
   printf("\n0x42 - PWINFO_RESULTMSG	");	
   printf("\n0x43 - PWINFO_CNFREQ		");	
   printf("\n0x44 - PWINFO_AUTLOCREF	");	
   printf("\n0x45 - PWINFO_AUTEXTREF	");	
   printf("\n0x46 - PWINFO_AUTHCODE	");	
   printf("\n0x47 - PWINFO_AUTRESPCODE	");	
   printf("\n0x48 - PWINFO_AUTDATETIME	");	
   printf("\n0x49 - PWINFO_DISCOUNTAMT	");	
   printf("\n0x4A - PWINFO_CASHBACKAMT	");	
   printf("\n0x4B - PWINFO_CARDNAME	");	
   printf("\n0x4C - PWINFO_ONOFF		");	
   printf("\n0x4D - PWINFO_BOARDINGTAX	");	
   printf("\n0x4E - PWINFO_TIPAMOUNT	");	
   printf("\n0x4F - PWINFO_INSTALLM1AMT");	
   printf("\n0x50 - PWINFO_INSTALLMAMNT");	
   printf("\n0x52 - PWINFO_RCPTFULL	");	
   printf("\n0x53 - PWINFO_RCPTMERCH	");	
   printf("\n0x54 - PWINFO_RCPTCHOLDER	");	
   printf("\n0x55 - PWINFO_RCPTCHSHORT	");	
   printf("\n0x57 - PWINFO_TRNORIGDATE	");	
   printf("\n0x58 - PWINFO_TRNORIGNSU	");	
   printf("\n0x60 - PWINFO_TRNORIGAMNT	");	
   printf("\n0x62 - PWINFO_TRNORIGAUTH	");	
   printf("\n0x72 - PWINFO_TRNORIGREQNUM");	
   printf("\n0x73 - PWINFO_TRNORIGTIME	");	
   printf("\n0xC1 - PWINFO_CARDFULLPAN	");	
   printf("\n0xC2 - PWINFO_CARDEXPDATE	");	
   printf("\n0xC8 - PWINFO_CARDPARCPAN	");	
   printf("\n0xE9 - PWINFO_BARCODENTMODE");
   printf("\n0xEA - PWINFO_BARCODE		");	
   printf("\n0xF0 - PWINFO_MERCHADDDATA1");	
   printf("\n0xF1 - PWINFO_MERCHADDDATA2");	
   printf("\n0xF2 - PWINFO_MERCHADDDATA3");
   printf("\n0xF3 - PWINFO_MERCHADDDATA4");	
   printf("\n0x1F21 - PWINFO_PAYMNTTYPE");		
   printf("\n0x7F01 - PWINFO_USINGPINPAD");		
   printf("\n0x7F02 - PWINFO_PPCOMMPORT");		
   printf("\n0x7F04 - PWINFO_IDLEPROCTIME");
   printf("\nCódigo = ");
   scanf("%hx", &iParam);

   // Executa a operação
   iRet = gstHwFuncs.pPW_iGetResult( iParam, szAux, sizeof(szAux));
   PrintReturnDescription(iRet, NULL);

   __fpurge(stdin);
   printf ("\n <tecle algo>\n\n");
   getchar();
}

/*=====================================================================================*\
 Funcao     :  Confirmation

 Descricao  :  Esta função captura os dados necesários e executa PW_iConfirmation.
 
 Entradas   :  nao ha.

 Saidas     :  nao ha.
 
 Retorno    :  nao ha.
\*=====================================================================================*/
static void Confirmation()
{
   Int16 iOpc=0, iRet=0;
   Uint32 ulStatus=0;
   char  szAux[129];
   
   printf("\n1 - PWCNF_CNF_AUT");	    
   printf("\n2 - PWCNF_CNF_MANU_AUT");	 
   printf("\n3 - PWCNF_REV_MANU_AUT");	 
   printf("\n4 - PWCNF_REV_PRN_AU");
   printf("\n5 - PWCNF_REV_DISP_AUT");
   printf("\n6 - PWCNF_REV_COMM_AUT");
   printf("\n7 - PWCNF_REV_ABORT");	 
   printf("\n8 - PWCNF_REV_OTHER_AUT");
   printf("\n9 - PWCNF_REV_PWR_AUT");
   printf("\n10 -PWCNF_REV_FISC_AUT");

   printf ("\n SELECIONE A OPCAO:");

   scanf("%hd", &iOpc);

   switch(iOpc)
   {
      case(1): 
         ulStatus = PWCNF_CNF_AUTO;
         break;

      case(2): 
         ulStatus = PWCNF_CNF_MANU_AUT;
         break;
      
      case(3): 
         ulStatus = PWCNF_REV_MANU_AUT;
         break;
      
      case(4): 
         ulStatus = PWCNF_REV_DISP_AUT;
         break;
      
      case(5): 
         ulStatus = PWCNF_REV_DISP_AUT;
         break;

      case(6): 
         ulStatus = PWCNF_REV_COMM_AUT;
         break;

      case(7): 
         ulStatus = PWCNF_REV_ABORT;
         break;
         
      case(8): 
         ulStatus = PWCNF_REV_OTHER_AUT;
         break;
         
      case(9): 
         ulStatus = PWCNF_REV_PWR_AUT;
         break;
      
      case(10): 
         ulStatus = PWCNF_REV_FISC_AUT;
         break;
   }

   // Pergunta ao usuário se ele deseja utilizar as informações armazenadas da ultima 
   // transação ou se deseja inserir manualmente as informações de uma transação qualquer
   // a ser confirmada
   printf ("\n (0) UTILIZAR INFORMACOES DA ULTIMA TRANSACAO PARA A CONFIRMACAO:");
   printf ("\n (1) CAPTURAR AS INFORMACOES PARA A CONFIRMACAO:");

   printf ("\n SELECIONE A OPCAO:");
   scanf("%hd", &iOpc);

   // Caso seja necessário capturar as informações da transação do usuário
   if(iOpc)
   {
      printf("\nDigite o valor de PWINFO_REQNUM (0(zero) para parametro ausente): ");
      scanf(" %[^\n]",szAux);
      if( atoi(szAux) == 0)
         memset( gstConfirmData.szReqNum, 0, sizeof(gstConfirmData.szReqNum));
      else
         strcpy(gstConfirmData.szReqNum, szAux);

      printf("\nDigite o valor de PWINFO_AUTLOCREF (0(zero) para parametro ausente): ");
      scanf(" %[^\n]",szAux);
      if( atoi(szAux) == 0)
         memset( gstConfirmData.szLocRef, 0, sizeof(gstConfirmData.szLocRef));
      else
         strcpy(gstConfirmData.szLocRef, szAux);

      printf("\nDigite o valor de PWINFO_AUTEXTREF (0(zero) para parametro ausente): ");
      scanf(" %[^\n]",szAux);
      if( atoi(szAux) == 0)
         memset( gstConfirmData.szHostRef, 0, sizeof(gstConfirmData.szHostRef));
      else
         strcpy(gstConfirmData.szHostRef, szAux);

      printf("\nDigite o valor de PWINFO_VIRTMERCH: ");
      scanf(" %[^\n]",szAux);
      if( atoi(szAux) == 0)
         memset( gstConfirmData.szVirtMerch, 0, sizeof(gstConfirmData.szVirtMerch));
      else
         strcpy(gstConfirmData.szVirtMerch, szAux);

      printf("\nDigite o valor de PWINFO_AUTHSYST (0(zero) para parametro ausente): ");
      scanf(" %[^\n]",szAux);
      if( !strcmp(szAux, "0"))
         memset( gstConfirmData.szAuthSyst, 0, sizeof(gstConfirmData.szAuthSyst));
      else
         strcpy(gstConfirmData.szAuthSyst, szAux);
   }

   printf("\n\nPROCESSANDO...\n");
   iRet = gstHwFuncs.pPW_iConfirmation(ulStatus, gstConfirmData.szReqNum, 
      gstConfirmData.szLocRef, gstConfirmData.szHostRef, gstConfirmData.szVirtMerch, 
      gstConfirmData.szAuthSyst);
   PrintReturnDescription(iRet, NULL);

   // Zera a estrutura que armazena informações para confirmação da transação
   memset( &gstConfirmData, 0, sizeof(gstConfirmData));  
}

/*=====================================================================================*\
 Funcao     :  IdleProc

 Descricao  :  Esta função executa PW_iIdleProc.
 
 Entradas   :  nao ha.

 Saidas     :  nao ha.
 
 Retorno    :  nao ha.
\*=====================================================================================*/
static void IdleProc()
{
   Int16 iRet=0;
   
   iRet = gstHwFuncs.pPW_iIdleProc();
   PrintReturnDescription(iRet, NULL);
}

/*=====================================================================================*\
 Funcao     :  PPGetCard

 Descricao  :  Esta função executa PW_iPPGetCard.
 
 Entradas   :  nao ha.

 Saidas     :  nao ha.
 
 Retorno    :  nao ha.
\*=====================================================================================*/
static void PPGetCard()
{
   Int16 iRet;
   char szDspMsg[128];
   Uint16 uiIndex=0;

   // Obtém o índice da captura, parâmetro obrigatório
   printf("\nIndice da captura = ");
   scanf("%hu", &uiIndex);

   // Executa a operação
   iRet = gstHwFuncs.pPW_iPPGetCard(uiIndex);
   PrintReturnDescription(iRet, szDspMsg);
   if(iRet)
      return;

   // Caso a operação tenha sido executada com sucesso, inicia o loop e trata os
   // retornos possíveis
   if(iRet == PWRET_OK)
   {
      printf("\nIniciando EventLoop...");
      do
      {
         iRet = gstHwFuncs.pPW_iPPEventLoop(szDspMsg, sizeof(szDspMsg));
         PrintReturnDescription(iRet, szDspMsg);
         if(iRet!=PWRET_OK && iRet!=PWRET_DISPLAY && iRet!=PWRET_NOTHING)
            return;
         usleep(1000*500);
      } while(iRet!=PWRET_OK);
   }
}

/*=====================================================================================*\
 Funcao     :  PPGetPIN

 Descricao  :  Esta função executa PW_iPPGetPIN.
 
 Entradas   :  nao ha.

 Saidas     :  nao ha.
 
 Retorno    :  nao ha.
\*=====================================================================================*/
static void PPGetPIN()
{
   Int16 iRet;
   char szDspMsg[128];
   Uint16 uiIndex=0;

   // Obtém o índice da captura, parâmetro obrigatório
   printf("\nIndice da captura = ");
   scanf("%hu", &uiIndex);

   // Executa a operação
   iRet = gstHwFuncs.pPW_iPPGetPIN(uiIndex);
   PrintReturnDescription(iRet, szDspMsg);
   if(iRet)
      return;

   // Caso a operação tenha sido executada com sucesso, inicia o loop e trata os
   // retornos possíveis
   if(iRet == PWRET_OK)
   {

      printf("\nIniciando EventLoop...");
      do
      {
         iRet = gstHwFuncs.pPW_iPPEventLoop(szDspMsg, sizeof(szDspMsg));
         PrintReturnDescription(iRet, szDspMsg);
         if(iRet!=PWRET_OK && iRet!=PWRET_DISPLAY && iRet!=PWRET_NOTHING)
            return;
         usleep(1000*500);
      }while(iRet!=PWRET_OK); 
   }
}

/*=====================================================================================*\
 Funcao     :  PPGetData

 Descricao  :  Esta função executa PW_iPPGetData.
 
 Entradas   :  nao ha.

 Saidas     :  nao ha.
 
 Retorno    :  nao ha.
\*=====================================================================================*/
static void PPGetData()
{
   Int16 iRet;
   char szDspMsg[128];
   Uint16 uiIndex=0;

   // Obtém o índice da captura, parâmetro obrigatório
   printf("\nIndice da captura = ");
   scanf("%hu", &uiIndex);

   // Executa a operação
   iRet = gstHwFuncs.pPW_iPPGetData(uiIndex);
   PrintReturnDescription(iRet, szDspMsg);
   if(iRet)
      return;

   // Caso a operação tenha sido executada com sucesso, inicia o loop e trata os
   // retornos possíveis
   if(iRet == PWRET_OK)
   {

      printf("\nIniciando EventLoop...");
      do
      {
         iRet =gstHwFuncs.pPW_iPPEventLoop(szDspMsg, sizeof(szDspMsg));
         PrintReturnDescription(iRet, szDspMsg);
         if(iRet!=PWRET_OK && iRet!=PWRET_DISPLAY && iRet!=PWRET_NOTHING)
            return;
         usleep(1000*500);
      } while(iRet!=PWRET_OK);
   }
}

/*=====================================================================================*\
 Funcao     :  PPGoOnChip

 Descricao  :  Esta função executa PW_iPPGoOnChip.
 
 Entradas   :  nao ha.

 Saidas     :  nao ha.
 
 Retorno    :  nao ha.
\*=====================================================================================*/
static void PPGoOnChip()
{
   Int16 iRet;
   char szDspMsg[128];
   Uint16 uiIndex=0;

   // Obtém o índice da captura, parâmetro obrigatório
   printf("\nIndice da captura = ");
   scanf("%hu", &uiIndex);

   // Executa a operação
   iRet = gstHwFuncs.pPW_iPPGoOnChip(uiIndex);
   PrintReturnDescription(iRet, szDspMsg);
   if(iRet)
      return;

   // Caso a operação tenha sido executada com sucesso, inicia o loop e trata os
   // retornos possíveis
   if(iRet == PWRET_OK)
   {

      printf("\nIniciando EventLoop...");
      do
      {
         iRet =gstHwFuncs.pPW_iPPEventLoop(szDspMsg, sizeof(szDspMsg));
         PrintReturnDescription(iRet, szDspMsg);
         if(iRet!=PWRET_OK && iRet!=PWRET_DISPLAY && iRet!=PWRET_NOTHING)
            return;
         usleep(1000*500);
      } while(iRet!=PWRET_OK);
   }
}

/*=====================================================================================*\
 Funcao     :  PPFinishChip

 Descricao  :  Esta função executa PW_iPPFinishChip.
 
 Entradas   :  nao ha.

 Saidas     :  nao ha.
 
 Retorno    :  nao ha.
\*=====================================================================================*/
static void PPFinishChip()
{
   Int16 iRet;
   char szDspMsg[128];
   Uint16 uiIndex=0;

   // Obtém o índice da captura, parâmetro obrigatório
   printf("\nIndice da captura = ");
   scanf("%hu", &uiIndex);

   // Executa a operação
   iRet = gstHwFuncs.pPW_iPPFinishChip(uiIndex);
   PrintReturnDescription(iRet, szDspMsg);
   if(iRet)
      return;

   // Caso a operação tenha sido executada com sucesso, inicia o loop e trata os
   // retornos possíveis
   if(iRet == PWRET_OK)
   {

      printf("\nIniciando EventLoop...");
      do
      {
         iRet =gstHwFuncs.pPW_iPPEventLoop(szDspMsg, sizeof(szDspMsg));
         PrintReturnDescription(iRet, szDspMsg);
         if(iRet!=PWRET_OK && iRet!=PWRET_DISPLAY && iRet!=PWRET_NOTHING)
            return;
         usleep(1000*500);
      } while(iRet!=PWRET_OK);
   }
}

/*=====================================================================================*\
 Funcao     :  PPConfirmData

 Descricao  :  Esta função executa PW_iPPConfirmData.
 
 Entradas   :  nao ha.

 Saidas     :  nao ha.
 
 Retorno    :  nao ha.
\*=====================================================================================*/
static void PPConfirmData()
{
   Int16 iRet;
   char szDspMsg[128];
   Uint16 uiIndex=0;

   // Obtém o índice da captura, parâmetro obrigatório
   printf("\nIndice da captura = ");
   scanf("%hu", &uiIndex);

   // Executa a operação
   iRet = gstHwFuncs.pPW_iPPConfirmData(uiIndex);
   PrintReturnDescription(iRet, szDspMsg);
   if(iRet)
      return;

   // Caso a operação tenha sido executada com sucesso, inicia o loop e trata os
   // retornos possíveis
   if(iRet == PWRET_OK)
   {

      printf("\nIniciando EventLoop...");
      do
      {
         iRet =gstHwFuncs.pPW_iPPEventLoop(szDspMsg, sizeof(szDspMsg));
         PrintReturnDescription(iRet, szDspMsg);
         if(iRet!=PWRET_OK && iRet!=PWRET_DISPLAY && iRet!=PWRET_NOTHING)
            return;
         usleep(1000*500);
      } while(iRet!=PWRET_OK);
   }
}

/*=====================================================================================*\
 Funcao     :  PPRemoveCard

 Descricao  :  Esta função executa PW_iPPRemoveCard.
 
 Entradas   :  nao ha.

 Saidas     :  nao ha.
 
 Retorno    :  nao ha.
\*=====================================================================================*/
static void PPRemoveCard()
{
   Int16 iRet;
   char szDspMsg[128];

   // Executa a operação
   iRet = gstHwFuncs.pPW_iPPRemoveCard();
   PrintReturnDescription(iRet, szDspMsg);
   if(iRet)
      return;

   // Caso a operação tenha sido executada com sucesso, inicia o loop e trata os
   // retornos possíveis
   if(iRet == PWRET_OK)
   {

      printf("\nIniciando EventLoop...");
      do
      {
         iRet =gstHwFuncs.pPW_iPPEventLoop(szDspMsg, sizeof(szDspMsg));
         PrintReturnDescription(iRet, szDspMsg);
         if(iRet!=PWRET_OK && iRet!=PWRET_DISPLAY && iRet!=PWRET_NOTHING)
            return;
         usleep(1000*500);
      } while(iRet!=PWRET_OK);
   }
}

/*=====================================================================================*\
 Funcao     :  PPDisplay

 Descricao  :  Esta função executa PW_iPPDisplay.
 
 Entradas   :  nao ha.

 Saidas     :  nao ha.
 
 Retorno    :  nao ha.
\*=====================================================================================*/
static void PPDisplay()
{
   Int16 iRet;
   char szDspMsg[128];
   char szAux[40];

   // Obtém a mensagem para exibição
   printf("\nDigite a mensagem a ser exibida no PIN-pad:");
   scanf(" %[^\n]",szAux);

   // Executa a operação
   iRet = gstHwFuncs.pPW_iPPDisplay(szAux);
   PrintReturnDescription(iRet, szDspMsg);
   if(iRet)
      return;

   // Caso a operação tenha sido executada com sucesso, inicia o loop e trata os
   // retornos possíveis
   if(iRet == PWRET_OK)
   {

      printf("\nIniciando EventLoop...");
      do
      {
         iRet =gstHwFuncs.pPW_iPPEventLoop(szDspMsg, sizeof(szDspMsg));
         PrintReturnDescription(iRet, szDspMsg);
         if(iRet!=PWRET_OK && iRet!=PWRET_DISPLAY && iRet!=PWRET_NOTHING)
            return;
         usleep(1000*100);
      } while(iRet!=PWRET_OK);
   }
}

/*=====================================================================================*\
 Funcao     :  PPWaitEvent

 Descricao  :  Esta função executa PW_iPPWaitEvent.
 
 Entradas   :  nao ha.

 Saidas     :  nao ha.
 
 Retorno    :  nao ha.
\*=====================================================================================*/
static void PPWaitEvent()
{
   Int16 iRet;
   char szDspMsg[128];
   Uint32 ulEvent=0;

   // Executa a operação
   iRet = gstHwFuncs.pPW_iPPWaitEvent(&ulEvent);
   PrintReturnDescription(iRet, szDspMsg);
   if(iRet)
      return;

   // Caso a operação tenha sido executada com sucesso, inicia o loop e trata os
   // retornos possíveis
   if(iRet == PWRET_OK)
   {

      printf("\nIniciando EventLoop...");
      do
      {
         iRet =gstHwFuncs.pPW_iPPEventLoop(szDspMsg, sizeof(szDspMsg));
         PrintReturnDescription(iRet, szDspMsg);
         if(iRet!=PWRET_OK && iRet!=PWRET_DISPLAY && iRet!=PWRET_NOTHING)
            return;
         usleep(1000*500);
      } while(iRet!=PWRET_OK);

      switch(ulEvent)
      {
         case(PWPPEVT_MAGSTRIPE):
            printf("\n\nEVENTO = PWPPEVT_MAGSTRIPE");
            break;

         case(PWPPEVT_ICC):
            printf("\n\nEVENTO = PWPPEVT_ICC");
            break;

         case(PWPPEVT_KEYCONF):
            printf("\n\nEVENTO = PWPPEVT_KEYCONF");
            break;

         case(PWPPEVT_KEYBACKSP):
            printf("\n\nEVENTO = PWPPEVT_KEYBACKSP");
            break;

         case(PWPPEVT_KEYCANC):
            printf("\n\nEVENTO = PWPPEVT_KEYCANC");
            break;

         case(PWPPEVT_KEYF1):
            printf("\n\nEVENTO = PWPPEVT_KEYF1");
            break;

         case(PWPPEVT_KEYF2):
            printf("\n\nEVENTO = PWPPEVT_KEYF2");
            break;

         case(PWPPEVT_KEYF3):
            printf("\n\nEVENTO = PWPPEVT_KEYF3");
            break;

         case(PWPPEVT_KEYF4):
            printf("\n\nEVENTO = PWPPEVT_KEYF4");
            break;
      }
   }
}
  
/*=====================================================================================*\
 Funcao     :  PPGenericCmd

 Descricao  :  Esta função executa PPGenericCmd.
 
 Entradas   :  nao ha.

 Saidas     :  nao ha.
 
 Retorno    :  nao ha.
\*=====================================================================================*/
static void PPGenericCmd ()
{
   Int16 iRet;
   char szDspMsg[128];
   Uint16 uiIndex=0;


   // Obtém o índice da captura, parâmetro obrigatório
   printf("\nIndice da captura = ");
   scanf("%hu", &uiIndex);

   // Executa a operação
   iRet = gstHwFuncs.pPW_iPPGenericCMD (uiIndex);
   PrintReturnDescription (iRet, szDspMsg);
   if (iRet) {
      return;
   }

   // Caso a operação tenha sido executada com sucesso, inicia o loop e trata os
   // retornos possíveis
   printf ("\nIniciando EventLoop...");
   do 
   {
      iRet = gstHwFuncs.pPW_iPPEventLoop (szDspMsg, sizeof (szDspMsg));
      PrintReturnDescription (iRet, szDspMsg);
      if (iRet != PWRET_OK && iRet != PWRET_DISPLAY && iRet != PWRET_NOTHING) {
         return;
      }

      usleep (1000 * 500);
   } while (iRet != PWRET_OK); 
}

/*=====================================================================================*\
 Funcao     :  TesteInstalacao

 Descricao  :  Esta função inicia uma transação de instalação através de PW_iNewTransac,
               adiciona os parâmetros obrigatórios através de PW_iAddParam e em seguida 
               se comporta de forma idêntica a ExecTransac.
 
 Entradas   :  nao ha.

 Saidas     :  nao ha.
 
 Retorno    :  nao ha.
\*=====================================================================================*/
static void TesteInstalacao()
{
   PW_GetData vstParam[10];
   Int16   iNumParam = 10, iRet;

   // Inicializa a transação de instalação
   iRet = gstHwFuncs.pPW_iNewTransac(PWOPER_INSTALL);
   if( iRet)
      printf("\nErro PW_iNewTransac <%d>", iRet);

   // Adiciona os parâmetros obrigatórios
   AddMandatoryParams();
   
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
}

/*=====================================================================================*\
 Funcao     :  TesteRecarga

 Descricao  :  Esta função inicia uma transação de recarga através de PW_iNewTransac,
               adiciona os parâmetros obrigatórios através de PW_iAddParam e em seguida 
               se comporta de forma idêntica a ExecTransac.
 
 Entradas   :  nao ha.

 Saidas     :  nao ha.
 
 Retorno    :  nao ha.
\*=====================================================================================*/
static void TesteRecarga()
{
   PW_GetData vstParam[10];
   Int16   iNumParam = 10, iRet;

   // Inicializa a transação de instalação
   iRet = gstHwFuncs.pPW_iNewTransac(PWOPER_PREPAID);
   if( iRet)
      printf("\nErro PW_iNewTransac <%d>", iRet);

   // Adiciona os parâmetros obrigatórios
   AddMandatoryParams();
   
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
}

/*=====================================================================================*\
 Funcao     :  TesteVenda

 Descricao  :  Esta função inicia uma transação de venda através de PW_iNewTransac,
               adiciona os parâmetros obrigatórios através de PW_iAddParam e em seguida 
               se comporta de forma idêntica a ExecTransac.
 
 Entradas   :  nao ha.

 Saidas     :  nao ha.
 
 Retorno    :  nao ha.
\*=====================================================================================*/
static void TesteVenda()
{
   PW_GetData vstParam[10];
   Int16   iNumParam = 10, iRet;

   /// Inicializa a transação de venda
   iRet = gstHwFuncs.pPW_iNewTransac(PWOPER_SALE);
   if( iRet)
      printf("\nErro PW_iNewTransacr <%d>", iRet);

   // Adiciona os parâmetros obrigatórios
   AddMandatoryParams();
   
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
static void TesteAdmin()
{
   PW_GetData vstParam[10];
   Int16   iNumParam = 10, iRet;

   /// Inicializa a transação de instalação
   iRet = gstHwFuncs.pPW_iNewTransac(PWOPER_ADMIN);
   if( iRet)
      printf("\nErro PW_iNewTransac <%d>", iRet);

   // Adiciona os parâmetros obrigatórios
   AddMandatoryParams();
   
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

/*=====================================================================================*\
 Funcao     :  iTestLoop

 Descricao  :  Esta função oferece ao usuário um menu com todas as operações possíveis e 
               captura a operação desejada pelo usuário, executando-a. Este loop só para
               se o usuário selecionar a opção SAIR.
 
 Entradas   :  nao ha.

 Saidas     :  nao ha.
 
 Retorno    :  nao ha.
\*=====================================================================================*/
static void iTestLoop (void)
{
   Int16   iKey;

   for(;;)
   {
      // Exibe as opções
      printf ("\n===================");
      printf ("\nFUNCOES");
      printf ("\n===================");
      printf("\n0 - SAIR");
      printf("\n1 - PW_iInit");
      printf("\n2 - PW_iNewTransac");
      printf("\n3 - PW_iAddParam");
      printf("\n4 - PW_iExecTransac");
      printf("\n5 - PW_iGetResult");
      printf("\n6 - PW_iConfirmation");
      printf("\n7 - PW_iIdleProc");
      printf("\n8 - PW_iPPGetCard");  
      printf("\n9 - PW_iPPGetPIN");   
      printf("\na - PW_iPPGetData"); 
      printf("\nb - PW_iPPGoOnChip");
      printf("\nc - PW_iPPFinishChip");
      printf("\nd - PW_iPPConfirmData");
      printf("\ne - PW_iPPRemoveCard");
      printf("\nf - PW_iPPDisplay");
      printf("\ng - PW_iPPWaitEvent");
      printf("\nh - PW_iPPGenericCMD");

      printf("\nv - Teste autoatendimento");
      printf("\nx - Teste instalacao");
      printf("\ny - Teste recarga");
      printf("\nz - Teste venda");
      printf("\nw - Teste admin");

      

      printf ("\n\nESCOLHA A FUNCAO: "); 

      __fpurge(stdin);
      // Verifica se foi selecionada uma opção válida
      do {
         iKey = getchar ();
      } while (iKey != '0' && iKey != '1' && iKey != '2' && iKey != '3' && iKey != '4' && iKey != '5' &&
               iKey != '6' && iKey != '7' && iKey != '8' && iKey != '9' && iKey != 'a' && iKey != 'b' &&
               iKey != 'c' && iKey != 'd' && iKey != 'e' && iKey != 'f' && iKey != 'g' && iKey != 'h' && 
               iKey != 'x' && iKey != 'y' && iKey != 'z' && iKey != 'w' && iKey != 'v');
      printf ("%c\n", iKey);
   
      // Executa a operação selecionada pelo usuário
      switch( iKey)
      {
         case('1'):    
            Init();
            break;
         case('2'):    
            NewTransac();
            break;
         case('3'):
            AddParam();
            break;
         case('4'):
            ExecTransac();
            break;
         case('5'):    
            GetResult();
            break;
         case('6'):    
            Confirmation();
            break;
         case('7'):    
            IdleProc();
            break;
         case('8'):    
            PPGetCard();
            break;
         case('9'):    
            PPGetPIN();
            break;
         case('a'):    
            PPGetData();
            break;
         case('b'):    
            PPGoOnChip();
            break;
         case('c'):    
            PPFinishChip();
            break;
         case('d'):  
            PPConfirmData();     
            break;
         case('e'):  
            PPRemoveCard();     
            break;
         case('f'):  
            PPDisplay();     
            break;
         case('g'):  
            PPWaitEvent();     
            break;
         case('h'):  
            PPGenericCmd();     
            break;

         case('x'):
            TesteInstalacao();        
            break;
         case('y'):
            TesteRecarga();        
            break;
         case('z'):
            TesteVenda();
            break;
         case('w'):
            TesteAdmin();
            break;


         case('v'):
            gfAutoAtendimento = TRUE;

            TesteAA();

            gfAutoAtendimento = FALSE;
            break;

         default:       
            return;
            break;        
      }
   }
}

/******************************************/
/* FUNÇÃO DE ENTRADA DO APLICATIVO        */
/******************************************/
int main(int argc, char* argv[])
{
   printf ("\n\n");
   printf ("\n========================================");
   printf ("\nPGWebLibTest v%s", PGWEBLIBTEST_VERSION);
   printf ("\nPrograma de testes da biblioteca");
   printf ("\nPay&Go WEB - DLL de integracao");
   printf ("\n========================================");
   printf ("\n");

   // Tenta carregar a DLL que deve estar na mesma pasta do executável deste aplicativo
   ghHwLib = dlopen("./PGWebLib.so", RTLD_LAZY);

   // Caso não consiga carregar a DLL retorna erro
   if( ghHwLib == NULL)
   {
      printf ("\n\nNao foi possivel carregar PGWebLib.so\n%s\n\n", dlerror());
   }
   else
   {
      // Carrega todas as funções exportadas pela DLL para uso no aplicativo
      gstHwFuncs.pPW_iInit          = dlsym  (ghHwLib, "PW_iInit");
      if( gstHwFuncs.pPW_iInit == NULL)
         printf ("\n\nNao foi possivel carregar PW_iInit\n\n");
      gstHwFuncs.pPW_iNewTransac    = dlsym  (ghHwLib, "PW_iNewTransac");
      if( gstHwFuncs.pPW_iNewTransac == NULL)
         printf ("\n\nNao foi possivel carregar PW_iNewTransac\n\n");
      gstHwFuncs.pPW_iAddParam      = dlsym  (ghHwLib, "PW_iAddParam");
      if( gstHwFuncs.pPW_iAddParam == NULL)
         printf ("\n\nNao foi possivel carregar PW_iAddParam\n\n");
      gstHwFuncs.pPW_iExecTransac   = dlsym  (ghHwLib, "PW_iExecTransac");
      if( gstHwFuncs.pPW_iExecTransac == NULL)
         printf ("\n\nNao foi possivel carregar PW_iExecTransac\n\n");
      gstHwFuncs.pPW_iGetResult     = dlsym  (ghHwLib, "PW_iGetResult");
      if( gstHwFuncs.pPW_iGetResult == NULL)
         printf ("\n\nNao foi possivel carregar PW_iGetResult\n\n");
      gstHwFuncs.pPW_iConfirmation  = dlsym  (ghHwLib, "PW_iConfirmation");
      if( gstHwFuncs.pPW_iConfirmation == NULL)
         printf ("\n\nNao foi possivel carregar PW_iConfirmation\n\n");
      gstHwFuncs.pPW_iIdleProc      = dlsym  (ghHwLib, "PW_iIdleProc");
      if( gstHwFuncs.pPW_iIdleProc == NULL)
         printf ("\n\nNao foi possivel carregar PW_iIdleProc\n\n");
      gstHwFuncs.pPW_iPPAbort       = dlsym  (ghHwLib, "PW_iPPAbort");
      if( gstHwFuncs.pPW_iPPAbort == NULL)
         printf ("\n\nNao foi possivel carregar PW_iPPAbort\n\n");
      gstHwFuncs.pPW_iPPEventLoop   = dlsym  (ghHwLib, "PW_iPPEventLoop");
      if( gstHwFuncs.pPW_iPPEventLoop == NULL)
         printf ("\n\nNao foi possivel carregar PW_iPPEventLoop\n\n");
      gstHwFuncs.pPW_iPPGetCard     = dlsym  (ghHwLib, "PW_iPPGetCard");
      if( gstHwFuncs.pPW_iPPGetCard == NULL)
         printf ("\n\nNao foi possivel carregar PW_iPPGetCard\n\n");
      gstHwFuncs.pPW_iPPGetPIN      = dlsym  (ghHwLib, "PW_iPPGetPIN");
      if( gstHwFuncs.pPW_iPPGetPIN == NULL)
         printf ("\n\nNao foi possivel carregar PW_iPPGetPIN\n\n");
      gstHwFuncs.pPW_iPPGetData     = dlsym  (ghHwLib, "PW_iPPGetData");
      if( gstHwFuncs.pPW_iPPGetData == NULL)
         printf ("\n\nNao foi possivel carregar PW_iPPGetData\n\n");
      gstHwFuncs.pPW_iPPGoOnChip    = dlsym  (ghHwLib, "PW_iPPGoOnChip");
      if( gstHwFuncs.pPW_iPPGoOnChip == NULL)
         printf ("\n\nNao foi possivel carregar PW_iPPGoOnChip\n\n");
      gstHwFuncs.pPW_iPPFinishChip  = dlsym  (ghHwLib, "PW_iPPFinishChip");
      if( gstHwFuncs.pPW_iPPFinishChip == NULL)
         printf ("\n\nNao foi possivel carregar PW_iPPFinishChip\n\n");
      gstHwFuncs.pPW_iPPConfirmData = dlsym  (ghHwLib, "PW_iPPConfirmData");
      if( gstHwFuncs.pPW_iPPConfirmData == NULL)
         printf ("\n\nNao foi possivel carregar PW_iPPConfirmData\n\n");
      gstHwFuncs.pPW_iPPRemoveCard  = dlsym  (ghHwLib, "PW_iPPRemoveCard");
      if( gstHwFuncs.pPW_iPPRemoveCard == NULL)
         printf ("\n\nNao foi possivel carregar PW_iPPRemoveCard\n\n");
      gstHwFuncs.pPW_iPPDisplay     = dlsym  (ghHwLib, "PW_iPPDisplay");
      if( gstHwFuncs.pPW_iPPDisplay == NULL)
         printf ("\n\nNao foi possivel carregar PW_iPPDisplay\n\n");
      gstHwFuncs.pPW_iPPWaitEvent   = dlsym  (ghHwLib, "PW_iPPWaitEvent");
      if( gstHwFuncs.pPW_iPPWaitEvent == NULL)
         printf ("\n\nNao foi possivel carregar PW_iPPWaitEvent\n\n");
      gstHwFuncs.pPW_iPPGenericCMD  = dlsym  (ghHwLib, "PW_iPPGenericCMD");
      if (gstHwFuncs.pPW_iPPGenericCMD == NULL)
         printf ("\n\nNao foi possivel carregar PW_iPPGenericCMD\n\n");

      // Inicia o Loop oferecendo as opções possíveis e aguardando o usuário selecionar
      iTestLoop ();

      // Libera a memória alocada pela biblioteca
      dlclose (ghHwLib);
   }

   __fpurge(stdin);
   printf ("\n\nPROGRAMA FINALIZADO\n   <tecle algo>\n\n");
   getchar();

   return 0;
}