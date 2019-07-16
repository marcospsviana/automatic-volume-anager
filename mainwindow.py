import subprocess
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class RaspControl(object):
    def __init__(self):
        self.gtk_style()
        builder = Gtk.Builder()
        builder.add_from_file("index.glade")
        builder.connect_signals({
        "btn_locar_clicked_cb": self.btn_locar_clicked_cb,
        "entry_nome_activate_cb": self.entry_nome_activate_cb,
        "gtk_widget_destroy": self.gtk_widget_destroy,
        "gtk_widget_show": self.on_show_locacao,
        "gtk_widget_hide": self.on_hide_cursor,
        "on_onpen": self.abrir,
        "gtk_main_quit": Gtk.main_quit
        })
        self.window = builder.get_object("main_window")
        self.window.fullscreen()
        self.locar = builder.get_object("locar_window")
        self.teclado = builder.get_object("teclado")
        self.locacao = builder.get_object("locacao")
        self.entry_nome = builder.get_object("entry_nome")
        self.entry_nome.connect('focus-in-event', self.focus_in)
        self.entry_nome.connect('focus-out-event', self.focus_out)
        self.window.show()

    def focus_out(self, entry, event):
        subprocess.Popen(["pkill", "onboard"]) 
    
    def focus_in(self, entry, event):
        subprocess.Popen("onboard")

    def gtk_widget_destroy(self, widget):
        self.locar.hide()
    
    def btn_locar_clicked_cb(self, widget):
        self.locar.fullscreen()
        self.locar.show()
    def on_show_locacao(self, widget):
        self.locacao.show()
        
    
    def entry_nome_activate_cb(self, widget):
        self.teclado.show()
        

    def on_hide_cursor(self, widget):
        self.teclado.hide()    
        
    def abrir(self, widget):
        pass
    
    def gtk_style(self):
        css = b"""
        #btn_locar { color: #000000;  font-size: 32px;}
        #btn_abrir { color: #000000;  font-size: 32px;}
        #btn_encerrar { color: #000000;  font-size: 32px;}
        #locar_window { background-color: #fff}
        #btn_num{ background-color: red}
        #grid_teclado { font-size: 15px}
        """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    



if __name__ == "__main__":
    app = RaspControl()
    Gtk.main()
