from time import *

import gi
from gi.repository import Gdk, Gtk

gi.require_version('Gtk', '3.0')


class WindowSelectCartao:
    def __init__(self):
        self.build = Gtk.Builder()
        self.build.add_from_file('ui/window_select_cartao.glade')
        self.build.connect_signals(
            {
                'gtk_main_quit': Gtk.main_quit,
                'on_btn_credito_button_press_event': self.on_btn_credito_button_press_event,
                'on_btn_debito_button_press_event': self.on_btn_debito_button_press_event,
                'on_btn_cancelar_button_press_event': self.on_btn_cancelar_button_press_event,
            }
        )
        self.btn_credito = self.build.get_object('btn_credito')
        self.btn_credito.connect(
            'button-press-event', self.on_btn_credito_button_press_event
        )
        self.btn_debito = self.build.get_object('btn_debito')
        # self.btn_debito.connect("button-press-event", self.on_btn_debito_button_press_event)
        self.btn_cancelar = self.build.get_object('btn_cancelar')
        # self.btn_cancelar.connect("button-press-event", self.on_btn_cancelar_button_press_event)
        self.tipo_cartao = ''

        self.window_select_cartao = self.build.get_object(
            'window_select_cartao'
        )
        self.window_select_cartao.show()

    def on_btn_credito_button_press_event(self, event, args):
        # print("1")
        self.send_tipo_cartao('CREDITO')
        sleep(0.5)

    def on_btn_debito_button_press_event(self, event, args):
        # print("2")
        self.send_tipo_cartao('DEBITO')
        sleep(0.5)

    def on_btn_cancelar_button_press_event(self, event, args):
        # print("CANCELA")
        self.send_tipo_cartao(0x13)
        sleep(0.5)
        self.window_select_cartao.destroy()

    def send_tipo_cartao(self, tipo):
        print(tipo)
        return tipo
        self.window_select_cartao.destroy()


if __name__ == '__main__':
    app = WindowSelectCartao()
    Gtk.main()
