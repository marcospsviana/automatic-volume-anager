import gi

from controllers import Management
from window_op_hora_diaria import OpcaoHoraDiaria

from datetime import datetime

import numpy as np
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk, GdkPixbuf, Gio, GLib, GObject, Gtk


class SelectSize(object):
    def __init__(self, arg):
        self.manager = Management()
        self.language = arg
        print('language select size', self.language)
        self.classe = ''
        self.builder = Gtk.Builder()
        self.builder.add_from_file('ui/select_size.glade')
        # self.builder.add_from_file("ui/tamanhos_tarifas.glade")
        self.builder.connect_signals(
            {
                'gtk_main_quit': Gtk.main_quit,
                'on_btn_malasx4_button_press_event': self.on_btn_malasx4_button_press_event,
                'on_btn_malasx2_button_press_event': self.on_btn_malasx2_button_press_event,
                'on_btn_mochilasx2_button_press_event': self.on_btn_mochilasx2_button_press_event,
                'on_btn_cameraenotebook_button_press_event': self.on_btn_cameraenotebook_button_press_event,
                # "on_btn_confirmar_button_press_event": self.on_btn_confirmar_button_press_event,
                # "on_btn_tamanhos_tarifas_button_press_event": self.on_btn_tamanhos_tarifas_button_press_event,
                'on_btn_retornar_button_press_event': self.on_btn_retornar_button_press_event,
                # "on_window_tamanhos_tarifas_button_press_event": self.on_btn_tamanhos_tarifas_button_press_event,
                'on_btn_dialog_unavailable_button_press_event': self.on_btn_dialog_unavailable_button_press_event,
                'on_btn_usa_button_press_event': self.on_btn_usa_button_press_event,
                'on_btn_br_button_press_event': self.on_btn_br_button_press_event,
            }
        )
        # janela principal
        self.window_select_size = self.builder.get_object('window_select_size')

        # =============== BOTOES ====================
        self.btn_malasx4 = self.builder.get_object('btn_malasx4')
        # self.btn_malasx4.connect("button_press_event", self.on_btn_malasx4_button_press_event)
        self.btn_malasx2 = self.builder.get_object('btn_malasx2')
        # self.btn_malasx2.connect("button_press_event", self.on_btn_malasx2_button_press_event)
        self.btn_mochilasx2 = self.builder.get_object('btn_mochilasx2')
        # self.btn_mochilasx2.connect("button_press_event", self.on_btn_mochilasx2_button_press_event)
        self.btn_cameraenotebook = self.builder.get_object('btn_cameraenotebook')
        # self.btn_cameraenotebook.connect("button_press_event", self.on_btn_cameraenotebook_button_press_event)
        self.btn_retornar = self.builder.get_object('btn_retornar')
        # self.btn_retornar.connect("button_press_event", self.on_btn_retornar_button_press_event)
        # self.btn_confirmar = self.builder.get_object("btn_confirmar")
        # self.btn_tamanhos_tarifas = self.builder.get_object("btn_tamanhos_tarifas")
        # self.btn_tamanhos_tarifas.connect("button_press_event", self.on_btn_tamanhos_tarifas_button_press_event)

        self.btn_usa = self.builder.get_object('btn_usa')
        self.btn_br = self.builder.get_object('btn_br')

        # self.btn_br.connect("clicked", self.on_change_language_br)
        # self.btn_usa.connect("clicked", self.on_change_language_usa)

        # ============= FIM BOTOES ==================

        # ============== LABELS ======================
        self.label_malasx4 = self.builder.get_object('label_malasx4')
        self.label_malasx2 = self.builder.get_object('label_malasx2')
        self.label_mochilasx2 = self.builder.get_object('label_mochilasx2')
        self.label_cameraenotebook = self.builder.get_object('label_cameraenotebook')

        self.label_titulo_select_size = self.builder.get_object('label_titulo_select_size')

        self.label_horario = self.builder.get_object('label_horario')
        self.label_data = self.builder.get_object('label_data')
        # ============== FIM LABELS =================
        """# ============== TELA TAMANHO E TARIFAS =====
        self.window_tamanhos_tarifas = self.builder.get_object("window_tamanhos_tarifas")
        self.btn_retornar_tarifas = self.builder.get_object("btn_retornar")
        self.btn_confirmar_tarifas = self.builder.get_object("btn_confirmar_tarifas")
        self.btn_confirmar_tarifas.connect("button_press_event", self.on_btn_confirmar_button_press_event)
        self.btn_malasx4_tarifas = self.builder.get_object("btn_malasx4_tarifas")
        self.btn_malasx4_tarifas.connect("toggled", self.on_btn_malasx4_toggled )
        self.btn_malasx2_tarifas = self.builder.get_object("btn_malasx2_tarifas")
        self.btn_malasx2_tarifas.connect("toggled", self.on_btn_malasx2_toggled)
        self.btn_mochilasx2_tarifas = self.builder.get_object("btn_mochilasx2_tarifas")
        self.btn_mochilasx2_tarifas.connect("toggled", self.on_btn_mochilasx2_toggled)
        self.btn_cameraenotebook_tarifas = self.builder.get_object("btn_cameraenotebook_tarifas")
        self.btn_cameraenotebook_tarifas.connect("toggled", self.on_btn_cameraenotebook_toggled)"""

        # WINDOW DIALOG UNAVAILABLE
        self.dialog_unavailable = self.builder.get_object('dialog_unavailable')
        self.label_message_armario_unavailable = self.builder.get_object('label_message_armario_unavailable')
        self.btn_dialog_unavailable = self.builder.get_object('btn_dialog_unavailable')
        self.btn_dialog_unavailable.connect(
            'button_press_event',
            self.on_btn_dialog_unavailable_button_press_event,
        )

        if self.language == 'pt_BR':
            self.label_malasx4.set_text('IDEAL PARA')
            self.label_malasx2.set_text('IDEAL PARA')
            self.label_mochilasx2.set_text('IDEAL PARA')
            self.label_cameraenotebook.set_text('IDEAL PARA')
            # self.btn_confirmar.set_label("CONFIRMAR")
            self.btn_retornar.set_label('TELA ANTERIOR')
            # self.btn_tamanhos_tarifas.set_label("TAMANHOS E TARIFAS")
            self.label_titulo_select_size.set_text('ESCOLHA o TAMANHO do COFRE DESEJADO!')

        elif self.language == 'en_US':
            self.label_malasx4.set_text('IDEAL FOR')
            self.label_malasx2.set_text('IDEAL FOR')
            self.label_mochilasx2.set_text('IDEAL FOR')
            self.label_cameraenotebook.set_text('IDEAL FOR')
            # self.btn_confirmar.set_label("CONFIRM")
            self.btn_retornar.set_label('PREVIOUS SCREEN')
            # self.btn_tamanhos_tarifas.set_label("SIZES AND RATES")
            self.label_titulo_select_size.set_text('CHOOSE THE DESIRED SAFE SIZE!')

        classes = self.manager.lista_armarios()
        if 'A' not in np.array(classes):
            if self.language == 'pt_BR':
                self.label_malasx4.set_text('INDISPONÍVEL')
            else:
                self.label_malasx4.set_text('UNAVAILABLE')

            self.btn_malasx4.set_name('btn_malasx4_inativo')

        if 'B' not in np.array(classes):
            if self.language == 'pt_BR':
                self.label_malasx2.set_text('INDISPONÍVEL')

            else:
                self.label_malasx2.set_text('UNAVAILABLE')
            self.btn_malasx2.set_name('btn_malasx2_inativo')
        if 'C' not in np.array(classes):
            # self.btn_malasx2.set_sensitive(False)
            if self.language == 'pt_BR':
                self.label_mochilasx2.set_text('INDISPONÍVEL')
            else:
                self.label_mochilasx2.set_text('UNAVAILABLE')
            self.btn_mochilasx2.set_name('btn_mochilasx2_inativo')
        if 'D' not in np.array(classes):
            # self.btn_malasx2.set_sensitive(False)
            if self.language == 'pt_BR':
                self.label_cameraenotebook.set_text('INDISPONÍVEL')
            else:
                self.label_cameraenotebook.set_text('UNAVAILABLE')
            self.btn_cameraenotebook.set_name('btn_cameraenotebook_inativo')

        GLib.timeout_add(1000, self.hora_certa)

        self.window_select_size.fullscreen()
        self.window_select_size.show()

    def hora_certa(self):
        dia = datetime.now()
        dia_hora = dia.strftime('%H:%M:%S')
        dia_data = dia.strftime('%d/%m/%Y')
        self.label_horario.set_text(str(dia_hora))
        self.label_data.set_text(str(dia_data))
        return (self.label_data, self.label_horario)

    def on_btn_dialog_unavailable_button_press_event(self, widget, event):
        self.dialog_unavailable.hide()

    def on_btn_malasx4_button_press_event(self, widget, event):

        self.classe = 'A'
        # self.btn_cameraenotebook.get_active()
        classes = self.manager.lista_armarios()
        print('classes obtidas', classes)
        if self.classe in np.array(classes):
            OpcaoHoraDiaria(self.classe, self.language)
            self.window_select_size.hide()
        else:
            self.classe = ''
            if self.language == 'pt_BR':
                self.label_message_armario_unavailable.set_text(' INDISPONÍVEL, POR FAVOR ESCOLHA OUTRO TAMANHO! ')
            elif self.language == 'en_US':
                self.label_message_armario_unavailable.set_text(' UNAVAILABLE, PLEASE SELECT ANOTHER SIZE! ')
            # self.dialog_unavailable.show()
            self.btn_malasx4.set_name('btn_malasx4_inativo')

    def on_btn_malasx2_button_press_event(self, widget, event):
        # if self.btn_malasx2.get_active():
        self.classe = 'B'
        print(self.classe)
        classes = self.manager.lista_armarios()
        if self.classe in np.array(classes):
            OpcaoHoraDiaria(self.classe, self.language)
            self.window_select_size.hide()
        else:
            self.classe = ''
            if self.language == 'pt_BR':
                self.label_message_armario_unavailable.set_text(' INDISPONÍVEL, POR FAVOR ESCOLHA OUTRO TAMANHO! ')
            elif self.language == 'en_US':
                self.label_message_armario_unavailable.set_text(' UNAVAILABLE, PLEASE SELECT ANOTHER SIZE! ')
            # self.dialog_unavailable.show()
            self.btn_malasx2.set_name('btn_malasx2_inativo')
            print('não tem')

    def on_btn_mochilasx2_button_press_event(self, widget, event):
        # if self.btn_mochilasx2.get_active():
        self.classe = 'C'
        print(self.classe)

        classes = self.manager.lista_armarios()
        print('classes obtidas', classes)
        if self.classe in np.array(classes):
            OpcaoHoraDiaria(self.classe, self.language)
            self.window_select_size.hide()
        else:
            self.classe = ''
            if self.language == 'pt_BR':
                self.label_message_armario_unavailable.set_text(' INDISPONÍVEL, POR FAVOR ESCOLHA OUTRO TAMANHO! ')
            elif self.language == 'en_US':
                self.label_message_armario_unavailable.set_text(' UNAVAILABLE, PLEASE SELECT ANOTHER SIZE! ')
            # self.dialog_unavailable.show()
            self.btn_mochilasx2.set_name('btn_mochilasx2_inativo')

    def on_btn_cameraenotebook_button_press_event(self, widget, event):
        # if self.btn_cameraenotebook.get_active():
        self.classe = 'D'
        print(self.classe)
        classes = self.manager.lista_armarios()
        print('classes obtidas', classes)
        if self.classe in np.array(classes):
            OpcaoHoraDiaria(self.classe, self.language)
            self.window_select_size.hide()
        else:
            self.classe = ''
            if self.language == 'pt_BR':
                self.label_message_armario_unavailable.set_text(' INDISPONÍVEL, POR FAVOR ESCOLHA OUTRO TAMANHO! ')
            elif self.language == 'en_US':
                self.label_message_armario_unavailable.set_text(' UNAVAILABLE, PLEASE SELECT ANOTHER SIZE! ')
            # self.dialog_unavailable.show()
            self.btn_cameraenotebook.set_name('btn_cameraenotebook_inativo')

    """def on_btn_confirmar_button_press_event(self, widget, event):
        if self.classe == "":
            print ("É necessário escolher um tamanho de armário")
        else:
            print("classe selecionada",self.classe)
            OpcaoHoraDiaria(self.classe, self.language)
            self.window_select_size.hide()"""

    def on_btn_retornar_button_press_event(self, widget, event):
        self.window_select_size.hide()

    """def on_btn_tamanhos_tarifas_button_press_event(self, widget, event):
        TamanhosTarifas(self.language)"""

    def on_btn_br_button_press_event(self, event, arg):
        self.language = 'pt_BR'
        if self.label_malasx4.get_label() == 'UNAVAILABLE' or self.label_malasx4.get_label() == 'INDISPONÍVEL':
            self.label_malasx4.set_text('INDISPONÍVEL')
        else:
            self.label_malasx4.set_text('IDEAL PARA')

        if self.label_malasx2.get_label() == 'UNAVAILABLE' or self.label_malasx2.get_label() == 'INDISPONÍVEL':
            self.label_malasx2.set_text('INDISPONÍVEL')
        else:
            self.label_malasx2.set_text('IDEAL PARA')
        if self.label_mochilasx2.get_label() == 'UNAVAILABLE' or self.label_mochilasx2.get_label() == 'INDISPONÍVEL':
            self.label_mochilasx2.set_text('INDISPONÍVEL')
        else:
            self.label_mochilasx2.set_text('IDEAL PARA')
        if self.label_cameraenotebook.get_label() == 'UNAVAILABLE' or self.label_cameraenotebook.get_label() == 'INDISPONÍVEL':
            self.label_cameraenotebook.set_text('INDISPONÍVEL')
        else:
            self.label_cameraenotebook.set_text('IDEAL PARA')
        # self.btn_confirmar.set_label("CONFIRMAR")
        self.btn_retornar.set_label('TELA ANTERIOR')
        # self.btn_tamanhos_tarifas.set_label("TAMANHOS E TARIFAS")
        self.label_titulo_select_size.set_text('ESCOLHA o TAMANHO do COFRE DESEJADO!')

    def on_btn_usa_button_press_event(self, event, arg):
        self.language = 'en_US'
        print('en_US')
        if self.label_malasx4.get_label() == 'INDISPONÍVEL' or self.label_malasx4.get_label() == 'UNAVAILABLE':
            self.label_malasx4.set_text('UNAVAILABLE')
        else:
            self.label_malasx4.set_text('IDEAL FOR')

        if self.label_malasx2.get_label() == 'INDISPONÍVEL' or self.label_malasx2.get_label() == 'UNAVAILABLE':
            self.label_malasx2.set_text('UNAVAILABLE')
        else:
            self.label_malasx2.set_text('IDEAL FOR')
        if self.label_mochilasx2.get_label() == 'INDISPONÍVEL' or self.label_mochilasx2.get_label() == 'UNAVAILABLE':
            self.label_mochilasx2.set_text('UNAVAILABLE')
        else:
            self.label_mochilasx2.set_text('IDEAL FOR')
        if self.label_cameraenotebook.get_label() == 'INDISPONÍVEL' or self.label_cameraenotebook.get_label() == 'UNAVAILABLE':
            self.label_cameraenotebook.set_text('UNAVAILABLE')
        else:
            self.label_cameraenotebook.set_text('IDEAL FOR')
        # self.btn_confirmar.set_label("CONFIRM")
        self.btn_retornar.set_label('PREVIOUS SCREEN')
        # self.btn_tamanhos_tarifas.set_label("SIZES AND RATES")
        self.label_titulo_select_size.set_text('CHOOSE THE DESIRED SAFE SIZE!')
