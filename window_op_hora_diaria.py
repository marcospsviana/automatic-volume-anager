import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from datetime import datetime, date

class OpcaoHoraDiaria(object):
    def __init__(self):
        self.build = Gtk.Builder()
        self.build.add_from_file("ui/locacar_hora_diaria.glade")
        self.window_hora_diaria = self.build.get_object("window_op_hora_diaria")
        self.buid.connect_signals(
            {
                "gtk_main_quit": Gtk.main_quit,
            }
        )


if __name__ == "__main__":
    app = OpcaoHoraDiaria()
    Gtk.main()