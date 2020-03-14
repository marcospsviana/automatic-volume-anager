from comtele_sdk.textmessage_service import TextMessageService
import sys, os
import datetime
import json
from time import sleep
import smtplib
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import string
import subprocess
import random
import string
from random import choice, sample
import pandas as pd



class TransacsOps(object):
    def __init__(self, diretorio = os.getcwd()):
        self.diretorio = diretorio
    
    
    @classmethod
    def retorno_transacao(self):
        """ Esta função verifica o resultado da transação seja bem ou mal sucedida
        le o arquivo json que contem PWINFO_RESULTMSG a mensagem da transacao obtido da 
        biblioteca paygo 
        Entrada: Ausente 
        Retorno: type(json) PWINFO_RESULTMSG
        caso a transação não ocorra o arquivo é gravado com o valor da chave PWINFO_RESULTMSG str("SEM TRANSACAO")
        No caso de transacao efetuada é feita a leitura retorna PWINFO_RESULTMSG logo após é colocado um valor default
        para não interferir na proxima consulta, pois se na for setado a proxima consulta irá receber o valor de PWINFO_RESULTMSG
        da transacao anterior.
        """

        data = datetime.datetime.now()
        self.diretorio = os.getcwd()
        # LENDO O RETORNO DA TRANSACAO
        with open('%s/engine/paygoWeb/comprovantes/retornotransacao.json'%(self.diretorio), 'r') as f:
            self.resultado_transacao = json.load(f)
        sleep(0.2)

        # FIM DE LEITURA DE RETORNO

        #SETANDO RETORNO PARA NÃO FICAR COM O ÚLTIMO DADO DE TRANSAÇÃO PARA A PROXIMA CONSULTA
        retorno = open('%s/engine/paygoWeb/comprovantes/retornotransacao.json'%(self.diretorio), 'w+')
        retorno.write('\n{  \n')
        retorno.write('     "DATA" : "%s %s %s %s %s",\n'%(data.day, data.month, data.year, data.hour, data.minute))
        retorno.write('     "PWINFO_RESULTMSG" : "SEM TRANSACAO"')
        retorno.write('\n}  \n')
        retorno.close()
        print("self.resultado_transacao transacops", self.resultado_transacao)
        return self.resultado_transacao
    @classmethod
    def send_sms(self, nome, senha, compartimento, data_locacao, hora_inicio_locacao, data_limite,  hora_fim_locacao, telefone):
        __api_key = '664e67a9-5fdd-4718-9cc2-3bd2a54c9520'
        textmessage_service = TextMessageService(__api_key)
        message = """Senha %s para liberacao..\n 
                COMPARTIMENTO: %s\n
                DATA LOCAÇÃO: %s %s\n
                DATA LIMITE: %s %s\n
                Obrigado por utilizar nossos serviços Sr(a) %s.\n
                CoolbagSafe"""%( senha, compartimento,data_locacao, hora_inicio_locacao,data_limite, hora_fim_locacao, nome)
        result = textmessage_service.send('CoolbagSafe', message, [str(telefone)])
    
    @classmethod
    def send_email(self, nome, email, senha, compartimento, data_locacao, hora_inicio_locacao, data_limite,  hora_fim_locacao, language):
        # __server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        from smtplib import SMTP
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        RECIBO = ''
        diretorio = os.getcwd()
        comprovante_pagamento = open('%s/engine/paygoWeb/comprovantes/COMPROVANTE CLIENTE EMAIL.txt'%(diretorio),'r')
        for l in comprovante_pagamento:
            RECIBO += l + '<br>'
        comprovante_pagamento.close()
        
    
        msg = MIMEMultipart()
        __nome = string.capwords(nome)
        css= """<style type='text/css' >
            .flex-box {
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: flex-center;
            }
            .body{

            background: #FDCF03;
            }

            .message{
                position: absolute;
            }
            .pai{
                
                position: relative;
                text-align: center;
                margin-left: 40%;
                width: 300px;
                height: 500px;
                background: #ffffff;
                margin-bottom: 10px;
            }
            .filho{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                text-align: center;
            }

            </style>"""
        HTML_NOVO = """<!-- Emails use the XHTML Strict doctype -->
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "https://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="https://www.w3.org/1999/xhtml">
<head>
  <!-- The character set should be utf-8 -->
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <meta name="viewport" content="width=device-width"/>
  <!-- Link to the email's CSS, which will be inlined into the email -->
  <link rel="stylesheet" href="assets/css/foundation-emails.css">
  <style>
    <!-- Your CSS to inline should be added here -->
  </style>
</head>

<body>
  <!-- Wrapper for the body of the email -->
  <table class="body" data-made-with-foundation>
    <tr>
      <!-- The class, align, and <center> tag center the container -->
      <td class="float-center" align="center" valign="top">
        <center>
          <strong>Este e-mail foi enviado de forma automática ,não responda diretamente a este e-mail!</strong><br><br>
                    Obrigado por utilizar nossos serviços<b> %s</b>, abaixo encontra-se os seus dados de acesso para liberação do compartimento:<br><br>
                <p>COMPARTIMENTO: <b> %s  </b>
                <p>SENHA:<b> %s</b>
                <p>DATA LOCAÇÃO:<b> %s %s  </b>
                <p>DATA LIMITE:<b> %s %s</b>
        </center>
      </td>
    </tr>
  </table>
</body>
</html>"""
        if language == "pt_BR":
            __message = """<html><head> %s </head> 
            <body class='body'> 
            <div class='message'>
              <strong>Este e-mail foi enviado de forma automática ,não responda diretamente a este e-mail!</strong><br><br>
                    Obrigado por utilizar nossos serviços<b> %s</b>, abaixo encontra-se os seus dados de acesso para liberação do compartimento:<br><br>
                <p>COMPARTIMENTO: <b> %s  </b>
                <p>SENHA:<b> %s</b>
                <p>DATA LOCAÇÃO:<b> %s %s  </b>
                <p>DATA LIMITE:<b> %s %s</b>
            </div>
        <div class='flex-box pai'>
             <div class='filho'>%s</div>
        </div>
        </body></html>""" % (css, __nome, compartimento, senha, data_locacao, hora_inicio_locacao, data_limite, hora_fim_locacao, RECIBO)

        elif language == "en_US":
            __message = """<html><head> %s </head>
            <body class='body'> <div class='message'><strong>
        This email was sent automatically,please do not reply directly to this email! </strong><br><br>
        Thanks for using our services <b>%s</b>, below is your compartment release access details:<br><br>
        <p>COMPARTMENT: <b> %s  </b>
        <p>PASSWORD: <b> %s  </b>
        <p>DATE RENT: <b> %s %s  </b>
        <p>DEADLINE:  <b> %s %s </b><br>
        </div>
        <div class='flex-box pai'>
             <div class='filho'>%s</div>
        </div>
        
        </body></html>""" % (css, __nome, compartimento, senha, data_locacao, hora_inicio_locacao, data_limite, hora_fim_locacao, RECIBO)

       
        body = MIMEText(__message, 'html')
                    

       
        msg['Subject'] = 'CoolBag-SafeLocker - Credentials Access'
        msg.attach(body)

        msg['From'] = 'coolbagsafecustomer@gmail.com'
        msg['To'] = email
        password = "CBS@2020"
        __server = SMTP('smtp.gmail.com:587')
        __server.starttls()
        __server.ehlo()
        __server.login("coolbagsafecustomer@gmail.com", "CBS@2020")

        __server.sendmail( msg['From'], msg['To'].split(","), msg.as_string())

        __server.quit()
    
    