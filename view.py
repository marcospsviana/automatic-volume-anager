import webview
from flask import Flask, url_for
from rasp import app

class View(object):
    def __init__(self):
        
        app.run()
        webview.create_window('','http://127.0.0.1:5000', frameless=False)
        webview.load_url('http://127.0.0.1:5000/index')
        
        

if __name__ == "__main__":
    View()
    
     
     