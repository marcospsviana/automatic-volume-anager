import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Handler:
    
    def onDestroy(self, *args):
        Gtk.main_quit()
    
    def on_btn_locar_clicked(self, *args):
        armarios.run()
           



builder = Gtk.Builder()
builder.add_from_file("main_raspcontrol.glade")

builder.connect_signals(Handler())


window = builder.get_object("main_window")


window.show_all()

Gtk.main()
