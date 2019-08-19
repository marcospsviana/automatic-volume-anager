import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from datetime import datetime, date

class CadastroUsuario(Gtk.Window):
    def __init__(self):
        self.builder = Gtk.Builder()
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


