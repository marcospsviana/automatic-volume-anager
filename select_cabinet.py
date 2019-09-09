import gi
gi.require_versions({'Gtk': '3.0', 'GLib': '2.0', 'Gio': '2.0'})
from gi.repository import Gtk, Gdk
from datetime import datetime, timedelta
import time
from gi.repository import GLib 

from window_select_size import SelectSize
from tamanhos_tarifas import TamanhosTarifas
#from login import Login
from window_login import WindowLogin

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
        self.btn_abrir = self.builder.get_object("btn_abrir")
        self.btn_concluir = self.builder.get_object("btn_concluir")
        self.btn_medidas = self.builder.get_object("btn_medidas")
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
        # =========== BUTTONS IMAGES =========================
        self.image_start_reservation = Gtk.Image()
        self.image_iniciar_reserva = Gtk.Image()
        self.image_abrir = Gtk.Image()
        self.image_open_safe = Gtk.Image()
        self.image_concluir_reserva = Gtk.Image()
        self.image_complete_reservation = Gtk.Image()
        self.image_precos_medidas = Gtk.Image()
        self.image_sizes_rates = Gtk.Image()

        self.image_abrir.set_from_file("static/images/cadeado.svg")
        self.image_open_safe.set_from_file("static/images/open_safe.svg")
        self.image_start_reservation.set_from_file("static/images/start_reservation.svg")
        self.image_iniciar_reserva.set_from_file("static/images/inicio_reserva.svg")
        self.image_concluir_reserva.set_from_file("static/images/cartao.svg")
        self.image_complete_reservation.set_from_file("static/images/complete_reservation.svg")
        self.image_precos_medidas.set_from_file("static/images/precosmedidas.svg")
        self.image_sizes_rates.set_from_file("static/images/sizes_rates.svg")

        # ========== END BUTTONS IMAGES ======================
        if self.language == "pt_BR":
            self.btn_reservar.set_image(self.image_iniciar_reserva)
            self.btn_concluir.set_image(self.image_concluir_reserva)
            self.btn_abrir.set_image(self.image_abrir)
            self.btn_medidas.set_image(self.image_precos_medidas)
        elif self.language == "en_US":
            self.btn_reservar.set_image(self.image_start_reservation)
            self.btn_concluir.set_image(self.image_complete_reservation)
            self.btn_abrir.set_image(self.image_open_safe)
            self.btn_medidas.set_image(self.image_sizes_rates)

        GLib.timeout_add(1000, self.hora_certa )
            
       
        self.select_cabinet.fullscreen()
        self.select_cabinet.show()
        

    def on_reservar_button_press_event(self, widget, event):
        SelectSize(self.language)
        self.select_cabinet.hide()
        
    
    def hora_certa(self):
        dia = datetime.now()
        self.label_data.set_text(str(dia.day) + "/"+ str(dia.month))
        self.label_horario.set_text(str(dia.hour)+":"+str(dia.minute)+":"+str(dia.second))
        return (self.label_data, self.label_horario)
    
    def on_abrir_cofre_button_press_event(self, widget, event):
        self.select_cabinet.hide()
        WindowLogin("abrir", self.language)
    
    def on_btn_concluir_button_press_event(self, widget, event):
        self.select_cabinet.hide()
        WindowLogin("encerrar", self.language)
    def on_precosemedidas_button_press_event(self, widget, event):
        TamanhosTarifas(self.language)
        self.select_cabinet.hide()
    
    def on_change_language_br(self, event):
        self.language = "pt_BR"
        self.btn_reservar.set_image(self.image_iniciar_reserva)
        self.btn_concluir.set_image(self.image_concluir_reserva)
        self.btn_abrir.set_image(self.image_abrir)
        self.btn_medidas.set_image(self.image_precos_medidas)
    
    def on_change_language_usa(self, event):
        self.language = "en_US"
        self.btn_reservar.set_image(self.image_start_reservation)
        self.btn_concluir.set_image(self.image_complete_reservation)
        self.btn_abrir.set_image(self.image_open_safe)
        self.btn_medidas.set_image(self.image_sizes_rates)
        
        

     


if __name__ == "__main__":
    app = SelectCabinet()
    Gtk.main()
    