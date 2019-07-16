import gi 
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Teclado(object):
    def __init__(self):
        self.winTeclado = Gtk.Window()
        self.winTeclado.connect("destroy", Gtk.main_quit)
        self.winTeclado.show()
        alfa = list(string.ascii_lowercase) # alfabeto para gerar o teclado
    
    
        num = list(map(lambda x: x, range(10))) # números para o teclado numérico
        


if __name__ == "__main__":
    app = Teclado()
    Gtk.main()