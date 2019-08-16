#!/usr/bin/env python3
# -*- coding: utf-8 -*- 


import sys, os

import gi
import numpy as np
import string
import encodings.unicode_escape
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from controllers import Management
from login import Login
from encerrar import Encerrar
from locar import Locar


class RaspControl(object):
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/coolbag_safe.glade")
        self.builder.connect_signals({
            "gtk_main_quit": Gtk.main_quit,
            "on_btn_principal_clicked": self.on_btn_principal_clicked,
        })
        self.main_window = self.builder.get_object("mainwindow")
        self.main_window.show()


    def on_btn_principal_clicked(self, event):
        print("ok")

if __name__ == "__main__":
    app = RaspControl()
    Gtk.main()