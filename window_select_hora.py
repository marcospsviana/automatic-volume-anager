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
    def __init__(self):
        #teste = args
        #print("op diaria", teste)
        #self.classe = args[0]
        #self.language = args[1]
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
        self.builder = Gtk.Builder()
        self.gtk_style()
        self.builder.add_from_file("ui/window_select_horas.glade")
        self.builder.connect_signals(
            {
                "gtk_main_quit"                           : self.on_window_select_horas_destroy,
            }
        )


        self.window_select_horas = self.builder.get_object("window_select_horas")
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


        self.window_select_horas.show()
        
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