from flask import Flask, render_template, url_for, request, redirect, make_response
import sys, os

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

@app.route('/armarios')
def armarios():
    return render_template('armarios.html')

@app.route('/tempo', methods=['GET', 'POST'])
def tempo():
    from engine.data import Banco
    b = Banco()

    dia = 0
    hora = 0
    minuto = 0
    form = FormTempo(request.form)
    
    if request.method == 'POST':
        dia = form.dia.data
        hora = form.hora.data
        minuto = form.minuto.data
        nome = form.nome.data
        email = form.email.data
        telefone = form.telefone.data
        dia = dia* 24 * 3600
        hora = hora * 3600
        minuto = minuto * 60
        total = (dia+hora+minuto) * 0.15

        datas = {'dia':dia, 'hora':hora, 'minuto': minuto, 'nome': nome, 'total': total}
        
        
    return render_template('tempo.html', form=form)
    return redirect(url_for('pagamento',dia=dia, hora=hora, minuto= minuto, nome= nome, total= total))


@app.route('/pagamento')
def pagamento():
        return render_template('pagamento.html',dia=dia, hora=hora, minuto= minuto, nome= nome, total= total)

        

@app.route('/monitoramento')
def monitor():
        return render_template('monitoramento.html')


if __name__ == '__main__':
    coolbagsafe = '10.15.1.175'
    app.run(host='localhost', port=5000, debug=True)
