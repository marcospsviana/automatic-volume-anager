import gi 
import string
import time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from controllers import Management


class WindowLogin(Gtk.Window):
    def __init__(self, *args):
        self.opcao = args[0]
        self.language = args[1]
        self.screen = Gdk.Screen.get_default()
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/window_login.glade")
        self.manager = Management()
        self.value = ''
        self.entrada = ''
        self.alfa = list(string.ascii_lowercase) # alfabeto para gerar o teclado
        self.num = list(map(lambda x: x, range(10))) # números para o teclado numérico
        self.builder.connect_signals({
            "on_btn_retornar_entrada_dados_pressed": self.on_btn_retornar_entrada_dados_pressed
        })
        for alfabet in self.alfa:
            self.alfabet = self.builder.get_object("%s"%(alfabet))
            self.alfabet.connect("clicked", self.on_entry_button_press_event)
        for num in self.num:
            self.number = self.builder.get_object("num_%s"%(num))
            self.number.connect("clicked", self.on_entry_button_press_event)
        
        self.entry = self.builder.get_object("entry_entrada_dados")
        self.btn_confirmar_entrada_dados = self.builder.get_object("btn_confirmar_entrada_dados")
        self.btn_retornar_entrada_dados = self.builder.get_object("btn_retornar_entrada_dados")
        self.btn_retornar_entrada_dados.connect("clicked", self.on_btn_retornar_entrada_dados_pressed)
        self.btn_confirmar_entrada_dados.connect("clicked", self.on_btn_confirmar_entrada_dados_pressed)
        self.window_login = self.builder.get_object("window_login")
        self.window_login.show()

    def on_entry_button_press_event(self, widget):
        self.value = widget.get_label()
        self.text_entrada = self.entry.get_text() + self.value
        self.entry.set_text(self.text_entrada)
        self.entry.set_position(-1)
    
    def on_btn_confirmar_entrada_dados_pressed(self, event):
        self.message = ''
        senha = self.entry.get_text()
        if self.opcao == "abrir":
            result = self.manager.abre_armario(senha, nome)
        elif self.opcao == "encerrar":
            result = self.manager.liberar_armarios(senha)
        print('result login', result)
        if result == 'armario liberado':
            self.window_login.hide()
            self.entry.set_text('')
            print('abrir')
        elif result == 'senha incorreta, tente novamente':
            #self.window_login.hide()
            self.entry.set_text('')
            
             
            self.label_dialog_senha_incorreta.set_text('senha incorreta, tente novamente')
            self.dialog_senha_incorreta.show()
            
        else:
            #self.window_login.close()

            print('ok fechou')
            self.message = str(result)
            self.lbl_message.set_text(self.message)
            self.dialog_cobranca.show()
            result = ''

    def on_btn_retornar_entrada_dados_pressed(self, event):
        self.entry.set_text("")
        self.window_login.hide()
        
    

if __name__ == "__main__":
    app = WindowLogin()
    Gtk.main()
    
