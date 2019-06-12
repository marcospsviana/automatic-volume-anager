import webview
from flask import Flask
from rasp import app

class View(object):
    def __init__(self):
        
       
        webview.create_window('','http://127.0.0.1:5000', frameless=False)
        webview.load_html('', "app.run(host='localhost', port=5000)")
        

if __name__ == "__main__":
    View()
    
     
     