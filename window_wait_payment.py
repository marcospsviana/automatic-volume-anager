import gi

gi.require_version('Gtk', '3.0')
import calendar
import datetime
import string
import threading
import time
from decimal import Decimal

import _threading_local
import PIL
from gi.repository import Gdk, GdkPixbuf, Gio, GObject, Gtk
from PIL import Image

from controllers import Management


class WindowWaitPayment(object):
    def __init__(self):
        # self.args = args
        self.locacao = ''
        self.pagamento_ext = ''

        self.language = 'pt_BR'
        self.gtk_style()
        self.builder = Gtk.Builder()
        self.builder.add_from_file('ui/window_wait_payment.glade')
        self.builder.connect_signals(
            {
                'gtk_main_quit': Gtk.main_quit,
            }
        )
        self.window_payment = self.builder.get_object('window_wait_payment')
        self.spinner = self.builder.get_object('spinner')

        # self.spinner.start()
        self.window_payment.fullscreen()
        self.window_payment.show()
        time.sleep(0.5)

    def gtk_style(self):
        css = b"""
        
        @import url("static/css/gtk.css");
        """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )


if __name__ == '__main__':
    app = WindowWaitPayment()
    Gtk.main()
