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
                "on_num_button_press_event": self.on_num_button_press_event,
                "on_cancela_clicked": self.on_cancela_clicked,
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
        self.a = builder.get_object("a")
        self.a.connect("clicked", self.on_entry_button_press_event)
        self.b = builder.get_object("b")
        self.b.connect("clicked", self.on_entry_button_press_event)
        self.c = builder.get_object("c")
        self.c.connect("clicked", self.on_entry_button_press_event)
        self.d = builder.get_object("d")
        self.d.connect("clicked", self.on_entry_button_press_event)
        self.e = builder.get_object("e")
        self.e.connect("clicked", self.on_entry_button_press_event)
        self.f = builder.get_object("f")
        self.f.connect("clicked", self.on_entry_button_press_event)
        self.g = builder.get_object("g")
        self.g.connect("clicked", self.on_entry_button_press_event)
        self.h = builder.get_object("h")
        self.h.connect("clicked", self.on_entry_button_press_event)
        self.i = builder.get_object("i")
        self.i.connect("clicked", self.on_entry_button_press_event)
        self.j = builder.get_object("j")
        self.j.connect("clicked", self.on_entry_button_press_event)
        self.k = builder.get_object("k")
        self.k.connect("clicked", self.on_entry_button_press_event)
        self.l = builder.get_object("l")
        self.l.connect("clicked", self.on_entry_button_press_event)
        self.m = builder.get_object("m")
        self.m.connect("clicked", self.on_entry_button_press_event)
        self.n = builder.get_object("n")
        self.n.connect("clicked", self.on_entry_button_press_event)
        self.o = builder.get_object("o")
        self.o.connect("clicked", self.on_entry_button_press_event)
        self.p = builder.get_object("p")
        self.p.connect("clicked", self.on_entry_button_press_event)
        self.q = builder.get_object("q")
        self.q.connect("clicked", self.on_entry_button_press_event)
        self.r = builder.get_object("r")
        self.r.connect("clicked", self.on_entry_button_press_event)
        self.s = builder.get_object("s")
        self.s.connect("clicked", self.on_entry_button_press_event)
        self.t = builder.get_object("t")
        self.t.connect("clicked", self.on_entry_button_press_event)
        self.u = builder.get_object("u")
        self.u.connect("clicked", self.on_entry_button_press_event)
        self.v = builder.get_object("v")
        self.v.connect("clicked", self.on_entry_button_press_event)
        self.w = builder.get_object("w")
        self.w.connect("clicked", self.on_entry_button_press_event)
        self.x = builder.get_object("x")
        self.x.connect("clicked", self.on_entry_button_press_event)
        self.y = builder.get_object("y")
        self.y.connect("clicked", self.on_entry_button_press_event)
        self.z = builder.get_object("z")
        self.z.connect("clicked", self.on_entry_button_press_event)
        
        self.space = builder.get_object("space")
        self.btn_delete = builder.get_object("DELETE")
        self.btn_login = builder.get_object("btn_login")
        #self.enter = builder.get_object("ENTER")
        #self.enter.connect("clicked", self.on_ENTER_clicked)
        self.lbl_time = builder.get_object("time")
        self.window_time = builder.get_object("window_time")
        self.dialog_cobranca = builder.get_object("dialog_cobranca")
        self.lbl_message = builder.get_object("lbl_message")
        self.btn_num = builder.get_object("num")
        self.space = builder.get_object("space")
        self.btn_delete = builder.get_object("DELETE")
        self.btn_login = builder.get_object("btn_login")
        self.lbl_time = builder.get_object("time")
        self.window_time = builder.get_object("window_time")
        self.dialog_cobranca = builder.get_object("dialog_cobranca")
        self.lbl_message = builder.get_object("lbl_message")
        

        #========== fim elementos do teclado =====================
        #conectando os botões aos eventos ========================
        self.btn_delete.connect("clicked", self.on_entry_backspace)
        #conectando os botões aos eventos ========================
        self.btn_delete.connect("clicked", self.on_entry_backspace)
        self.window_login.set_resolution(72)
        self.window_login.show()
    
    def on_cancela_clicked(self, event):
        self.window_login.hide()
    
        
    def on_num_button_press_event(self, widget, event):
        if self.num == False:
            self.num = True
            self.a.set_label('a')
            self.b.set_label('b')
            self.c.set_label('c')
            self.d.set_label('d')
            self.e.set_label('e')
            self.f.set_label('f')
            self.g.set_label('g')
            self.h.set_label('h')
            self.i.set_label('i')
            self.j.set_label('j')
            self.k.set_label('k')
            self.l.set_label('l')
            self.m.set_label('m')
            self.n.set_label('n')
            self.o.set_label('o')
            self.p.set_label('p')
            self.q.set_label('q')
            self.r.set_label('r')
            self.s.set_visible(True)
            self.t.set_visible(True)
            self.u.set_visible(True)
            self.v.set_visible(True)
            self.w.set_visible(True)
            self.x.set_visible(True)
            self.y.set_visible(True)
            self.z.set_visible(True)
            
            self.btn_num.set_label('123..')
        else:
            self.num = False
            self.a.set_label('0')
            self.b.set_label('1')
            self.c.set_label('2')
            self.d.set_label('3')
            self.e.set_label('4')
            self.f.set_label('5')
            self.g.set_label('6')
            self.h.set_label('7')
            self.i.set_label('8')
            self.j.set_label('9')
            self.k.set_label('@')
            self.l.set_label('_')
            self.m.set_label('-')
            self.n.set_label('.')
            self.o.set_label('.com')
            self.p.set_label('@gmail')
            self.q.set_label('@outlook')
            self.r.set_label('@yahoo')
            self.s.set_visible(False)
            self.t.set_visible(False)
            self.u.set_visible(False)
            self.v.set_visible(False)
            self.w.set_visible(False)
            self.x.set_visible(False)
            self.y.set_visible(False)
            self.z.set_visible(False)
            self.btn_num.set_label('abc..')
            
        
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

    '''def gtk_style(self):
        css = b"""
        *{ font-size: 27px;}        
        #grid_teclado { font-size: 15px}
        #btn_cancelar { font-size: 20px; background-color: red; color: #fff }
        #label { font-size: 25px; }
        #lbl_time { font-size: 52px }       
        #label_telefone { color: #fff }
        #label_senha { color: #fff }
        #window { background-color: #000; color: #fff;}
        #entry { font-size: 32px}
        """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )'''

if __name__ == "__main__":
    Login()