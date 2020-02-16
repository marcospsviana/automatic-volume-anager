from cadastro_usuarios import CadastroUsuarios
from controllers import Management
from taxas import *
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import string
import time
import locale
from datetime import datetime, timedelta
import calendar
from time import sleep


class WindowSelectHora:
    def __init__(self, *args):
        #teste = args
        #print("op diaria", teste)
        #self.classe = args[0]
        #self.language = args[1]
        self.tempo_locacao = args[0]
        self.classe = args[1][0]
        self.language = args[2]
        if self.classe == "A" and self.tempo_locacao == "horas":
            self.taxa = TaxAndRates.TAXA_HORA_A.value
        elif self.classe == "B" and self.tempo_locacao == "horas":
            self.taxa = TaxAndRates.TAXA_HORA_B.value
        elif self.classe == "C" and self.tempo_locacao == "horas":
            self.taxa = TaxAndRates.TAXA_HORA_C.value
        elif self.classe == "D" and self.tempo_locacao == "horas":
            self.taxa = TaxAndRates.TAXA_HORA_D.value
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
        self.builder = Gtk.Builder()
        self.gtk_style()
        self.builder.add_from_file("ui/window_select_horas.glade")
        self.builder.connect_signals(
            {
                "gtk_main_quit"             : self.on_window_select_horas_destroy,
                "on_btn_button_press_event" : self.on_btn_button_press_event,
                "on_bnt_confirmar_select_horas_button_press_event": self.on_bnt_confirmar_select_horas_button_press_event,
                "on_btn_cancelar_select_hora_button_press_event": self.on_btn_cancelar_select_hora_button_press_event,
            }
        )


        self.window_select_horas = self.builder.get_object("window_select_horas")

        self.bnt_confirmar_select_horas = self.builder.get_object("bnt_confirmar_select_horas")
        self.bnt_confirmar_select_horas.connect("button_press_event", self.on_bnt_confirmar_select_horas_button_press_event)
        self.btn_cancelar_select_hora = self.builder.get_object("btn_cancelar_select_hora")
        self.btn_cancelar_select_hora.connect("button_press_event", self.on_btn_cancelar_select_hora_button_press_event)


        self.btn1 = self.builder.get_object('btn1')
        self.btn2 = self.builder.get_object('btn2')
        self.btn3 = self.builder.get_object('btn3')
        self.btn4 = self.builder.get_object('btn4')
        self.btn5 = self.builder.get_object('btn5')
        self.btn6 = self.builder.get_object('btn6')
        self.btn7 = self.builder.get_object('btn7')
        self.btn8 = self.builder.get_object('btn8')
        self.btn9 = self.builder.get_object('btn9')
        self.btn10 = self.builder.get_object('btn10')
        self.btn11 = self.builder.get_object('btn11')
        self.btn12 = self.builder.get_object('btn12')
        self.btn13 = self.builder.get_object('btn13')
        self.btn14 = self.builder.get_object('btn14')
        self.btn15 = self.builder.get_object('btn15')
        self.btn16 = self.builder.get_object('btn16')
        self.btn17 = self.builder.get_object('btn17')
        self.btn18 = self.builder.get_object('btn18')
        self.btn19 = self.builder.get_object('btn19')
        self.btn20 = self.builder.get_object('btn20')
        self.btn21 = self.builder.get_object('btn21')
        self.btn22 = self.builder.get_object('btn22')
        self.btn23 = self.builder.get_object('btn23')
        self.btn24 = self.builder.get_object('btn24')
        self.btn1.connect("button_press_event", self.on_btn_button_press_event)
        self.btn2.connect("button_press_event", self.on_btn_button_press_event)
        self.btn3.connect("button_press_event", self.on_btn_button_press_event)
        self.btn4.connect("button_press_event", self.on_btn_button_press_event)
        self.btn5.connect("button_press_event", self.on_btn_button_press_event)
        self.btn6.connect("button_press_event", self.on_btn_button_press_event)
        self.btn7.connect("button_press_event", self.on_btn_button_press_event)
        self.btn8.connect("button_press_event", self.on_btn_button_press_event)
        self.btn9.connect("button_press_event", self.on_btn_button_press_event)
        self.btn10.connect("button_press_event", self.on_btn_button_press_event)
        self.btn11.connect("button_press_event", self.on_btn_button_press_event)
        self.btn12.connect("button_press_event", self.on_btn_button_press_event)
        self.btn13.connect("button_press_event", self.on_btn_button_press_event)
        self.btn14.connect("button_press_event", self.on_btn_button_press_event)
        self.btn15.connect("button_press_event", self.on_btn_button_press_event)
        self.btn16.connect("button_press_event", self.on_btn_button_press_event)
        self.btn17.connect("button_press_event", self.on_btn_button_press_event)
        self.btn18.connect("button_press_event", self.on_btn_button_press_event)
        self.btn19.connect("button_press_event", self.on_btn_button_press_event)
        self.btn20.connect("button_press_event", self.on_btn_button_press_event)
        self.btn21.connect("button_press_event", self.on_btn_button_press_event)
        self.btn22.connect("button_press_event", self.on_btn_button_press_event)
        self.btn23.connect("button_press_event", self.on_btn_button_press_event)
        self.btn24.connect("button_press_event", self.on_btn_button_press_event)

        self.label_valor_total_value = self.builder.get_object("label_valor_total_value")


        self.window_select_horas.show()
    def on_btn_button_press_event(self, widget,  event):
        hora = int(widget.get_label())
        valor_total = hora * self.taxa
        self.label_valor_total_value.set_text("%.2f"%valor_total)

    def on_bnt_confirmar_select_horas_button_press_event(self, widget, event):
        self.total = self.label_valor_total_value.get_text()
        CadastroUsuarios(self.total , self.language)
    
    def on_btn_cancelar_select_hora_button_press_event(self, widget, event):
        self.label_valor_total_value.set_text("")
        self.window_select_horas.hide()
        
    def on_window_select_horas_destroy(self):
        self.window_select_horas.destroy()

    def gtk_style(self):
        css = b"""
        
        @import url("static/css/calendario.css");
        """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )


if __name__ == "__main__":
    app = WindowSelectHora()
    Gtk.main()