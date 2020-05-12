#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import sys, os
import datetime
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf, GObject, GLib
from taxas import *
import string
import time
import locale
from datetime import datetime, timedelta, date
import calendar
import PIL
from PIL import Image
from decimal import Decimal
import encodings.unicode_escape

#from login import Login
#from encerrar import Encerrar
#from locar import Locar
from select_option import SelectOption
DDD = ''



class CollBagSafe(object):
    def __init__(self):
        #idioma padrao pt_BR
        self.language = "pt_BR"
        self.gtk_style()
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/coolbag_safe.glade")
        self.builder.connect_signals({
            "gtk_main_quit": Gtk.main_quit,
            "on_btn_principal_clicked": self.on_btn_principal_clicked,
        })
        self.main_window = self.builder.get_object("mainwindow")
        self.label_horario = self.builder.get_object("label_horario")
        self.label_data = self.builder.get_object("label_data")
        self.btn_flag_br = self.builder.get_object("btn_flag_br")
        self.btn_flag_usa = self.builder.get_object("btn_flag_usa")
        self.spinner_coolbag = self.builder.get_object("spinner_coolbag")
        self.btn_flag_br.connect("clicked", self.on_change_language_br)
        self.btn_flag_usa.connect("clicked", self.on_change_language_usa)
        GLib.timeout_add(1000, self.hora_certa)
        
        self.main_window.fullscreen()
        self.main_window.show()
    
    def hora_certa(self):
        """atualiza a hora e data na tela setando as respectivas labels
        """
        dia = datetime.now()
        dia_hora = dia.strftime("%H:%M:%S")
        dia_data = dia.strftime("%d/%m/%Y")
        self.label_horario.set_text(str(dia_hora))
        self.label_data.set_text(str(dia_data))
        return (self.label_data,self.label_horario)



    def on_btn_principal_clicked(self, event):
        SelectOption(self.language)
    def on_change_language_br(self, event):
        self.language = "pt_BR"
    
    def on_change_language_usa(self, event):
        self.language = "en_US"

    def gtk_style(self):
        css = b"""
        
        @import url("static/css/gtk.css");
        """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    

if __name__ == "__main__":
    app = CollBagSafe()
    Gtk.main()