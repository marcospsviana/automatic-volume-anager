import gi 
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from controllers import Management

class MainWindowCad():
    def __init__(self, *args, **kwargs):
        builder = Gtk.Builder()
        builder.add_from_file("cadastros_armarios.glade")
        builder.connect_signals(
            {
                "gtk_main_quit": Gtk.main_quit,
                "on_btn_cadastrar_armario_button_press_event": self.on_btn_cadastrar_armario_button_press_event,
            }
        )
        
        self.window_cad = builder.get_object("cad_armarios_window")
        self.combo_classe = builder.get_object("combobox_classe")
        self.combo_coluna = builder.get_object("combobox_coluna")
        self.combo_nivel = builder.get_object("combobox_nivel")
        self.combo_terminal = builder.get_object("combobox_terminal")
        self.btn_cadastrar = builder.get_object("btn_cadastrar_armario")
        self.btn_cadastrar.connect("clicked", self.on_btn_cadastrar_armario_button_press_event)
        self.window_cad.show()

    def on_btn_cadastrar_armario_button_press_event(self, event):
        CLASSES = ["A", "B", "C", "D"]
        NIVEIS = ["SUPERIOR", "INFERIOR", "SUPERIOR DIREITA", "SUPERIOR ESQUERDA", "INFERIOR DIREITA", "INFERIOR ESQUERDA"]
        COLUNAS = list(map(lambda x: x, range(1,17)))
        TERMINAIS = ["OTHON PALACE HOTEL", "PORTO FUTURO HOTEL"]
        self.classe = CLASSES[self.combo_classe.get_active()]
        self.nivel = NIVEIS[self.combo_nivel.get_active()]
        self.coluna = COLUNAS[self.combo_coluna.get_active()]
        self.terminal = TERMINAIS[self.combo_terminal.get_active()]
        print(self.classe, self.nivel, self.coluna, self.terminal)
        manager = Management()
        result = manager.cad_armarios( self.classe, self.terminal, self.coluna, self.nivel)
        self.lbl_resultado.set_text(result)


        

if __name__ == "__main__":
    app = MainWindowCad()
    Gtk.main()