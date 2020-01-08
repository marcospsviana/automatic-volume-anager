import gi 
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class WindowSelectCartao:
    def __init__(self):
        self.build = Gtk.Builder()
        self.build.add_from_file("window_select_cartao.glade")
        self.build.connect_signals(
            {
                "gtk_main_quit" : Gtk.main_quit,
                "on_btn_credito_button_press_event": self.on_btn_credito_button_press_event,
                "on_btn_debito_button_press_event": self.on_btn_debito_button_press_event,
                "on_btn_cancelar_button_press_event": self.on_btn_cancelar_button_press_event
            }
        )
        self.btn_credito = self.build.get_object("btn_credito")
        #self.btn_credito.connect("button-press-event", self.on_btn_credito_button_press_event)
        self.btn_debito = self.build.get_object("btn_debito")
        #self.btn_debito.connect("button-press-event", self.on_btn_debito_button_press_event)
        self.btn_cancelar = self.build.get_object("btn_cancelar")
        #self.btn_cancelar.connect("button-press-event", self.on_btn_cancelar_button_press_event)
        
    
        self.window_select_cartao = self.build.get_object("window_select_cartao")
        self.window_select_cartao.show()
    @staticmethod
    def on_btn_credito_button_press_event(self, event):
            print("on_btn_credito_button_press_event")
    @staticmethod
    def on_btn_debito_button_press_event(self, event):
        print("on_btn_debito_button_press_event")
    @staticmethod
    def on_btn_cancelar_button_press_event(self, event):
        print("on_btn_cancelar_button_press_event")
        Gtk.main_quit()

if __name__ == "__main__":
    app = WindowSelectCartao()
    Gtk.main()