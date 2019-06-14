import webview

class View(object):
    def __init__(self):
        
       
        webview.create_window('','http://localhost:5000', frameless=False)
        
        
        

if __name__ == "__main__":
    View()
    
     
     