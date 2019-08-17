import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from datetime import datetime, timedelta
import time

class SelectCabinet(object):
    def __init__(self):
        self.condicao = True
        self.build = Gtk.Builder()
        self.build.add_from_file("ui/escolha.glade")
        self.build.connect_signals(
            {
                "gtk_main_quit": Gtk.main_quit,
                "on_reservar_button_press_event": self.on_reservar_button_press_event,
            }
        )
        self.select_cabinet = self.build.get_object("window_select")
        self.btn_reservar = self.build.get_object("btn_reservar")
        self.label_horario = self.build.get_object("label_horario")
        self.label_data = self.build.get_object("label_data")
        while self.condicao:
            self.hora_certa()
            self.condicao = False
       
        self.select_cabinet.fullscreen()
        self.select_cabinet.show()
        

    def on_reservar_button_press_event(self, event):
        print("reservar")
    def hora_certa(self):
        self.data = datetime.today()
        self.label_data.set_text(str(self.data.day) + "/"+ str(self.data.month))
        self.label_horario.set_text(str(self.data.hour)+":"+str(self.data.minute)+":"+str(self.data.second))
    
     


if __name__ == "__main__":
    
    app = SelectCabinet()
    
    self.condicao = True
    Gtk.main(hora_certa())
    