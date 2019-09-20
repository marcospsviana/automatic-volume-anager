import gi
gi.require_versions({'Gtk': '3.0', 'GLib': '2.0', 'Gio': '2.0'})
from gi.repository import Gtk, Gdk, GLib
from window_op_hora_diaria import OpcaoHoraDiaria
from tamanhos_tarifas import TamanhosTarifas
from controllers import Management
import numpy as np
class SelectSize(object):
    def __init__(self, arg):
        self.manager = Management()
        self.language = arg
        print("language select size", self.language)
        self.classe = ""
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/select_size.glade")
        self.builder.add_from_file("ui/tamanhos_tarifas.glade")
        self.builder.connect_signals({
            "gtk_main_quit": Gtk.main_quit,
            "on_btn_malasx4_toggled": self.on_btn_malasx4_toggled,
            "on_btn_malasx2_toggled": self.on_btn_malasx2_toggled,
            "on_btn_mochilasx2_toggled": self.on_btn_mochilasx2_toggled,
            "on_btn_cameraenotebook_toggled": self.on_btn_cameraenotebook_toggled,
            "on_btn_confirmar_button_press_event": self.on_btn_confirmar_button_press_event,
            "on_btn_tamanhos_tarifas_button_press_event": self.on_btn_tamanhos_tarifas_button_press_event,
            "on_btn_retornar_button_press_event": self.on_btn_retornar_button_press_event,
            "on_window_tamanhos_tarifas_button_press_event": self.on_btn_tamanhos_tarifas_button_press_event,
            "on_btn_dialog_unavailable_pressed_event": self.on_btn_dialog_unavailable_pressed_event,
        })
        # janela principal
        self.window_select_size = self.builder.get_object("window_select_size")

        # =============== BOTOES ====================
        self.btn_malasx4 = self.builder.get_object("btn_malasx4")
        self.btn_malasx4.connect("toggled", self.on_btn_malasx4_toggled)
        self.btn_malasx2 = self.builder.get_object("btn_malasx2")
        self.btn_malasx2.connect("toggled", self.on_btn_malasx2_toggled)
        self.btn_mochilasx2 = self.builder.get_object("btn_mochilasx2")
        self.btn_mochilasx2.connect("toggled", self.on_btn_mochilasx2_toggled)
        self.btn_cameraenotebook = self.builder.get_object("btn_cameraenotebook")
        self.btn_cameraenotebook.connect("toggled", self.on_btn_cameraenotebook_toggled)
        self.btn_retornar = self.builder.get_object("btn_retornar")
        self.btn_retornar.connect("button_press_event", self.on_btn_retornar_button_press_event)
        self.btn_confirmar = self.builder.get_object("btn_confirmar")
        self.btn_tamanhos_tarifas = self.builder.get_object("btn_tamanhos_tarifas")

        self.btn_usa = self.builder.get_object("btn_usa")
        self.btn_br = self.builder.get_object("btn_br")

        self.btn_br.connect("clicked", self.on_change_language_br)
        self.btn_usa.connect("clicked", self.on_change_language_usa)
       
        # ============= FIM BOTOES ==================

        #============== LABELS ======================
        self.label_malasx4 = self.builder.get_object("label_malasx4")
        self.label_malasx2 = self.builder.get_object("label_malasx2")
        self.label_mochilasx2 = self.builder.get_object("label_mochilasx2")
        self.label_cameraenotebook = self.builder.get_object("label_cameraenotebook")
        
        
        # ============== FIM LABELS =================
        # ============== TELA TAMANHO E TARIFAS =====
        self.window_tamanhos_tarifas = self.builder.get_object("window_tamanhos_tarifas")
        self.btn_retornar_tarifas = self.builder.get_object("btn_retornar_tarifas")
        self.btn_confirmar_tarifas = self.builder.get_object("btn_confirmar_tarifas")
        self.btn_confirmar_tarifas.connect("button_press_event", self.on_btn_confirmar_button_press_event)
        self.btn_malasx4_tarifas = self.builder.get_object("btn_malasx4_tarifas")
        self.btn_malasx4_tarifas.connect("toggled", self.on_btn_malasx4_toggled )
        self.btn_malasx2_tarifas = self.builder.get_object("btn_malasx2_tarifas")
        self.btn_malasx2_tarifas.connect("toggled", self.on_btn_malasx2_toggled)
        self.btn_mochilasx2_tarifas = self.builder.get_object("btn_mochilasx2_tarifas")
        self.btn_mochilasx2_tarifas.connect("toggled", self.on_btn_mochilasx2_toggled)
        self.btn_cameraenotebook_tarifas = self.builder.get_object("btn_cameraenotebook_tarifas")
        self.btn_cameraenotebook_tarifas.connect("toggled", self.on_btn_cameraenotebook_toggled)

        # WINDOW DIALOG UNAVAILABLE
        self.dialog_unavailable = self.builder.get_object("dialog_unavailable")
        self.label_message_armario_unavailable = self.builder.get_object("label_message_armario_unavailable")
        self.btn_dialog_unavailable = self.builder.get_object("btn_dialog_unavailable")
        self.btn_dialog_unavailable.connect("button_press_event", self.on_btn_dialog_unavailable_pressed_event)

        if self.language == "pt_BR":
            self.label_malasx4.set_text("IDEAL PARA")
            self.label_malasx2.set_text("IDEAL PARA")
            self.label_mochilasx2.set_text("IDEAL PARA")
            self.label_cameraenotebook.set_text("IDEAL PARA")
            self.btn_confirmar.set_label("CONFIRMAR")
            self.btn_retornar.set_label("RETORNAR TELA ANTERIOR")
            self.btn_tamanhos_tarifas.set_label("TAMANHOS E TARIFAS")

        elif self.language == "en_US":
            self.label_malasx4.set_text("IDEAL FOR")
            self.label_malasx2.set_text("IDEAL FOR")
            self.label_mochilasx2.set_text("IDEAL FOR")
            self.label_cameraenotebook.set_text("IDEAL FOR")
            self.btn_confirmar.set_label("CONFIRM")
            self.btn_retornar.set_label("PREVIOUS SCREEN")
            self.btn_tamanhos_tarifas.set_label("SIZES AND RATES")
       

        self.window_select_size.fullscreen()
        self.window_select_size.show()

    def on_btn_dialog_unavailable_pressed_event(self, widget, event):
        self.dialog_unavailable.hide()
       
    def on_btn_malasx4_toggled(self, widget):
        
        if self.btn_malasx4.get_active():
            self.classe = "A"
            self.btn_cameraenotebook.get_active()
        else:
            self.classe = ""
        classes = self.manager.lista_armarios()
        print("classes obtidas", classes)
        if self.classe in np.array(classes):
            pass
        else:
            self.classe =""
            if self.language == "pt_BR":
                self.label_message_armario_unavailable.set_text(" INDISPONÍVEL, POR FAVOR ESCOLHA OUTRO TAMANHO! ")
            elif self.language == "en_US":
                self.label_message_armario_unavailable.set_text(" UNAVAILABLE, PLEASE SELECT ANOTHER SIZE! ")
            self.dialog_unavailable.show()

        
        
        
    
    def on_btn_malasx2_toggled(self, widget):
        if self.btn_malasx2.get_active():
            self.classe = "B"
            print(self.classe)
        else:
            self.classe =""
        classes = self.manager.lista_armarios()
        print("classes obtidas", classes)
        if self.classe in np.array(classes):
            pass
        else:
            self.classe =""
            if self.language == "pt_BR":
                self.label_message_armario_unavailable.set_text(" INDISPONÍVEL, POR FAVOR ESCOLHA OUTRO TAMANHO! ")
            elif self.language == "en_US":
                self.label_message_armario_unavailable.set_text(" UNAVAILABLE, PLEASE SELECT ANOTHER SIZE! ")
            self.dialog_unavailable.show()
            

        
    
    def on_btn_mochilasx2_toggled(self, widget):
        if self.btn_mochilasx2.get_active():
            self.classe = "C"
            print(self.classe)
        else:
            self.classe =""
        classes = self.manager.lista_armarios()
        print("classes obtidas", classes)
        if self.classe in np.array(classes):
            pass
        else:
            self.classe =""
            if self.language == "pt_BR":
                self.label_message_armario_unavailable.set_text(" INDISPONÍVEL, POR FAVOR ESCOLHA OUTRO TAMANHO! ")
            elif self.language == "en_US":
                self.label_message_armario_unavailable.set_text(" UNAVAILABLE, PLEASE SELECT ANOTHER SIZE! ")
            self.dialog_unavailable.show()
        

    def on_btn_cameraenotebook_toggled(self, widget):
        if self.btn_cameraenotebook.get_active():
            self.classe = "D"
            print(self.classe)
        else:
            self.classe =""
        classes = self.manager.lista_armarios()
        print("classes obtidas", classes)
        if self.classe in np.array(classes):
            pass
        else:
            self.classe =""
            if self.language == "pt_BR":
                self.label_message_armario_unavailable.set_text(" INDISPONÍVEL, POR FAVOR ESCOLHA OUTRO TAMANHO! ")
            elif self.language == "en_US":
                self.label_message_armario_unavailable.set_text(" UNAVAILABLE, PLEASE SELECT ANOTHER SIZE! ")
            self.dialog_unavailable.show()
        
    
    def on_btn_confirmar_button_press_event(self, widget, event):
        if self.classe == "":
            print ("É necessário escolher um tamanho de armário")
        else:
            print("classe selecionada",self.classe)
            OpcaoHoraDiaria(self.classe, self.language)
            self.window_select_size.hide()
            
    
    def on_btn_retornar_button_press_event(self, widget, event):
        self.window_select_size.hide()
    
    
    
    def on_btn_tamanhos_tarifas_button_press_event(self, widget, event):
        TamanhosTarifas(self.language)
    
    def on_change_language_br(self, event):
        self.language = "pt_BR"
        self.label_malasx4.set_text("IDEAL PARA")
        self.label_malasx2.set_text("IDEAL PARA")
        self.label_mochilasx2.set_text("IDEAL PARA")
        self.label_cameraenotebook.set_text("IDEAL PARA")
        self.btn_retornar.set_label("RETORNAR TELA ANTERIOR")
        self.btn_tamanhos_tarifas.set_label("TAMANHOS E TARIFAS")
        
    
    def on_change_language_usa(self, event):
        self.language = "en_US"
        self.label_malasx4.set_text("IDEAL FOR")
        self.label_malasx2.set_text("IDEAL FOR")
        self.label_mochilasx2.set_text("IDEAL FOR")
        self.label_cameraenotebook.set_text("IDEAL FOR")
        self.btn_retornar.set_label("RETURN TO THE PREVIOUS SCREEN")
        self.btn_tamanhos_tarifas.set_label("SIZES AND RATES")
    
    

if __name__ == "__main__":
    app = SelectSize()
    Gtk.main()