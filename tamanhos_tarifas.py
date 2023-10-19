import gi
import numpy as np
from gi.repository import Gdk, GLib, Gtk
from window_op_hora_diaria import OpcaoHoraDiaria

from controllers import Management

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')


class TamanhosTarifas(object):
    def __init__(self, arg):
        self.language = arg
        print('language select size', self.language)
        self.classe = ''
        self.manager = Management()
        self.builder = Gtk.Builder()
        self.builder.add_from_file('ui/tamanhos_tarifas.glade')
        self.builder.connect_signals(
            {
                'gtk_main_quit': Gtk.main_quit,
                'on_btn_malasx4_tarifas_toggled': self.on_btn_malasx4_tarifas_toggled,
                'on_btn_malasx2_tarifas_toggled': self.on_btn_malasx2_tarifas_toggled,
                'on_btn_mochilasx2_tarifas_toggled': self.on_btn_mochilasx2_tarifas_toggled,
                'on_btn_cameraenotebook_tarifas_toggled': self.on_btn_cameraenotebook_tarifas_toggled,
                'on_btn_confirmar_button_press_event': self.on_btn_confirmar_button_press_event,
                'on_btn_tamanhos_tarifas_button_press_event': self.on_btn_tamanhos_tarifas_button_press_event,
                'on_btn_retornar_button_press_event': self.on_btn_retornar_button_press_event,
                'on_btn_retornar_tarifas_button_press_event': self.on_btn_retornar_tarifas_button_press_event,
                'on_window_tamanhos_tarifas_button_press_event': self.on_btn_tamanhos_tarifas_button_press_event,
                'on_btn_dialog_unavailable_button_press_event': self.on_btn_dialog_unavailable_button_press_event,
            }
        )
        # janela principal
        self.window_tamanhos_tarifas = self.builder.get_object('window_tamanhos_tarifas')

        # =============== BOTOES ====================

        self.btn_retornar_tarifas = self.builder.get_object('btn_retornar_tarifas')
        self.btn_retornar_tarifas.connect(
            'button_press_event',
            self.on_btn_retornar_tarifas_button_press_event,
        )
        self.btn_confirmar_tarifas = self.builder.get_object('btn_confirmar_tarifas')
        self.btn_confirmar_tarifas.connect('button_press_event', self.on_btn_confirmar_button_press_event)
        self.btn_malasx4_tarifas = self.builder.get_object('btn_malasx4_tarifas')
        self.btn_malasx4_tarifas.connect('toggled', self.on_btn_malasx4_tarifas_toggled)
        self.btn_malasx2_tarifas = self.builder.get_object('btn_malasx2_tarifas')
        self.btn_malasx2_tarifas.connect('toggled', self.on_btn_malasx2_tarifas_toggled)
        self.btn_mochilasx2_tarifas = self.builder.get_object('btn_mochilasx2_tarifas')
        self.btn_mochilasx2_tarifas.connect('toggled', self.on_btn_mochilasx2_tarifas_toggled)
        self.btn_cameraenotebook_tarifas = self.builder.get_object('btn_cameraenotebook_tarifas')
        self.btn_cameraenotebook_tarifas.connect('toggled', self.on_btn_cameraenotebook_tarifas_toggled)

        self.btn_usa = self.builder.get_object('btn_usa')
        self.btn_br = self.builder.get_object('btn_br')

        self.btn_br.connect('clicked', self.on_change_language_br)
        self.btn_usa.connect('clicked', self.on_change_language_usa)

        self.btn_dialog_unavailable = self.builder.get_object('btn_dialog_unavailable')
        self.btn_dialog_unavailable.connect(
            'button_press_event',
            self.on_btn_dialog_unavailable_button_press_event,
        )

        # ============= FIM BOTOES ==================

        # ============== LABELS ======================
        self.label_tamanhos_tarifas_malasx4 = self.builder.get_object('label_tamanhos_tarifas_malasx4')
        self.label_tamanhos_tarifas_malasx2 = self.builder.get_object('label_tamanhos_tarifas_malasx2')
        self.label_tamanhos_tarifas_mochilasx2 = self.builder.get_object('label_tamanhos_tarifas_mochilasx2')
        self.label_tamanhos_tarifas_cameraenotebook = self.builder.get_object('label_tamanhos_tarifas_cameraenotebook')
        self.label_titulo_tamanhos_tarifas = self.builder.get_object('label_titulo_tamanhos_tarifas')

        self.label_message_armario_unavailable = self.builder.get_object('label_message_armario_unavailable')
        # ============== FIM LABELS =================

        # =============== DIALOGS ====================
        self.dialog_unavailable = self.builder.get_object('dialog_unavailable')

        # ============== FIM DIALOGS ================
        if self.language == 'pt_BR':
            self.label_tamanhos_tarifas_malasx4.set_text('IDEAL PARA')
            self.label_tamanhos_tarifas_malasx2.set_text('IDEAL PARA')
            self.label_tamanhos_tarifas_mochilasx2.set_text('IDEAL PARA')
            self.label_tamanhos_tarifas_cameraenotebook.set_text('IDEAL PARA')
            self.label_titulo_tamanhos_tarifas.set_text('TAMANHOS E TARIFAS')
            self.btn_retornar_tarifas.set_label('RETORNAR TELA ANTERIOR')
            self.btn_confirmar_tarifas.set_label('CONFIRMAR')
            self.label_message_armario_unavailable.set_text(
                'TAMANHO DE ARMÁRIO INDISPONÍVEL NO MOMENTO,\n POR FAVOR ESCOLHA OUTRO!'
            )
        elif self.language == 'en_US':
            self.label_tamanhos_tarifas_malasx4.set_text('IDEAL FOR')
            self.label_tamanhos_tarifas_malasx2.set_text('IDEAL FOR')
            self.label_tamanhos_tarifas_mochilasx2.set_text('IDEAL FOR')
            self.label_tamanhos_tarifas_cameraenotebook.set_text('IDEAL FOR')
            self.label_titulo_tamanhos_tarifas.set_text('SIZES AND RATES')
            self.btn_retornar_tarifas.set_label('PREVIOUS SCREEN')
            self.btn_confirmar_tarifas.set_label('CONFIRM')
            self.label_message_armario_unavailable.set_text('CABINET SIZE UNAVAILABLE AT THE TIME,\n PLEASE CHOOSE ANOTHER!')

        self.window_tamanhos_tarifas.fullscreen()
        self.window_tamanhos_tarifas.show()

    def on_btn_dialog_unavailable_button_press_event(self, widget, event):
        self.dialog_unavailable.hide()

    def on_btn_malasx4_tarifas_toggled(self, widget):

        if self.btn_malasx4_tarifas.get_active():
            self.classe = 'A'
        else:
            self.classe = ''
        classes = self.manager.lista_armarios()
        print('classes obtidas', classes)
        if self.classe in np.array(classes):
            pass
        else:
            self.classe = ''
            if self.language == 'pt_BR':
                self.label_message_armario_unavailable.set_text(' INDISPONÍVEL, POR FAVOR ESCOLHA OUTRO TAMANHO! ')
            elif self.language == 'en_US':
                self.label_message_armario_unavailable.set_text(' UNAVAILABLE, PLEASE SELECT ANOTHER SIZE! ')
            self.dialog_unavailable.show()

    def on_btn_malasx2_tarifas_toggled(self, widget):
        if self.btn_malasx2_tarifas.get_active():
            self.classe = 'B'
        else:
            self.classe = ''
        classes = self.manager.lista_armarios()
        print('classes obtidas', classes)
        if self.classe in np.array(classes):
            pass
        else:
            self.classe = ''
            if self.language == 'pt_BR':
                self.label_message_armario_unavailable.set_text(' INDISPONÍVEL, POR FAVOR ESCOLHA OUTRO TAMANHO! ')
            elif self.language == 'en_US':
                self.label_message_armario_unavailable.set_text(' UNAVAILABLE, PLEASE SELECT ANOTHER SIZE! ')
            self.dialog_unavailable.show()

    def on_btn_mochilasx2_tarifas_toggled(self, widget):
        if self.btn_mochilasx2_tarifas.get_active():
            self.classe = 'C'
            print(self.classe)
        else:
            self.classe = ''
        classes = self.manager.lista_armarios()
        print('classes obtidas', classes)
        if self.classe in np.array(classes):
            pass
        else:
            self.classe = ''
            if self.language == 'pt_BR':
                self.label_message_armario_unavailable.set_text(' INDISPONÍVEL, POR FAVOR ESCOLHA OUTRO TAMANHO! ')
            elif self.language == 'en_US':
                self.label_message_armario_unavailable.set_text(' UNAVAILABLE, PLEASE SELECT ANOTHER SIZE! ')
            self.dialog_unavailable.show()

    def on_btn_cameraenotebook_tarifas_toggled(self, widget):
        if self.btn_cameraenotebook_tarifas.get_active():
            self.classe = 'D'
            print(self.classe)
        else:
            self.classe = ''
        classes = self.manager.lista_armarios()
        print('classes obtidas', classes)
        if self.classe in np.array(classes):
            pass
        else:
            self.classe = ''
            if self.language == 'pt_BR':
                self.label_message_armario_unavailable.set_text(' INDISPONÍVEL, POR FAVOR ESCOLHA OUTRO TAMANHO! ')
            elif self.language == 'en_US':
                self.label_message_armario_unavailable.set_text(' UNAVAILABLE, PLEASE SELECT ANOTHER SIZE! ')
            self.dialog_unavailable.show()

    def on_btn_confirmar_button_press_event(self, widget, event):
        if self.classe == '':
            print('É necessário escolher um tamanho de armário')
        else:
            print('classe selecionada', self.classe)
            OpcaoHoraDiaria(self.classe, self.language)
            self.window_tamanhos_tarifas.hide()

    def on_btn_retornar_button_press_event(self, widget, event):
        self.window_tamanhos_tarifas.hide()

    def on_btn_retornar_tarifas_button_press_event(self, widget, event):
        self.window_tamanhos_tarifas.hide()

    def on_btn_tamanhos_tarifas_button_press_event(self, event):
        self.window_tamanhos_tarifas.show()

    def on_change_language_br(self, event):
        self.language = 'pt_BR'
        self.label_tamanhos_tarifas_malasx4.set_text('IDEAL PARA')
        self.label_tamanhos_tarifas_malasx2.set_text('IDEAL PARA')
        self.label_tamanhos_tarifas_mochilasx2.set_text('IDEAL PARA')
        self.label_tamanhos_tarifas_cameraenotebook.set_text('IDEAL PARA')

    def on_change_language_usa(self, event):
        self.language = 'en_US'
        self.label_tamanhos_tarifas_malasx4.set_text('IDEAL FOR')
        self.label_tamanhos_tarifas_malasx2.set_text('IDEAL FOR')
        self.label_tamanhos_tarifas_mochilasx2.set_text('IDEAL FOR')
        self.label_tamanhos_tarifas_cameraenotebook.set_text('IDEAL FOR')


if __name__ == '__main__':
    app = SelectSize()
    Gtk.main()
