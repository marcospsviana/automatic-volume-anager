import gi 
import string
import time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from controllers import Management


class WindowLogin(Gtk.Window):
    def __init__(self, *args):
        self.opcao = args[0]
        self.language = args[1]
        self.screen = Gdk.Screen.get_default()
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/window_login.glade")
        self.manager = Management()
        self.value = ''
        self.entrada = ''
        self.alfa = list(string.ascii_lowercase) # alfabeto para gerar o teclado
        self.num = list(map(lambda x: x, range(10))) # números para o teclado numérico
        self.builder.connect_signals({
            "on_btn_retornar_entrada_dados_pressed": self.on_btn_retornar_entrada_dados_pressed,
            "on_btn_shift_button_press_event": self.on_btn_shift_button_press_event,
            "on_btn_efetuar_pagamento_button_press_event": self.on_btn_efetuar_pagamento_button_press_event,
        })
        # ================ DIALOGS ==============================
        self.dialog_cobranca = self.builder.get_object("dialog_cobranca")
        # ======== BOTOES DO TECLADO ============================
        for alfabet in self.alfa:
            self.alfabet = self.builder.get_object(alfabet)
            self.alfabet.connect("clicked", self.on_entry_button_press_event)
        for num in self.num:
            self.number = self.builder.get_object("num_"+str(num))
            self.number.connect("clicked", self.on_entry_button_press_event)
        
        self.btn_shift = self.builder.get_object("btn_shift")
        self.btn_shift.connect("button_press_event", self.on_btn_shift_button_press_event)
        
        # ==============================================
        # ============================== BUTTONS =========================================

        self.btn_efetuar_pagamento = self.builder.get_object("btn_efetuar_pagamento")
        self.btn_efetuar_pagamento.connect("button_press_event", self.on_btn_efetuar_pagamento_button_press_event)
        self.btn_encerrar_sessao = self.builder.get_object("btn_encerrar_sessao")

        
        self.entry = self.builder.get_object("entry_entrada_dados")
        self.btn_confirmar_entrada_dados = self.builder.get_object("btn_confirmar_entrada_dados")
        self.btn_retornar_entrada_dados = self.builder.get_object("btn_retornar_entrada_dados")
        self.btn_retornar_entrada_dados.connect("clicked", self.on_btn_retornar_entrada_dados_pressed)
        self.btn_confirmar_entrada_dados.connect("clicked", self.on_btn_confirmar_entrada_dados_pressed)

        #========= LABELS =========================
        self.lbl_message = self.builder.get_object("lbl_message")
        self.label_locacao_inicial = self.builder.get_object("label_locacao_inicial")
        self.label_data_locacao_inicial = self.builder.get_object("label_data_locacao_inicial")
        self.label_hour_locacao_inicial = self.builder.get_object("label_hour_locacao_inicial")
        self.label_locacao_encerrada = self.builder.get_object("label_locacao_encerrada")
        self.label_data_locacao_encerrada = self.builder.get_object("label_data_locacao_encerrada")
        self.label_hour_locacao_encerrada = self.builder.get_object("label_hour_locacao_encerrada")
        self.label_tempo_extra = self.builder.get_object("label_tempo_extra")
        self.label_tempo_extra_days = self.builder.get_object("label_tempo_extra_days")
        self.label_tempo_extra_hours = self.builder.get_object("label_tempo_extra_hours")
        self.label_tempo_extra_minutes = self.builder.get_object("label_tempo_extra_minutes")
        self.label_valor_extra = self.builder.get_object("label_valor_extra")
        self.label_valor_extra_value = self.builder.get_object("label_valor_extra_value")

         # ================== SET LANGUAGE ===================================

        if self.language == "pt_BR":
            self.label_locacao_inicial.set_text("LOCAÇÃO INICIAL")
            self.label_locacao_encerrada.set_text("LOCAÇÃO ENCERRADA ÀS")
            self.label_tempo_extra.set_text("TEMPO EXTRA")
            self.label_valor_extra.set_text("VALOR EXTRA")
            self.btn_efetuar_pagamento.set_label("EFETUAR PAGAMENTO")
        elif self.language == "en_US":
            self.label_locacao_inicial.set_text("START DATE OF LEASE")
            self.label_locacao_encerrada.set_text("FINAL DATE OF LEASE")
            self.label_tempo_extra.set_text("TIME OVER")
            self.label_valor_extra.set_text("OVERTIME CHARGE")
            self.btn_efetuar_pagamento("PAYMENT")
        
        self.window_pagamento_extra = self.builder.get_object("window_pagamento_extra")
        self.window_login = self.builder.get_object("window_login")
        self.window_login.show()

        

    def on_entry_button_press_event(self, widget):
        self.value = widget.get_label()
        self.text_entrada = self.entry.get_text() + self.value
        self.entry.set_text(self.text_entrada)
        self.entry.set_position(-1)
    
    def on_btn_confirmar_entrada_dados_pressed(self, event):
        self.message = ''
        senha = self.entry.get_text()
        if self.opcao == "abrir":
            result = self.manager.abre_armario(senha)
        elif self.opcao == "encerrar":
            result = self.manager.liberar_armarios(senha)
        print('result login', result)
        if result == 'armario liberado':
            self.window_login.hide()
            self.entry.set_text('')
            print('abrir')
        elif result == 'senha incorreta, tente novamente':
            #self.window_login.hide()
            self.entry.set_text('')
            
             
            self.label_dialog_senha_incorreta.set_text('senha incorreta, tente novamente')
            self.dialog_senha_incorreta.show()
            
        else:
            #self.window_login.close()
            __result = result[0]
            __data_locacao = result[1] 
            __data_limite = result[2] 
            __dia_da_semana_locacao = result[3] 
            __dia_da_semana_locado = result[4]
            self.label_data_locacao_inicial.set_text(__data_locacao)
            

            print('ok fechou')
            self.message = str(__result)
            self.lbl_message.set_text(self.message)
            self.dialog_cobranca.show()
            result = ''

    def on_btn_retornar_entrada_dados_pressed(self, event):
        self.entry.set_text("")
        self.window_login.hide()
    
    def on_btn_shift_button_press_event(self, widget, event):

        
        for alfabet in self.alfa:
            print(self.alfabet.get_label())
            if self.a.get_label().islower():
               self.a.set_label("A")
            elif self.alfabet.get_label().isupper():
                self.alfabet.set_label(alfabet.lower())
        
        
    

if __name__ == "__main__":
    app = WindowLogin()
    Gtk.main()
    
