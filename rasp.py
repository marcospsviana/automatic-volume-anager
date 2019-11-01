# -*- coding: utf-8 -*-


from flask import Flask, render_template, url_for, request, redirect, flash
import sys
import os
import json
import string
import datetime
from controllers import Management
from engine.forms import FormTempo, CadArmario, RecuperarBagagem
#from engine.cobranca import Cobranca as cb
#from engine.locacao import Locacao as loc
#from engine.usuario import User as usr
from engine.armario import Armario as arm



app = Flask(__name__)
app.config[
    'SECRET_KEY'] = b"y\x84\x7f\xc0<\x15\xb6z\xdbv\xcaG\xa7\xc5\x9cf\xadYr\xfa) =\xac\x1f\xcd\xea\xf8%\xd9\xda=\xdb\x03\xbc\x16\x92\xe5\x1eh\xc2\xe4\xc0\x85xz\xb47{\xa6{\xfa\xed\x97\xeeN\xf2\xc7!\xe6'\x94d\x8e\xd4\x886\xe3\xb5\xe2#a\xfb\x1b\xcauh\x0f\xf6\xbf\x0f**h\x98iM\xe8\xe6\xb5s<\x82\x15D/(\xc4\xd0\xd8\xa9N&a\x02\xe4\x90\xbf\x93-\xa5B \xf9c\xd1T\x9e}\xad\xcd\xf8>\xbaa\x86\xf5^\xafVA\x00Ef\xf5\xfc\xae\x11U\xe0N\xb2\xddJ\xf5\x88\xad.\xac\xc3@3\xc7`\xbf\x11\x84\xadR&<b\xaa\x00c\x90\xb8P\x89\xd7\x10z\x80`H\xc3\x06G\xdc\x89\x06i\x19\x98\xaa\xadA\x89o\xd2T.Q\x9b\xf1d\xa2\xb8+\xb0\x9ec\xa6\xb8{\x88\x04C\x86\xe8\xb2>\xae`\x8b!b=\x9c\x0f\x1c\xb8x\xf9\xdf\x1b\xe9>\xbeu\xb6\xfe\xa2\xa8\xa9\x87.\x8b\xcaYM\x0b[C\xe5\xd5\xdd\xfd \xed&\xa6%A\x94a"
manager = Management()

@app.route('/')
def index(methods=['GET', 'POST']):
    return render_template('index.html')


@app.route('/frances')
def frances():
    return ('e')


@app.route('/espanhol')
def espanhol():
    return ('e')


@app.route('/ingles')
def ingles():
    return ('e')


@app.route('/locar')
def locar():
    return render_template('locar.html')


@app.route('/armarios', methods=['GET', 'POST'])
def armarios():
    manager = Management()
    armario = ''
    classes = ''
    classes = manager.lista_armarios()
    print(classes)
    if request.method == 'POST':
        armario = request.form.get('armario')
        print(armario)
    return render_template('armarios.html', armario = armario, classes= classes)


@app.route('/tempo', methods=['GET', 'POST'])
def tempo():    
    form = FormTempo(request.form)
    manager = Management()
    dia = dias = hora = horas = minuto = minutos = total = ''
    nome = ''
    email = ''
    telefone = ''
    result = ''
    armario = ''
    
    armario = request.args.get('armario')

    if request.method == "POST":
        
        dia = request.form.get('dia')
        hora = request.form.get('hora')
        minuto = request.form.get('minuto')
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        #confirma = request.form.get('confirma')
        
        
        
        total = manager.calculo(dia, hora, minuto)
        #if confirma == 'sim':
        result = manager.locacao( nome, email, telefone, dia, hora, minuto, armario )
        return redirect(url_for('sucesso', dia=dia,  hora=hora, minuto=minuto, nome=nome, total=total, email=email, telefone=telefone, armario=armario, result=result))

        print('Nome: ' + nome)
        print('Total: ' + str(total))

    return render_template('tempo.html', form=form, dia=dia,  hora=hora, minuto=minuto, nome=nome, total=total, email=email, telefone=telefone, armario=armario, result=result)


@app.route('/cad_armario', methods=['GET', 'POST'])
def cad_armarios():
    
    form = CadArmario()
    message = ''
    if request.method == 'POST':
        classe = request.form.get('classe')
        nivel = request.form.get('nivel')
        coluna = request.form.get('coluna')
        terminal = request.form.get('terminal')
        manager.cad_armarios(classe, terminal, coluna, nivel)
        message = ('armário classe : %s , nível : %s, coluna : %s, terminal : %s, cadastrado com sucesso' % (
            classe, nivel, coluna, terminal))
    return render_template('cad_armario.html', form=form, flash=message)
m= 0

@app.route('/remove', methods=['GET', 'POST'])
def remove_armario():
    import time
    global m
    for i in range(0,60):
        i = datetime.datetime.now()
        i = i.second
        if i == 59:
            m = m + 1
        return'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="1">
    <title>Document</title>
</head>
<body>
    <h3>minutos %s segundos %s</h3>
</body>
</html>
'''%(m,i)
    if m == 1:
        return redirect('index.html')


@app.route('/pagamento', methods=['GET','POST'])
def pagamento():
    total = ''
    token = ''
    email_count = ''
    

    if request.method == 'GET':
        total = request.args.get('total')
        nome= request.args.get('nome')
        senha = request.args.get('senha')
        result = arm.finalizar( nome, senha)
        
    return render_template('finalizar.html', result=result)
    
       
        
   
   
        
    


    return render_template('pagamento.html', total= total, nome=nome, senha=senha, result=result, token=token, email_count=email_count)


@app.route('/sucesso', methods=['GET'])
def sucesso():
    nome = ''
    dia = ''
    hora = ''
    minuto = ''
    email = ''
    total = ''
    if request.method == 'GET':
        nome = request.args.get('nome')
        dia = request.args.get('dia')
        hora = request.args.get('hora')
        minuto = request.args.get('minuto')
        email = request.args.get('email')
        total = request.args.get('total')

    return render_template('sucesso.html', dia=dia, hora=hora, nome=nome, email=email, minuto=minuto, total= total)

@app.route('/resgatar_bagagem', methods=['GET', 'POST'])
def resgatar_bagagem():
    message = ''
    total = ''
    alfa = list(string.ascii_lowercase) # alfabeto para gerar o teclado
    
    result = ''
    num = list(map(lambda x: x, range(10))) # números para o teclado numérico
    form = RecuperarBagagem()
    if request.method == 'POST':
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        result = manager.liberar_armarios(senha, nome)
        if result != 'armario liberado':
            result = float(result)
        print('rasp result ---->', result)
        
        if result != 'armario liberado' :
            message = " há tempo excedente totalizando em: "
            return redirect(url_for('pagamento', total = result, nome=nome, senha=senha))

            
            
            
        else:
            manager.liberar_armarios(senha, nome)
            message = 'armario liberado'
            return message

    


    return render_template('resgatar_bagagem.html', form=form, alfa=alfa, num=num, result=result, message=message)



@app.route('/finalizar/<string:result>', methods=['GET', 'POST'])
def finalizar(result):
    
    nome = ''
    senha = ''
    total = ''
    result = ''
    if request.method == 'GET':
        result = request.args.get('result')

    
    return render_template('finalizar.html', result = result)
@app.route('/listagem')
def listagem():
    armario = ''
    data_limite = ''
    tempo_total = ''
    return "listagem"


if __name__ == '__main__':
    servidor = '10.15.1.175'
    app.run(host='localhost', port=5000, debug=True)
