import gi
gi.require_versions({"Gtk": "3.0","Gio": "2.0"})
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf, GObject


class WindowConclusaoPagamento(Gtk.Window):
    def __init__(self, *args):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/window_conclusao_pagamento.glade")
        self.builder.connect_signals({
            "gtk_main_quit": Gtk.main_quit,
        })
        self.window_conclusao_pagamento = self.builder.get_object("window_conclusao_pagamento")
        self.window_conclusao_pagamento.show()
app = WindowConclusaoPagamento()
Gtk.main()