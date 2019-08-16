import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class SelectCabinet(object):
    def __init__(self):
        self.build = Gtk.Builder()
        self.build.add_from_file("ui/escolha.glade")
        self.build.connect_signals(
            {
                "gtk_main_quit": Gtk.main_quit,
                "on_box_iniciar_reserva_touch_event": self.on_box_iniciar_reserva_touch_event,
            }
        )
        self.select_cabinet = self.build.get_object("window_select")
        self.select_cabinet.show()

    def on_box_iniciar_reserva_touch_event(self, event):
        print("reservar")

if __name__ == "__main__":
    app = SelectCabinet()
    Gtk.main()