import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from datetime import datetime, date

class CadastroUsuarios(Gtk.Window):
    def __init__(self, tempo_locacao):
        self.tempo_locacao = tempo_locacao
        self.builder = Gtk.Builder()
        self.builder.connect_signals({
            "gtk_main_quit": Gtk.main_quit,
            "on_btn_confirmar_button_press_event": self.on_btn_confirmar_button_press_event,
            "on_btn_retornar_button_press_event": self.on_btn_retornar_button_press_event,
            "on_entry_nome_button_press_event": self.on_entry_nome_button_press_event,
            "on_entry_email_button_press_event": self.on_entry_email_button_press_event,
            "on_entry_celular_button_press_event": self.on_entry_celular_button_press_event,
            "on_entry_quantidade_diaria_button_press_event": self.on_entry_quantidade_diaria_button_press_event,
            "on_entry_quantidade_horas_button_press_event": self.on_entry_quantidade_horas_button_press_event,
            "on_entry_minutos_button_press_event": self.on_entry_minutos_button_press_event,
            "on_btn_limbar_nome_button_press_event": self.on_btn_limbar_nome_button_press_event,
            "on_btn_limbar_email_button_press_event": self.on_btn_limbar_email_button_press_event,
            "on_btn_limbar_celular_button_press_event": self.on_btn_limbar_celular_button_press_event,
            "on_btn_limpar_quantidade_diaria_button_press_event": self.on_btn_limpar_quantidade_diaria_button_press_event,
            "on_btn_limpar_horas_button_press_event": self.on_btn_limpar_horas_button_press_event,
        })
        self.builder.add_from_file("ui/cadastro_usuario.glade")
        self.window_cadastro_usuario = self.builder.get_object("window_cadastro_usuario")
        """ =================LABELS ====================="""

        self.label_nome = self.builder.get_object("label_nome")
        self.label_email = self.builder.get_object("label_email")
        self.label_telefone = self.builder.get_object("label_telefone")
        self.label_quantidade_diaria = self.builder.get_object("label_quantidade_diaria")
        self.label_quantidade_horas = self.builder.get_object("label_quantidade_horas")
        self.label_quantidade_minutos = self.builder.get_object("label_quantidade_minutos")
        
        """ ================FIM LABELS==================="""

        """ ================= ENTRYS ===================="""
        self.enty_nome = self.builder.get_object("entry_nome")
        self.entry_email = self.builder.get_object("entry_email")
        self.entry_telefone = self.builder.get_object("entry_telefone")
        self.entry_quantidade_diaria = self.builder.get_object("entry_quantidade_diaria")
        self.entry_quantidade_horas = self.builder.get_object("entry_quantidade_horas")
        self.entry_minutos = self.builder.get_object("entry_minutos")

        """ =================FIM ENTRYS==================="""

        """ =================BOTOES======================"""

        self.btn_limpar_nome = self.builder.get_object("btn_limpar_nome")
        self.btn_limpar_email = self.builder.get_object("btn_limpar_email")
        self.btn_limpar_telefone = self.builder.get_object("btn_limpar_telefone")
        self.btn_limpar_quantidade_diaria = self.builder.get_object("btn_limpar_quantidade_diaria")
        self.btn_limpar_horas = self.builder.get_object("btn_limpar_horas")
        self.btn_limpar_minutos = self.builder.get_object("btn_limpar_minutos")
        self.btn_confirmar = self.builder.get_object("btn_confirmar")
        self.btn_retornar = self.builder.get_object("btn_retornar")

        """ ================FIM BOTOES===================="""

        if self.tempo_locacao == "diaria":
            self.label_quantidade_horas.hide()
            self.label_quantidade_minutos.hide()
            self.entry_minutos.hide()
            self.entry_quantidade_horas.hide()
            self.btn_limpar_horas.hide()
            self.btn_limpar_minutos.hide()
        elif self.tempo_locacao == "horas":
            self.label_quantidade_diaria.hide()
            self.entry_quantidade_diaria.hide()
            self.btn_limpar_quantidade_diaria.hide()


        self.window_cadastro_usuario.show()

        def on_btn_confirmar_button_press_event(self, widget, event):
            __nome = self.entry_nome.get_text()
            __email = self.entry_email.get_text()
            __telefone = self.entry_telefone.get_text()
        
        def on_btn_retornar_button_press_event(self, widget, event):
            pass
        
        def on_entry_nome_button_press_event(self, widget, event):
            pass
        
        def on_entry_email_button_press_event(self, widget, event):
            pass
        
        def on_entry_celular_button_press_event(self, widget, event):
            pass
        
        def on_entry_quantidade_diaria_button_press_event(self, widget, event):
            pass
        
        def on_entry_quantidade_horas_button_press_event(self, widget, event):
            pass

        def on_entry_minutos_button_press_event(self, widget, event):
            pass
        
        def on_btn_limbar_nome_button_press_event(self, widget, event):
            pass
        
        def on_btn_limbar_email_button_press_event(self, widget, event):
            pass
        
        def on_btn_limbar_celular_button_press_event(self, widget, event):
            pass
        
        def on_btn_limpar_quantidade_diaria_button_press_event(self, widget, event):
            pass
        
        def on_btn_limpar_horas_button_press_event(self, widget, event):
            pass

        def

if __name__ == "__main__":
    CadastroUsuarios()


