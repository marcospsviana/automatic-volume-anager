import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from datetime import datetime, date
from cadastro_usuarios import CadastroUsuarios

class OpcaoHoraDiaria(object):
    def __init__(self, *args):
        teste = args
        print("op diaria", teste)
        self.classe = args[0]
        self.language = args[1]
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/locacar_hora_diaria.glade")
        self.window_hora_diaria = self.builder.get_object("window_op_hora_diaria")
        self.list_store_flags = self.builder.get_object("list_store_flags")
        self.builder.connect_signals(
            {
                "gtk_main_quit": Gtk.main_quit,
                "on_btn_loc_hora_button_press_event": self.on_btn_loc_hora_button_press_event,
                "on_btn_loc_diaria_button_press_event": self.on_btn_loc_diaria_button_press_event,
                "on_btn_tela_hora_diaria_button_press_event": self.on_btn_tela_hora_diaria_button_press_event,
            }
        )
        
        self.label_por_hora = self.builder.get_object("label_por_hora")
        self.label_por_diaria = self.builder.get_object("label_por_diaria")
        self.btn_tela_hora_diaria = self.builder.get_object("btn_tela_hora_diaria")
        self.btn_usa = self.builder.get_object("btn_usa")
        self.btn_br = self.builder.get_object("btn_br")

        self.btn_br.connect("clicked", self.on_change_language_br)
        self.btn_usa.connect("clicked", self.on_change_language_usa)
        if self.language == "pt_BR":
            self.label_por_hora.set_text("POR HORA")
            self.label_por_diaria.set_text("POR DIÁRIA")
            self.btn_tela_hora_diaria.set_label("RETORNAR TELA ANTERIOR")
        elif self.language == "en_US":
            self.label_por_hora.set_text("HOURLY")
            self.label_por_diaria.set_text("DAILY")
            self.btn_tela_hora_diaria.set_label("RETURN TO THE PREVIOUS SCREEN")

        self.window_hora_diaria.show()
    
    def on_btn_loc_hora_button_press_event(self, widget, event):
        tempo_locacao = "horas"
        CadastroUsuarios(tempo_locacao, self.classe, self.language)
        self.window_hora_diaria.hide()
    
    def on_btn_loc_diaria_button_press_event(self, widget, event):
        tempo_locacao = "diaria"
        CadastroUsuarios(tempo_locacao, self.classe, self.language)
        self.window_hora_diaria.hide()
    
    def on_btn_tela_hora_diaria_button_press_event(self, widget, event):
        self.window_hora_diaria.hide()
    
    def on_change_language_br(self, event):
        self.language = "pt_BR"
        self.label_por_hora.set_text("POR HORA")
        self.label_por_diaria.set_text("POR DIÁRIA")
        self.btn_tela_hora_diaria.set_label("RETORNAR TELA ANTERIOR")
    
    def on_change_language_usa(self, event):
        self.language = "en_US"
        self.label_por_hora.set_text("HOURLY")
        self.label_por_diaria.set_text("DAILY")
        self.btn_tela_hora_diaria.set_label("RETURN TO THE\n PREVIOUS SCREEN")

if __name__ == "__main__":
    app = OpcaoHoraDiaria()
    Gtk.main()