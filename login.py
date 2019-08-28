import gi 
import string
import time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from controllers import Management

class Login(Gtk.Window):
    def __init__(self):
        #self.gtk_style()    
        self.screen = Gdk.Screen.get_default()
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/login.glade")
        self.manager = Management()
        self.value = ''
        self.entrada = ''
        self.alfa = list(string.ascii_lowercase) # alfabeto para gerar o teclado
        self.num = list(map(lambda x: x, range(10))) # números para o teclado numérico
        self.builder.connect_signals(
            {
                "on_window_login_destroy": self.on_window_login_destroy,
                "on_ENTER_clicked": self.on_ENTER_clicked,
                "on_entry_email_telefone_button_press_event": self.on_entry_email_telefone_button_press_event,
                "on_entry_senha_button_press_event": self.on_entry_senha_button_press_event,
                "on_btn_login_clicked": self.on_btn_login_clicked,
                "on_cancela_clicked": self.on_cancela_clicked,
                "gtk_widget_destroy" : self.gtk_widget_destroy
            }
        )
        self.window_login = self.builder.get_object("window_login")
        self.window_entrada_dados = self.builder.get_object("window_entrada_dados")
        # adicionando elementos da janela
        self.entry_nome = self.builder.get_object("entry_email_telefone")
        
        self.entry_senha = self.builder.get_object('entry_senha')
        self.entry_nome.connect("button-press-event", self.on_entry_email_telefone_button_press_event)
        self.entry_senha.connect("button-press-event", self.on_entry_senha_button_press_event)
        #adicionando os elementos do teclado =======================
        self.a = self.builder.get_object("a")
        self.a.connect("clicked", self.on_entry_button_press_event)
        self.b = self.builder.get_object("b")
        self.b.connect("clicked", self.on_entry_button_press_event)
        self.c = self.builder.get_object("c")
        self.c.connect("clicked", self.on_entry_button_press_event)
        self.d = self.builder.get_object("d")
        self.d.connect("clicked", self.on_entry_button_press_event)
        self.e = self.builder.get_object("e")
        self.e.connect("clicked", self.on_entry_button_press_event)
        self.f = self.builder.get_object("f")
        self.f.connect("clicked", self.on_entry_button_press_event)
        self.g = self.builder.get_object("g")
        self.g.connect("clicked", self.on_entry_button_press_event)
        self.h = self.builder.get_object("h")
        self.h.connect("clicked", self.on_entry_button_press_event)
        self.i = self.builder.get_object("i")
        self.i.connect("clicked", self.on_entry_button_press_event)
        self.j = self.builder.get_object("j")
        self.j.connect("clicked", self.on_entry_button_press_event)
        self.k = self.builder.get_object("k")
        self.k.connect("clicked", self.on_entry_button_press_event)
        self.l = self.builder.get_object("l")
        self.l.connect("clicked", self.on_entry_button_press_event)
        self.m = self.builder.get_object("m")
        self.m.connect("clicked", self.on_entry_button_press_event)
        self.n = self.builder.get_object("n")
        self.n.connect("clicked", self.on_entry_button_press_event)
        self.o = self.builder.get_object("o")
        self.o.connect("clicked", self.on_entry_button_press_event)
        self.p = self.builder.get_object("p")
        self.p.connect("clicked", self.on_entry_button_press_event)
        self.q = self.builder.get_object("q")
        self.q.connect("clicked", self.on_entry_button_press_event)
        self.r = self.builder.get_object("r")
        self.r.connect("clicked", self.on_entry_button_press_event)
        self.s = self.builder.get_object("s")
        self.s.connect("clicked", self.on_entry_button_press_event)
        self.t = self.builder.get_object("t")
        self.t.connect("clicked", self.on_entry_button_press_event)
        self.u = self.builder.get_object("u")
        self.u.connect("clicked", self.on_entry_button_press_event)
        self.v = self.builder.get_object("v")
        self.v.connect("clicked", self.on_entry_button_press_event)
        self.w = self.builder.get_object("w")
        self.w.connect("clicked", self.on_entry_button_press_event)
        self.x = self.builder.get_object("x")
        self.x.connect("clicked", self.on_entry_button_press_event)
        self.y = self.builder.get_object("y")
        self.y.connect("clicked", self.on_entry_button_press_event)
        self.z = self.builder.get_object("z")
        self.z.connect("clicked", self.on_entry_button_press_event)
        
        self.space = self.builder.get_object("space")
        #self.btn_delete = self.builder.get_object("DELETE")
        self.btn_login = self.builder.get_object("btn_login")
        #self.enter = self.builder.get_object("ENTER")
        #self.enter.connect("clicked", self.on_ENTER_clicked)
        self.lbl_time = self.builder.get_object("time")
        self.window_time = self.builder.get_object("window_time")
        self.dialog_cobranca = self.builder.get_object("dialog_cobranca")
        self.lbl_message = self.builder.get_object("lbl_message")
        self.btn_num = self.builder.get_object("num")
        
        

        #========== fim elementos do teclado =====================
        #conectando os botões aos eventos ========================
        #self.btn_delete.connect("clicked", self.on_entry_backspace)
        #conectando os botões aos eventos ========================
        #self.btn_delete.connect("clicked", self.on_entry_backspace)
        #s = Gdk.Screen.get_default()'''
        #self.window_login.fullscreen()
        self.window_login.show()
    
    def on_cancela_clicked(self, event):
        self.window_login.hide()
    
        
   
            
        
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
    def on_entry_email_telefone_button_press_event(self, widget, event):
        #self.entrada = '7'
        #return self.entrada
        self.window_entrada_dados.show()
    
    def on_entry_senha_button_press_event(self, widget, event):
        self.entrada = '8'
        return self.entrada
    


    def on_entry_button_press_event(self, widget):
        self.value = widget.get_label()
        
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