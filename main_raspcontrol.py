#!/usr/bin/env python3
# -*- coding: utf-8 -*- 


import sys, os
import datetime
import gi
import numpy as np
import string
import encodings.unicode_escape
gi.require_versions({'Gtk': '3.0', 'GLib': '2.0'})
from gi.repository import Gtk, Gdk, GLib
from datetime import datetime, date
from controllers import Management
from login import Login
from encerrar import Encerrar
from locar import Locar
from select_cabinet import SelectCabinet

class RaspControl(object):
    def __init__(self):
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
        GLib.timeout_add(1000, self.hora_certa)
        self.main_window.fullscreen()
        self.main_window.show()
    
    def hora_certa(self):
        dia = datetime.now()
        self.label_horario.set_text(str(dia.hour)+ ":" + str(dia.minute) + ":" + str(dia.second))
        self.label_data.set_text(str(dia.day)+"/"+str(dia.month))
        return (self.label_data,self.label_horario)



    def on_btn_principal_clicked(self, event):
        SelectCabinet()
    
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
    app = RaspControl()
    Gtk.main()