import gi 
import string
import time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from controllers import Management


class WindowLogin(Gtk.Window):
    def __init__(self, *args):
        #self.opcao = args[0]
        #self.language = args[1]
        self.screen = Gdk.Screen.get_default()
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/window_login.glade")
        self.manager = Management()
        self.value = ''
        self.entrada = ''
        self.alfa = list(string.ascii_lowercase) # alfabeto para gerar o teclado
        self.num = list(map(lambda x: x, range(10))) # números para o teclado numérico
        #self.builder.connect_signals()
        for alfabet in self.alfa:
            self.alfabet = self.builder.get_object("%s"%(alfabet))
            self.alfabet.connect("clicked", self.on_entry_button_press_event)
        
        self.entry = self.builder.get_object("entry_entrada_dados")
        self.window_login = self.builder.get_object("window_login")
        self.window_login.show()

    def on_entry_button_press_event(self, widget):
        self.value = widget.get_label()
        self.text_entrada = self.entry.get_text() + self.value
        self.entry.set_text(self.text_entrada)
        self.entry.set_position(-1)

app = WindowLogin()
Gtk.main()
    
