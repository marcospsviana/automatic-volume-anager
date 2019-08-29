import gi
gi.require_versions({'Gtk': '3.0', 'GLib': '2.0', 'Gio': '2.0'})
from gi.repository import Gtk, Gdk
from datetime import datetime, timedelta
import time
from gi.repository import GLib 

from window_select_size import SelectSize
from login import Login

class SelectCabinet(object):
    def __init__(self):
        self.build = Gtk.Builder()
        self.build.add_from_file("ui/escolha.glade")
        self.build.connect_signals(
            {
                "gtk_main_quit": Gtk.main_quit,
                "on_reservar_button_press_event": self.on_reservar_button_press_event,
                "on_abrir_cofre_button_press_event": self.on_abrir_cofre_button_press_event,
                "on_concluir_reserva_button_press_event": self.on_concluir_reserva_button_press_event,
                "on_precosemedidas_button_press_event": self.on_precosemedidas_button_press_event,
            }
        )
        self.select_cabinet = self.build.get_object("window_select")
        self.btn_reservar = self.build.get_object("btn_reservar")
        self.label_horario = self.build.get_object("label_horario")
        self.label_data = self.build.get_object("label_data")
        GLib.timeout_add(1000, self.hora_certa )
            
       
        self.select_cabinet.fullscreen()
        self.select_cabinet.show()
        

    def on_reservar_button_press_event(self, widget, event):
        SelectSize()
        self.select_cabinet.hide()
        
    
    def hora_certa(self):
        dia = datetime.now()
        self.label_data.set_text(str(dia.day) + "/"+ str(dia.month))
        self.label_horario.set_text(str(dia.hour)+":"+str(dia.minute)+":"+str(dia.second))
        return (self.label_data, self.label_horario)
    
    def on_abrir_cofre_button_press_event(self, widget, event):
        self.select_cabinet.hide()
        Login("abrir")
    
    def on_concluir_reserva_button_press_event(self, widget, event):
        self.select_cabinet.hide()
        Login("encerrar")
    def on_precosemedidas_button_press_event(self, widget, event):
        pass

     


if __name__ == "__main__":
    app = SelectCabinet()
    Gtk.main()
    