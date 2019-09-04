import gi
gi.require_versions({'Gtk': '3.0', 'GLib': '2.0', 'Gio': '2.0'})
from gi.repository import Gtk, Gdk
from datetime import datetime, timedelta
import time
from gi.repository import GLib 

from window_select_size import SelectSize
from login import Login

class SelectCabinet(object):
    def __init__(self, arg):
        self.language = arg
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/select_option.glade")
        self.builder.connect_signals(
            {
                "gtk_main_quit": Gtk.main_quit,
                "on_reservar_button_press_event": self.on_reservar_button_press_event,
                "on_abrir_cofre_button_press_event": self.on_abrir_cofre_button_press_event,
                "on_btn_concluir_button_press_event": self.on_btn_concluir_button_press_event,
                "on_precosemedidas_button_press_event": self.on_precosemedidas_button_press_event,
            }
        )
        self.select_cabinet = self.builder.get_object("window_select")
        self.btn_reservar = self.builder.get_object("btn_reservar")
        self.label_horario = self.builder.get_object("label_horario")
        self.label_data = self.builder.get_object("label_data")
        self.btn_flag_br = self.builder.get_object("btn_flag_br")
        self.btn_flag_usa = self.builder.get_object("btn_flag_usa")
        self.btn_flag_br.connect("clicked", self.on_change_language_br)
        self.btn_flag_usa.connect("clicked", self.on_change_language_usa)
        self.label_iniciar_reserva = self.builder.get_object("label_iniciar_reserva")
        self.label_concluir_reserva = self.builder.get_object("label_concluir_reserva")
        self.label_abrir_cofre = self.builder.get_object("label_abrir_cofre")
        self.label_tamanhos_tafifas = self.builder.get_object("label_tamanhos_tafifas")
        if self.language == "pt_BR":
            self.label_abrir_cofre.set_text("ABRIR\n COFRE")
            self.label_concluir_reserva.set_text("CONCLUIR\n RESERVA")
            self.label_iniciar_reserva.set_text("INICIAR\n RESERVA")
            self.label_tamanhos_tafifas.set_text("TAMANHOS\n E\n TARIFAS")
        elif self.language == "en_US":
            self.label_abrir_cofre.set_text("OPEN\n SAFE")
            self.label_concluir_reserva.set_text("COMPLETE\n RESERVATON")
            self.label_iniciar_reserva.set_text("START\n RESERVATION")
            self.label_tamanhos_tafifas.set_text("SIZES\n AND\n RATES")

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
    
    def on_btn_concluir_button_press_event(self, widget, event):
        self.select_cabinet.hide()
        Login("encerrar")
    def on_precosemedidas_button_press_event(self, widget, event):
        SelectSize().on_btn_tamanhos_tarifas_button_press_event()
        self.select_cabinet.hide()
    
    def on_change_language_br(self, event):
        self.language = "pt_BR"
        self.label_abrir_cofre.set_text("ABRIR\n COFRE")
        self.label_concluir_reserva.set_text("CONCLUIR\n RESERVA")
        self.label_iniciar_reserva.set_text("INICIAR\n RESERVA")
        self.label_tamanhos_tafifas.set_text("TAMANHOS\n E\n TARIFAS")
    
    def on_change_language_usa(self, event):
        self.language = "en_US"
        self.label_abrir_cofre.set_text("OPEN\n SAFE")
        self.label_concluir_reserva.set_text("COMPLETE\n RESERVATON")
        self.label_iniciar_reserva.set_text("START\n RESERVATION")
        self.label_tamanhos_tafifas.set_text("SIZES\n AND\n RATES")
        
        

     


if __name__ == "__main__":
    app = SelectCabinet()
    Gtk.main()
    