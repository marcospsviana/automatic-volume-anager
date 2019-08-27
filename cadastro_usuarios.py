import gi
gi.require_versions({"Gtk": "3.0","Gio": "2.0"})
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf
from datetime import datetime, date
from controllers import Management

class CadastroUsuarios(object):
    def __init__(self, *args):
        teste = args
        print(teste)
        self.tempo_locacao = args[0]
        self.classe = args[1]
        print(self.tempo_locacao)
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
            "on_btn_limpar_minutos_button_press_event": self.on_btn_limpar_minutos_button_press_event,
            "on_btn_retornar_entrada_dados_button_press_event": self.on_btn_retornar_entrada_dados_button_press_event,
            "on_entry_entrada_dados_button_press_event": self.on_entry_entrada_dados_button_press_event,
            "on_btn_confirmar_entrada_dados_button_press_event": self.on_btn_confirmar_entrada_dados_button_press_event,
            "on_btn_confirmar_entrada_numero_button_press_event": self.on_btn_confirmar_entrada_numero_button_press_event,
            "on_btn_retornar_entrada_numeros_button_press_event": self.on_btn_retornar_entrada_numeros_button_press_event,
            "on_entry_entrada_numeros_button_press_event": self.on_entry_entrada_numeros_button_press_event,
            
        })
        self.builder.add_from_file("ui/cadastro_usuario.glade")
        self.window_cadastro_usuario = self.builder.get_object("window_cadastro_usuario")
        self.window_entrada_dados = self.builder.get_object("window_entrada_dados")
        self.window_entrada_numeros = self.builder.get_object("window_entrada_numeros")
        """ =================LABELS ====================="""

        self.label_nome = self.builder.get_object("label_nome")
        self.label_email = self.builder.get_object("label_email")
        self.label_telefone = self.builder.get_object("label_telefone")
        self.label_quantidade_diaria = self.builder.get_object("label_quantidade_diaria")
        self.label_quantidade_horas = self.builder.get_object("label_quantidade_horas")
        self.label_quantidade_minutos = self.builder.get_object("label_quantidade_minutos")
        " ----------   LABEL ENTRADA_DADOS --------------"
        self.label_entrada_dados = self.builder.get_object("label_entrada_dados")

        " ----------   LABEL ENTRADA NUMEROS ------------"
        self.label_entrada_numeros = self.builder.get_object("label_entrada_numeros")
        
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
        self.btn_limpar_email.connect("button_press_event", self.on_btn_limpar_email_button_press_event)
        self.btn_limpar_celular = self.builder.get_object("btn_limpar_celular")
        self.btn_limpar_celular.connect("button_press_event", self.on_btn_limpar_celular_button_press_event)
        self.btn_limpar_quantidade_diaria = self.builder.get_object("btn_limpar_quantidade_diaria")
        self.btn_limpar_quantidade_diaria.connect("button_press_event", self.on_btn_limpar_quantidade_diaria_button_press_event)
        self.btn_limpar_horas = self.builder.get_object("btn_limpar_horas")
        self.btn_limpar_horas.connect("button_press_event", self.on_btn_limpar_horas_button_press_event)
        self.btn_limpar_minutos = self.builder.get_object("btn_limpar_minutos")
        self.btn_limpar_minutos.connect("button_press_event", self.on_btn_limpar_minutos_button_press_event)
        self.btn_confirmar = self.builder.get_object("btn_confirmar")
        self.btn_confirmar.connect("button_press_event", self.on_btn_confirmar_button_press_event)
        self.btn_retornar = self.builder.get_object("btn_retornar")
        self.btn_retornar.connect("button_press_event", self.on_btn_retornar_button_press_event)

        " ----------- BOTOES ENTRADA_DADOS --------------- "
        self.btn_confirmar_entrada_dados = self.builder.get_object("btn_confirmar_entrada_dados")
        self.btn_confirmar_entrada_dados.connect("button_press_event", self.on_btn_confirmar_entrada_dados_button_press_event)
        self.btn_retornar_entrada_dados = self.builder.get_object("btn_retornar_entrada_dados")
        self.btn_retornar_entrada_dados.connect("button_press_event", self.on_btn_retornar_entrada_dados_button_press_event)

        """ ================FIM BOTOES==================== """
        " ----------- BOTOES TELA ENTRADA NUMEROS --------- "
        self.btn_um = self.builder.get_object("btn_um")
        self.btn_um.connect("clicked", self.on_entry_entrada_numeros_button_press_event)
        self.btn_dois = self.builder.get_object("btn_dois")
        self.btn_dois.connect("clicked", self.on_entry_entrada_numeros_button_press_event)
        self.btn_tres = self.builder.get_object("btn_tres")
        self.btn_tres.connect("clicked", self.on_entry_entrada_numeros_button_press_event)
        self.btn_quatro = self.builder.get_object("btn_quatro")
        self.btn_quatro.connect("clicked", self.on_entry_entrada_numeros_button_press_event)
        self.btn_cinco = self.builder.get_object("btn_cinco")
        self.btn_cinco.connect("clicked", self.on_entry_entrada_numeros_button_press_event)
        self.btn_seis = self.builder.get_object("btn_seis")
        self.btn_seis.connect("clicked", self.on_entry_entrada_numeros_button_press_event)
        self.btn_sete = self.builder.get_object("btn_sete")
        self.btn_sete.connect("clicked", self.on_entry_entrada_numeros_button_press_event)
        self.btn_oito = self.builder.get_object("btn_oito")
        self.btn_oito.connect("clicked", self.on_entry_entrada_numeros_button_press_event)
        self.btn_nove = self.builder.get_object("btn_nove")
        self.btn_nove.connect("clicked", self.on_entry_entrada_numeros_button_press_event)
        self.btn_zero = self.builder.get_object("btn_zero")
        self.btn_zero.connect("clicked", self.on_entry_entrada_numeros_button_press_event)
        self.btn_confirmar_entrada_numero = self.builder.get_object("btn_confirmar_entrada_numero")
        self.btn_confirmar_entrada_numero.connect("button_press_event", self.on_btn_confirmar_entrada_numero_button_press_event )
        self.btn_retornar_entrada_numeros = self.builder.get_object("btn_retornar_entrada_numeros")
        self.btn_retornar_entrada_numeros.connect("button_press_event", self.on_btn_retornar_entrada_numeros_button_press_event)
        """ ===================GRIDS====================== """
        self.grid_numbers = self.builder.get_object("grid_numbers")

        """ ========== adicionando os elementos do teclado ======================= """
        self.num_1 = self.builder.get_object("num_1")
        self.num_1.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.num_2 = self.builder.get_object("num_2")
        self.num_2.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.num_3 = self.builder.get_object("num_3")
        self.num_3.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.num_4 = self.builder.get_object("num_4")
        self.num_4.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.num_5 = self.builder.get_object("num_5")
        self.num_5.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.num_6 = self.builder.get_object("num_6")
        self.num_6.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.num_7 = self.builder.get_object("num_7")
        self.num_7.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.num_8 = self.builder.get_object("num_8")
        self.num_8.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.num_9 = self.builder.get_object("num_9")
        self.num_9.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.num_0 = self.builder.get_object("num_0")
        self.num_0.connect("clicked", self.on_entry_entrada_dados_button_press_event)
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
        self.btn_espaco = self.builder.get_object("btn_espaco")
        self.btn_espaco.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.btn_gmail = self.builder.get_object("btn_gmail")
        self.btn_gmail.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.btn_outlook = self.builder.get_object("btn_outlook")
        self.btn_outlook.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.btn_yahoo = self.builder.get_object("btn_yahoo")
        self.btn_yahoo.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        """========== fim elementos do teclado  """
        """ ========= lista combobox ========= """
        self.cell_renderer = Gtk.CellRendererPixbuf()
        br = alb = Gtk.Image()
        
        FLAG_BR = ["static/images/flags_ddd/Flag_of_Brazil.svg"]
        FLAG_ALB = ["static/images/flags_ddd/Flag_of_Albania.svg"]
        FLAGS = [[FLAG_BR], [FLAG_ALB]]
        self.list_flag_ddd = Gtk.ListStore(Gtk.Image)
        
        
        for f in range(len(FLAGS)):
            self.list_flag_ddd.append(FLAGS[f])
        #self.list_flag_ddd.append([pb])
       
        #self.combobox_flags_ddd = Gtk.ComboBox.new_with_model(self.list_flags)
        
        self.combobox_flags_ddd = self.builder.get_object("combobox_flags_ddd")
        #self.combobox_flags_ddd.pack_start(self.cell_renderer, True)
        self.combobox_flags_ddd.set_property("model", self.list_flag_ddd)
        #self.combobox_flags_ddd.add_attribute(self.cell_renderer,"Brasil", 0)
        
        self.combobox_flags_ddd.set_active(0)
        #self.combobox_flags_ddd.add_attribute(self.cell_renderer, "GdkPixbuf", 0)
        
        
    

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

        
        self.window_cadastro_usuario.fullscreen()
        self.window_cadastro_usuario.show()

    def on_btn_confirmar_button_press_event(self, widget, event):
        if self.tempo_locacao == "horas":
            self.entry_quantidade_diaria.set_text("0")
        elif self.tempo_locacao == "diaria":
            self.entry_quantidade_horas.set_text("0")
            self.entry_minutos.set_text("0")
        manager = Management()
        __nome = self.entry_nome.get_text()
        __email = self.entry_email.get_text()
        __telefone = self.entry_celular.get_text()
        __quantidade_diaria = self.entry_quantidade_diaria.get_text()
        __quantidade_horas = self.entry_quantidade_horas.get_text()
        __quantidade_minutos = self.entry_minutos.get_text()
        print("locacao", __quantidade_diaria, __quantidade_horas, __quantidade_minutos)
        #result =  manager.locacao(__nome, __email, __telefone, __quantidade_diaria, __quantidade_horas, __quantidade_minutos)
        #return result

    def on_btn_retornar_button_press_event(self, widget, event):
        self.window_cadastro_usuario.hide()
    
    def on_entry_nome_button_press_event(self, widget, event):
        self.entry = "1" #setando entrada para mudar o estado da janela de entrada de dados
        self.label_entrada_dados.set_text("NOME")
        self.window_entrada_dados.show()
        return (self.entry, self.label_entrada_dados)
    
    def on_entry_email_button_press_event(self, widget, event):
        self.entry = "2"
        self.label_entrada_dados.set_text("EMAIL")
        self.window_entrada_dados.show()
        return self.entry
    
    def on_entry_celular_button_press_event(self, widget, event):
        self.entry = "3"
        self.label_entrada_numeros.set_text("CELULAR")
        
        self.window_entrada_numeros.show()
        return self.entry
    
    def on_entry_quantidade_diaria_button_press_event(self, widget, event):
        self.entry = "4"
        self.label_entrada_numeros.set_text("QUANTIDADE DIÁRIA")
        self.window_entrada_numeros.show()
        return self.entry
    
    def on_entry_quantidade_horas_button_press_event(self, widget, event):
        self.entry = "5"
        self.label_entrada_numeros.set_text("QUANTIDADE HORAS")
        self.window_entrada_numeros.show()
        return self.entry

    def on_entry_minutos_button_press_event(self, widget, event):
        self.entry = "6"
        self.label_entrada_numeros.set_text("QUANTIDADE MINUTOS")
        self.window_entrada_numeros.show()
        return self.entry
    
    def on_btn_limpar_nome_button_press_event(self, widget, event):
        self.entry_nome.set_text("")
        self.entry_nome.set_position(0)
    
    def on_btn_limpar_email_button_press_event(self, widget, event):
        self.entry_email.set_text("")
        self.entry_email.set_position(0)
    
    def on_btn_limpar_celular_button_press_event(self, widget, event):
        self.entry_celular.set_text("")
        self.entry_celular.set_position(0)
    
    def on_btn_limpar_quantidade_diaria_button_press_event(self, widget, event):
        self.entry_quantidade_diaria.set_text("")
        self.entry_quantidade_diaria.set_position(0)
    
    def on_btn_limpar_horas_button_press_event(self, widget, event):
        self.entry_quantidade_horas.set_text("")
        self.entry_quantidade_horas.set_position(0)
    
    def on_btn_limpar_minutos_button_press_event(self, widget, event):
        self.entry_minutos.set_text("")
        self.entry_minutos.set_position(0)
    
    def on_btn_retornar_entrada_dados_button_press_event(self, widget, event):
        self.entry_entrada_dados.set_text("")
        self.window_entrada_dados.hide()
    
    def on_entry_entrada_dados_button_press_event(self, widget):
        self.widget = widget
        self.value = self.widget.get_label()
        self.text_entrada = self.entry_entrada_dados.get_text() + self.value
        self.entry_entrada_dados.set_text(self.text_entrada)
        self.entry_entrada_dados.set_position(-1)
        
    def on_btn_confirmar_entrada_dados_button_press_event(self, widget, event):
        self.text_entrada = self.entry_entrada_dados.get_text()
        print(self.label_entrada_dados.get_text())
        if self.label_entrada_dados.get_text() == "NOME":
            self.entry_nome.set_text(self.text_entrada)
            self.entry_nome.set_position(-1)
        elif self.label_entrada_dados.get_text() == "EMAIL":
            self.entry_email.set_text(self.text_entrada)
            self.entry_email.set_position(-1)
        elif self.label_entrada_dados.get_text() == "CELULAR":
            self.entry_celular.set_text(self.text_entrada)
            self.entry_celular.set_position(-1)
            self.entry_celular.activate

        self.entry_entrada_dados.set_text("")
        self.window_entrada_dados.hide()
    
    def on_btn_confirmar_entrada_numero_button_press_event(self, widget, event):
        pass
    
    def on_btn_retornar_entrada_numeros_button_press_event(self, widget, event):
        self.window_entrada_numeros.hide()
    
    def on_entry_entrada_numeros_button_press_event(self, widget):
        self.widget = widget
        self.value = self.widget.get_label()
        self.text_entrada = self.entry_entrada_dados.get_text() + self.value
        self.entry_entrada_dados.set_text(self.text_entrada)
        self.entry_entrada_dados.set_position(-1)


if __name__ == "__main__":
    app = CadastroUsuarios()
    Gtk.main()


