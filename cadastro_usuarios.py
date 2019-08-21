import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from datetime import datetime, date

class CadastroUsuarios(object):
    def __init__(self, tempo_locacao):
        self.tempo_locacao = tempo_locacao
        self.entry = ""
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
            "on_btn_limpar_nome_button_press_event": self.on_btn_limpar_nome_button_press_event,
            "on_btn_limpar_email_button_press_event": self.on_btn_limpar_email_button_press_event,
            "on_btn_limpar_celular_button_press_event": self.on_btn_limpar_celular_button_press_event,
            "on_btn_limpar_quantidade_diaria_button_press_event": self.on_btn_limpar_quantidade_diaria_button_press_event,
            "on_btn_limpar_horas_button_press_event": self.on_btn_limpar_horas_button_press_event,
            "on_btn_retornar_entrada_dados_button_release_event": self.on_btn_retornar_entrada_dados_button_release_event,
            "on_entry_entrada_dados_button_press_event": self.on_entry_entrada_dados_button_press_event,
        })
        self.builder.add_from_file("ui/cadastro_usuario.glade")
        self.window_cadastro_usuario = self.builder.get_object("window_cadastro_usuario")
        self.window_entrada_dados = self.builder.get_object("window_entrada_dados")
        """ =================LABELS ====================="""

        self.label_nome = self.builder.get_object("label_nome")
        self.label_email = self.builder.get_object("label_email")
        self.label_telefone = self.builder.get_object("label_telefone")
        self.label_quantidade_diaria = self.builder.get_object("label_quantidade_diaria")
        self.label_quantidade_horas = self.builder.get_object("label_quantidade_horas")
        self.label_quantidade_minutos = self.builder.get_object("label_quantidade_minutos")
        " ----------   LABEL ENTRADA_DADOS --------------"
        self.label_entrada_dados = self.builder.get_object("label_entrada_dados")
        
        """ ================FIM LABELS==================="""

        """ ================= ENTRYS ===================="""

        self.entry_nome = self.builder.get_object("entry_nome")
        self.entry_nome.connect("button_press_event", self.on_entry_nome_button_press_event)
        self.entry_email = self.builder.get_object("entry_email")
        self.entry_email.connect("button_press_event", self.on_entry_email_button_press_event)
        self.entry_celular = self.builder.get_object("entry_celular")
        self.entry_celular.connect("button_press_event", self.on_entry_celular_button_press_event)
        self.entry_quantidade_diaria = self.builder.get_object("entry_quantidade_diaria")
        self.entry_quantidade_diaria.connect("button_press_event", self.on_entry_celular_button_press_event)
        self.entry_quantidade_horas = self.builder.get_object("entry_quantidade_horas")
        self.entry_quantidade_horas.connect("button_press_event", self.on_entry_quantidade_horas_button_press_event)
        self.entry_minutos = self.builder.get_object("entry_minutos")
        self.entry_minutos.connect("button_press_event", self.on_entry_minutos_button_press_event)

        """ -----------ENTRY WINDOW_ENTRADA_DADOS ------------"""
        self.entry_entrada_dados = self.builder.get_object("entry_entrada_dados")
        self.entry_entrada_dados.connect("button_press_event", self.on_entry_entrada_dados_button_press_event)

        """ =================FIM ENTRYS=================== """

        """ =================BOTOES======================= """

        self.btn_limpar_nome = self.builder.get_object("btn_limpar_nome")
        self.btn_limpar_nome.connect("button_press_event", self.on_btn_limpar_nome_button_press_event)
        self.btn_limpar_email = self.builder.get_object("btn_limpar_email")
        self.btn_limpar_telefone = self.builder.get_object("btn_limpar_telefone")
        self.btn_limpar_quantidade_diaria = self.builder.get_object("btn_limpar_quantidade_diaria")
        self.btn_limpar_horas = self.builder.get_object("btn_limpar_horas")
        self.btn_limpar_minutos = self.builder.get_object("btn_limpar_minutos")
        self.btn_confirmar = self.builder.get_object("btn_confirmar")
        self.btn_retornar = self.builder.get_object("btn_retornar")

        " ----------- BOTOES ENTRADA_DADOS --------------- "
        self.btn_confirmar_entrada_dados = self.builder.get_object("btn_confirmar_entrada_dados")
        self.btn_retornar_entrada_dados = self.builder.get_object("btn_retornar_entrada_dados")
        self.btn_retornar_entrada_dados.connect("button_press_event", self.on_btn_retornar_entrada_dados_button_release_event)

        """ ================FIM BOTOES==================== """
        """ ===================GRIDS====================== """
        self.grid_numbers = self.builder.get_object("grid_numbers")

         '''adicionando os elementos do teclado ======================='''
        self.a = self.builder.get_object("a")
        self.a.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.b = self.builder.get_object("b")
        self.b.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.c = self.builder.get_object("c")
        self.c.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.d = self.builder.get_object("d")
        self.d.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.e = self.builder.get_object("e")
        self.e.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.f = self.builder.get_object("f")
        self.f.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.g = self.builder.get_object("g")
        self.g.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.h = self.builder.get_object("h")
        self.h.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.i = self.builder.get_object("i")
        self.i.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.j = self.builder.get_object("j")
        self.j.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.k = self.builder.get_object("k")
        self.k.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.l = self.builder.get_object("l")
        self.l.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.m = self.builder.get_object("m")
        self.m.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.n = self.builder.get_object("n")
        self.n.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.o = self.builder.get_object("o")
        self.o.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.p = self.builder.get_object("p")
        self.p.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.q = self.builder.get_object("q")
        self.q.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.r = self.builder.get_object("r")
        self.r.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.s = self.builder.get_object("s")
        self.s.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.t = self.builder.get_object("t")
        self.t.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.u = self.builder.get_object("u")
        self.u.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.v = self.builder.get_object("v")
        self.v.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.w = self.builder.get_object("w")
        self.w.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.x = self.builder.get_object("x")
        self.x.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.y = self.builder.get_object("y")
        self.y.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.z = self.builder.get_object("z")
        self.z.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.space = self.builder.get_object("space")
        """========== fim elementos do teclado  """

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
        __quantidade_diaria = self.entry_quantidade_diaria.get_text()
        __quantidade_horas = self.entry_quantidade_horas.get_text()
        __quantidade_minutos = self.entry_minutos.get_text()
    
    def on_btn_retornar_button_press_event(self, widget, event):
        pass
    
    def on_entry_nome_button_press_event(self, widget, event):
        self.entry = "1" #setando entrada para mudar o estado da janela de entrada de dados
        self.label_entrada_dados.set_text("NOME")
        self.grid_numbers.visible(False)
        self.window_entrada_dados.show()
        return self.entry
    
    def on_entry_email_button_press_event(self, widget, event):
        self.entry = "2"
        self.label_entrada_dados.set_text("EMAIL")
        self.window_entrada_dados.show()
        return self.entry
    
    def on_entry_celular_button_press_event(self, widget, event):
        self.entry = "3"
        self.label_entrada_dados.set_text("CELULAR")
        self.window_entrada_dados.show()
        return self.entry
    
    def on_entry_quantidade_diaria_button_press_event(self, widget, event):
        self.entry = "4"
        return self.entry
    
    def on_entry_quantidade_horas_button_press_event(self, widget, event):
        self.entry = "5"
        return self.entry

    def on_entry_minutos_button_press_event(self, widget, event):
        self.entry = "6"
        return self.entry
    
    def on_btn_limpar_nome_button_press_event(self, widget, event):
        self.entry_nome.set_text("")
        self.entry_nome.set_position(0)
    
    def on_btn_limpar_email_button_press_event(self, widget, event):
        pass
    
    def on_btn_limpar_celular_button_press_event(self, widget, event):
        pass
    
    def on_btn_limpar_quantidade_diaria_button_press_event(self, widget, event):
        pass
    
    def on_btn_limpar_horas_button_press_event(self, widget, event):
        pass
    
    def on_btn_retornar_entrada_dados_button_release_event(self, widget, event):
        self.entry_entrada_dados.set_text("")
        self.window_entrada_dados.hide()
    
    def on_entry_entrada_dados_button_press_event(self, widget, event):
        pass

if __name__ == "__main__":
    app = CadastroUsuarios()
    Gtk.main()


