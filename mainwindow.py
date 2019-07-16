import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class RaspControl(object):
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("index.glade")
        builder.connect_signals({
        "btn_locar_clicked_cb": self.btn_locar_clicked_cb,
        "gtk_widget_destroy": self.gtk_widget_destroy,
        "on_onpen": self.abrir,
        "gtk_main_quit": Gtk.main_quit
        })
        self.window = builder.get_object("main_window")
        self.locar = builder.get_object("locar_window")
        self.window.show()
        

       
    
    
    def gtk_widget_destroy(self, widget):
        self.locar.hide()
    
    def btn_locar_clicked_cb(self, widget):
        self.locar.show()

        
        
    def abrir(self, widget):
        pass
    
           





if __name__ == "__main__":
    app = RaspControl()
    Gtk.main()
