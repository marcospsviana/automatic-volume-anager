import gi
gi.require_versions({'Gtk': '3.0', 'GLib': '2.0', 'Gio': '2.0'})
from gi.repository import Gtk, Gdk, GLib

class SelectSize(object):
    def __init__(self, *args):
        self.locacao = args[0]
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/select_size.glade")
        self.builder.connect_signals({
            "gtk_main_quit": Gtk.main_quit,
            "on_btn_malasx4_button_press_event": self.on_btn_malasx4_button_press_event,
            "on_btn_malax2_button_press_event": self.on_btn_malax2_button_press_event,
            "on_btn_mochilasx2_button_press_event": self.on_btn_mochilasx2_button_press_event,
            "on_btn_cameraenotebook_button_press_event": self.on_btn_cameraenotebook_button_press_event,
            "on_btn_confirmar_button_press_event": self.on_btn_confirmar_button_press_event,
            "on_btn_tamanhos_tarifas_button_press_event": self.on_btn_tamanhos_tarifas_button_press_event,
            "on_btn_retornar_button_press_event": self.on_btn_retornar_button_press_event,
        })
        # janela principal
        self.window_select_size = self.builder.get_object("window_select_size")

        # =============== BOTOES ====================
        self.btn_malasx4 = self.builder.get_object("btn_malasx4")
        self.btn_malasx4.connect("button_press_event", self.on_btn_malasx4_button_press_event)
        self.btn_malasx2 = self.builder.get_object("btn_malasx2")
        self.btn_malasx2.connect("button_press_event", self.on_btn_malax2_button_press_event)
        self.btn_mochilasx2 = self.builder.get_object("btn_mochilasx2")
        self.btn_mochilasx2.connect("button_press_event", self.on_btn_mochilasx2_button_press_event)
        self.btn_cameraenotebook = self.builder.get_object("btn_cameraenotebook")
        self.btn_cameraenotebook.connect("button_press_event", self.on_btn_cameraenotebook_button_press_event)
        self.btn_retornar = self.builder.get_object("btn_retornar")
        self.btn_retornar.connect("button_press_event", self.on_btn_retornar_button_press_event)
        # ============= FIM BOTOES ==================

        #============== LABELS ======================
        self.label_malasx4 = self.builder.get_object("label_malasx4")
        self.label_malasx2 = self.builder.get_object("label_malasx2")
        self.label_mochilasx2 = self.builder.get_object("label_mochilasx2")
        self.label_cameraenotebook = self.builder.get_object("label_cameraenotebook")
        # ============== FIM LABELS ================
    
       
    def on_btn_malasx4_button_press_event(self, widget, event):
        pass
    
    def on_btn_malax2_button_press_event(self, widget, event):
        pass
    
    def on_btn_mochilasx2_button_press_event(self, widget, event):
        pass

    def on_btn_cameraenotebook_button_press_event(self, widget, event):
        pass

    def on_btn_confirmar_button_press_event(self, widget, event):
        pass
    
    def on_btn_retornar_button_press_event(self, widget, event):
        pass
    
    def on_btn_tamanhos_tarifas_button_press_event(self, widget, event):
        pass

