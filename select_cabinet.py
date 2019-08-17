import gi
gi.require_versions({'Gtk': '3.0', 'GLib': '2.0', 'Gio': '2.0'})
from gi.repository import Gtk, Gdk
from datetime import datetime, timedelta
import time
from gi.repository import GObject 

from window_op_hora_diaria import OpcaoHoraDiaria

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
        GObject.timeout_add(1000, self.hora_certa )
            
       
        self.select_cabinet.fullscreen()
        self.select_cabinet.show()
        

    def on_reservar_button_press_event(self, event):
        OpcaoHoraDiaria()
    
    def hora_certa(self):
        dia = datetime.now()
        self.label_data.set_text(str(dia.day) + "/"+ str(dia.month))
        self.label_horario.set_text(str(dia.hour)+":"+str(dia.minute)+":"+str(dia.second))
        return (self.label_data, self.label_horario)
        
    
     


if __name__ == "__main__":
    
    app = SelectCabinet()
    
    self.condicao = True
    Gtk.main(hora_certa())
    