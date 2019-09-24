from controllers import Management
from window_wait_payment import WindowWaitPayment
from gi.repository import Gtk, Gdk
import gi
import string
import time
gi.require_version('Gtk', '3.0')


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
        # alfabeto para gerar o teclado
        self.alfa = list(string.ascii_uppercase)
        # números para o teclado numérico
        self.num = list(map(lambda x: x, range(10)))
        self.builder.connect_signals({
            "on_btn_retornar_entrada_dados_pressed": self.on_btn_retornar_entrada_dados_pressed,
            "on_btn_backspace_button_press_event": self.on_btn_backspace_button_press_event,
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

        self.btn_backspace = self.builder.get_object("btn_backspace")
        

        # ==============================================
        # ============================== BUTTONS =========================================

        self.btn_efetuar_pagamento = self.builder.get_object(
            "btn_efetuar_pagamento")
        self.btn_efetuar_pagamento.connect(
            "button_press_event", self.on_btn_efetuar_pagamento_button_press_event)
        self.btn_encerrar_sessao = self.builder.get_object(
            "btn_encerrar_sessao")

        self.entry = self.builder.get_object("entry_entrada_dados")
        self.btn_confirmar_entrada_dados = self.builder.get_object(
            "btn_confirmar_entrada_dados")
        self.btn_retornar_entrada_dados = self.builder.get_object(
            "btn_retornar_entrada_dados")
        self.btn_retornar_entrada_dados.connect(
            "clicked", self.on_btn_retornar_entrada_dados_pressed)
        self.btn_confirmar_entrada_dados.connect(
            "clicked", self.on_btn_confirmar_entrada_dados_pressed)

        # ========= LABELS =========================
        self.lbl_message = self.builder.get_object("lbl_message")
        self.label_locacao_inicial = self.builder.get_object(
            "label_locacao_inicial")
        self.label_data_locacao_inicial = self.builder.get_object(
            "label_data_locacao_inicial")
        self.label_hour_locacao_inicial = self.builder.get_object(
            "label_hour_locacao_inicial")
        self.label_locacao_encerrada = self.builder.get_object(
            "label_locacao_encerrada")
        self.label_data_locacao_encerrada = self.builder.get_object(
            "label_data_locacao_encerrada")
        self.label_hour_locacao_encerrada = self.builder.get_object(
            "label_hour_locacao_encerrada")
        self.label_tempo_extra = self.builder.get_object("label_tempo_extra")
        self.label_tempo_extra_days = self.builder.get_object(
            "label_tempo_extra_days")
        self.label_tempo_extra_hours = self.builder.get_object(
            "label_tempo_extra_hours")
        self.label_tempo_extra_minutes = self.builder.get_object(
            "label_tempo_extra_minutes")
        self.label_valor_extra = self.builder.get_object("label_valor_extra")
        self.label_valor_extra_value = self.builder.get_object(
            "label_valor_extra_value")
        self.label_tempo_extra_days = self.builder.get_object(
            "label_tempo_extra_days")
        self.label_tempo_extra_hours = self.builder.get_object(
            "label_tempo_extra_hours")
        self.label_tempo_extra_minutes = self.builder.get_object(
            "label_tempo_extra_minutes")
        
        self.label_entrada_dados = self.builder.get_object(
            "label_entrada_dados")

        # ================== SET LANGUAGE ===================================

        if self.language == "pt_BR":
            self.label_locacao_inicial.set_text("LOCAÇÃO INICIAL")
            self.label_locacao_encerrada.set_text("LOCAÇÃO ENCERRADA ÀS")
            self.label_tempo_extra.set_text("TEMPO EXTRA")
            self.label_valor_extra.set_text("VALOR EXTRA")
            self.label_entrada_dados.set_text("SENHA")
            self.btn_efetuar_pagamento.set_label("EFETUAR PAGAMENTO")
            self.btn_confirmar_entrada_dados.set_label("CONFIRMAR")
            self.btn_retornar_entrada_dados.set_label("RETORNAR TELA ANTERIOR")
        elif self.language == "en_US":
            self.label_locacao_inicial.set_text("START DATE OF LEASE")
            self.label_locacao_encerrada.set_text("FINAL DATE OF LEASE")
            self.label_tempo_extra.set_text("TIME OVER")
            self.label_valor_extra.set_text("OVERTIME CHARGE")
            self.label_entrada_dados.set_text("PASSWORD")
            self.btn_efetuar_pagamento.set_label("PAYMENT")
            self.btn_confirmar_entrada_dados.set_label("CONFIRM")
            self.btn_retornar_entrada_dados.set_label("PREVIOUS SCREEN")

        self.window_pagamento_extra = self.builder.get_object(
            "window_pagamento_extra")
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
            # self.window_login.hide()
            self.entry.set_text('')

            self.label_dialog_senha_incorreta.set_text(
                'senha incorreta, tente novamente')
            self.dialog_senha_incorreta.show()

        else:
            # self.window_login.close()
            __result = result[0]
            __data_locacao = result[1]
            __data_limite = result[2]
            __dia_da_semana_locacao = result[3]
            __dia_da_semana_locado = result[4]
            __hora_locacao = result[5]
            __hora_locado = result[6]
            __dia_extra = result[7]
            __hora_extra = result[8]
            __minuto_extra = result[9]
            self.label_data_locacao_inicial.set_text(
                str(__dia_da_semana_locacao[0]) + "  " + __data_locacao)
            self.label_data_locacao_encerrada.set_text(
                str(__dia_da_semana_locado[0]) + "  " + __data_limite)
            self.label_hour_locacao_inicial.set_text(__hora_locacao)
            self.label_hour_locacao_encerrada.set_text(__hora_locado)
            self.label_tempo_extra_days.set_text(str(__dia_extra))
            self.label_tempo_extra_hours.set_text(str(__hora_extra))
            self.label_tempo_extra_minutes.set_text(str(__minuto_extra))
            self.label_valor_extra_value.set_text("R$ " + str(__result))

            self.window_pagamento_extra.show()

           
    def on_btn_efetuar_pagamento_button_press_event(self, widget, event):
        WindowWaitPayment()

    def on_btn_retornar_entrada_dados_pressed(self, event):
        self.entry.set_text("")
        self.window_login.hide()

    def on_btn_backspace_button_press_event(self, widget, event):
        self.texto = self.entry.get_text()
        self.texto = self.texto[:-1]
        self.entry.set_text(self.texto)
        self.entry.set_position(-1)
        
    


if __name__ == "__main__":
    app = WindowLogin()
    Gtk.main()
