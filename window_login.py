from controllers import Management
from window_wait_payment import WindowWaitPayment as WWP
from gi.repository import Gtk, Gdk
import gi
import string
import time
from time import sleep
gi.require_version('Gtk', '3.0')


class WindowLogin(Gtk.Window):
    def __init__(self, *args):
        self.opcao = args[0]
        self.language = args[1]
        self.screen = Gdk.Screen.get_default()
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/window_login.glade")
        self.builder.add_from_file("ui/window_select_cartao.glade")
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
            "on_btn_window_payment_wait_button_press_event": self.on_btn_window_payment_wait_button_press_event,
            #"on_button_fechar_armario_button_press_event": self.on_button_fechar_armario_button_press_event,
        })
        # ================ DIALOGS ==============================
        #self.dialog_cobranca = self.builder.get_object("dialog_cobranca")
        self.dialog_senha_incorreta = self.builder.get_object(
            "dialog_senha_incorreta")
        self.dialog_instrucao_fecha_armario = self.builder.get_object(
            "dialog_instrucao_fecha_armario")

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

        self.button_fechar_armario = self.builder.get_object(
            "button_fechar_armario")
        self.button_fechar_armario.connect(
            "button_press_event", self.on_button_fechar_armario_button_press_event)

        self.btn_efetuar_pagamento = self.builder.get_object(
            "btn_efetuar_pagamento")
        self.btn_efetuar_pagamento.connect(
            "button_press_event", self.on_btn_efetuar_pagamento_button_press_event)
        self.btn_encerrar_sessao = self.builder.get_object(
            "btn_encerrar_sessao")

        self.entry_entrada_dados = self.builder.get_object("entry_entrada_dados")
        self.btn_confirmar_entrada_dados = self.builder.get_object(
            "btn_confirmar_entrada_dados")
        self.btn_retornar_entrada_dados = self.builder.get_object(
            "btn_retornar_entrada_dados")
        self.btn_retornar_entrada_dados.connect(
            "clicked", self.on_btn_retornar_entrada_dados_pressed)
        self.btn_confirmar_entrada_dados.connect(
            "clicked", self.on_btn_confirmar_entrada_dados_pressed)

        self.btn_window_payment_wait = self.builder.get_object(
            "btn_window_payment_wait")
        self.btn_window_payment_wait.connect(
            "button_press_event", self.on_btn_window_payment_wait_button_press_event)
        self.btn_tentar_dialog_senha_incorreta = self.builder.get_object(
            "btn_tentar_dialog_senha_incorreta")
        self.btn_tentar_dialog_senha_incorreta.connect(
            "clicked", self.on_btn_tentar_dialog_senha_incorreta)
        self.btn_dialog_cancelar_senha_incorreta = self.builder.get_object(
            "btn_dialog_cancelar_senha_incorreta")
        self.btn_dialog_cancelar_senha_incorreta.connect(
            "clicked", self.on_btn_dialog_cancelar_senha_incorreta)

        # ========= LABELS =========================
        self.lbl_message = self.builder.get_object("lbl_message")
        self.label_dialog_senha_incorreta = self.builder.get_object(
            "label_dialog_senha_incorreta")
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

        self.label_instrucao = self.builder.get_object(
            "label_instrucao")

        # ================== SET LANGUAGE ===================================

        if self.language == "pt_BR":
            self.label_dialog_senha_incorreta.set_text(
                "SENHA INCORRETA,\n TENTE NOVAMENTE")
            self.label_locacao_inicial.set_text("LOCAÇÃO INICIAL")
            self.label_locacao_encerrada.set_text("LOCAÇÃO ENCERRADA ÀS")
            self.label_tempo_extra.set_text("TEMPO EXTRA")
            self.label_valor_extra.set_text("VALOR EXTRA")
            self.label_entrada_dados.set_text("SENHA")
            self.btn_efetuar_pagamento.set_label("EFETUAR PAGAMENTO")
            self.btn_confirmar_entrada_dados.set_label("CONFIRMAR")
            self.btn_retornar_entrada_dados.set_label("RETORNAR TELA ANTERIOR")
            self.btn_dialog_cancelar_senha_incorreta.set_label("CANCELAR")
            self.btn_tentar_dialog_senha_incorreta.set_label(
                "TENTAR NOVAMENTE")
            self.button_fechar_armario.set_label("FECHAR ARMÁRIO")
            self.label_instrucao.set_label("""
                    Após guardar todo o volume necessário,\n
                    empurre a porta sem forçar até encostar na trava,\n
                    depois para finalizar clique no botão abaixo com nome: FECHAR ARMÁRIO.\n
                    Observação: A responsabilidade de fechar o armário é do usuário,\n
                    caso esqueça de fechá-lo a empresa não se responsabilizará por perdas!
                    """
                                           )

        elif self.language == "en_US":
            self.label_dialog_senha_incorreta.set_text(
                "WRONG PASSWORD,\n TRY AGAIN")
            self.label_locacao_inicial.set_text("START DATE OF LEASE")
            self.label_locacao_encerrada.set_text("FINAL DATE OF LEASE")
            self.label_tempo_extra.set_text("TIME OVER")
            self.label_valor_extra.set_text("OVERTIME CHARGE")
            self.label_entrada_dados.set_text("PASSWORD")
            self.btn_efetuar_pagamento.set_label("PAYMENT")
            self.btn_confirmar_entrada_dados.set_label("CONFIRM")
            self.btn_retornar_entrada_dados.set_label("PREVIOUS SCREEN")
            self.btn_dialog_cancelar_senha_incorreta.set_label("CANCEL")
            self.btn_tentar_dialog_senha_incorreta.set_label("TRY AGAIN")
            self.button_fechar_armario.set_label("CLOSE CABINET")
            self.label_instrucao.set_label("""
                    After saving all the required volume,\n
                    push the door without force until it touches the lock,\n
                    then to finish click the button below with name: CLOSET CLOSER.\n
                    Note: It is the responsibility of the user to close the cabinet,\n
                    if you forget to close it the company will not be responsible for any losses!
                    """
                                            )
         # ======================== BOTOES TELA OPCAO CARTAO ======================
        self.btn_credito = self.builder.get_object("btn_credito")
        self.btn_credito.connect("button-press-event", self.on_btn_credito_button_press_event)
        self.btn_debito = self.builder.get_object("btn_debito")
        self.btn_debito.connect("button-press-event", self.on_btn_debito_button_press_event)
        self.btn_cancelar_escolha = self.builder.get_object("btn_cancelar_escolha")
        self.btn_cancelar_escolha.connect("button-press-event", self.on_btn_cancelar_button_press_event)

        # ========================= FIM OPCOES CARTAO ================================

        self.window_payment = self.builder.get_object("window_payment_wait")
        self.window_pagamento_extra = self.builder.get_object("window_pagamento_extra")
        self.window_select_cartao = self.builder.get_object("window_select_cartao")
        self.window_login = self.builder.get_object("window_login")
        self.window_login.show()

    def on_entry_button_press_event(self, widget):
        self.value = widget.get_label()
        self.text_entrada = self.entry_entrada_dados.get_text() + self.value
        self.entry_entrada_dados.set_text(self.text_entrada)
        self.entry_entrada_dados.set_position(-1)

    def on_btn_confirmar_entrada_dados_pressed(self, event):
        self.message = ''
        result = ''
        self.__senha = self.entry_entrada_dados.get_text()
        print(self.__senha)
        self.id_armario = self.manager.localiza_id_armario(self.__senha)
        
        if self.id_armario == []:
            result == 'senha incorreta, tente novamente'
        print("id_armario window login abrir", self.id_armario)
        if self.opcao == "abrir":
            #result = self.manager.abre_armario(self.id_armario)
            result = self.manager.abre_armario(self.__senha)
            if result == 'armario liberado':
                self.window_login.hide()
                self.entry_entrada_dados.set_text('')
                print('abrir')
                self.dialog_instrucao_fecha_armario.show()
            elif result == 'senha incorreta, tente novamente':
                # self.window_login.hide()
                self.entry_entrada_dados.set_text('')
                self.dialog_senha_incorreta.show()

            else:

                print("result window_login", result)
                # self.window_login.close()
                #result = dict(zip(result))
                self.__total = result["total"]
                #print(self.__total, result)

                locacao = result["data_locacao"]
                limite = result["tempo_locado"]
                print("locacao window_login", locacao)
                print(type(locacao))

                __dia_da_semana_locacao = result["dia_locacao"]
                __dia_da_semana_locado = result["dia_limite"]
                __hora_locacao = result["hora_locacao"]
                __hora_locado = result["hora_locado"]
                __dia_extra = result["dia_extra"]
                __hora_extra = result["hora_extra"]
                __minuto_extra = result["minuto_extra"]
                self.label_data_locacao_inicial.set_text(__dia_da_semana_locacao + " " +
                                                        str(locacao))  # locacao)[8:10] + "/" + str(locacao)[5:7])
                self.label_data_locacao_encerrada.set_text(__dia_da_semana_locado + " " +
                                                        str(limite))  # [8:10] + "/" + str(limite)[5:7])
                self.label_hour_locacao_inicial.set_text(str(__hora_locacao))
                self.label_hour_locacao_encerrada.set_text(str(__hora_locado))
                self.label_tempo_extra_days.set_text(str(__dia_extra))
                self.label_tempo_extra_hours.set_text(str(__hora_extra))
                self.label_tempo_extra_minutes.set_text(str(__minuto_extra))
                self.label_valor_extra_value.set_text("R$ " + result["total"])
                if float(result["total"]) <= 0.00:
                    resultado = self.manager.finalizar(self.__senha)
                    if resultado == 'armario liberado':
                        self.window_login.hide()
                        self.entry_entrada_dados.set_text('')
                        print('abrir')
                        self.dialog_instrucao_fecha_armario.show() # adicionar instrucao de fim de locacao
                else:
                    self.window_pagamento_extra.show()
            
        elif self.opcao == "encerrar":
            result = self.manager.finalizar(self.__senha)
            print('result login encerrar', result)
            if result == 'armario liberado':
                self.window_login.hide()
                self.entry_entrada_dados.set_text('')
                print('abrir')
                self.dialog_instrucao_fecha_armario.show()
            elif result == 'senha incorreta, tente novamente':
                # self.window_login.hide()
                self.entry_entrada_dados.set_text('')
                self.dialog_senha_incorreta.show()

            else:

                print("result window_login", result)
                # self.window_login.close()
                #result = dict(zip(result))
                self.__total = result["total"]
                #print(self.__total, result)

                locacao = result["data_locacao"]
                limite = result["tempo_locado"]
                print("locacao window_login", locacao)
                print(type(locacao))

                __dia_da_semana_locacao = result["dia_locacao"]
                __dia_da_semana_locado = result["dia_limite"]
                __hora_locacao = result["hora_locacao"]
                __hora_locado = result["hora_locado"]
                __dia_extra = result["dia_extra"]
                __hora_extra = result["hora_extra"]
                __minuto_extra = result["minuto_extra"]
                self.label_data_locacao_inicial.set_text(__dia_da_semana_locacao + " " +
                                                        str(locacao))  # locacao)[8:10] + "/" + str(locacao)[5:7])
                self.label_data_locacao_encerrada.set_text(__dia_da_semana_locado + " " +
                                                        str(limite))  # [8:10] + "/" + str(limite)[5:7])
                self.label_hour_locacao_inicial.set_text(str(__hora_locacao))
                self.label_hour_locacao_encerrada.set_text(str(__hora_locado))
                self.label_tempo_extra_days.set_text(str(__dia_extra))
                self.label_tempo_extra_hours.set_text(str(__hora_extra))
                self.label_tempo_extra_minutes.set_text(str(__minuto_extra))
                self.label_valor_extra_value.set_text("R$ " + result["total"])

                self.window_login.hide()
                self.window_pagamento_extra.show()
        return (self.__senha, self.id_armario)

    def on_btn_efetuar_pagamento_button_press_event(self, widget, event):
        """self.window_payment.show()
        retorno = self.manager.pagamento(self.__total, self.entry_entrada_dados.get_text())
        if retorno == "lk4thHG34=GKss0xndhe":

            self.wait_payment.hide()"""
        
        self.window_select_cartao.show()

    def on_btn_retornar_entrada_dados_pressed(self, event):
        self.entry_entrada_dados.set_text("")
        self.window_login.hide()

    def on_btn_backspace_button_press_event(self, widget, event):
        self.texto = self.entry_entrada_dados.get_text()
        self.texto = self.texto[:-1]
        self.entry_entrada_dados.set_text(self.texto)
        self.entry_entrada_dados.set_position(-1)

    def on_btn_window_payment_wait_button_press_event(self, widget, event):
        self.window_payment.hide()
        self.window_pagamento_extra.hide()
        self.window_login.hide()
        self.dialog_instrucao_fecha_armario.show()

    def on_btn_tentar_dialog_senha_incorreta(self, widget):
        self.dialog_senha_incorreta.hide()

    def on_btn_dialog_cancelar_senha_incorreta(self, widget):
        self.dialog_senha_incorreta.hide()
        self.window_login.hide()

    def wait_payment(self):
        self.window_payment.hide()

    def on_button_fechar_armario_button_press_event(self, *args):
        print("args button fechar window login", args)
        manager = Management()
        #id_armario = manager.localiza_id_armario(self.__senha)
        manager.fechar_armario(self.id_armario)
        self.dialog_instrucao_fecha_armario.hide()
    
    def select_cartao(self):
        if self.language == "pt_BR":
            
            self.btn_credito.set_label("CRÉDITO")
            self.btn_debito.set_label("DÉBITO")
            self.btn_cancelar_escolha.set_label("CANCELA")

        elif self.language == "en_US":
            self.btn_credito.set_label("CREDIT")
            self.btn_debito.set_label("DEBIT")
            self.btn_cancelar_escolha.set_label("CANCEL")
            
        self.window_select_cartao.show()
    def on_btn_credito_button_press_event(self, event, args):
        #self.send_tipo_cartao("CREDITO")
        self.window_select_cartao.hide()
        #self.window_payment.show()
        self.send_tipo_cartao("CREDITO")
        
        sleep(0.5)       

    def on_btn_debito_button_press_event(self, event, args):
        #self.send_tipo_cartao("DEBITO")
        self.window_select_cartao.hide()
        #self.window_payment.show()
        self.send_tipo_cartao("DEBITO")
        
        sleep(0.5)
         

    def on_btn_cancelar_button_press_event(self, event, args):
        self.window_select_cartao.hide()

    def send_tipo_cartao(self, tipo):
        
        print(tipo)
        total = self.__total
        print("total para json", total)
        total = total.replace('.','')
        print("total para json formatado", total)
        with open("engine/paygoWeb/comprovantes/valor_venda.json", "w+") as f:
            f.write('\n{  \n\n')
            f.write('"TOTAL": "%s",  \n'%(total))
            f.write('"LANGUAGE": "%s",  \n'%(self.language))
            f.write('"PWINFO_CARDTYPE": "%s"  \n'%(tipo))
            f.write('\n}  \n')
        #self.wait_payment()
        

       
        pagamento_extra = {
            "SENHA"         : self.__senha, 
            "VALOR_TOTAL"   : self.__total
        }
        self.window_select_cartao.hide()
        self.window_login.hide()
        self.window_pagamento_extra.hide()
        WWP(pagamento_extra)
        

if __name__ == "__main__":
    app = WindowLogin()
    Gtk.main()
