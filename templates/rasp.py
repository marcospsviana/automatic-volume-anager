from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
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

if __name__ == '__main__':
    app.run(host='localhost', port=8000)