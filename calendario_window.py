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


class WindowCalendario:
    def __init__(self):
        #teste = args
        #print("op diaria", teste)
        #self.classe = args[0]
        #self.language = args[1]
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
        self.builder = Gtk.Builder()
        self.gtk_style()
        self.builder.add_from_file("ui/calendario_window.glade")
        self.builder.connect_signals(
            {
                "gtk_main_quit"                           : self.on_window_calendario_destroy,
            }
        )


        self.window_calendario = self.builder.get_object("window_calendario")
        self.window_calendario.show()
        
    def on_window_calendario_destroy(self):
        self.window_calendario.destroy()

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
    app = WindowCalendario()
    Gtk.main()