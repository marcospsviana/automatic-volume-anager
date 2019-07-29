import gi 
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MainWindowCad():
    def __init__(self, *args, **kwargs):
        
        window = Gtk.Window(title="Cadastro de Armários")
        window.connect('destroy', Gtk.main_quit)
        window.show()
        Gtk.main()

if __name__ == "__main__":
    MainWindowCad()