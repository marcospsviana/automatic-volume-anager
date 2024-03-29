import os

import gi

import window_op_hora_diaria
from cadastro_usuarios import CadastroUsuarios
from taxas import *

import calendar
import locale
from datetime import datetime, timedelta


from controllers import Management
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk, GdkPixbuf, Gio, GLib, GObject, Gtk


class WindowCalendario:
    def __init__(self, *args):
        # op_and_language = args
        # print("op diaria", teste)
        self.resultado_dias = 0
        self.total_horas = 0
        self.tempo_locacao = args[0]
        self.classe = args[1][0]
        self.language = args[2]
        if self.classe == 'A':
            self.taxa = TaxAndRates.TAXA_DIARIA_A.value
        elif self.classe == 'B':
            self.taxa = TaxAndRates.TAXA_DIARIA_B.value

        elif self.classe == 'C':
            self.taxa = TaxAndRates.TAXA_DIARIA_C.value

        elif self.classe == 'D':
            self.taxa = TaxAndRates.TAXA_DIARIA_D.value

        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        self.builder = Gtk.Builder()
        self.gtk_style_calendario()
        self.builder.add_from_file('ui/calendario_window.glade')
        self.builder.connect_signals(
            {
                'on_btn_button_press_event': self.on_btn_button_press_event,
                'on_btn_previous_mont_button_press_event': self.on_btn_previous_mont_button_press_event,
                'on_btn_next_month_button_press_event': self.on_btn_next_month_button_press_event,
                # "on_btn_previous_year_button_press_event" : self.on_btn_previous_year_button_press_event,
                # "on_btn_next_year_button_press_event"     : self.on_btn_next_year_button_press_event,
                'on_btn_confirmar_calendario_button_press_event': self.on_btn_confirmar_calendario_button_press_event,
                'on_btn_cancelar_calendario_button_press_event': self.on_btn_cancelar_calendario_button_press_event,
                'gtk_main_quit': self.on_calendario_window_quit,
            }
        )
        self.calendario_window = self.builder.get_object('calendario_window')

        # ===================== LABELS ========================
        self.label_month = self.builder.get_object('label_month')
        # self.label_year = self.builder.get_object("label_year")
        self.label_valor_total_value = self.builder.get_object('label_valor_total_value')
        self.label_valor_total = self.builder.get_object('label_valor_total')

        self.label_data_hora_inicial = self.builder.get_object('label_data_hora_inicial')
        self.label_data_hora_final = self.builder.get_object('label_data_hora_final')
        self.label_ate = self.builder.get_object('label_ate')
        self.label_periodo_do = self.builder.get_object('label_periodo_do')

        # ===================== BUTTONS ========================
        self.btn_previous_mont = self.builder.get_object('btn_previous_mont')
        self.btn_next_mont = self.builder.get_object('btn_next_mont')
        # self.btn_previous_year = self.builder.get_object("btn_previous_year")
        # self.btn_next_year = self.builder.get_object("btn_next_year")

        self.btn_confirmar_calendario = self.builder.get_object('btn_confirmar_calendario')
        self.btn_cancelar_calendario = self.builder.get_object('btn_cancelar_calendario')
        # self.btn_confirmar.connect("button_press_event", self.on_btn_confirmar_button_press_event)

        self.btn0 = self.builder.get_object('btn0')
        self.btn1 = self.builder.get_object('btn1')
        self.btn2 = self.builder.get_object('btn2')
        self.btn3 = self.builder.get_object('btn3')
        self.btn4 = self.builder.get_object('btn4')
        self.btn5 = self.builder.get_object('btn5')
        self.btn6 = self.builder.get_object('btn6')
        self.btn7 = self.builder.get_object('btn7')
        self.btn8 = self.builder.get_object('btn8')
        self.btn9 = self.builder.get_object('btn9')
        self.btn10 = self.builder.get_object('btn10')
        self.btn11 = self.builder.get_object('btn11')
        self.btn12 = self.builder.get_object('btn12')
        self.btn13 = self.builder.get_object('btn13')
        self.btn14 = self.builder.get_object('btn14')
        self.btn15 = self.builder.get_object('btn15')
        self.btn16 = self.builder.get_object('btn16')
        self.btn17 = self.builder.get_object('btn17')
        self.btn18 = self.builder.get_object('btn18')
        self.btn19 = self.builder.get_object('btn19')
        self.btn20 = self.builder.get_object('btn20')
        self.btn21 = self.builder.get_object('btn21')
        self.btn22 = self.builder.get_object('btn22')
        self.btn23 = self.builder.get_object('btn23')
        self.btn24 = self.builder.get_object('btn24')
        self.btn25 = self.builder.get_object('btn25')
        self.btn26 = self.builder.get_object('btn26')
        self.btn27 = self.builder.get_object('btn27')
        self.btn28 = self.builder.get_object('btn28')
        self.btn29 = self.builder.get_object('btn29')
        self.btn30 = self.builder.get_object('btn30')
        self.btn31 = self.builder.get_object('btn31')
        self.btn32 = self.builder.get_object('btn32')
        self.btn33 = self.builder.get_object('btn33')
        self.btn34 = self.builder.get_object('btn34')
        self.btn35 = self.builder.get_object('btn35')
        self.btn36 = self.builder.get_object('btn36')
        self.btn37 = self.builder.get_object('btn37')
        self.btn38 = self.builder.get_object('btn38')
        self.btn39 = self.builder.get_object('btn39')
        self.btn40 = self.builder.get_object('btn40')
        self.btn41 = self.builder.get_object('btn41')

        self.data = datetime.now()
        self.date_calendar = calendar.Calendar()
        self.meses_indices = {
            'January': 1,
            'February': 2,
            'March': 3,
            'April': 4,
            'May': 5,
            'June': 6,
            'July': 7,
            'August': 8,
            'September': 9,
            'October': 10,
            'November': 11,
            'December': 12,
        }

        self.meses = calendar.month_name   # lista dos nomes dos meses do ano mes[1] == "January"
        self.ano = self.data.year
        self.label_month.set_label(self.data.strftime('%B'))
        # self.label_year.set_label(str(self.ano))
        self.label_data_hora_inicial.set_text(self.data.strftime('%d/%m/%Y - %H:%M'))
        self.label_data_hora_final.set_text(self.data.strftime('%d/%m/%Y - %H:%M'))
        calendar.setfirstweekday(calendar.SUNDAY)
        if self.language == 'pt_BR':
            self.label_periodo_do.set_text('Período do')
            # self.label_definir_prazo.set_text("Definir o Prazo")
            self.label_valor_total.set_text('Valor total')
            self.label_ate.set_text('até')
            self.btn_cancelar_calendario.set_label('TELA ANTERIOR')
            self.btn_confirmar_calendario.set_label('CONFIRMAR')

        elif self.language == 'en_US':
            self.label_periodo_do.set_text('Start Time')
            # self.label_definir_prazo.set_text("Set the Time")
            self.label_valor_total.set_text('Total price')
            self.label_ate.set_text('End Time')
            self.btn_cancelar_calendario.set_label('PREVIOUS SCREEN')
            self.btn_confirmar_calendario.set_label('CONFIRM')

        self.dias_meses = [
            [
                self.btn0,
                self.btn1,
                self.btn2,
                self.btn3,
                self.btn4,
                self.btn5,
                self.btn6,
            ],
            [
                self.btn7,
                self.btn8,
                self.btn9,
                self.btn10,
                self.btn11,
                self.btn12,
                self.btn13,
            ],
            [
                self.btn14,
                self.btn15,
                self.btn16,
                self.btn17,
                self.btn18,
                self.btn19,
                self.btn20,
            ],
            [
                self.btn21,
                self.btn22,
                self.btn23,
                self.btn24,
                self.btn25,
                self.btn26,
                self.btn27,
            ],
            [
                self.btn28,
                self.btn29,
                self.btn30,
                self.btn31,
                self.btn32,
                self.btn33,
                self.btn34,
            ],
            [
                self.btn35,
                self.btn36,
                self.btn37,
                self.btn38,
                self.btn39,
                self.btn40,
                self.btn41,
            ],
        ]
        self.dias_dom = [
            self.btn0,
            self.btn7,
            self.btn14,
            self.btn21,
            self.btn28,
            self.btn6,
            self.btn13,
            self.btn20,
            self.btn27,
            self.btn34,
            self.btn35,
            self.btn41,
        ]
        self.dias_totais = [
            self.btn0,
            self.btn1,
            self.btn2,
            self.btn3,
            self.btn4,
            self.btn5,
            self.btn6,
            self.btn7,
            self.btn8,
            self.btn9,
            self.btn10,
            self.btn11,
            self.btn12,
            self.btn13,
            self.btn14,
            self.btn15,
            self.btn16,
            self.btn17,
            self.btn18,
            self.btn19,
            self.btn20,
            self.btn21,
            self.btn22,
            self.btn23,
            self.btn24,
            self.btn25,
            self.btn26,
            self.btn27,
            self.btn28,
            self.btn29,
            self.btn30,
            self.btn31,
            self.btn32,
            self.btn33,
            self.btn34,
            self.btn35,
            self.btn36,
            self.btn37,
            self.btn38,
            self.btn39,
            self.btn40,
            self.btn41,
        ]

        self.set_calendario(self.data.year, self.data.month)

        # self.calendario_window.fullscreen()
        self.calendario_window.show()

    def on_btn_cancelar_calendario_button_press_event(self, widget, event):
        self.label_valor_total_value.set_text('')
        self.calendario_window.hide()
        window_op_hora_diaria.OpcaoHoraDiaria(self.classe, self.language)

    def on_btn_confirmar_calendario_button_press_event(self, widget, event):
        self.total = self.label_valor_total_value.get_label()
        self.on_calendario_window_quit()
        CadastroUsuarios(
            self.total,
            self.language,
            self.classe,
            self.resultado_dias,
            self.total_horas,
        )

    def on_btn_button_press_event(self, widget, args):
        self.widget = widget.get_label()
        data = datetime(
            self.data.year,
            self.data.month,
            self.data.day,
            self.data.hour,
            self.data.minute,
        )
        mes_escolhido = self.meses_indices[self.label_month.get_label()]
        print('mes_escolhido', mes_escolhido)
        # ano_escolhido = int(self.label_year.get_label())
        data2 = datetime(
            self.data.year,
            mes_escolhido,
            int(self.widget),
            self.data.hour,
            self.data.minute,
        )
        self.resultado_dias = abs((data2 - data).days)
        total = self.taxa * self.resultado_dias   # (int(self.widget) - self.data.day)
        print('total = %.2f' % (total))
        total = str('%.2f' % total)
        total = total.replace('.', ',')
        self.label_valor_total_value.set_text('R$ ' + total)
        # self.label_valor_total_value.set_text("%.2f"%(total))
        self.label_data_hora_final.set_text(data2.strftime('%d/%m/%Y - %H:%M'))
        print(self.widget)
        for i in range(len(self.dias_meses)):
            for j, d in zip(self.dias_meses[i], range(7)):

                if (
                    self.dias_meses[i][d].get_label() != ''
                    and int(self.dias_meses[i][d].get_label()) >= self.data.day
                    and int(self.dias_meses[i][d].get_label()) < int(self.widget)
                ):
                    self.dias_meses[i][d].set_name('intervalo_selecionado')
                elif self.dias_meses[i][d].get_label() == '' or (
                    self.meses_indices[self.label_month.get_label()] == self.data.month
                    and int(self.dias_meses[i][d].get_label()) < self.data.day
                ):
                    print(
                        'dias messess',
                        self.dias_meses[i][d].get_label(),
                        ' button ==> ',
                        self.dias_meses[i][d].get_name(),
                    )
                    self.dias_meses[i][d].set_sensitive(False)
                    self.dias_meses[i][d].set_name('dia_passado')
                elif (
                    self.dias_meses[i][d].get_label() != ''
                    and int(self.dias_meses[i][d].get_label()) < int(self.widget)
                    and self.meses_indices[self.label_month.get_label()] > self.meses_indices[self.meses[self.data.month]]
                ):
                    self.dias_meses[i][d].set_name('intervalo_selecionado')

                elif (
                    self.dias_meses[i][d].get_label() != ''
                    and self.label_month.get_label() != self.meses[self.data.month]
                    and self.dias_meses[i][d] not in self.dias_dom
                ):
                    print('dias normais', self.dias_meses[i][d].get_label())
                    self.dias_meses[i][d].set_sensitive(True)
                    self.dias_meses[i][d].set_name('btn_calendario')
                elif (
                    self.dias_meses[i][d].get_label() != ''
                    and self.dias_meses[i][d] in self.dias_dom
                    and not (
                        self.meses_indices[self.label_month.get_label()] == self.data.month
                        and int(self.dias_meses[i][d].get_label()) < self.data.day
                    )
                ):
                    self.dias_meses[i][d].set_name('btn_calendario_dom')
                elif (
                    int(self.dias_meses[i][d].get_label()) == data.day
                    and self.meses_indices[self.label_month.get_label()] == data.month
                ):
                    self.dias_meses[i][d].set_name('dia_corrente')
                    self.dias_meses[i][d].set_sensitive(False)
                else:
                    self.dias_meses[i][d].set_name('btn_calendario')
                    self.dias_meses[i][d].set_sensitive(True)

                if self.dias_meses[i][d].get_label() == '':
                    self.dias_meses[i][d].set_sensitive(False)
                    self.dias_meses[i][d].set_name('dia_passado')
                if self.dias_meses[i][d].get_label() == self.widget:
                    self.dias_meses[i][d].set_name('dia_selecionado')

        return self.resultado_dias

    def set_calendario(self, ano, mes):

        self.mes = calendar.monthcalendar(ano, mes)
        self.month = mes
        self.label_month.set_text(self.meses[mes])
        # self.label_year.set_text(str(ano))
        data = datetime.now()

        self.dias_meses = [
            [
                self.btn0,
                self.btn1,
                self.btn2,
                self.btn3,
                self.btn4,
                self.btn5,
                self.btn6,
            ],
            [
                self.btn7,
                self.btn8,
                self.btn9,
                self.btn10,
                self.btn11,
                self.btn12,
                self.btn13,
            ],
            [
                self.btn14,
                self.btn15,
                self.btn16,
                self.btn17,
                self.btn18,
                self.btn19,
                self.btn20,
            ],
            [
                self.btn21,
                self.btn22,
                self.btn23,
                self.btn24,
                self.btn25,
                self.btn26,
                self.btn27,
            ],
            [
                self.btn28,
                self.btn29,
                self.btn30,
                self.btn31,
                self.btn32,
                self.btn33,
                self.btn34,
            ],
            [
                self.btn35,
                self.btn36,
                self.btn37,
                self.btn38,
                self.btn39,
                self.btn40,
                self.btn41,
            ],
        ]
        self.dias_dom = [
            self.btn0,
            self.btn7,
            self.btn14,
            self.btn21,
            self.btn28,
            self.btn6,
            self.btn13,
            self.btn20,
            self.btn27,
            self.btn34,
            self.btn35,
            self.btn41,
        ]
        self.dias_totais = [
            self.btn0,
            self.btn1,
            self.btn2,
            self.btn3,
            self.btn4,
            self.btn5,
            self.btn6,
            self.btn7,
            self.btn8,
            self.btn9,
            self.btn10,
            self.btn11,
            self.btn12,
            self.btn13,
            self.btn14,
            self.btn15,
            self.btn16,
            self.btn17,
            self.btn18,
            self.btn19,
            self.btn20,
            self.btn21,
            self.btn22,
            self.btn23,
            self.btn24,
            self.btn25,
            self.btn26,
            self.btn27,
            self.btn28,
            self.btn29,
            self.btn30,
            self.btn31,
            self.btn32,
            self.btn33,
            self.btn34,
            self.btn35,
            self.btn36,
            self.btn37,
            self.btn38,
            self.btn39,
            self.btn40,
            self.btn41,
        ]
        self.dia = 0
        # grantindo que o botão não terá valor None
        for i in range(len(self.dias_meses)):
            for d in range(len(self.dias_meses[i])):
                self.dias_meses[i][d].set_label('')
                self.dias_meses[i][d].set_name('dia_passado')
                self.dias_meses[i][d].set_sensitive(False)

        for i in range(len(self.mes)):
            for j, d in zip(self.mes[i], range(7)):
                if self.mes[i][d] == 0 or self.mes[i][d] == None:
                    self.dias_meses[i][d].set_label('')
                    self.dias_meses[i][d].set_sensitive(False)
                    self.dias_meses[i][d].set_name('dia_passado')
                else:
                    self.dias_meses[i][d].set_label(str(self.mes[i][d]))

        for i in range(len(self.mes)):
            for j, d in zip(self.mes[i], range(7)):
                print(
                    'self.meses_indices[self.label_month.get_label()',
                    self.meses_indices[self.label_month.get_label()],
                )
                print('self.data.month', self.data.month)
                print(
                    'self.dias_meses[i][d] in self.dias_dom',
                    self.dias_meses[i][d] in self.dias_dom,
                )
                if self.dias_meses[i][d].get_label() == '0':
                    self.dias_meses[i][d].set_label('')
                    self.dias_meses[i][d].set_sensitive(False)
                elif (
                    self.dias_meses[i][d].get_label() != ''
                    and int(self.dias_meses[i][d].get_label()) == data.day
                    and self.meses_indices[self.label_month.get_label()] == data.month
                ):
                    self.dias_meses[i][d].set_name('dia_corrente')
                    self.dias_meses[i][d].set_sensitive(False)

                elif self.dias_meses[i][d].get_label() == '' or (
                    self.meses_indices[self.label_month.get_label()] == self.data.month
                    and int(self.dias_meses[i][d].get_label()) < self.data.day
                ):
                    print('dias messess', self.dias_meses[i][d].get_label())
                    self.dias_meses[i][d].set_sensitive(False)
                    self.dias_meses[i][d].set_name('dia_passado')
                elif (
                    self.label_month.get_label() != self.meses[self.data.month] and self.dias_meses[i][d] not in self.dias_dom
                ):
                    print('dias normais', self.dias_meses[i][d].get_label())
                    self.dias_meses[i][d].set_sensitive(True)
                    self.dias_meses[i][d].set_name('btn_calendario')
                elif self.dias_meses[i][d] in self.dias_dom and not (
                    self.meses_indices[self.label_month.get_label()] == self.data.month
                    and int(self.dias_meses[i][d].get_label()) < self.data.day
                ):
                    self.dias_meses[i][d].set_name('btn_calendario_dom')
                    self.dias_meses[i][d].set_sensitive(True)

                else:
                    self.dias_meses[i][d].set_sensitive(True)
                    self.dias_meses[i][d].set_name('btn_calendario')
                    self.dia = self.dias_meses[i][d].get_label()
                if self.dias_meses[i][d].get_label() == '':
                    self.dias_meses[i][d].set_sensitive(False)
                    self.dias_meses[i][d].set_name('dia_passado')
        # caso o tamanho de meses indices seja maior que o mes corrente desativa os botões restantes que estarão vazios
        if len(self.mes) == 5:
            for i in self.dias_meses[5]:
                i.set_sensitive(False)

        teste = self.meses_indices[self.label_month.get_label()]
        print('teste', teste)
        teste2 = self.label_month.get_label()
        print('teste2', teste2)
        if self.meses_indices[self.label_month.get_label()] == self.data.month:
            self.btn_previous_mont.set_sensitive(False)
        else:
            self.btn_previous_mont.set_sensitive(True)

        """if int(self.label_year.get_label()) == self.data.year:
            self.btn_previous_year.set_sensitive(False) 
        else:
            self.btn_previous_year.set_sensitive(True)"""

    def on_btn_previous_mont_button_press_event(self, event, args):
        self.label_valor_total_value.set_text('')
        self.mes_atual = self.meses_indices[self.label_month.get_label()]
        print('self.mes_atual', self.mes_atual)
        self.ano_atual = self.data.year   # int(self.label_year.get_label())
        if self.mes_atual == 1:
            self.mes_atual = 12
            # self.ano_atual = self.ano_atual - 1
        else:
            self.mes_atual = self.mes_atual - 1

        self.set_calendario(self.ano_atual, self.mes_atual)

    def on_btn_next_month_button_press_event(self, event, args):
        self.label_valor_total_value.set_text('')
        self.mes_atual = self.meses_indices[self.label_month.get_label()]
        print('self.mes_atual', self.mes_atual)
        self.ano_atual = self.data.year   # int(self.label_year.get_label())
        if self.mes_atual == 12:
            self.mes_atual = 1
            # self.ano_atual = self.ano_atual + 1
        else:
            self.mes_atual = self.mes_atual + 1

        self.set_calendario(self.ano_atual, self.mes_atual)

    """def on_btn_previous_year_button_press_event(self, event, args):
        self.label_valor_total_value.set_text("")
        self.mes_atual = self.meses_indices[self.label_month.get_label()]
        print("self.mes_atual", self.mes_atual)
        self.ano_atual = self.data.year #int(self.label_year.get_label())
       
        self.ano_atual = self.ano_atual - 1

        self.set_calendario(self.ano_atual, self.mes_atual)"""

    """def on_btn_next_year_button_press_event(self, event, args):
        self.label_valor_total_value.set_text("")
        self.mes_atual = self.meses_indices[self.label_month.get_label()]
        print("self.mes_atual", self.mes_atual)
        self.ano_atual = self.data.year #int(self.label_year.get_label())
       
        self.ano_atual = self.ano_atual + 1

        self.set_calendario(self.ano_atual, self.mes_atual)"""

    def on_calendario_window_quit(self):
        self.calendario_window.hide()

    def gtk_style_calendario(self):
        css = b'@import url("static/css/calendario.css");'
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )
