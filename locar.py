import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class Locar(object):
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("ui/locacao.glade")
        self.window_locacao = builder.get_object("locacao_window")
        self.window_locacao.fullscreen(True)
        self.window_locacao.show()

if __name__ == "__main__":
    Locar()