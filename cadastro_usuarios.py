import gi
gi.require_versions({"Gtk": "3.0","Gio": "2.0"})
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf, GObject
from datetime import datetime, date, time
import string
from controllers import Management
import PIL
from PIL import Image
TAXA = 0.15

class CadastroUsuarios(object):
    def __init__(self, *args):
        teste = args
        print(teste)
        self.tempo_locacao = args[0]
        self.classe = args[1][0]
        self.language = args[2]
        print(self.classe)
        print(self.tempo_locacao)
        print(self.language)
        self.alfa = list(string.ascii_lowercase) # alfabeto para gerar o teclado
        self.num = list(map(lambda x: x, range(10))) # números para o teclado numérico
        self.entry = ""
        self.dia = self.hora = self.minuto = 0
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
        self.dialog_retorno_cadastro = self.builder.get_object("dialog_retorno_cadastro")
        """ =================LABELS ====================="""

        self.label_nome = self.builder.get_object("label_nome")
        self.label_email = self.builder.get_object("label_email")
        self.label_telefone = self.builder.get_object("label_celular")
        self.label_quantidade_diaria = self.builder.get_object("label_quantidade_diaria")
        self.label_quantidade_horas = self.builder.get_object("label_quantidade_horas")
        self.label_quantidade_minutos = self.builder.get_object("label_quantidade_minutos")
        self.label_total = self.builder.get_object("label_total")
        self.label_valor_da_locacao = self.builder.get_object("label_valor_da_locacao")

        " ----------   LABEL ENTRADA_DADOS --------------"
        self.label_entrada_dados = self.builder.get_object("label_entrada_dados")

        " ----------   LABEL ENTRADA NUMEROS ------------"
        self.label_entrada_numeros = self.builder.get_object("label_entrada_numeros")
        " ----------   LABEL DIALOGO RETORNO CADASTRO ---"
        self.label_retorno_cadastro = self.builder.get_object("label_retorno_cadastro")
        """ ================FIM LABELS==================="""

        """ ================= ENTRYS ===================="""

        self.entry_nome = self.builder.get_object("entry_nome")
        self.entry_nome.connect("button_press_event", self.on_entry_nome_button_press_event)
        self.entry_email = self.builder.get_object("entry_email")
        self.entry_email.connect("button_press_event", self.on_entry_email_button_press_event)
        self.entry_celular = self.builder.get_object("entry_celular")
        self.entry_celular.connect("button_press_event", self.on_entry_celular_button_press_event)
        self.entry_quantidade_diaria = self.builder.get_object("entry_quantidade_diaria")
        self.entry_quantidade_diaria.connect("button_press_event", self.on_entry_quantidade_diaria_button_press_event)
        self.entry_quantidade_horas = self.builder.get_object("entry_quantidade_horas")
        self.entry_quantidade_horas.connect("button_press_event", self.on_entry_quantidade_horas_button_press_event)
        self.entry_minutos = self.builder.get_object("entry_minutos")
        self.entry_minutos.connect("button_press_event", self.on_entry_minutos_button_press_event)

        """ -----------ENTRY WINDOW_ENTRADA_DADOS ------------"""
        self.entry_entrada_dados = self.builder.get_object("entry_entrada_dados")
        self.entry_entrada_dados.connect("button_press_event", self.on_entry_entrada_dados_button_press_event)
        """ -----------ENTRY WINDOW_ENTRADA_NUMEROS ---------"""
        self.entry_entrada_numeros = self.builder.get_object("entry_entrada_numeros")

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

        """ =================== BOTÃO DIALOGO RETORNO CADASTRO ===================="""
        self.btn_ok_dialog_retorno_cadastro = self.builder.get_object("btn_ok_dialog_retorno_cadastro")
        self.btn_ok_dialog_retorno_cadastro.connect("button_press_event", self.on_btn_ok_dialog_retorno_cadastro_pressed)
        """ ===================GRIDS====================== """
        self.grid_numbers = self.builder.get_object("grid_numbers")

        """ ========== adicionando os elementos do teclado ======================= """
        for alfabet in self.alfa:
            self.alfabet = self.builder.get_object("%s"%(alfabet))
            self.alfabet.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        for num in self.num:
            self.number = self.builder.get_object("num_%s"%(num))
            self.number.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        
        self.btn_espaco = self.builder.get_object("btn_espaco")
        self.btn_espaco.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.btn_gmail = self.builder.get_object("btn_gmail")
        self.btn_gmail.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.btn_outlook = self.builder.get_object("btn_outlook")
        self.btn_outlook.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.btn_yahoo = self.builder.get_object("btn_yahoo")
        self.btn_yahoo.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.btn_dot = self.builder.get_object("btn_dot")
        self.btn_dot.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.btn_dash = self.builder.get_object("btn_dash")
        self.btn_dash.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.btn_under = self.builder.get_object("btn_under")
        self.btn_under.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        """========== fim elementos do teclado  """
        """ ========= lista combobox ========= """
        #self.cell_renderer = Gtk.CellRendererPixbuf()
        self.cell_renderer_text = Gtk.CellRendererText()
        
        
        #FLAG_BR = GdkPixbuf.Pixbuf("static/images/flags_ddd/brasil.png")
        #FLAG_ALB = gtk_image_new_from_file("static/images/flags_ddd/albania.png")
        #print(type(FLAG_BR))
        FLAGS = [["Brasil"], ["Albania"]]
        self.list_flag_ddd = Gtk.ListStore(str)
        
        
        for f in range(len(FLAGS)):
            self.list_flag_ddd.append(FLAGS[f])
        #self.list_flag_ddd.append([pb])
       
        #self.combobox_flags_ddd = Gtk.ComboBox.new_with_model(self.list_flags)
        
        self.combobox_flags_ddd = self.builder.get_object("combobox_flags_ddd")
        self.combobox_flags_ddd.pack_start(self.cell_renderer_text, False)
        #self.combobox_flags_ddd.pack_start(self.cell_renderer, True)
        self.combobox_flags_ddd.set_property("model", self.list_flag_ddd)
        self.combobox_flags_ddd.add_attribute(self.cell_renderer_text,"text", 0)
        #self.combobox_flags_ddd.add_attribute(self.cell_renderer, "pixbuf", 1)
        self.combobox_flags_ddd.set_active(0)
        
        
        
    

        if self.tempo_locacao == "diaria":
            self.label_quantidade_horas.hide()
            self.label_quantidade_minutos.hide()
            self.entry_minutos.hide()
            self.entry_minutos.set_text("0")
            self.entry_quantidade_horas.hide()
            self.entry_quantidade_horas.set_text("0")
            self.btn_limpar_horas.hide()
            self.btn_limpar_minutos.hide()
        elif self.tempo_locacao == "horas":
            self.label_quantidade_diaria.hide()
            self.entry_quantidade_diaria.hide()
            self.entry_quantidade_diaria.set_text("0")
            self.btn_limpar_quantidade_diaria.hide()
        
        if self.language == "pt_BR":
            self.label_nome.set_text("NOME")
            self.label_telefone.set_text("CELULAR")
            self.label_quantidade_diaria.set_text("QUANTIDADE DIÁRIA") #daily amount
            self.label_quantidade_horas.set_text("QUANTIDADE DE HORAS") #quantity of hours
            self.label_quantidade_minutos.set_text("QUANTIDADE DE MINUTOS") #quantity of minutes
            self.label_valor_da_locacao.set_text("VALOR DA LOCAÇÃO R$")
            self.btn_confirmar.set_label("CONFIRMAR")
            self.btn_retornar.set_label("RETORNAR TELA ANTERIOR")
            self.btn_limpar_celular.set_label("LIMPAR")
            self.btn_limpar_email.set_label("LIMPAR")
            self.btn_limpar_horas.set_label("LIMPAR")
            self.btn_limpar_minutos.set_label("LIMPAR")
            self.btn_limpar_nome.set_label("LIMPAR")
            self.btn_limpar_quantidade_diaria.set_label("LIMPAR")
            self.btn_confirmar_entrada_dados.set_label("CONFIRMAR")
            self.btn_confirmar_entrada_numero.set_label("CONFIRMAR")
            self.btn_retornar_entrada_dados.set_label("RETORNAR TELA ANTERIOR")
            self.btn_retornar_entrada_numeros.set_label("RETORNAR TELA ANTERIOR")
            
        elif self.language == "en_US":
            self.label_nome.set_text("NAME")
            self.label_telefone.set_text("PHONE")
            self.label_quantidade_diaria.set_text("DAILY AMOUNT") 
            self.label_quantidade_horas.set_text("QUANTITY OF HOURS") 
            self.label_quantidade_minutos.set_text("QUANTITY OF MINUTES")
            self.label_valor_da_locacao.set_text("RENTAL VALUE R$")
            self.btn_confirmar.set_label("CONFIRM")
            self.btn_retornar.set_label("RETURN TO THE PREVIOUS SCREEN")
            self.btn_confirmar_entrada_dados.set_label("CONFIRM")
            self.btn_confirmar_entrada_numero.set_label("CONFIRM")
            self.btn_retornar_entrada_dados.set_label("RETURN TO THE PREVIOUS SCREEN")
            self.btn_retornar_entrada_numeros.set_label("RETURN TO THE PREVIOUS SCREEN")
            self.btn_limpar_celular.set_label("CLEAR")
            self.btn_limpar_email.set_label("CLEAR")
            self.btn_limpar_horas.set_label("CLEAR")
            self.btn_limpar_minutos.set_label("CLEAR")
            self.btn_limpar_nome.set_label("CLEAR")
            self.btn_limpar_quantidade_diaria.set_label("CLEAR")
        

         

        
        self.window_cadastro_usuario.fullscreen()
        self.window_cadastro_usuario.show()
    def on_btn_ok_dialog_retorno_cadastro_pressed(self, widget, event):
        self.dialog_retorno_cadastro.hide()
        self.window_cadastro_usuario.destroy()

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
        if self.entry_quantidade_diaria.get_text() == "":
            __quantidade_diaria = "0"
        else:
            __quantidade_diaria = self.entry_quantidade_diaria.get_text()
        if self.entry_quantidade_horas.get_text() == "":
            __quantidade_horas = "0"
        else:
            __quantidade_horas = self.entry_quantidade_horas.get_text()
        if self.entry_minutos.get_text() == "":
            __quantidade_minutos = "0"
        else:
            __quantidade_minutos = self.entry_minutos.get_text()
        print("qtd minutos ", __quantidade_minutos)
        __armario = self.classe
        print("locacao", __quantidade_diaria, __quantidade_horas, __quantidade_minutos)
        result =  manager.locacao(__nome, __email, __telefone, __quantidade_diaria, __quantidade_horas, __quantidade_minutos, __armario)
        print("result cadastro usuario ", result[0])
        if result[0] == "locacao concluida com sucesso":
            self.window_cadastro_usuario.hide()
        elif result[0] == "armario da classe escolhida indisponível":
            if self.language == "pt_BR":
                self.label_retorno_cadastro.set_text("tamanho de armario\n  escolhido indisponível")
                self.dialog_retorno_cadastro.show()
            elif self.language == "en_US":
                self.label_retorno_cadastro.set_text("chosen cabinet\n size unavailable")
                self.dialog_retorno_cadastro.show()


    def on_btn_retornar_button_press_event(self, widget, event):
        self.window_cadastro_usuario.hide()
        
    
    def on_entry_nome_button_press_event(self, widget, event):
        self.label_entrada_dados.set_text("NOME")
        self.window_entrada_dados.show()
        return (self.entry, self.label_entrada_dados)
    
    def on_entry_email_button_press_event(self, widget, event):
        self.label_entrada_dados.set_text("EMAIL")
        self.window_entrada_dados.show()
        return self.entry
    
    def on_entry_celular_button_press_event(self, widget, event):
        self.label_entrada_numeros.set_text("CELULAR")
        
        self.window_entrada_numeros.show()
        
    
    def on_entry_quantidade_diaria_button_press_event(self, widget, event):
        self.label_entrada_numeros.set_text("QUANTIDADE DIÁRIA")
        self.window_entrada_numeros.show()
        
    
    def on_entry_quantidade_horas_button_press_event(self, widget, event):
        self.label_entrada_numeros.set_text("QUANTIDADE HORAS")
        self.window_entrada_numeros.show()
        

    def on_entry_minutos_button_press_event(self, widget, event):
        self.label_entrada_numeros.set_text("QUANTIDADE MINUTOS")
        self.window_entrada_numeros.show()
        
    
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
        print("self.value entrada de dados ===> ",self.value)
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
        

        self.entry_entrada_dados.set_text("")
        self.window_entrada_dados.hide()
    
    def on_btn_confirmar_entrada_numero_button_press_event(self, widget, event):
        if self.label_entrada_numeros.get_text() == "CELULAR":
            self.ddd = self.combobox_flags_ddd.get_active()
            if self.ddd == 0:
                self.ddd = "+55 "
            elif self.ddd == 1:
                self.ddd = "+1 "
            self.entry_celular.set_text(self.ddd + self.text_entrada)
            self.entry_celular.set_position(-1)
        elif self.label_entrada_numeros.get_text() == "QUANTIDADE DIÁRIA":
            
            self.entry_quantidade_diaria.set_text(self.text_entrada)
            print("entry qtd diaria ===>",self.entry_quantidade_diaria.get_text())
            self.entry_quantidade_diaria.set_position(-1)
            
        elif self.label_entrada_numeros.get_text() == "QUANTIDADE HORAS":
            self.entry_quantidade_horas.set_text(self.text_entrada)
            print("entry qtd horas ===>",self.entry_quantidade_horas.get_text())
            self.entry_quantidade_horas.set_position(-1)
        elif self.label_entrada_numeros.get_text() == "QUANTIDADE MINUTOS":
            self.entry_minutos.set_text(self.text_entrada)
            self.entry_minutos.set_position(-1)
        self.dia = self.entry_quantidade_diaria.get_text() + ".0"
        self.dia = float(self.dia)
        self.dia = self.dia * 50
        self.hora = self.entry_quantidade_horas.get_text()
        self.hora = self.hora +".0"
        self.hora = float(self.hora) 
        self.hora = self.hora * 60 * TAXA
        self.minuto = self.entry_minutos.get_text()
        self.minuto = self.minuto + ".0"
        self.minuto = float(self.minuto) 
        self.minuto = self.minuto * TAXA
        self.total =  self.dia + self.hora + self.minuto
        print(self.total)
        
        self.label_total.set_text(str(self.total))
        self.entry_entrada_numeros.set_text("")
        self.window_entrada_numeros.hide()
    
    def on_btn_retornar_entrada_numeros_button_press_event(self, widget, event):
        self.window_entrada_numeros.hide()
    
    def on_entry_entrada_numeros_button_press_event(self, widget):
        self.widget = widget
        self.value = self.widget.get_label()
        self.text_entrada = self.entry_entrada_numeros.get_text() + self.value
        self.entry_entrada_numeros.set_text(self.text_entrada)
        self.entry_entrada_numeros.set_position(-1)


if __name__ == "__main__":
    app = CadastroUsuarios()
    Gtk.main()


