import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf, GObject
import datetime
import time
from time import sleep
import calendar
import string
from controllers import Management
import PIL
from PIL import Image
from decimal import Decimal
import threading, _threading_local




class WindowWaitPayment(object):
    def __init__(self, args):
        self.args = args
        self.locacao = ''
        self.pagamento_ext = ''
        if "NOME" in args:
            self.locacao = self.args
        elif "SENHA" in args:
            self.pagamento_ext = self.args
        self.language = "pt_BR"
        self.gtk_style()
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/window_wait_payment.glade")
        self.builder.connect_signals({
            "gtk_main_quit": Gtk.main_quit,
        })
        self.window_payment = self.builder.get_object("window_wait_payment")
        self.spinner = self.builder.get_object("spinner")
        
        
        #self.spinner_coolbag.start()
        self.window_payment.fullscreen()
        self.window_payment.show()
        sleep(0.5)

        if self.locacao == '':
            self.window_payment.show()
            self.pagamento_extra(self.pagamento_ext)
        elif self.pagamento_ext == '':
            self.window_payment.show()
            self.efetuar_pagamento(self.locacao)
        
    

    
    def gtk_style(self):
        css = b"""
        
        @import url("static/css/gtk.css");
        """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    def efetuar_pagamento(self, locacao):
        self.window_payment.show()
        self.__armario = self.classe
        print("locacao", self.__quantidade_diaria, self.__quantidade_horas, self.__quantidade_minutos)
        manager = Management()
        self.__result =  manager.locacao(self.__nome, self.__email, self.__telefone, self.__quantidade_diaria, self.__quantidade_horas, self.__quantidade_minutos, self.__armario, self.language, self.valor_total)
        count = 0
        #self.__result = self.__result[0]
        print("self.__result cadastro usuario ", self.__result[0])
        if self.__result[0][0] == "locacao concluida com sucesso":
            dia_inicio_locacao = self.__result[0][1]
            print("dia_inicio cadastro usuario", dia_inicio_locacao)
            hora_inicio_locacao = self.__result[0][2]
            print("hora_inicio cadastro usuario", hora_inicio_locacao)
            data_fim_locacao = self.__result[0][3]
            print("data_fim cadastro usuario", data_fim_locacao)
            hora_fim_locacao = self.__result[0][4]
            print("hora_fim cadastro usuario", hora_fim_locacao)
            self.senha = self.__result[0][5]
            print("__senha cadastro usuario", self.senha)
            compartimento = self.__result[0][6]
            print("compartimento cadastro usuario", compartimento)
            
        
            self.label_date_inicio_locacao.set_text(dia_inicio_locacao)
            self.label_date_fim_locacao.set_text(data_fim_locacao)
            self.label_hour_inicio_locacao.set_text(hora_inicio_locacao)
            self.label_hour_fim_locacao.set_text(hora_fim_locacao)
            self.label_senha.set_text(str(self.senha))
            self.label_compartimento.set_text(str(compartimento))
            
            #self.window_payment.hide()
            self.window_payment.hide()
            self.window_conclusao.show()
            
            
            self.id_armario = manager.localiza_id_armario(self.senha)
            return self.id_armario
            
            
        elif self.__result[0] == "armario da classe escolhida indisponível":
            if self.language == "pt_BR":
                self.label_retorno_cadastro.set_text("tamanho de armario\n  escolhido indisponível")
                self.dialog_retorno_cadastro.show()
            elif self.language == "en_US":
                self.label_retorno_cadastro.set_text("chosen cabinet\n size unavailable")
                self.dialog_retorno_cadastro.show()
        else:
            self.window_payment.hide()
            self.label_window_erro_pagamentos.set_text(self.__result[0])
            self.window_erro_pagamento()
    
    def window_erro_pagamento(self):
        self.window_payment.hide()
        self.window_erro_pagamentos.show()
    
    def on_btn_tente_novamente_window_erro_pagamentos_button_press_event(self, widget, event):
        self.window_erro_pagamentos.hide()
        self.window_select_cartao.show()

    def on_btn_cancelar_window_erro_pagamentos_button_press_event(self, widget, event):
        self.window_erro_pagamentos.hide()
        self.window_payment.hide()
        self.window_select_cartao.hide()
    @classmethod
    def pagamento_extra(self, pagamento_ext):
        self.window_payment.show()
        pagamento_extra = pagamento_ext
        resultado = Management.pagamento_extra(pagamento_extra["VALOR_TOTAL"], pagamento_extra["SENHA"])
        print(resultado)
        if "aprovada" in resultado:
            self.window_payment.hide()
            self.window_conclusao.show()

if __name__ == "__main__":
    app = WindowWaitPayment()
    Gtk.main()