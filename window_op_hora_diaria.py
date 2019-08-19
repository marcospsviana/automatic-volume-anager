import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from datetime import datetime, date

class OpcaoHoraDiaria(object):
    def __init__(self):
        self.build = Gtk.Builder()
        self.build.add_from_file("ui/locacar_hora_diaria.glade")
        self.window_hora_diaria = self.build.get_object("window_op_hora_diaria")
        self.build.connect_signals(
            {
                "gtk_main_quit": Gtk.main_quit,
                "on_btn_loc_hora_button_press_event": self.on_btn_loc_hora_button_press_event,
                "on_btn_loc_diaria_button_press_event": self.on_btn_loc_diaria_button_press_event,
            }
        )
        self.window_hora_diaria.show()
    
    def on_btn_loc_hora_button_press_event(self, widget, event):
        pass
    
    def on_btn_loc_diaria_button_press_event(self, widget, event):
        pass


if __name__ == "__main__":
    app = OpcaoHoraDiaria()
    Gtk.main()