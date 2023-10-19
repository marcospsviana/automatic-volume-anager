import os

import gi

import op_hora_diaria
from cadastro_usuarios import CadastroUsuarios
from taxas import *

import locale
from datetime import datetime, timedelta


from controllers import Management
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk, GdkPixbuf, Gio, GLib, GObject, Gtk


class SelectHora(object):
    """docstring for SelectHora"""

    def __init__(self, *args):
        super(SelectHora, self).__init__()
        self.tempo_locacao = args[0]
        self.classe = args[1][0]
        self.language = args[2]
        if self.classe == 'A':
            self.taxa = TaxAndRates.TAXA_HORA_A.value
        elif self.classe == 'B':
            self.taxa = TaxAndRates.TAXA_HORA_B.value
        elif self.classe == 'C':
            self.taxa = TaxAndRates.TAXA_HORA_C.value
        elif self.classe == 'D':
            self.taxa = TaxAndRates.TAXA_HORA_D.value
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        self.gtk_style_calendario()
        self.diretorio = os.getcwd()
        self.builder = Gtk.Builder()
        self.builder.add_from_file('ui/w_select_hora.glade')
        self.builder.connect_signals(
            {
                'gtk_main_quit': Gtk.main_quit,
                'on_btn_diminui_hora_button_press_event': self.on_btn_diminui_hora_button_press_event,
                'on_btn_aumenta_hora_button_press_event': self.on_btn_aumenta_hora_button_press_event,
                'on_btn_retornar_select_hora_button_press_event': self.on_btn_retornar_select_hora_button_press_event,
                'on_btn_confirmar_select_hora_button_press_event': self.on_btn_confirmar_select_hora_button_press_event,
                'on_btn_diminui_minuto_button_press_event': self.on_btn_diminui_minuto_button_press_event,
                'on_btn_aumenta_minuto_button_press_event': self.on_btn_aumenta_minuto_button_press_event,
            }
        )
        self.select_hora_window = self.builder.get_object('w_select_hora')
        self.btn_diminui_hora = self.builder.get_object('btn_diminui_hora')
        self.btn_aumenta_hora = self.builder.get_object('btn_aumenta_hora')
        self.btn_diminui_minuto = self.builder.get_object('btn_diminui_minuto')
        self.btn_aumenta_minuto = self.builder.get_object('btn_aumenta_minuto')
        self.btn_retornar_select_hora = self.builder.get_object('btn_retornar_select_hora')
        self.btn_confirmar_select_hora = self.builder.get_object('btn_confirmar_select_hora')

        self.label_hora_ecolhida = self.builder.get_object('label_hora_ecolhida')
        # self.label_hora_ecolhida_up = self.builder.get_object("label_hora_ecolhida_up")
        # s#elf.label_hora_ecolhida_down = self.builder.get_object("label_hora_ecolhida_down")
        # self.label_minuto_ecolhido = self.builder.get_object("label_minuto_ecolhido")
        # self.gtk_treeview_lista_horas = self.builder.get_object("gtk_treeview_lista_horas")
        self.label_data_hora_inicial = self.builder.get_object('label_data_hora_inicial')
        self.label_data_hora_final = self.builder.get_object('label_data_hora_final')

        self.data_atual = datetime.now()
        hora = self.data_atual + timedelta(hours=1)
        self.hora_acrescida = [hora.hour, self.data_atual.minute]
        # self.label_hora_ecolhida_up.set_text("2 horas")

        # self.label_minuto_ecolhido.set_text(self.data_atual.strftime("%M"))
        self.label_data_hora_inicial.set_text(self.data_atual.strftime('%d/%m/%Y - %H:%M'))
        self.label_data_hora_final.set_text(hora.strftime('%d/%m/%Y - %H:%M'))
        self.label_periodo_do = self.builder.get_object('label_periodo_do')
        self.label_definir_prazo = self.builder.get_object('label_definir_prazo')
        self.label_valor_total = self.builder.get_object('label_valor_total')
        self.label_ate = self.builder.get_object('label_ate')
        self.label_valor_total_horas = self.builder.get_object('label_valor_total_horas')
        self.label_valor_total_horas.set_text('R$ ' + str(self.taxa))

        if self.language == 'pt_BR':
            self.label_periodo_do.set_text('Período do')
            self.label_definir_prazo.set_text('Definir o Prazo')
            self.label_valor_total.set_text('Valor total')
            self.label_ate.set_text('até')
            self.btn_retornar_select_hora.set_label('TELA ANTERIOR')
            self.btn_confirmar_select_hora.set_label('CONFIRMAR')
        elif self.language == 'en_US':
            self.label_periodo_do.set_text('Start Time')
            self.label_definir_prazo.set_text('Set the Time')
            self.label_valor_total.set_text('Total price')
            self.label_ate.set_text('End Time')
            self.btn_retornar_select_hora.set_label('PREVIOUS SCREEN')
            self.btn_confirmar_select_hora.set_label('CONFIRM')
        if self.language == 'pt_BR':
            # self.btn_aumenta_hora.set_label("23 horas")
            self.label_hora_ecolhida.set_text('1 hora')
            # self.label_hora_ecolhida_down.set_text("23 horas")
            # self.btn_diminui_hora.set_label("2 horas")
            self.horas = {
                '1 hora': 1,
                '2 horas': 2,
                '3 horas': 3,
                '4 horas': 4,
                '5 horas': 5,
                '6 horas': 6,
                '7 horas': 7,
                '8 horas': 8,
                '9 horas': 9,
                '10 horas': 10,
                '11 horas': 11,
                '12 horas': 12,
                '13 horas': 13,
                '14 horas': 14,
                '15 horas': 15,
                '16 horas': 16,
                '17 horas': 17,
                '18 horas': 18,
                '19 horas': 19,
                '20 horas': 20,
                '21 horas': 21,
                '22 horas': 22,
                '23 horas': 23,
            }
            self.hora_labels = [
                '1 hora',
                '2 horas',
                '3 horas',
                '4 horas',
                '5 horas',
                '6 horas',
                '7 horas',
                '8 horas',
                '9 horas',
                '10 horas',
                '11 horas',
                '12 horas',
                '13 horas',
                '14 horas',
                '15 horas',
                '16 horas',
                '17 horas',
                '18 horas',
                '19 horas',
                '20 horas',
                '21 horas',
                '22 horas',
                '23 horas',
            ]
            self.horas_ad = {
                0: '1 hora',
                1: '2 horas',
                2: '3 horas',
                3: '4 horas',
                4: '5 horas',
                5: '6 horas',
                6: '7 horas',
                7: '8 horas',
                8: '9 horas',
                9: '10 horas',
                10: '11 horas',
                11: '12 horas',
                12: '13 horas',
                13: '14 horas',
                14: '15 horas',
                15: '16 horas',
                16: '17 horas',
                17: '18 horas',
                18: '19 horas',
                19: '20 horas',
                20: '21 horas',
                21: '22 horas',
                22: '23 horas',
            }
        elif self.language == 'en_US':
            # self.btn_aumenta_hora.set_label("23 hours")
            self.label_hora_ecolhida.set_text('1 hour')
            # self.label_hora_ecolhida_down.set_text("23 horas")
            # self.btn_diminui_hora.set_label("2 hours")
            self.horas = {
                '1 hour': 1,
                '2 hours': 2,
                '3 hours': 3,
                '4 hours': 4,
                '5 hours': 5,
                '6 hours': 6,
                '7 hours': 7,
                '8 hours': 8,
                '9 hours': 9,
                '10 hours': 10,
                '11 hours': 11,
                '12 hours': 12,
                '13 hours': 13,
                '14 hours': 14,
                '15 hours': 15,
                '16 hours': 16,
                '17 hours': 17,
                '18 hours': 18,
                '19 hours': 19,
                '20 hours': 20,
                '21 hours': 21,
                '22 hours': 22,
                '23 hours': 23,
            }

            self.hora_labels = [
                '1 hour',
                '2 hours',
                '3 hours',
                '4 hours',
                '5 hours',
                '6 hours',
                '7 hours',
                '8 hours',
                '9 hours',
                '10 hours',
                '11 hours',
                '12 hours',
                '13 hours',
                '14 hours',
                '15 hours',
                '16 hours',
                '17 hours',
                '18 hours',
                '19 hours',
                '20 hours',
                '21 hours',
                '22 hours',
                '23 hours',
            ]
            self.horas_ad = {
                0: '1 hour',
                1: '2 hours',
                2: '3 hours',
                3: '4 hours',
                4: '5 hours',
                5: '6 hours',
                6: '7 hours',
                7: '8 hours',
                8: '9 hours',
                9: '10 hours',
                10: '11 hours',
                11: '12 hours',
                12: '13 hours',
                13: '14 hours',
                14: '15 hours',
                15: '16 hours',
                16: '17 hours',
                17: '18 hours',
                18: '19 hours',
                19: '20 hours',
                20: '21 hours',
                21: '22 hours',
                22: '23 hours',
            }

        """store = Gtk.ListStore(str)
        dados_horas = [["1 hora"]  , ["2 horas"] ,["3 horas"] ,["4 horas"] ,["5 horas"] , ["6 horas"] , ["7 horas"] , ["8 horas"] , ["9 horas"] ,
        ["10 horas"], ["11 horas"], ["12 horas"], ["13 horas"], ["14 horas"], ["15 horas"], ["16 horas"], ["17 horas"], ["18 horas"],
        ["19 horas"], ["20 horas"], ["21 horas"], ["22 horas"], ["23 horas"],]"""

        self.select_hora_window.show()

    def on_btn_aumenta_hora_button_press_event(self, event, arg):
        data = datetime.now()
        data = data + timedelta(hours=1)
        self.label_data_hora_final.set_text(data.strftime('%d/%m/%Y - %H:%M'))
        hora_total = self.label_hora_ecolhida.get_label()
        print('hora_total', hora_total)

        hora = self.horas[hora_total]
        print('hora', hora)
        # hora -= 2
        print('hora -1', hora)
        """if hora == 22:
                                    hora = 0
                                else:"""
        hora -= 2

        self.label_hora_ecolhida.set_text(self.hora_labels[hora])
        # self.btn_aumenta_hora.set_label(self.hora_labels[hora -1])
        # self.btn_diminui_hora.set_label(self.hora_labels[hora + 1])
        total_atual = self.label_valor_total_horas.get_label()
        total_atual = total_atual.replace(',', '.')
        total = float(self.horas[self.label_hora_ecolhida.get_label()]) * self.taxa
        total = str('%.2f' % total)
        total = total.replace('.', ',')
        self.label_valor_total_horas.set_text('R$ ' + total)

        data_final = data + timedelta(hours=int(self.horas[self.label_hora_ecolhida.get_label()]))
        self.label_data_hora_inicial.set_text(data.strftime('%d/%m/%Y - %H:%M'))
        self.label_data_hora_final.set_text(data_final.strftime('%d/%m/%Y - %H:%M'))

    def on_btn_diminui_hora_button_press_event(self, event, arg):
        data = datetime.now()
        data = data + timedelta(hours=1)
        self.label_data_hora_final.set_text(data.strftime('%d/%m/%Y - %H:%M'))
        hora_total = self.label_hora_ecolhida.get_label()
        hora = 0
        hora = self.horas[hora_total]
        hora = hora - 1
        if hora == 22:
            hora = 0
        else:
            hora += 1
        self.label_hora_ecolhida.set_text(self.horas_ad[hora])
        # self.label_hora_ecolhida_up.set_text(self.hora_labels[hora + 1])
        # self.label_hora_ecolhida_down.set_text(self.hora_labels[hora - 1])
        # if self.label_hora_ecolhida.get_label() == "23 horas" or self.label_hora_ecolhida.get_label() == "23 hours":
        # self.btn_diminui_hora.set_label(self.hora_labels[0])
        # self.btn_aumenta_hora.set_label(self.hora_labels[hora - 1])
        # else:
        # self.btn_diminui_hora.set_label(self.hora_labels[hora + 1])
        # self.btn_aumenta_hora.set_label(self.hora_labels[hora - 1])

        total = float(self.horas[self.label_hora_ecolhida.get_label()]) * self.taxa   # + float(total_atual)
        total = str('%.2f' % total)
        total = total.replace('.', ',')
        self.label_valor_total_horas.set_text('R$ ' + total)
        data_final = data + timedelta(hours=int(self.horas[self.label_hora_ecolhida.get_label()]))
        self.label_data_hora_inicial.set_text(data.strftime('%d/%m/%Y - %H:%M'))
        self.label_data_hora_final.set_text(data_final.strftime('%d/%m/%Y - %H:%M'))

    def on_btn_diminui_minuto_button_press_event(self, event, arg):
        pass

    def on_btn_aumenta_minuto_button_press_event(self, event, arg):
        pass

    def on_btn_retornar_select_hora_button_press_event(self, event, arg):
        # self.label_valor_total_value.set_text("")
        self.select_hora_window.hide()
        op_hora_diaria.OpcaoHoraDiaria(self.classe, self.language)

    def on_btn_confirmar_select_hora_button_press_event(self, event, arg):
        self.total = self.label_valor_total_horas.get_text()
        self.total = self.total[3:]
        print(self.total)
        self.hora = self.horas[self.label_hora_ecolhida.get_label()]
        dia = 0
        self.select_hora_window.hide()
        CadastroUsuarios(self.total, self.language, self.classe, dia, self.hora)

    def gtk_style_calendario(self):
        css = b"""
        @import url("static/css/calendario.css");
        """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )
