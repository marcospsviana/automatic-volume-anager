import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from  engine.portas import Portas

class WindowControleMotor:
    def __init__(self):
        self.p = Portas()
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/controle_motor.ui")
        self.builder.connect_signals(
            {
                "gtk_main_quit": Gtk.main_quit,
            }
        )
        self.window = self.builder.get_object("window_controle")
        self.window.set_title("CONTROLE MOTOR")
        self.btn_abrir = self.builder.get_object("btn_abrir")
        self.btn_fechar = self.builder.get_object("btn_fechar")

        self.btn_abrir.connect("button-press-event", self.on_btn_abrir_pressed)
        self.btn_fechar.connect("button-press-event", self.on_btn_fechar_pressed)
        self.window.show()
    
    def on_btn_abrir_pressed(self, event, args):
        self.p.exec_port("A0", "abre", "aberto")

    def on_btn_fechar_pressed(self, event, args):
        self.p.exec_port("A0", "fecha", "fechado")
        



if __name__ == "__main__":
    app = WindowControleMotor()
    Gtk.main()