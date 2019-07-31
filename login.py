import gi 
import string
import time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from controllers import Management

class Login(Gtk.Window):
    def __init__(self):
    
        builder = Gtk.Builder()
        builder.add_from_file("ui/login.glade")
        self.manager = Management()
        self.value = ''
        self.entrada = ''
        self.alfa = list(string.ascii_lowercase) # alfabeto para gerar o teclado
        self.num = list(map(lambda x: x, range(10))) # números para o teclado numérico
        builder.connect_signals(
            {
                "on_window_login_destroy": self.on_window_login_destroy,
                "on_ENTER_clicked": self.on_ENTER_clicked,
                "on_entry_nome": self.on_entry_nome,
                "on_entry_senha": self.on_entry_senha,
                "on_btn_login_clicked": self.on_btn_login_clicked,
                "gtk_widget_destroy" : self.gtk_widget_destroy
            }
        )
        self.window_login = builder.get_object("window_login")
        # adicionando elementos da janela
        self.entry_nome = builder.get_object("entry_nome")
        self.entry_senha = builder.get_object('entry_senha')
        self.entry_nome.connect("button-press-event", self.on_entry_nome)
        self.entry_senha.connect("button-press-event", self.on_entry_senha)
        #adicionando os elementos do teclado =======================
        for a in self.alfa:
            self.a = builder.get_object("%s"%a)
            self.a.connect("clicked", self.on_entry_button_press_event)
        for n in self.num:
            self.n = builder.get_object("%s"%n)
            self.n.connect("clicked", self.on_entry_button_press_event)

        self.arroba = builder.get_object("arroba")
        self.dot = builder.get_object("dot")
        self.under = builder.get_object("under")
        self.dash = builder.get_object("dash")
        self.dotCom = builder.get_object("dotCom")
        self.gmail = builder.get_object("gmail")
        self.yahoo = builder.get_object("yahoo")
        self.outlook  = builder.get_object("outlook")
        self.space = builder.get_object("space")
        self.btn_delete = builder.get_object("DELETE")
        self.btn_login = builder.get_object("btn_login")
        self.enter = builder.get_object("ENTER")
        self.enter.connect("clicked", self.on_ENTER_clicked)
        self.lbl_time = builder.get_object("time")
        self.window_time = builder.get_object("window_time")
        self.dialog_cobranca = builder.get_object("dialog_cobranca")
        self.lbl_message = builder.get_object("lbl_message")
        #========== fim elementos do teclado =====================
        #conectando os botões aos eventos ========================
        self.btn_delete.connect("clicked", self.on_entry_backspace)
        self.arroba.connect("clicked", self.on_entry_button_press_event)
        self.dotCom.connect("clicked", self.on_entry_button_press_event)
        self.dot.connect("clicked", self.on_entry_button_press_event)
        self.dash.connect("clicked", self.on_entry_button_press_event)
        self.under.connect("clicked", self.on_entry_button_press_event)
        self.yahoo.connect("clicked", self.on_entry_button_press_event)
        self.gmail.connect("clicked", self.on_entry_button_press_event)
        self.outlook.connect("clicked", self.on_entry_button_press_event)
        #self.btn_login.connect("clicked", self.on_btn_login_clicked)
        
        

        self.window_login.show()
        
    def on_ENTER_clicked(self, widget):
        self.window_time.show()
        j = 10
        for i in range(0,5):
            self.lbl_time.set_text(str(j-i))
            time.sleep(1)
            
        
            

    def on_btn_login_clicked(self, event):
        self.message = ''
        nome = self.entry_nome.get_text()
        senha = self.entry_senha.get_text()
        result = self.manager.abre_armario(senha, nome)
        print('result login', result)
        if result == 'armario liberado':
            self.window_login.hide()
            self.entry_nome.set_text('')
            self.entry_senha.set_text('')
            print('abrir')
        else:
            self.window_login.close()

            print('ok fechou')
            self.message = str(result)
            self.lbl_message.set_text(self.message)
            self.dialog_cobranca.show()
            result = ''

    def dialog_cobranca_show(self):
        #self.dialog_cobranca.show()
        print('cobranca em dialogo')   
    def on_entry_nome(self, widget, event):
        self.entrada = '7'
        return self.entrada
    
    def on_entry_senha(self, widget, event):
        self.entrada = '8'
        return self.entrada
    


    def on_entry_button_press_event(self, widget):
        self.widget = widget
        self.value =  self.widget.get_label()
        
        if self.entrada == '7':
            
            self.text_nome = self.entry_nome.get_text() + self.value
            if self.text_nome.isalpha() or (self.text_nome.isalpha and string.whitespace):
                self.entry_nome.set_text(self.text_nome)
                self.entry_nome.set_position(-1)
                
            
        elif self.entrada == '8':
            self.text_senha = self.entry_senha.get_text() + self.value
            self.entry_senha.set_text(self.text_senha)
            self.entry_senha.set_position(-1)
    
    def on_entry_backspace(self, widget):
        
        if self.entrada == '7':
            self.texto = ''
            self.texto = self.entry_nome.get_text()
            self.texto = self.texto[:-1]
            self.entry_nome.set_text(self.texto)
            self.entry_nome.set_position(-1)
        elif self.entrada == '8':
            self.texto = ''
            self.texto = self.entry_senha.get_text()
            self.texto = self.texto[:-1]
            self.entry_senha.set_text(self.texto)
            self.entry_senha.set_position(-1)
    def gtk_widget_destroy(self, widget):
        self.entry_senha.set_text('')
        self.entry_nome.set_text('')
        self.on_window_login_destroy
        self.dialog_cobranca.destroy()
    def on_window_login_destroy(self, widget):
        self.window_login.close()

if __name__ == "__main__":
    Login()