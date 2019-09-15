import gi
gi.require_versions({"Gtk": "3.0","Gio": "2.0"})
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf, GObject
from controllers import Management


class WindowConclusaoPagamento(object):
    def __init__(self, *args):
        lista = args
        print("lista --- ",lista)
        self.__nome = args[0]
        self.__email = args[1]
        self.__telefone = args[2]
        self.__quantidade_diaria = args[3]
        self.__quantidade_horas = args[4]
        self.__quantidade_minutos = args[5]
        self.__armario = args[6]
        self.language = args[7]
        self.manager = Management()
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/window_conclusao_pagamento.glade")
        self.builder.connect_signals({
            "gtk_main_quit": Gtk.main_quit,
            "on_btn_efetuar_pagamento_button_press_event": self.on_btn_efetuar_pagamento_button_press_event,
        })
        
        # ============================== BUTTONS =========================================

        self.btn_efetuar_pagamento = self.builder.get_object("btn_efetuar_pagamento")
        self.btn_efetuar_pagamento.connect("button_press_event", self.on_btn_efetuar_pagamento_button_press_event)
        self.btn_encerrar_sessao = self.builder.get_object("btn_encerrar_sessao")

        # ============================== LABELS ==========================================

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
            self.btn_efetuar_pagamento("MAKE THE PAYMENT")


        self.window_conclusao_pagamento = self.builder.get_object("window_conclusao_pagamento")
        self.window_conclusao_pagamento.show()

    def on_btn_efetuar_pagamento_button_press_event(self, widget, event):
        manager = Management()
        result = manager.locacao(self.__nome, self.__email, self.__telefone, self.__quantidade_diaria, self.__quantidade_horas, self.__quantidade_minutos)
        print(result)    

if __name__ == "__main__":
    app = WindowConclusaoPagamento()
    Gtk.main()