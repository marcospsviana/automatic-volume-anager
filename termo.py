import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gdk, Gtk

gi.require_version('WebKit2', '4.1')
from gi.repository import WebKit2


class Term:
    def __init__(self):

        self.window = Gtk.Window()  # self.builder.get_object('termo_de_uso')
        self.window.connect('delete-event', Gtk.main_quit)
        self.window.set_default_size(1000, 550)
        self.header_bar = Gtk.HeaderBar()
        self.header_bar.set_show_close_button(True)

        str_uri = open('templates/term.html', 'r')
        self.web = WebKit2.WebView()
        self.web.load_uri('file:///home/marcos/coolbag/raspcontrol/templates/term.html')
        self.web.show()
        self.window.add(self.web)
        self.window.show_all()


if __name__ == '__main__':
    Term()
    Gtk.main()
