from flask import Flask, render_template, url_for, request, redirect, flash
import sys, os, json
import webview

from engine.forms import FormTempo

app = Flask(__name__)
app.config['SECRET_KEY'] = b"y\x84\x7f\xc0<\x15\xb6z\xdbv\xcaG\xa7\xc5\x9cf\xadYr\xfa) =\xac\x1f\xcd\xea\xf8%\xd9\xda=\xdb\x03\xbc\x16\x92\xe5\x1eh\xc2\xe4\xc0\x85xz\xb47{\xa6{\xfa\xed\x97\xeeN\xf2\xc7!\xe6'\x94d\x8e\xd4\x886\xe3\xb5\xe2#a\xfb\x1b\xcauh\x0f\xf6\xbf\x0f**h\x98iM\xe8\xe6\xb5s<\x82\x15D/(\xc4\xd0\xd8\xa9N&a\x02\xe4\x90\xbf\x93-\xa5B \xf9c\xd1T\x9e}\xad\xcd\xf8>\xbaa\x86\xf5^\xafVA\x00Ef\xf5\xfc\xae\x11U\xe0N\xb2\xddJ\xf5\x88\xad.\xac\xc3@3\xc7`\xbf\x11\x84\xadR&<b\xaa\x00c\x90\xb8P\x89\xd7\x10z\x80`H\xc3\x06G\xdc\x89\x06i\x19\x98\xaa\xadA\x89o\xd2T.Q\x9b\xf1d\xa2\xb8+\xb0\x9ec\xa6\xb8{\x88\x04C\x86\xe8\xb2>\xae`\x8b!b=\x9c\x0f\x1c\xb8x\xf9\xdf\x1b\xe9>\xbeu\xb6\xfe\xa2\xa8\xa9\x87.\x8b\xcaYM\x0b[C\xe5\xd5\xdd\xfd \xed&\xa6%A\x94a"

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

@app.route('/armarios', methods=['GET','POST'])
def armarios():
    return render_template('armarios.html')

@app.route('/tempo', methods=['GET','POST'])
def tempo():
    from engine.data import Banco
    b = Banco()
    form = FormTempo(request.form)
    import requests

    dia = dias = hora = horas = minuto = minutos = total = 0
    nome = ''
    email = ''
    telefone = ''
    
    
    
    if request.method == "POST":
        dia = int(request.form.get('dia'))
        hora = int(request.form.get('hora'))
        minuto = int(request.form.get('minuto'))
        nome = request.form.get('nome')
        email = request.form.get('email')
        
        
        print('Nome: '+ nome )
        print('Total: ' + str(total) )
        

    
        
        

        
    return render_template('tempo.html', form=form, dia=dia, dias=dias, hora=hora, horas=horas, minutos = minutos,minuto=minuto, nome= nome, total= total, email=email, telefone=telefone)
    


@app.route('/pagamento', methods=['POST',])
def pagamento():
    nome = request.form['nome']
    dia = request.form['dia']
    hora = request.form['hora']
    minuto = request.form['minuto']
    email = request.form['email']
    dias = int(dia)
    horas = int(hora)
    minutos = int(minuto)
    telefone = request.form.get('telefone')
    dia = (int(dia) * 24  )
        
    hora = (int(hora) + int(dia)) * 3600
    minuto = int(minuto) * 60
    total = ((dia)+(hora)+(minuto)) * (1/3600)
    total = "%.2f" % total
    print(nome)
    
    
       
    return render_template('pagamento.html', dias=dias, horas=horas, nome=nome,email=email,minutos=minutos)
       
        


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
    