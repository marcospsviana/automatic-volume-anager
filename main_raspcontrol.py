#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

from taxas import *
import sys, os
import datetime
import gi
import numpy as np
from taxas import *
import string
import time
import locale
from datetime import datetime, timedelta, date
import calendar
from time import sleep
import PIL
from PIL import Image
from decimal import Decimal
import encodings.unicode_escape
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf, GObject, GLib
from controllers import Management
#from login import Login
#from encerrar import Encerrar
#from locar import Locar
#from select_option import SelectOption
DDD = ''



class CollBagSafe(object):
    def __init__(self):
        self.language = "pt_BR"
        self.gtk_style()
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/coolbag_safe.glade")
        self.builder.connect_signals({
            "gtk_main_quit": Gtk.main_quit,
            "on_btn_principal_clicked": self.on_btn_principal_clicked,
        })
        self.main_window = self.builder.get_object("mainwindow")
        self.label_horario = self.builder.get_object("label_horario")
        self.label_data = self.builder.get_object("label_data")
        self.btn_flag_br = self.builder.get_object("btn_flag_br")
        self.btn_flag_usa = self.builder.get_object("btn_flag_usa")
        self.spinner_coolbag = self.builder.get_object("spinner_coolbag")
        self.btn_flag_br.connect("clicked", self.on_change_language_br)
        self.btn_flag_usa.connect("clicked", self.on_change_language_usa)
        GLib.timeout_add(1000, self.hora_certa)
        
        self.main_window.fullscreen()
        self.main_window.show()
    
    def hora_certa(self):
        dia = datetime.now()
        dia_hora = dia.strftime("%H:%M:%S")
        dia_data = dia.strftime("%d/%m/%Y")
        self.label_horario.set_text(str(dia_hora))
        self.label_data.set_text(str(dia_data))
        return (self.label_data,self.label_horario)



    def on_btn_principal_clicked(self, event):
        SelectOption(self.language)
    def on_change_language_br(self, event):
        self.language = "pt_BR"
    
    def on_change_language_usa(self, event):
        self.language = "en_US"

    def gtk_style(self):
        css = b"""
        
        @import url("static/css/gtk.css");
        """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

class SelectOption(object):
    def __init__(self, arg):
        self.language = arg
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/select_option.glade")
        self.builder.connect_signals(
            {
                "gtk_main_quit": Gtk.main_quit,
                "on_reservar_button_press_event": self.on_reservar_button_press_event,
                "on_abrir_cofre_button_press_event": self.on_abrir_cofre_button_press_event,
                "on_btn_concluir_button_press_event": self.on_btn_concluir_button_press_event,
                #"on_precosemedidas_button_press_event": self.on_precosemedidas_button_press_event,
            }
        )
        self.select_option = self.builder.get_object("window_select")
        self.btn_reservar = self.builder.get_object("btn_reservar")
        self.btn_abrir = self.builder.get_object("btn_abrir")
        self.btn_concluir = self.builder.get_object("btn_concluir")
        #self.btn_medidas = self.builder.get_object("btn_medidas")
        self.label_horario = self.builder.get_object("label_horario")
        self.label_data = self.builder.get_object("label_data")
        self.btn_flag_br = self.builder.get_object("btn_flag_br")
        self.btn_flag_usa = self.builder.get_object("btn_flag_usa")
        self.btn_flag_br.connect("clicked", self.on_change_language_br)
        self.btn_flag_usa.connect("clicked", self.on_change_language_usa)
        self.label_iniciar_reserva = self.builder.get_object("label_iniciar_reserva")
        self.label_concluir_reserva = self.builder.get_object("label_concluir_reserva")
        self.label_abrir_cofre = self.builder.get_object("label_abrir_cofre")
        #self.label_tamanhos_tafifas = self.builder.get_object("label_tamanhos_tafifas")
        # =========== BUTTONS IMAGES =========================
        self.image_start_reservation = Gtk.Image()
        self.image_iniciar_reserva = Gtk.Image()
        self.image_abrir = Gtk.Image()
        self.image_open_safe = Gtk.Image()
        self.image_concluir_reserva = Gtk.Image()
        self.image_complete_reservation = Gtk.Image()
        #self.image_precos_medidas = Gtk.Image()
        #self.image_sizes_rates = Gtk.Image()

        self.image_abrir.set_from_file("static/images/cadeado.svg")
        self.image_open_safe.set_from_file("static/images/open_safe.svg")
        self.image_start_reservation.set_from_file("static/images/start_reservation.svg")
        self.image_iniciar_reserva.set_from_file("static/images/inicio_reserva.svg")
        self.image_concluir_reserva.set_from_file("static/images/encerrar.svg")
        self.image_complete_reservation.set_from_file("static/images/complete_reservation.svg")
        #self.image_precos_medidas.set_from_file("static/images/precosmedidas.svg")
        #self.image_sizes_rates.set_from_file("static/images/sizes_rates.svg")

        # ========== END BUTTONS IMAGES ======================
        if self.language == "pt_BR":
            self.btn_reservar.set_image(self.image_iniciar_reserva)
            self.btn_concluir.set_image(self.image_concluir_reserva)
            self.btn_abrir.set_image(self.image_abrir)
            #self.btn_medidas.set_image(self.image_precos_medidas)
        elif self.language == "en_US":
            self.btn_reservar.set_image(self.image_start_reservation)
            self.btn_concluir.set_image(self.image_complete_reservation)
            self.btn_abrir.set_image(self.image_open_safe)
            #self.btn_medidas.set_image(self.image_sizes_rates)

        GLib.timeout_add(1000, self.hora_certa )
            
       
        self.select_option.fullscreen()
        self.select_option.show()
        

    def on_reservar_button_press_event(self, widget, event):
        SelectSize(self.language)
        self.select_option.hide()
        
    
    def hora_certa(self):
        dia = datetime.now()
        dia_hora = dia.strftime("%H:%M:%S")
        dia_data = dia.strftime("%d/%m/%Y")
        self.label_horario.set_text(str(dia_hora))
        self.label_data.set_text(str(dia_data))
        return (self.label_data, self.label_horario)
    
    def on_abrir_cofre_button_press_event(self, widget, event):
        self.select_option.hide()
        WindowLogin("abrir", self.language)
    
    def on_btn_concluir_button_press_event(self, widget, event):
        self.select_option.hide()
        WindowLogin("encerrar", self.language)
    def on_precosemedidas_button_press_event(self, widget, event):
        TamanhosTarifas(self.language)
        self.select_option.hide()
    
    def on_change_language_br(self, event):
        self.language = "pt_BR"
        self.btn_reservar.set_image(self.image_iniciar_reserva)
        self.btn_concluir.set_image(self.image_concluir_reserva)
        self.btn_abrir.set_image(self.image_abrir)
        self.btn_medidas.set_image(self.image_precos_medidas)
    
    def on_change_language_usa(self, event):
        self.language = "en_US"
        self.btn_reservar.set_image(self.image_start_reservation)
        self.btn_concluir.set_image(self.image_complete_reservation)
        self.btn_abrir.set_image(self.image_open_safe)
        self.btn_medidas.set_image(self.image_sizes_rates)

class SelectSize(object):
    def __init__(self, arg):
        self.manager = Management()
        self.language = arg
        print("language select size", self.language)
        self.classe = ""
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/select_size.glade")
        #self.builder.add_from_file("ui/tamanhos_tarifas.glade")
        self.builder.connect_signals({
            "gtk_main_quit": Gtk.main_quit,
            "on_btn_malasx4_button_press_event": self.on_btn_malasx4_button_press_event,
            "on_btn_malasx2_button_press_event": self.on_btn_malasx2_button_press_event,
            "on_btn_mochilasx2_button_press_event": self.on_btn_mochilasx2_button_press_event,
            "on_btn_cameraenotebook_button_press_event": self.on_btn_cameraenotebook_button_press_event,
            #"on_btn_confirmar_button_press_event": self.on_btn_confirmar_button_press_event,
            #"on_btn_tamanhos_tarifas_button_press_event": self.on_btn_tamanhos_tarifas_button_press_event,
            "on_btn_retornar_button_press_event": self.on_btn_retornar_button_press_event,
            #"on_window_tamanhos_tarifas_button_press_event": self.on_btn_tamanhos_tarifas_button_press_event,
            "on_btn_dialog_unavailable_button_press_event": self.on_btn_dialog_unavailable_button_press_event,
            "on_btn_usa_button_press_event": self.on_btn_usa_button_press_event,
            "on_btn_br_button_press_event": self.on_btn_br_button_press_event,


        
        })
        # janela principal
        self.window_select_size = self.builder.get_object("window_select_size")

        # =============== BOTOES ====================
        self.btn_malasx4 = self.builder.get_object("btn_malasx4")
        #self.btn_malasx4.connect("button_press_event", self.on_btn_malasx4_button_press_event)
        self.btn_malasx2 = self.builder.get_object("btn_malasx2")
        #self.btn_malasx2.connect("button_press_event", self.on_btn_malasx2_button_press_event)
        self.btn_mochilasx2 = self.builder.get_object("btn_mochilasx2")
        #self.btn_mochilasx2.connect("button_press_event", self.on_btn_mochilasx2_button_press_event)
        self.btn_cameraenotebook = self.builder.get_object("btn_cameraenotebook")
        #self.btn_cameraenotebook.connect("button_press_event", self.on_btn_cameraenotebook_button_press_event)
        self.btn_retornar = self.builder.get_object("btn_retornar")
        #self.btn_retornar.connect("button_press_event", self.on_btn_retornar_button_press_event)
        #self.btn_confirmar = self.builder.get_object("btn_confirmar")
        #self.btn_tamanhos_tarifas = self.builder.get_object("btn_tamanhos_tarifas")
        #self.btn_tamanhos_tarifas.connect("button_press_event", self.on_btn_tamanhos_tarifas_button_press_event)

        self.btn_usa = self.builder.get_object("btn_usa")
        self.btn_br = self.builder.get_object("btn_br")

        #self.btn_br.connect("clicked", self.on_change_language_br)
        #self.btn_usa.connect("clicked", self.on_change_language_usa)
       
        # ============= FIM BOTOES ==================

        #============== LABELS ======================
        self.label_malasx4 = self.builder.get_object("label_malasx4")
        self.label_malasx2 = self.builder.get_object("label_malasx2")
        self.label_mochilasx2 = self.builder.get_object("label_mochilasx2")
        self.label_cameraenotebook = self.builder.get_object("label_cameraenotebook")

        self.label_titulo_select_size = self.builder.get_object("label_titulo_select_size")
        
        
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
        self.dialog_unavailable = self.builder.get_object("dialog_unavailable")
        self.label_message_armario_unavailable = self.builder.get_object("label_message_armario_unavailable")
        self.btn_dialog_unavailable = self.builder.get_object("btn_dialog_unavailable")
        self.btn_dialog_unavailable.connect("button_press_event", self.on_btn_dialog_unavailable_button_press_event)

        if self.language == "pt_BR":
            self.label_malasx4.set_text("IDEAL PARA")
            self.label_malasx2.set_text("IDEAL PARA")
            self.label_mochilasx2.set_text("IDEAL PARA")
            self.label_cameraenotebook.set_text("IDEAL PARA")
            #self.btn_confirmar.set_label("CONFIRMAR")
            self.btn_retornar.set_label("TELA ANTERIOR")
            #self.btn_tamanhos_tarifas.set_label("TAMANHOS E TARIFAS")
            self.label_titulo_select_size.set_text("ESCOLHA o TAMANHO do COFRE DESEJADO!")

        elif self.language == "en_US":
            self.label_malasx4.set_text("IDEAL FOR")
            self.label_malasx2.set_text("IDEAL FOR")
            self.label_mochilasx2.set_text("IDEAL FOR")
            self.label_cameraenotebook.set_text("IDEAL FOR")
            #self.btn_confirmar.set_label("CONFIRM")
            self.btn_retornar.set_label("PREVIOUS SCREEN")
            #self.btn_tamanhos_tarifas.set_label("SIZES AND RATES")
            self.label_titulo_select_size.set_text("CHOOSE THE DESIRED SAFE SIZE!")

        classes = self.manager.lista_armarios()
        if "A" not in np.array(classes):
            if self.language == "pt_BR":
                self.label_malasx4.set_text("INDISPONÍVEL")
            else:
                self.label_malasx4.set_text("UNAVAILABLE")
            
            self.btn_malasx4.set_name("btn_malasx4_inativo")
            
        if "B" not in np.array(classes):
            if self.language == "pt_BR":
                self.label_malasx2.set_text("INDISPONÍVEL")
                
            else:
                self.label_malasx2.set_text("UNAVAILABLE")
            self.btn_malasx2.set_name("btn_malasx2_inativo")
        if "C" not in np.array(classes):
            #self.btn_malasx2.set_sensitive(False)
            if self.language == "pt_BR":
                self.label_mochilasx2.set_text("INDISPONÍVEL")
            else:
                self.label_mochilasx2.set_text("UNAVAILABLE")
            self.btn_mochilasx2.set_name("btn_mochilasx2_inativo")
        if "D" not in np.array(classes):
            #self.btn_malasx2.set_sensitive(False)
            if self.language == "pt_BR":
                self.label_cameraenotebook.set_text("INDISPONÍVEL")
            else:
                self.label_cameraenotebook.set_text("UNAVAILABLE")
            self.btn_cameraenotebook.set_name("btn_cameraenotebook_inativo")
       

        self.window_select_size.fullscreen()
        self.window_select_size.show()

    def on_btn_dialog_unavailable_button_press_event(self, widget, event):
        self.dialog_unavailable.hide()
       
    def on_btn_malasx4_button_press_event(self, widget, event):
        
        
        self.classe = "A"
        #self.btn_cameraenotebook.get_active()   
        classes = self.manager.lista_armarios()
        print("classes obtidas", classes)
        if self.classe in np.array(classes):
            OpcaoHoraDiaria(self.classe, self.language)
            self.window_select_size.hide()
        else:
            self.classe =""
            if self.language == "pt_BR":
                self.label_message_armario_unavailable.set_text(" INDISPONÍVEL, POR FAVOR ESCOLHA OUTRO TAMANHO! ")
            elif self.language == "en_US":
                self.label_message_armario_unavailable.set_text(" UNAVAILABLE, PLEASE SELECT ANOTHER SIZE! ")
            #self.dialog_unavailable.show()
            self.btn_malasx4.set_name("btn_malasx4_inativo")

        
        
        
    
    def on_btn_malasx2_button_press_event(self, widget, event):
        #if self.btn_malasx2.get_active():
        self.classe = "B"
        print(self.classe)
        classes = self.manager.lista_armarios()
        if self.classe in np.array(classes):
            OpcaoHoraDiaria(self.classe, self.language)
            self.window_select_size.hide()
        else:
            self.classe =""
            if self.language == "pt_BR":
                self.label_message_armario_unavailable.set_text(" INDISPONÍVEL, POR FAVOR ESCOLHA OUTRO TAMANHO! ")
            elif self.language == "en_US":
                self.label_message_armario_unavailable.set_text(" UNAVAILABLE, PLEASE SELECT ANOTHER SIZE! ")
            #self.dialog_unavailable.show()
            self.btn_malasx2.set_name("btn_malasx2_inativo")
            print("não tem")
            

        
    
    def on_btn_mochilasx2_button_press_event(self, widget, event):
        #if self.btn_mochilasx2.get_active():
        self.classe = "C"
        print(self.classe)
        
        classes = self.manager.lista_armarios()
        print("classes obtidas", classes)
        if self.classe in np.array(classes):
            OpcaoHoraDiaria(self.classe, self.language)
            self.window_select_size.hide()
        else:
            self.classe =""
            if self.language == "pt_BR":
                self.label_message_armario_unavailable.set_text(" INDISPONÍVEL, POR FAVOR ESCOLHA OUTRO TAMANHO! ")
            elif self.language == "en_US":
                self.label_message_armario_unavailable.set_text(" UNAVAILABLE, PLEASE SELECT ANOTHER SIZE! ")
            #self.dialog_unavailable.show()
            self.btn_mochilasx2.set_name("btn_mochilasx2_inativo")
        

    def on_btn_cameraenotebook_button_press_event(self, widget, event):
        #if self.btn_cameraenotebook.get_active():
        self.classe = "D"
        print(self.classe)
        classes = self.manager.lista_armarios()
        print("classes obtidas", classes)
        if self.classe in np.array(classes):
            OpcaoHoraDiaria(self.classe, self.language)
            self.window_select_size.hide()
        else:
            self.classe =""
            if self.language == "pt_BR":
                self.label_message_armario_unavailable.set_text(" INDISPONÍVEL, POR FAVOR ESCOLHA OUTRO TAMANHO! ")
            elif self.language == "en_US":
                self.label_message_armario_unavailable.set_text(" UNAVAILABLE, PLEASE SELECT ANOTHER SIZE! ")
            #self.dialog_unavailable.show()
            self.btn_cameraenotebook.set_name("btn_cameraenotebook_inativo")
        
    
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
    
    def on_btn_br_button_press_event(self,  event, arg):
        self.language = "pt_BR"
        if self.label_malasx4.get_label() == "UNAVAILABLE" or self.label_malasx4.get_label() == "INDISPONÍVEL":
            self.label_malasx4.set_text("INDISPONÍVEL")
        else:
            self.label_malasx4.set_text("IDEAL PARA")
        
        if self.label_malasx2.get_label() == "UNAVAILABLE" or self.label_malasx2.get_label() == "INDISPONÍVEL":
            self.label_malasx2.set_text("INDISPONÍVEL")
        else:
            self.label_malasx2.set_text("IDEAL PARA")
        if self.label_mochilasx2.get_label() == "UNAVAILABLE" or self.label_mochilasx2.get_label() == "INDISPONÍVEL":
            self.label_mochilasx2.set_text("INDISPONÍVEL")
        else:
            self.label_mochilasx2.set_text("IDEAL PARA")
        if self.label_cameraenotebook.get_label() == "UNAVAILABLE" or self.label_cameraenotebook.get_label() == "INDISPONÍVEL":
            self.label_cameraenotebook.set_text("INDISPONÍVEL")
        else:
            self.label_cameraenotebook.set_text("IDEAL PARA")
        #self.btn_confirmar.set_label("CONFIRMAR")
        self.btn_retornar.set_label("TELA ANTERIOR")
        #self.btn_tamanhos_tarifas.set_label("TAMANHOS E TARIFAS")
        self.label_titulo_select_size.set_text("ESCOLHA o TAMANHO do COFRE DESEJADO!")
        
    
    def on_btn_usa_button_press_event(self, event, arg):
        self.language = "en_US"
        print("en_US")
        if self.label_malasx4.get_label() == "INDISPONÍVEL" or self.label_malasx4.get_label() == "UNAVAILABLE":
            self.label_malasx4.set_text("UNAVAILABLE")
        else:
            self.label_malasx4.set_text("IDEAL FOR")
        
        if self.label_malasx2.get_label() == "INDISPONÍVEL" or self.label_malasx2.get_label() == "UNAVAILABLE":
            self.label_malasx2.set_text("UNAVAILABLE")
        else:
            self.label_malasx2.set_text("IDEAL FOR")
        if self.label_mochilasx2.get_label() == "INDISPONÍVEL" or self.label_mochilasx2.get_label() == "UNAVAILABLE":
            self.label_mochilasx2.set_text("UNAVAILABLE")
        else:
            self.label_mochilasx2.set_text("IDEAL FOR")
        if self.label_cameraenotebook.get_label() == "INDISPONÍVEL" or self.label_cameraenotebook.get_label() == "UNAVAILABLE" :
            self.label_cameraenotebook.set_text("UNAVAILABLE")
        else:
            self.label_cameraenotebook.set_text("IDEAL FOR")
        #self.btn_confirmar.set_label("CONFIRM")
        self.btn_retornar.set_label("PREVIOUS SCREEN")
        #self.btn_tamanhos_tarifas.set_label("SIZES AND RATES")
        self.label_titulo_select_size.set_text("CHOOSE THE DESIRED SAFE SIZE!")
class OpcaoHoraDiaria(object):
    def __init__(self, *args):
        teste = args
        print("op diaria", teste)
        self.classe = args[0]
        self.language = args[1]
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/locacar_hora_diaria.glade")
        self.window_hora_diaria = self.builder.get_object("window_op_hora_diaria")
        self.list_store_flags = self.builder.get_object("list_store_flags")
        self.builder.connect_signals(
            {
                "gtk_main_quit": Gtk.main_quit,
                "on_btn_loc_hora_button_press_event": self.on_btn_loc_hora_button_press_event,
                "on_btn_loc_diaria_button_press_event": self.on_btn_loc_diaria_button_press_event,
                "on_btn_tela_hora_diaria_button_press_event": self.on_btn_tela_hora_diaria_button_press_event,
            }
        )
        
        self.label_por_hora = self.builder.get_object("label_por_hora")
        self.label_por_diaria = self.builder.get_object("label_por_diaria")
        self.btn_tela_hora_diaria = self.builder.get_object("btn_tela_hora_diaria")
        self.btn_usa = self.builder.get_object("btn_usa")
        self.btn_br = self.builder.get_object("btn_br")

        self.btn_br.connect("clicked", self.on_change_language_br)
        self.btn_usa.connect("clicked", self.on_change_language_usa)
        if self.language == "pt_BR":
            self.label_por_hora.set_text("POR HORA")
            self.label_por_diaria.set_text("POR DIÁRIA")
            self.btn_tela_hora_diaria.set_label("RETORNAR TELA ANTERIOR")
        elif self.language == "en_US":
            self.label_por_hora.set_text("HOURLY")
            self.label_por_diaria.set_text("DAILY")
            self.btn_tela_hora_diaria.set_label("RETURN TO THE PREVIOUS SCREEN")

        #self.window_hora_diaria.fullscreen()
        self.window_hora_diaria.show()
    
    def on_btn_loc_hora_button_press_event(self, widget, event):
        tempo_locacao = "horas"
        #CadastroUsuarios(tempo_locacao, self.classe, self.language)
        self.window_hora_diaria.destroy()
        SelectHora(tempo_locacao, self.classe, self.language)
    
    def on_btn_loc_diaria_button_press_event(self, widget, event):
        tempo_locacao = "diaria"
        #CadastroUsuarios(tempo_locacao, self.classe, self.language)
        self.window_hora_diaria.destroy()
        WindowCalendario(tempo_locacao, self.classe, self.language)
        
    
    def on_btn_tela_hora_diaria_button_press_event(self, widget, event):
        self.window_hora_diaria.destroy()
        SelectSize(self.language)
    
    def on_change_language_br(self, event):
        self.language = "pt_BR"
        self.label_por_hora.set_text("POR HORA")
        self.label_por_diaria.set_text("POR DIÁRIA")
        self.btn_tela_hora_diaria.set_label("RETORNAR TELA ANTERIOR")
    
    def on_change_language_usa(self, event):
        self.language = "en_US"
        self.label_por_hora.set_text("HOURLY")
        self.label_por_diaria.set_text("DAILY")
        self.btn_tela_hora_diaria.set_label("RETURN TO THE PREVIOUS SCREEN")



class SelectHora(object):
    """docstring for SelectHora"""
    def __init__(self, *args):
        super(SelectHora, self).__init__()
        self.tempo_locacao = args[0]
        self.classe = args[1][0]
        self.language = args[2]
        if self.classe == "A":
            self.taxa = TaxAndRates.TAXA_HORA_A.value
        elif self.classe == "B":
            self.taxa = TaxAndRates.TAXA_HORA_B.value
        elif self.classe == "C":
            self.taxa = TaxAndRates.TAXA_HORA_C.value
        elif self.classe == "D":
            self.taxa = TaxAndRates.TAXA_HORA_D.value
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
        self.gtk_style_calendario()
        self.diretorio = os.getcwd()
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/w_select_hora.glade")
        self.builder.connect_signals({
            "gtk_main_quit": Gtk.main_quit,
            "on_btn_diminui_hora_button_press_event": self.on_btn_diminui_hora_button_press_event,
            "on_btn_aumenta_hora_button_press_event": self.on_btn_aumenta_hora_button_press_event,
            "on_btn_retornar_select_hora_button_press_event": self.on_btn_retornar_select_hora_button_press_event,
            "on_btn_confirmar_select_hora_button_press_event": self.on_btn_confirmar_select_hora_button_press_event,
            "on_btn_diminui_minuto_button_press_event": self.on_btn_diminui_minuto_button_press_event,
            "on_btn_aumenta_minuto_button_press_event": self.on_btn_aumenta_minuto_button_press_event,

            })
        self.select_hora_window = self.builder.get_object("w_select_hora")
        self.btn_diminui_hora = self.builder.get_object("btn_diminui_hora")
        self.btn_aumenta_hora = self.builder.get_object("btn_aumenta_hora")
        self.btn_diminui_minuto = self.builder.get_object("btn_diminui_minuto")
        self.btn_aumenta_minuto = self.builder.get_object("btn_aumenta_minuto")
        self.btn_retornar_select_hora = self.builder.get_object("btn_retornar_select_hora")
        self.btn_confirmar_select_hora = self.builder.get_object("btn_confirmar_select_hora")

        self.label_hora_ecolhida = self.builder.get_object("label_hora_ecolhida")
        #self.label_hora_ecolhida_up = self.builder.get_object("label_hora_ecolhida_up")
        #s#elf.label_hora_ecolhida_down = self.builder.get_object("label_hora_ecolhida_down")
        #self.label_minuto_ecolhido = self.builder.get_object("label_minuto_ecolhido")
        #self.gtk_treeview_lista_horas = self.builder.get_object("gtk_treeview_lista_horas")
        self.label_data_hora_inicial = self.builder.get_object("label_data_hora_inicial")
        self.label_data_hora_final = self.builder.get_object("label_data_hora_final")

        self.data_atual = datetime.now()
        hora = self.data_atual + timedelta(hours=1)
        self.hora_acrescida = [hora.hour , self.data_atual.minute]
        #self.label_hora_ecolhida_up.set_text("2 horas")
       
        #self.label_minuto_ecolhido.set_text(self.data_atual.strftime("%M"))
        self.label_data_hora_inicial.set_text(self.data_atual.strftime("%d/%m/%Y - %H:%M"))
        self.label_data_hora_final.set_text(hora.strftime("%d/%m/%Y - %H:%M"))
        self.label_periodo_do = self.builder.get_object("label_periodo_do")
        self.label_definir_prazo = self.builder.get_object("label_definir_prazo")
        self.label_valor_total = self.builder.get_object("label_valor_total")
        self.label_ate = self.builder.get_object("label_ate")
        self.label_valor_total_horas = self.builder.get_object("label_valor_total_horas")
        self.label_valor_total_horas.set_text("R$ " + str(self.taxa))

        if self.language == "pt_BR":
            self.label_periodo_do.set_text("Período do")
            self.label_definir_prazo.set_text("Definir o Prazo")
            self.label_valor_total.set_text("Valor total")
            self.label_ate.set_text("até")
            self.btn_retornar_select_hora.set_label("TELA ANTERIOR")
            self.btn_confirmar_select_hora.set_label("CONFIRMAR")
        elif self.language == "en_US":
            self.label_periodo_do.set_text("Start Time and Date")
            self.label_definir_prazo.set_text("Set the Time")
            self.label_valor_total.set_text("Total price")
            self.label_ate.set_text("End Time and Date")
            self.btn_retornar_select_hora.set_label("PREVIOUS SCREEN")
            self.btn_confirmar_select_hora.set_label("CONFIRM")
        if self.language == "pt_BR":
            self.btn_aumenta_hora.set_label("23 horas")
            self.label_hora_ecolhida.set_text("1 hora")
            #self.label_hora_ecolhida_down.set_text("23 horas")
            self.btn_diminui_hora.set_label("2 horas")
            self.horas = {
                            "1 hora"  : 1,
                            "2 horas" : 2,
                            "3 horas" : 3,
                            "4 horas" : 4,
                            "5 horas" : 5,
                            "6 horas" : 6,
                            "7 horas" : 7,
                            "8 horas" : 8,
                            "9 horas" : 9,
                            "10 horas" : 10,
                            "11 horas" : 11,
                            "12 horas" : 12,
                            "13 horas" : 13,
                            "14 horas" : 14,
                            "15 horas" : 15,
                            "16 horas" : 16,
                            "17 horas" : 17,
                            "18 horas" : 18,
                            "19 horas" : 19,
                            "20 horas" : 20,
                            "21 horas" : 21,
                            "22 horas" : 22,
                            "23 horas" : 23,
                        }
            self.hora_labels = [ "1 hora" ,
                             "2 horas",
                             "3 horas",
                             "4 horas",
                             "5 horas",
                             "6 horas",
                             "7 horas",
                             "8 horas",
                             "9 horas",
                            "10 horas",
                            "11 horas",
                            "12 horas",
                            "13 horas",
                            "14 horas",
                            "15 horas",
                            "16 horas",
                            "17 horas",
                            "18 horas",
                            "19 horas",
                            "20 horas",
                            "21 horas",
                            "22 horas",
                            "23 horas",
                            ]
            self.horas_ad = {   0 : "1 hora" ,
                        1  : "2 horas",
                        2  : "3 horas",
                        3  : "4 horas",
                        4  : "5 horas",
                        5  : "6 horas",
                        6  : "7 horas",
                        7  : "8 horas",
                        8  : "9 horas",
                        9  : "10 horas",
                        10 : "11 horas",
                        11 : "12 horas",
                        12 : "13 horas",
                        13 : "14 horas",
                        14 : "15 horas",
                        15 : "16 horas",
                        16 : "17 horas",
                        17 : "18 horas",
                        18 : "19 horas",
                        19 : "20 horas",
                        20 : "21 horas",
                        21 : "22 horas",
                        22 : "23 horas",
                        }
        elif self.language == "en_US":
            self.btn_aumenta_hora.set_label("23 hours")
            self.label_hora_ecolhida.set_text("1 hour")
            #self.label_hora_ecolhida_down.set_text("23 horas")
            self.btn_diminui_hora.set_label("2 hours")
            self.horas = {
                            "1 hour"  : 1,
                            "2 hours" : 2,
                            "3 hours" : 3,
                            "4 hours" : 4,
                            "5 hours" : 5,
                            "6 hours" : 6,
                            "7 hours" : 7,
                            "8 hours" : 8,
                            "9 hours" : 9,
                            "10 hours" : 10,
                            "11 hours" : 11,
                            "12 hours" : 12,
                            "13 hours" : 13,
                            "14 hours" : 14,
                            "15 hours" : 15,
                            "16 hours" : 16,
                            "17 hours" : 17,
                            "18 hours" : 18,
                            "19 hours" : 19,
                            "20 hours" : 20,
                            "21 hours" : 21,
                            "22 hours" : 22,
                            "23 hours" : 23,
                        }
        
            self.hora_labels = [ "1 hour" ,
                                    "2 hours",
                                    "3 hours",
                                    "4 hours",
                                    "5 hours",
                                    "6 hours",
                                    "7 hours",
                                    "8 hours",
                                    "9 hours",
                                "10 hours",
                                "11 hours",
                                "12 hours",
                                "13 hours",
                                "14 hours",
                                "15 hours",
                                "16 hours",
                                "17 hours",
                                "18 hours",
                                "19 hours",
                                "20 hours",
                                "21 hours",
                                "22 hours",
                                "23 hours",
                                ]
            self.horas_ad = {   0 : "1 hour" ,
                         1  : "2 hours",
                         2  : "3 hours",
                         3  : "4 hours",
                         4  : "5 hours",
                         5  : "6 hours",
                         6  : "7 hours",
                         7  : "8 hours",
                         8  : "9 hours",
                        9  : "10 hours",
                        10 : "11 hours",
                        11 : "12 hours",
                        12 : "13 hours",
                        13 : "14 hours",
                        14 : "15 hours",
                        15 : "16 hours",
                        16 : "17 hours",
                        17 : "18 hours",
                        18 : "19 hours",
                        19 : "20 hours",
                        20 : "21 hours",
                        21 : "22 hours",
                        22 : "23 hours",
                        }
        
        """store = Gtk.ListStore(str)
        dados_horas = [["1 hora"]  , ["2 horas"] ,["3 horas"] ,["4 horas"] ,["5 horas"] , ["6 horas"] , ["7 horas"] , ["8 horas"] , ["9 horas"] ,
        ["10 horas"], ["11 horas"], ["12 horas"], ["13 horas"], ["14 horas"], ["15 horas"], ["16 horas"], ["17 horas"], ["18 horas"],
        ["19 horas"], ["20 horas"], ["21 horas"], ["22 horas"], ["23 horas"],]"""


        self.select_hora_window.show()

    def on_btn_aumenta_hora_button_press_event(self, event, arg):
        data = datetime.now()
        data = data + timedelta(hours=1)
        self.label_data_hora_final.set_text(data.strftime("%d/%m/%Y - %H:%M"))
        hora_total = self.label_hora_ecolhida.get_label()
        print("hora_total", hora_total)

        hora = self.horas[hora_total]
        print("hora", hora)
        #hora -= 2 
        print("hora -1", hora)
        """if hora == 22:
                                    hora = 0
                                else:"""
        hora -=  2
        
        self.label_hora_ecolhida.set_text(self.hora_labels[hora])       
        self.btn_aumenta_hora.set_label(self.hora_labels[hora -1])
        self.btn_diminui_hora.set_label(self.hora_labels[hora + 1])
        total_atual = self.label_valor_total_horas.get_label()
        total_atual = total_atual.replace(",",".")
        total = float(self.horas[self.label_hora_ecolhida.get_label()]) * self.taxa 
        total = str("%.2f"%total)
        total = total.replace(".", ",")
        self.label_valor_total_horas.set_text("R$ " + total)
        
        data_final = data + timedelta(hours=int(self.horas[self.label_hora_ecolhida.get_label()]))
        self.label_data_hora_inicial.set_text(data.strftime("%d/%m/%Y - %H:%M"))
        self.label_data_hora_final.set_text(data_final.strftime("%d/%m/%Y - %H:%M"))

        

    def on_btn_diminui_hora_button_press_event(self, event, arg):
        data = datetime.now()
        data = data + timedelta(hours=1)
        self.label_data_hora_final.set_text(data.strftime("%d/%m/%Y - %H:%M"))
        hora_total = self.label_hora_ecolhida.get_label()
        hora = 0
        hora = self.horas[hora_total]
        hora = hora - 1
        if hora == 22:
            hora = 0
        else:
            hora +=   1
        self.label_hora_ecolhida.set_text(self.horas_ad[hora])
        #self.label_hora_ecolhida_up.set_text(self.hora_labels[hora + 1])
        #self.label_hora_ecolhida_down.set_text(self.hora_labels[hora - 1])
        if self.label_hora_ecolhida.get_label() == "23 horas" or self.label_hora_ecolhida.get_label() == "23 hours":
            self.btn_diminui_hora.set_label(self.hora_labels[0])
            self.btn_aumenta_hora.set_label(self.hora_labels[hora - 1])
        else:
            self.btn_diminui_hora.set_label(self.hora_labels[hora + 1])
            self.btn_aumenta_hora.set_label(self.hora_labels[hora - 1])

        total = float(self.horas[self.label_hora_ecolhida.get_label()]) * self.taxa #+ float(total_atual)
        total = str("%.2f"%total)
        total = total.replace(".", ",")
        self.label_valor_total_horas.set_text("R$ " + total)
        data_final = data + timedelta(hours=int(self.horas[self.label_hora_ecolhida.get_label()]))
        self.label_data_hora_inicial.set_text(data.strftime("%d/%m/%Y - %H:%M"))
        self.label_data_hora_final.set_text(data_final.strftime("%d/%m/%Y - %H:%M"))

    def on_btn_diminui_minuto_button_press_event(self, event, arg):
        pass

    def on_btn_aumenta_minuto_button_press_event(self, event, arg):
        pass
    def on_btn_retornar_select_hora_button_press_event(self, event, arg):
        #self.label_valor_total_value.set_text("")
        self.select_hora_window.hide()
        OpcaoHoraDiaria(self.classe, self.language)
    def on_btn_confirmar_select_hora_button_press_event(self, event, arg):
        self.total = self.label_valor_total_horas.get_text()
        self.total = self.total[3:]
        print(self.total)
        self.hora = self.horas[self.label_hora_ecolhida.get_label()]
        dia = 0
        self.select_hora_window.hide()
        CadastroUsuarios(self.total , self.language, self.classe, dia, self.hora)
    
    def gtk_style_calendario(self):
        css = b"""
        @import url("static/css/calendario.css");
        """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
class WindowCalendario:
    def __init__(self, *args):
        #op_and_language = args
        #print("op diaria", teste)
        self.resultado_dias = 0
        self.total_horas = 0
        self.tempo_locacao = args[0]
        self.classe = args[1][0]
        self.language = args[2]
        if self.classe == "A":
            self.taxa = TaxAndRates.TAXA_DIARIA_A.value
        elif self.classe == "B":
            self.taxa = TaxAndRates.TAXA_DIARIA_B.value
        
        elif self.classe == "C":
            self.taxa = TaxAndRates.TAXA_DIARIA_C.value
        
        elif self.classe == "D":
            self.taxa = TaxAndRates.TAXA_DIARIA_D.value
        
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
        self.builder = Gtk.Builder()
        self.gtk_style_calendario()
        self.builder.add_from_file("ui/calendario_window.glade")
        self.builder.connect_signals(
            {
                "on_btn_button_press_event"               : self.on_btn_button_press_event,
                "on_btn_previous_mont_button_press_event" : self.on_btn_previous_mont_button_press_event,
                "on_btn_next_month_button_press_event"    : self.on_btn_next_month_button_press_event,
                #"on_btn_previous_year_button_press_event" : self.on_btn_previous_year_button_press_event,
                #"on_btn_next_year_button_press_event"     : self.on_btn_next_year_button_press_event,
                "on_btn_confirmar_calendario_button_press_event"     : self.on_btn_confirmar_calendario_button_press_event,
                "on_btn_cancelar_calendario_button_press_event"      : self.on_btn_cancelar_calendario_button_press_event,
                "gtk_main_quit"                           : self.on_calendario_window_quit,
            }
        )
        self.calendario_window = self.builder.get_object("calendario_window")

        # ===================== LABELS ========================
        self.label_month = self.builder.get_object("label_month")
        #self.label_year = self.builder.get_object("label_year")
        self.label_valor_total_value = self.builder.get_object("label_valor_total_value")
        self.label_valor_total = self.builder.get_object("label_valor_total")

        self.label_data_hora_inicial = self.builder.get_object("label_data_hora_inicial")
        self.label_data_hora_final = self.builder.get_object("label_data_hora_final")
        self.label_ate = self.builder.get_object("label_ate")
        self.label_periodo_do = self.builder.get_object("label_periodo_do")


        #===================== BUTTONS ========================
        self.btn_previous_mont = self.builder.get_object("btn_previous_mont")
        self.btn_next_mont = self.builder.get_object("btn_next_mont")
        #self.btn_previous_year = self.builder.get_object("btn_previous_year")
        #self.btn_next_year = self.builder.get_object("btn_next_year")

        self.btn_confirmar_calendario = self.builder.get_object("btn_confirmar_calendario")
        self.btn_cancelar_calendario = self.builder.get_object("btn_cancelar_calendario")
        #self.btn_confirmar.connect("button_press_event", self.on_btn_confirmar_button_press_event)

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
        self.meses_indices = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12 }
        
        self.meses = calendar.month_name #lista dos nomes dos meses do ano mes[1] == "January"
        self.ano = self.data.year
        self.label_month.set_label(self.data.strftime("%B"))
        #self.label_year.set_label(str(self.ano))
        self.label_data_hora_inicial.set_text(self.data.strftime("%d/%m/%Y - %H:%M"))
        self.label_data_hora_final.set_text(self.data.strftime("%d/%m/%Y - %H:%M"))
        calendar.setfirstweekday(calendar.SUNDAY)
        if self.language == "pt_BR":
            self.label_periodo_do.set_text("Período do")
            #self.label_definir_prazo.set_text("Definir o Prazo")
            self.label_valor_total.set_text("Valor total")
            self.label_ate.set_text("até")
            self.btn_cancelar_calendario.set_label("TELA ANTERIOR")
            self.btn_confirmar_calendario.set_label("CONFIRMAR")
            
        elif self.language == "en_US":
            self.label_periodo_do.set_text("Start Time and Date")
            #self.label_definir_prazo.set_text("Set the Time")
            self.label_valor_total.set_text("Total price")
            self.label_ate.set_text("End Time and Date")
            self.btn_cancelar_calendario.set_label("PREVIOUS SCREEN")
            self.btn_confirmar_calendario.set_label("CONFIRM")

        self.dias_meses = [ [self.btn0, self.btn1, self.btn2, self.btn3, self.btn4, self.btn5,self.btn6],
                            [self.btn7, self.btn8, self.btn9, self.btn10,self.btn11,self.btn12,self.btn13],
                            [self.btn14,self.btn15,self.btn16,self.btn17,self.btn18,self.btn19, self.btn20],
                            [self.btn21,self.btn22,self.btn23,self.btn24, self.btn25,self.btn26,self.btn27],
                            [self.btn28,self.btn29, self.btn30,self.btn31,self.btn32,self.btn33,self.btn34],
                            [self.btn35,self.btn36, self.btn37,self.btn38,self.btn39,self.btn40,self.btn41]
                    ]
        self.dias_dom = [self.btn0, self.btn7, self.btn14, self.btn21, self.btn28, self.btn6, self.btn13, self.btn20, self.btn27, self.btn34, self.btn35, self.btn41]
        self.dias_totais = [self.btn0, self.btn1, self.btn2, self.btn3, self.btn4, self.btn5,self.btn6,
                            self.btn7, self.btn8, self.btn9, self.btn10,self.btn11,self.btn12,self.btn13,
                            self.btn14,self.btn15,self.btn16,self.btn17,self.btn18,self.btn19, self.btn20,
                            self.btn21,self.btn22,self.btn23,self.btn24, self.btn25,self.btn26,self.btn27,
                            self.btn28,self.btn29, self.btn30,self.btn31,self.btn32,self.btn33,self.btn34,
                            self.btn35,self.btn36, self.btn37,self.btn38,self.btn39,self.btn40,self.btn41]
        



        
        self.set_calendario(self.data.year, self.data.month)

        #self.calendario_window.fullscreen()
        self.calendario_window.show()
    def on_btn_cancelar_calendario_button_press_event(self, widget, event):
        self.label_valor_total_value.set_text("")
        self.calendario_window.hide()
        OpcaoHoraDiaria(self.classe, self.language)
    def on_btn_confirmar_calendario_button_press_event(self, widget, event):
        self.total = self.label_valor_total_value.get_label()
        self.on_calendario_window_quit()
        CadastroUsuarios(self.total , self.language, self.classe, self.resultado_dias, self.total_horas)

    def on_btn_button_press_event(self, widget, args):
        self.widget = widget.get_label()
        data = datetime(self.data.year, self.data.month, self.data.day, self.data.hour, self.data.minute)
        mes_escolhido = self.meses_indices[self.label_month.get_label()]
        print("mes_escolhido", mes_escolhido)
        #ano_escolhido = int(self.label_year.get_label())
        data2 = datetime(self.data.year, mes_escolhido, int(self.widget), self.data.hour, self.data.minute )
        self.resultado_dias = abs((data2 - data).days)
        total = self.taxa * self.resultado_dias #(int(self.widget) - self.data.day)
        print("total = %.2f"%(total))
        total = str("%.2f"%total)
        total = total.replace(".", ",")
        self.label_valor_total_value.set_text("R$ " + total)
        #self.label_valor_total_value.set_text("%.2f"%(total))
        self.label_data_hora_final.set_text(data2.strftime("%d/%m/%Y - %H:%M"))
        print(self.widget)
        for i in range(len(self.dias_meses)):
            for j,d in zip(self.dias_meses[i], range(7)):
                
                if self.dias_meses[i][d].get_label() != "" and int(self.dias_meses[i][d].get_label()) >= self.data.day and int(self.dias_meses[i][d].get_label()) < int(self.widget):
                    self.dias_meses[i][d].set_name("intervalo_selecionado")
                elif self.dias_meses[i][d].get_label() == "" or (self.meses_indices[self.label_month.get_label()] == self.data.month and int(self.dias_meses[i][d].get_label()) < self.data.day):
                    print("dias messess",self.dias_meses[i][d].get_label() , " button ==> ", self.dias_meses[i][d].get_name())
                    self.dias_meses[i][d].set_sensitive(False)
                    self.dias_meses[i][d].set_name("dia_passado")
                elif self.dias_meses[i][d].get_label() != "" and int(self.dias_meses[i][d].get_label()) < int(self.widget) and self.meses_indices[self.label_month.get_label()] > self.meses_indices[self.meses[self.data.month]]:
                    self.dias_meses[i][d].set_name("intervalo_selecionado")
               
                elif self.dias_meses[i][d].get_label() != "" and self.label_month.get_label() != self.meses[self.data.month] and self.dias_meses[i][d] not in self.dias_dom :
                    print("dias normais",self.dias_meses[i][d].get_label())
                    self.dias_meses[i][d].set_sensitive(True)
                    self.dias_meses[i][d].set_name("btn_calendario")
                elif self.dias_meses[i][d].get_label() != "" and self.dias_meses[i][d] in self.dias_dom and not(self.meses_indices[self.label_month.get_label()] == self.data.month and int(self.dias_meses[i][d].get_label()) < self.data.day):
                    self.dias_meses[i][d].set_name("btn_calendario_dom")
                elif int(self.dias_meses[i][d].get_label()) == data.day and self.meses_indices[self.label_month.get_label()] == data.month:
                    self.dias_meses[i][d].set_name("dia_corrente")
                    self.dias_meses[i][d].set_sensitive(False)
                else:
                    self.dias_meses[i][d].set_name("btn_calendario")
                    self.dias_meses[i][d].set_sensitive(True)
                
                if self.dias_meses[i][d].get_label() == "":
                    self.dias_meses[i][d].set_sensitive(False)
                    self.dias_meses[i][d].set_name("dia_passado")
                if self.dias_meses[i][d].get_label() == self.widget:
                    self.dias_meses[i][d].set_name("dia_selecionado")
                
        return self.resultado_dias


        
    def set_calendario(self, ano, mes):
        
        self.mes = calendar.monthcalendar(ano, mes)
        self.month = mes
        self.label_month.set_text(self.meses[mes])
        #self.label_year.set_text(str(ano))
        data  = datetime.now()

        self.dias_meses = [ [self.btn0, self.btn1, self.btn2, self.btn3, self.btn4, self.btn5,self.btn6],
                            [self.btn7, self.btn8, self.btn9, self.btn10,self.btn11,self.btn12,self.btn13],
                            [self.btn14,self.btn15,self.btn16,self.btn17,self.btn18,self.btn19, self.btn20],
                            [self.btn21,self.btn22,self.btn23,self.btn24, self.btn25,self.btn26,self.btn27],
                            [self.btn28,self.btn29, self.btn30,self.btn31,self.btn32,self.btn33,self.btn34],
                            [self.btn35,self.btn36, self.btn37,self.btn38,self.btn39,self.btn40,self.btn41]
                    ]
        self.dias_dom = [self.btn0, self.btn7, self.btn14, self.btn21, self.btn28, self.btn6, self.btn13, self.btn20, self.btn27, self.btn34, self.btn35, self.btn41]
        self.dias_totais = [self.btn0, self.btn1, self.btn2, self.btn3, self.btn4, self.btn5,self.btn6,
                            self.btn7, self.btn8, self.btn9, self.btn10,self.btn11,self.btn12,self.btn13,
                            self.btn14,self.btn15,self.btn16,self.btn17,self.btn18,self.btn19, self.btn20,
                            self.btn21,self.btn22,self.btn23,self.btn24, self.btn25,self.btn26,self.btn27,
                            self.btn28,self.btn29, self.btn30,self.btn31,self.btn32,self.btn33,self.btn34,
                            self.btn35,self.btn36, self.btn37,self.btn38,self.btn39,self.btn40,self.btn41]
        self.dia = 0
        #grantindo que o botão não terá valor None
        for i in range(len(self.dias_meses)):
            for d in range(len(self.dias_meses[i])):
                self.dias_meses[i][d].set_label("")
                self.dias_meses[i][d].set_name("dia_passado")
                self.dias_meses[i][d].set_sensitive(False)
                
        for i in range(len(self.mes)):
            for j,d in zip(self.mes[i], range(7)):
                if self.mes[i][d] == 0 or self.mes[i][d] == None:
                    self.dias_meses[i][d].set_label("")
                    self.dias_meses[i][d].set_sensitive(False)
                    self.dias_meses[i][d].set_name("dia_passado")
                else:
                    self.dias_meses[i][d].set_label(str(self.mes[i][d]))
       
        
        for i in range(len(self.mes)):
            for j,d in zip(self.mes[i], range(7)):
                print("self.meses_indices[self.label_month.get_label()", self.meses_indices[self.label_month.get_label()])
                print("self.data.month", self.data.month)
                print("self.dias_meses[i][d] in self.dias_dom", self.dias_meses[i][d] in self.dias_dom)
                if self.dias_meses[i][d].get_label() == '0':
                    self.dias_meses[i][d].set_label("")
                    self.dias_meses[i][d].set_sensitive(False)
                elif self.dias_meses[i][d].get_label() != "" and int(self.dias_meses[i][d].get_label()) == data.day and self.meses_indices[self.label_month.get_label()] == data.month:
                    self.dias_meses[i][d].set_name("dia_corrente")
                    self.dias_meses[i][d].set_sensitive(False)
                
                elif self.dias_meses[i][d].get_label() == "" or (self.meses_indices[self.label_month.get_label()] == self.data.month and int(self.dias_meses[i][d].get_label()) < self.data.day):
                    print("dias messess",self.dias_meses[i][d].get_label())
                    self.dias_meses[i][d].set_sensitive(False)
                    self.dias_meses[i][d].set_name("dia_passado")
                elif self.label_month.get_label() != self.meses[self.data.month] and self.dias_meses[i][d] not in self.dias_dom :
                    print("dias normais",self.dias_meses[i][d].get_label())
                    self.dias_meses[i][d].set_sensitive(True)
                    self.dias_meses[i][d].set_name("btn_calendario")
                elif self.dias_meses[i][d] in self.dias_dom and not(self.meses_indices[self.label_month.get_label()] == self.data.month and int(self.dias_meses[i][d].get_label()) < self.data.day):
                    self.dias_meses[i][d].set_name("btn_calendario_dom")
                    self.dias_meses[i][d].set_sensitive(True)
                
                else:
                    self.dias_meses[i][d].set_sensitive(True)
                    self.dias_meses[i][d].set_name("btn_calendario")
                    self.dia = self.dias_meses[i][d].get_label()
                if self.dias_meses[i][d].get_label() == "":
                    self.dias_meses[i][d].set_sensitive(False)
                    self.dias_meses[i][d].set_name("dia_passado")
        # caso o tamanho de meses indices seja maior que o mes corrente desativa os botões restantes que estarão vazios
        if len(self.mes) == 5:
            for i in self.dias_meses[5]:
                i.set_sensitive(False)

        teste = self.meses_indices[self.label_month.get_label()]
        print("teste", teste)
        teste2 = self.label_month.get_label()
        print("teste2", teste2)
        if self.meses_indices[self.label_month.get_label()] == self.data.month:
            self.btn_previous_mont.set_sensitive(False)
        else:
            self.btn_previous_mont.set_sensitive(True)

        """if int(self.label_year.get_label()) == self.data.year:
            self.btn_previous_year.set_sensitive(False) 
        else:
            self.btn_previous_year.set_sensitive(True)"""    

        
    
    def on_btn_previous_mont_button_press_event(self, event, args):
        self.label_valor_total_value.set_text("")
        self.mes_atual = self.meses_indices[self.label_month.get_label()]
        print("self.mes_atual", self.mes_atual)
        self.ano_atual = self.data.year #int(self.label_year.get_label())
        if self.mes_atual == 1:
            self.mes_atual = 12
            #self.ano_atual = self.ano_atual - 1
        else:
            self.mes_atual =  self.mes_atual - 1
            
            
        self.set_calendario(self.ano_atual, self.mes_atual) 
       
       
    
    def on_btn_next_month_button_press_event(self, event, args):
        self.label_valor_total_value.set_text("")
        self.mes_atual = self.meses_indices[self.label_month.get_label()]
        print("self.mes_atual", self.mes_atual)
        self.ano_atual = self.data.year #int(self.label_year.get_label())
        if self.mes_atual == 12:
            self.mes_atual = 1
            #self.ano_atual = self.ano_atual + 1
        else:
            self.mes_atual =  self.mes_atual + 1
            
            
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
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )



class CadastroUsuarios(object):
    def __init__(self, *args):
        teste = args
        print(teste)
        teste = args
        print(teste)
        self.valor_total = args[0]
        global DDD
        #self.classe = args[1][0]
        self.language = args[1]
        self.classe = args[2]
        #print(self.classe)
        print(self.valor_total)
        print(self.language)
        self.alfa = list(string.ascii_uppercase) # alfabeto para gerar o teclado
        self.num = list(map(lambda x: x, range(10))) # números para o teclado numérico
        self.entry = ""
        self.dia = args[3]
        self.hora = args[4]
        self.minuto = 0
        self.builder = Gtk.Builder()
        self.builder.connect_signals({
            "gtk_main_quit": Gtk.main_quit,
            "on_btn_confirmar_button_press_event": self.on_btn_confirmar_button_press_event,
            "on_btn_retornar_button_press_event": self.on_btn_retornar_button_press_event,
            "on_entry_nome_button_press_event": self.on_entry_nome_button_press_event,
            "on_entry_email_button_press_event": self.on_entry_email_button_press_event,
            "on_entry_celular_button_press_event": self.on_entry_celular_button_press_event,
            "on_entry_quantidade_diaria_button_press_event": self.on_entry_quantidade_diaria_button_press_event,
            "on_entry_quantidade_horas_button_press_event": self.on_entry_quantidade_horas_button_press_event,
            #"on_entry_minutos_button_press_event": self.on_entry_minutos_button_press_event,
            "on_btn_limpar_nome_button_press_event": self.on_btn_limpar_nome_button_press_event,
            "on_btn_limpar_email_button_press_event": self.on_btn_limpar_email_button_press_event,
            "on_btn_limpar_celular_button_press_event": self.on_btn_limpar_celular_button_press_event,
            "on_btn_limpar_quantidade_diaria_button_press_event": self.on_btn_limpar_quantidade_diaria_button_press_event,
            "on_btn_limpar_horas_button_press_event": self.on_btn_limpar_horas_button_press_event,
            #"on_btn_limpar_minutos_button_press_event": self.on_btn_limpar_minutos_button_press_event,
            "on_btn_retornar_entrada_dados_button_press_event": self.on_btn_retornar_entrada_dados_button_press_event,
            "on_entry_entrada_dados_button_press_event": self.on_entry_entrada_dados_button_press_event,
            "on_btn_confirmar_entrada_dados_button_press_event": self.on_btn_confirmar_entrada_dados_button_press_event,
            "on_btn_confirmar_entrada_numero_button_press_event": self.on_btn_confirmar_entrada_numero_button_press_event,
            "on_btn_retornar_entrada_numeros_button_press_event": self.on_btn_retornar_entrada_numeros_button_press_event,
            "on_entry_entrada_numeros_button_press_event": self.on_entry_entrada_numeros_button_press_event,
            "on_btn_dialog_preencher_campos_pressed_event": self.on_btn_dialog_preencher_campos_pressed_event,
            "on_btn_finalizar_sessao_button_press_event": self.on_btn_finalizar_sessao_button_press_event,
            "on_btn_backspace_button_press_event": self.on_btn_backspace_button_press_event,
            "on_btn_limpar_entrada_numeros_button_press_event": self.on_btn_limpar_entrada_numeros_button_press_event,
            #"on_btn_window_payment_wait_button_press_event": self.on_btn_window_payment_wait_button_press_event,
            "on_button_fechar_armario_button_press_event": self.on_button_fechar_armario_button_press_event,
            #"on_btn_credito_button_press_event": self.on_btn_credito_button_press_event,
            #"on_btn_debito_button_press_event": self.on_btn_debito_button_press_event,
            #"on_btn_cancelar_button_press_event": self.on_btn_cancelar_button_press_event
            "on_btn_tente_novamente_window_erro_pagamentos_button_press_event": self.on_btn_tente_novamente_window_erro_pagamentos_button_press_event,
            "on_btn_cancelar_window_erro_pagamentos_button_press_event": self.on_btn_cancelar_window_erro_pagamentos_button_press_event
        })
        self.builder.add_from_file("ui/cadastro_usuario.glade")
        self.window_cadastro_usuario = self.builder.get_object("window_cadastro_usuario")
        #self.window_payment = self.builder.get_object("window_payment_wait")
        self.window_entrada_dados = self.builder.get_object("window_entrada_dados")
        self.window_entrada_numeros = self.builder.get_object("window_entrada_numeros")
        self.window_select_cartao = self.builder.get_object("window_select_cartao")
        self.dialog_retorno_cadastro = self.builder.get_object("dialog_retorno_cadastro")
        self.dialog_message_preencher_campos = self.builder.get_object("dialog_message_preencher_campos")
        self.dialog_instrucao_fecha_armario = self.builder.get_object("dialog_instrucao_fecha_armario")
        self.window_conclusao  = self.builder.get_object("dialog_conclusao")
        self.window_erro_pagamentos = self.builder.get_object("window_erro_pagamento")
        

        """ =================LABELS ====================="""

        self.label_nome = self.builder.get_object("label_nome")
        self.label_email = self.builder.get_object("label_email")
        self.label_telefone = self.builder.get_object("label_celular")
        self.label_quantidade_diaria = self.builder.get_object("label_quantidade_diaria")
        self.label_quantidade_horas = self.builder.get_object("label_quantidade_horas")
        #self.label_quantidade_minutos = self.builder.get_object("label_quantidade_minutos")
        self.label_total = self.builder.get_object("label_total")
        self.label_total.set_text(self.valor_total)
        self.label_valor_da_locacao = self.builder.get_object("label_valor_da_locacao")
        
        self.label_senha0 = self.builder.get_object("label_senha0")
        self.label_senha1 = self.builder.get_object("label_senha1")
        self.label_senha2 = self.builder.get_object("label_senha2")
        self.label_senha3 = self.builder.get_object("label_senha3")
        self.label_compartimento_titulo = self.builder.get_object("label_compartimento_titulo")
        self.label_compartimento = self.builder.get_object("label_compartimento")
        self.label_inicio_locacao_titulo = self.builder.get_object("label_inicio_locacao_titulo")
        self.label_date_inicio_locacao = self.builder.get_object("label_date_inicio_locacao")
        self.label_hour_inicio_locacao = self.builder.get_object("label_hour_inicio_locacao")
        self.label_hour_inicio_locacao1 = self.builder.get_object("label_hour_inicio_locacao1")
        self.label_minute_inicio_locacao = self.builder.get_object("label_minute_inicio_locacao")
        self.label_fim_locacao_titulo = self.builder.get_object("label_fim_locacao_titulo")
        self.label_date_fim_locacao = self.builder.get_object("label_date_fim_locacao")
        self.label_hour_fim_locacao = self.builder.get_object("label_hour_fim_locacao")
        self.label_hour_fim_locacao1 = self.builder.get_object("label_hour_fim_locacao1")
        self.label_minute_fim_locacao = self.builder.get_object("label_minute_fim_locacao")
        self.label_message_envio_email = self.builder.get_object("label_message_envio_email")
        #self.label_senha = self.builder.get_object("label_senha")
        

        " ----------   LABEL ENTRADA_DADOS --------------"
        self.label_entrada_dados = self.builder.get_object("label_entrada_dados")

        " ----------   LABEL ENTRADA NUMEROS ------------"
        self.label_entrada_numeros = self.builder.get_object("label_entrada_numeros")
        " ----------   LABEL DIALOGO RETORNO CADASTRO ---"
        self.label_retorno_cadastro = self.builder.get_object("label_retorno_cadastro")
        " ----------   LABEL dialog_message_preencher_campos -------------"
        self.label_message_preencher_campos = self.builder.get_object("label_message_preencher_campos")
        " ----------   LABEL DIALOG INSTRUCAO FECHAR ARMARIO -------------"
        self.label_instrucao = self.builder.get_object("label_instrucao")
        " ----------   LABEL WINDOW CONCLUSAO ----------------------------"
        
        self.label_senha_titulo = self.builder.get_object("label_senha_titulo")
        self.label_inicio_locacao_titulo = self.builder.get_object("label_inicio_locacao_titulo")
        self.label_fim_locacao_titulo = self.builder.get_object("label_fim_locacao_titulo")
        " ----------------- LABEL WAIT PAYMENT ---------------------------"
        #self.label_aguarde_pagamento = self.builder.get_object("label_aguarde_pagamento")

        #================== LABEL window_erro_pagamentos =========================
        self.label_window_erro_pagamentos = self.builder.get_object("label_window_erro_pagamentos")

        self.label_menu = self.builder.get_object("label_menu")

        # ================FIM LABELS===================
        self.spinner = self.builder.get_object("spinner")

        # ================= ENTRYS ====================

        self.entry_nome = self.builder.get_object("entry_nome")
        self.entry_nome.connect("button_press_event", self.on_entry_nome_button_press_event)
        self.entry_email = self.builder.get_object("entry_email")
        self.entry_email.connect("button_press_event", self.on_entry_email_button_press_event)
        self.entry_celular = self.builder.get_object("entry_celular")
        self.entry_celular.connect("button_press_event", self.on_entry_celular_button_press_event)
        self.entry_quantidade_diaria = self.builder.get_object("entry_quantidade_diaria")
        self.entry_quantidade_diaria.connect("button_press_event", self.on_entry_quantidade_diaria_button_press_event)
        self.entry_quantidade_horas = self.builder.get_object("entry_quantidade_horas")
        self.entry_quantidade_horas.connect("button_press_event", self.on_entry_quantidade_horas_button_press_event)
        #self.entry_minutos = self.builder.get_object("entry_minutos")
        #self.entry_minutos.connect("button_press_event", self.on_entry_minutos_button_press_event)

        """ -----------ENTRY WINDOW_ENTRADA_DADOS ------------"""
        self.entry_entrada_dados = self.builder.get_object("entry_entrada_dados")
        self.entry_entrada_dados.connect("button_press_event", self.on_entry_entrada_dados_button_press_event)
        """ -----------ENTRY WINDOW_ENTRADA_NUMEROS ---------"""
        self.entry_entrada_numeros = self.builder.get_object("entry_entrada_numeros")

        """ =================FIM ENTRYS=================== """

        """ ================= BUTTONS ======================= """

        self.btn_limpar_nome = self.builder.get_object("btn_limpar_nome")
        self.btn_limpar_nome.connect("button_press_event", self.on_btn_limpar_nome_button_press_event)
        self.btn_limpar_email = self.builder.get_object("btn_limpar_email")
        self.btn_limpar_email.connect("button_press_event", self.on_btn_limpar_email_button_press_event)
        self.btn_limpar_celular = self.builder.get_object("btn_limpar_celular")
        self.btn_limpar_celular.connect("button_press_event", self.on_btn_limpar_celular_button_press_event)
        self.btn_limpar_quantidade_diaria = self.builder.get_object("btn_limpar_quantidade_diaria")
        self.btn_limpar_quantidade_diaria.connect("button_press_event", self.on_btn_limpar_quantidade_diaria_button_press_event)
        self.btn_limpar_horas = self.builder.get_object("btn_limpar_horas")
        self.btn_limpar_horas.connect("button_press_event", self.on_btn_limpar_horas_button_press_event)
        #self.btn_limpar_minutos = self.builder.get_object("btn_limpar_minutos")
        #self.btn_limpar_minutos.connect("button_press_event", self.on_btn_limpar_minutos_button_press_event)
        self.btn_confirmar = self.builder.get_object("btn_confirmar_cadastro_usuario")
        self.btn_confirmar.connect("button_press_event", self.on_btn_confirmar_button_press_event)
        self.btn_retornar = self.builder.get_object("btn_retornar")
        self.btn_retornar.connect("button_press_event", self.on_btn_retornar_button_press_event)
        self.btn_limpar_entrada_numeros = self.builder.get_object("btn_limpar_entrada_numeros")
        self.btn_limpar_entrada_numeros.connect("button_press_event", self.on_btn_limpar_entrada_numeros_button_press_event)

        #self.btn_finalizar_sessao = self.builder.get_object("btn_finalizar_sessao")

        #self.btn_window_payment_wait = self.builder.get_object("btn_window_payment_wait")
        #self.btn_window_payment_wait.connect("button_press_event", self.on_btn_window_payment_wait_button_press_event)

        " ----------- BOTOES ENTRADA_DADOS --------------- "
        self.btn_confirmar_entrada_dados = self.builder.get_object("btn_confirmar_entrada_dados")
        self.btn_confirmar_entrada_dados.connect("button_press_event", self.on_btn_confirmar_entrada_dados_button_press_event)
        self.btn_retornar_entrada_dados = self.builder.get_object("btn_retornar_entrada_dados")
        self.btn_retornar_entrada_dados.connect("button_press_event", self.on_btn_retornar_entrada_dados_button_press_event)
        self.btn_backspace = self.builder.get_object("btn_backspace")
        self.btn_backspace.connect("button_press_event", self.on_btn_backspace_button_press_event)

        # ================FIM BOTOES==================== 

        # ============= BOTOES TELA ENTRADA NUMEROS ==================
        self.btn_um = self.builder.get_object("btn_um")
        self.btn_um.connect("clicked", self.on_entry_entrada_numeros_button_press_event)
        self.btn_dois = self.builder.get_object("btn_dois")
        self.btn_dois.connect("clicked", self.on_entry_entrada_numeros_button_press_event)
        self.btn_tres = self.builder.get_object("btn_tres")
        self.btn_tres.connect("clicked", self.on_entry_entrada_numeros_button_press_event)
        self.btn_quatro = self.builder.get_object("btn_quatro")
        self.btn_quatro.connect("clicked", self.on_entry_entrada_numeros_button_press_event)
        self.btn_cinco = self.builder.get_object("btn_cinco")
        self.btn_cinco.connect("clicked", self.on_entry_entrada_numeros_button_press_event)
        self.btn_seis = self.builder.get_object("btn_seis")
        self.btn_seis.connect("clicked", self.on_entry_entrada_numeros_button_press_event)
        self.btn_sete = self.builder.get_object("btn_sete")
        self.btn_sete.connect("clicked", self.on_entry_entrada_numeros_button_press_event)
        self.btn_oito = self.builder.get_object("btn_oito")
        self.btn_oito.connect("clicked", self.on_entry_entrada_numeros_button_press_event)
        self.btn_nove = self.builder.get_object("btn_nove")
        self.btn_nove.connect("clicked", self.on_entry_entrada_numeros_button_press_event)
        self.btn_zero = self.builder.get_object("btn_zero")
        self.btn_zero.connect("clicked", self.on_entry_entrada_numeros_button_press_event)
        self.btn_confirmar_entrada_numero = self.builder.get_object("btn_confirmar_entrada_numero")
        self.btn_confirmar_entrada_numero.connect("button_press_event", self.on_btn_confirmar_entrada_numero_button_press_event )
        self.btn_retornar_entrada_numeros = self.builder.get_object("btn_retornar_entrada_numeros")
        self.btn_retornar_entrada_numeros.connect("button_press_event", self.on_btn_retornar_entrada_numeros_button_press_event)


        # =================== BOTÕES DIALOGOS ====================
        self.btn_ok_dialog_retorno_cadastro = self.builder.get_object("btn_ok_dialog_retorno_cadastro")
        self.btn_ok_dialog_retorno_cadastro.connect("button_press_event", self.on_btn_ok_dialog_retorno_cadastro_pressed)
        self.btn_dialog_preencher_campos = self.builder.get_object("btn_dialog_preencher_campos")
        self.btn_dialog_preencher_campos.connect("button_press_event", self.on_btn_dialog_preencher_campos_pressed_event)
        self.btn_finalizar_sessao = self.builder.get_object("btn_finalizar_sessao")
        self.btn_finalizar_sessao.connect("button_press_event", self.on_btn_finalizar_sessao_button_press_event)
        self.button_fechar_armario = self.builder.get_object("button_fechar_armario")
        self.button_fechar_armario.connect("button_press_event", self.on_button_fechar_armario_button_press_event)


        # ======================== BOTOES TELA OPCAO CARTAO ======================
        self.btn_credito = self.builder.get_object("btn_credito")
        self.btn_credito.connect("button-press-event", self.on_btn_credito_button_press_event)
        self.btn_debito = self.builder.get_object("btn_debito")
        self.btn_debito.connect("button-press-event", self.on_btn_debito_button_press_event)
        self.btn_cancelar_escolha = self.builder.get_object("btn_cancelar_escolha")
        self.btn_cancelar_escolha.connect("button-press-event", self.on_btn_cancelar_button_press_event)

        # ======================== BOTOES window_erro_pagamentos =================
        self.btn_tente_novamente_window_erro_pagamentos = self.builder.get_object("btn_tente_novamente_window_erro_pagamentos")
        self.btn_tente_novamente_window_erro_pagamentos.connect("button-press-event", self.on_btn_tente_novamente_window_erro_pagamentos_button_press_event)
        self.btn_cancelar_window_erro_pagamentos = self.builder.get_object("btn_cancelar_window_erro_pagamentos")
        self.btn_cancelar_window_erro_pagamentos.connect("button-press-event", self.on_btn_cancelar_window_erro_pagamentos_button_press_event )

        # ========================= FIM BOTOES ===================================


        # ========================    GRIDS     ==================================
        self.grid_numbers = self.builder.get_object("grid_numbers")

        """ ========== adicionando os elementos do teclado ======================= """
        for alfabet in self.alfa:
            self.alfabet = self.builder.get_object("%s"%(alfabet))
            self.alfabet.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        for num in self.num:
            self.number = self.builder.get_object("num_%s"%(num))
            self.number.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.btn_arroba = self.builder.get_object("btn_arroba")
        self.btn_arroba.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.btn_espaco = self.builder.get_object("btn_espaco")
        self.btn_espaco.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.btn_gmail = self.builder.get_object("btn_gmail")
        self.btn_gmail.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.btn_outlook = self.builder.get_object("btn_outlook")
        self.btn_outlook.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.btn_yahoo = self.builder.get_object("btn_yahoo")
        self.btn_yahoo.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.btn_dot = self.builder.get_object("btn_dot")
        self.btn_dot.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.btn_dash = self.builder.get_object("btn_dash")
        self.btn_dash.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.btn_under = self.builder.get_object("btn_under")
        self.btn_under.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.btn_dot_com = self.builder.get_object("btn_dot_com")
        self.btn_dot_com.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        self.btn_hotmail = self.builder.get_object("btn_hotmail")
        self.btn_hotmail.connect("clicked", self.on_entry_entrada_dados_button_press_event)
        """========== fim elementos do teclado  """
        """ ========= lista combobox ========= """
       
        
        self.combobox_flags_ddd = self.builder.get_object("combobox_flags_ddd")
        self.combobox_flags_ddd.set_wrap_width(6)
        
        self.list_flag_ddd = Gtk.ListStore(GdkPixbuf.Pixbuf, str)
        FLAG_BR = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/brasil.png", 32, 50)
        FLAG_AFRICA_SUL = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/africa_sul.png", 32, 50)
        FLAG_ALE = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/alemanha.png", 32, 50)
        FLAG_ARABIA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/arabia_saudita.png", 32, 50)
        FLAG_ARGEL = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/argelia.png", 32, 50)
        FLAG_ARGENTINA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/argentina.png", 32, 50)
        FLAG_AUSTRALIA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/australia.png", 32, 50)
        FLAG_AUSTRIA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/austria.png", 32, 50)
        FLAG_BAREIN = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/barein.png", 32, 50)
        FLAG_BELGICA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/belgica.png", 32, 50)
        FLAG_BOLIVIA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/bolivia.png", 32, 50)
        FLAG_CANADA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/canada.png", 32, 50)
        FLAG_CHILE = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/chile.png", 32, 50)
        FLAG_CHINA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/china.png", 32, 50)
        FLAG_COLOMBIA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/colombia.png", 32, 50)
        FLAG_COREIA_SUL = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/coreia_sul.png", 32, 50)
        FLAG_COSTA_RICA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/costa_rica.png", 32, 50)
        FLAG_DINAMARCA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/dinamarca.png", 32, 50)
        FLAG_EMIRADOS = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/emirados_arabes.png", 32, 50)
        FLAG_EQUADOR = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/equador.png", 32, 50)
        FLAG_ESPANHA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/espanha.png", 32, 50)
        FLAG_USA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/estados_unidos.png", 32, 50)
        FLAG_FINLANDIA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/finlandia.png", 32, 50)
        FLAG_FRANCA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/franca.png", 32, 50)
        FLAG_HONG_KONG = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/hong_kong.png", 32, 50)
        FLAG_IRAN = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/iran.png", 32, 50)
        FLAG_IRAQUE = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/iraque.png", 32, 50)
        FLAG_IRLANDA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/irlanda.png", 32, 50)
        FLAG_ISLANDIA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/islandia.png", 32, 50)
        FLAG_ISRAEL = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/israel.png", 32, 50)
        FLAG_ITALIA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/italia.png", 32, 50)
        FLAG_JAPAO = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/japao.png", 32, 50)
        FLAG_MEXICO = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/mexico.png", 32, 50)
        FLAG_NORUEGA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/noruega.png", 32, 50)
        FLAG_PARAGUAI = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/paraguai.png", 32, 50)
        FLAG_PORTUGAL = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/portugal.png", 32, 50)
        FLAG_REINO_UNIDO = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/reino_unido.png", 32, 50)
        FLAG_RUSSIA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/russia.png", 32, 50)
        FLAG_SINGAPURA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/singapura.png", 32, 50)
        FLAG_SUICA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/suica.png", 32, 50)
        FLAG_SUECIA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/suecia.png", 32, 50)
        FLAG_URUGUAI = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/uruguai.png", 32, 50)
        FLAG_VENEZUELA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/venezuela.png", 32, 50)
        FLAG_AFEGAN = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/afeganistao.png", 32, 50)
        FLAG_QUENIA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/quenia.png", 32, 50)
        FLAG_MONACO = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/monaco.png", 32, 50)
        FLAG_POLONIA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/polonia.png", 32, 50)
        FLAG_GRECIA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/grecia.png", 32, 50)
        FLAG_BULGARIA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/bulgaria.png", 32, 50)
        FLAG_HOLANDA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/holanda.png", 32, 50)
        FLAG_ROMENIA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/romenia.png", 32, 50)
        FLAG_CROACIA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/croacia.png", 32, 50)
        FLAG_ESLOVENIA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/eslovenia.png", 32, 50)
        FLAG_ESLOVAQUIA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/eslovaquia.png", 32, 50)
        FLAG_SERVIA = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/servia.png", 32, 50)
        NO_FLAG = GdkPixbuf.Pixbuf.new_from_file_at_size("static/images/flags_ddd/no_flag.png", 32, 50)

        
        FLAGS = [[FLAG_BR, "+55"], [FLAG_ARGENTINA, "+54"], [FLAG_CHILE, "+56"], [FLAG_COLOMBIA, "+57"],
                 [FLAG_PARAGUAI, "+595"], [FLAG_URUGUAI, "+598"], [FLAG_BOLIVIA, "+591"], [FLAG_SERVIA, "+381"],
                 [FLAG_ALE, "+49"], [FLAG_ARABIA, "+966"], [FLAG_CROACIA, "+385"], [FLAG_ESLOVENIA, "+386"], [FLAG_ESLOVAQUIA, "+421"],
                 [FLAG_ARGEL, "+213"], [FLAG_AUSTRALIA, "+61" ], [FLAG_AUSTRIA, "+43"], [FLAG_ROMENIA, "+40"],
                 [FLAG_BAREIN, "+973"], [FLAG_BELGICA, "+32"], [FLAG_CANADA, "+1"], [FLAG_MONACO, "+377"], [FLAG_HOLANDA, "+31"],
                 [FLAG_CHINA, "+86"], [ FLAG_COREIA_SUL, "+82"],  [FLAG_SINGAPURA, "+65"], [FLAG_POLONIA, "+48"], [FLAG_BULGARIA, "+359"],
                 [FLAG_COSTA_RICA, "+506"], [FLAG_DINAMARCA, "+45"], [FLAG_EMIRADOS, "+971"], [FLAG_EQUADOR, "+593"],[FLAG_GRECIA, "+30"],
                 [FLAG_ESPANHA, "+34"], [FLAG_USA, "+1"], [FLAG_FINLANDIA, "+358"], [FLAG_FRANCA, "+33"], [FLAG_HONG_KONG, "+852"],
                 [FLAG_IRAN, "+98"], [FLAG_IRAQUE, "+964"], [FLAG_IRLANDA, "+353"], [FLAG_ISLANDIA, "+354"], [FLAG_ISRAEL, "+972"],
                 [FLAG_ITALIA, "+39"], [FLAG_JAPAO, "+81"], [FLAG_MEXICO, "+52"], [FLAG_NORUEGA, "+47"], [FLAG_QUENIA, "+254"],
                 [FLAG_PORTUGAL, "+351"], [FLAG_REINO_UNIDO, "+44"], [FLAG_RUSSIA, "+7"], [FLAG_SUICA, "+46"],
                 [FLAG_SUECIA, "+41"], [FLAG_VENEZUELA, "+58"], [FLAG_AFRICA_SUL, "+27"], [FLAG_AFEGAN, "+93"], [NO_FLAG, "Others"]
        ]
        DDD = {}
        


        for i in range(0, len(FLAGS)):
            DDD[i] = FLAGS[i][1]
        for f in range(len(FLAGS)):
            self.list_flag_ddd.append(FLAGS[f])

        
        
        self.combobox_flags_ddd.set_property("model", self.list_flag_ddd)
        
        self.cell_renderer = Gtk.CellRendererPixbuf()
        self.combobox_flags_ddd.pack_start(self.cell_renderer, False)
        self.combobox_flags_ddd.add_attribute(self.cell_renderer, "pixbuf", 0)

        self.cell_renderer_text = Gtk.CellRendererText()
        self.combobox_flags_ddd.pack_start(self.cell_renderer_text, False)
        self.combobox_flags_ddd.add_attribute(self.cell_renderer_text, "text", 1)
        self.combobox_flags_ddd.set_active(0)
        
        
        
    

        """if self.tempo_locacao == "diaria":
            self.label_quantidade_horas.hide()
            #self.label_quantidade_minutos.hide()
            #self.entry_minutos.hide()
            #self.entry_minutos.set_text("0")
            self.entry_quantidade_horas.hide()
            self.entry_quantidade_horas.set_text("0")
            self.btn_limpar_horas.hide()
            #self.btn_limpar_minutos.hide()
        elif self.tempo_locacao == "horas":
            self.label_quantidade_diaria.hide()
            self.entry_quantidade_diaria.hide()
            self.entry_quantidade_diaria.set_text("0")
            self.btn_limpar_quantidade_diaria.hide()"""
        
        if self.language == "pt_BR":
            #self.label_aguarde_pagamento.set_text("AGUARDE PAGAMENTO")
            self.label_nome.set_text("NOME")
            self.label_telefone.set_text("CELULAR")
            self.label_quantidade_diaria.set_text("QUANTIDADE DIÁRIA") #daily amount
            self.label_quantidade_horas.set_text("QUANTIDADE HORAS") #quantity of hours
            #self.label_quantidade_minutos.set_text("QUANTIDADE\n MINUTOS") #quantity of minutes
            self.label_valor_da_locacao.set_text("VALOR DA LOCAÇÃO R$")
            self.btn_confirmar.set_label("CONFIRMAR")
            self.btn_retornar.set_label("TELA ANTERIOR")
            self.btn_limpar_celular.set_label("LIMPAR")
            self.btn_limpar_email.set_label("LIMPAR")
            self.btn_limpar_horas.set_label("LIMPAR")
            #self.btn_limpar_minutos.set_label("LIMPAR")
            self.btn_limpar_nome.set_label("LIMPAR")
            self.btn_limpar_quantidade_diaria.set_label("LIMPAR")
            self.btn_confirmar_entrada_dados.set_label("CONFIRMAR")
            self.btn_confirmar_entrada_numero.set_label("CONFIRMAR")
            self.btn_retornar_entrada_dados.set_label("TELA ANTERIOR")
            self.btn_retornar_entrada_numeros.set_label("TELA ANTERIOR")
            self.btn_limpar_entrada_numeros.set_label("LIMPAR")
            self.label_compartimento_titulo.set_text("SEU COMPARTIMENTO É")
            self.label_senha_titulo.set_text("SUA SENHA DE ACESSO É")
            self.label_inicio_locacao_titulo.set_text("INÍCIO LOCAÇÃO")
            self.label_fim_locacao_titulo.set_text("FIM DA LOCAÇÃO")
            self.label_message_envio_email.set_text("UM EMAIL COM O RECAPTULATIVO DE SUA\n RESERVA ACABA DE LHE SER ENVIADO!")
            self.button_fechar_armario.set_label("FECHAR ARMÁRIO")
            self.btn_tente_novamente_window_erro_pagamentos.set_label("TENTE NOVAMENTE")
            self.btn_cancelar_window_erro_pagamentos.set_label("CANCELAR")
            self.label_menu.set_text(" SELECIONE A OPÇÃO DE PAGAMENTO ")
            self.btn_credito.set_label("CRÉDITO")
            self.btn_debito.set_label("DÉBITO")
            self.btn_cancelar_escolha.set_label("CANCELAR")
            self.label_instrucao.set_text("Obigado por utilizar nossos serviços! Lhe desejamos um dia incrível!")
            """self.label_instrucao.set_text(Após guardar todo o volume necessário, \n
                                           empurre a porta sem forçar até encostar na trava,\n 
                                           depois para finalizar clique no botão abaixo com nome: FECHAR ARMÁRIO.\n
                                           Observação: A responsabilidade de fechar o armário é do usuário,\n
                                           caso esqueça de fechá-lo a empresa não se responsabilizará por perdas!
                                           )"""
            
        elif self.language == "en_US":
            #self.label_aguarde_pagamento.set_text("WAIT FOR PAYMENT")
            self.label_nome.set_text("NAME")
            self.label_telefone.set_text("PHONE ")
            self.label_quantidade_diaria.set_text("QUANTITY DAYS") 
            self.label_quantidade_horas.set_text("QUANTITY HOURS") 
            #self.label_quantidade_minutos.set_text("QUANTITY\n MINUTES")
            self.label_valor_da_locacao.set_text("RENTAL VALUE R$")
            self.btn_confirmar.set_label("CONFIRM")
            self.btn_retornar.set_label("PREVIOUS SCREEN")
            self.btn_confirmar_entrada_dados.set_label("CONFIRM")
            self.btn_confirmar_entrada_numero.set_label("CONFIRM")
            self.btn_retornar_entrada_dados.set_label("PREVIOUS SCREEN")
            self.btn_retornar_entrada_numeros.set_label("PREVIOUS SCREEN")
            self.btn_limpar_celular.set_label("CLEAR")
            self.btn_limpar_email.set_label("CLEAR")
            self.btn_limpar_horas.set_label("CLEAR")
            #self.btn_limpar_minutos.set_label("CLEAR")
            self.btn_limpar_nome.set_label("CLEAR")
            self.btn_limpar_quantidade_diaria.set_label("CLEAR")
            self.btn_limpar_entrada_numeros.set_label("CLEAR")
            self.label_compartimento_titulo.set_text("YOUR CABINET IS")
            self.label_senha_titulo.set_text("YOUR PASSWORD IS")
            self.label_inicio_locacao_titulo.set_text("START DATE OF LEASE")
            self.label_fim_locacao_titulo.set_text("FINAL DATE OF LEASE")
            self.label_message_envio_email.set_text("AN EMAIL WITH THE RECAPTULATIVE OF YOUR\n RESERVATION HAS JUST BEEN SENT!")
            self.button_fechar_armario.set_label("CLOSE CABINET")
            self.btn_tente_novamente_window_erro_pagamentos.set_label("TRY AGAIN")
            self.btn_cancelar_window_erro_pagamentos.set_label("CANCEL")
            self.label_menu.set_text(" SELECT A PAYMENT OPTION ")
            self.btn_credito.set_label("CREDIT")
            self.btn_debito.set_label("DEBIT")
            self.label_instrucao.set_text("Thanks for using our services. We desired an awesome day!")
            """self.label_instrucao.set_text(After saving all the required volume,\n
                                            push the door without force until it touches the lock,\n
                                            then to finish click the button below with name: CLOSET CLOSER.\n
                                            Note: It is the responsibility of the user to close the cabinet,\n
                                            if you forget to close it the company will not be responsible for any losses!
                                            )"""
        

        
        self.window_cadastro_usuario.fullscreen()
        self.window_cadastro_usuario.show()
    def on_btn_credito_button_press_event(self, event, args):
        self.window_select_cartao.hide()
        self.window_cadastro_usuario.hide()
        self.send_tipo_cartao("CREDITO")
        
        sleep(0.5)       

    def on_btn_debito_button_press_event(self, event, args):
        self.window_select_cartao.hide()
        self.window_cadastro_usuario.hide()
        #self.window_payment.show()
        self.send_tipo_cartao("DEBITO")
        
        sleep(0.5)
         

    def on_btn_cancelar_button_press_event(self, event, args):
        self.window_select_cartao.hide()


    def send_tipo_cartao(self, tipo):
        
        print(tipo)
        total = self.valor_total #"%.2f"%(self.valor_total)
        #print("total para json", total)
        total = total.replace('.','')
        total = total.replace(',','')
        print("total para json formatado", total)
        with open("/opt/paygoWeb/comprovantes/valor_venda.json", "w+") as f:
            f.write('\n{  \n\n')
            f.write('"TOTAL": "%s",  \n'%(total))
            f.write('"LANGUAGE": "%s",  \n'%(self.language))
            f.write('"PWINFO_CARDTYPE": "%s"  \n'%(tipo))
            f.write('\n}  \n')
        #self.wait_payment()
        self.window_select_cartao.hide()
        """if self.tempo_locacao == "horas":
                self.entry_quantidade_diaria.set_text("0")
        elif self.tempo_locacao == "diaria":
            self.entry_quantidade_horas.set_text("0")
            #self.entry_minutos.set_text("0")"""
        
        self.__nome = self.entry_nome.get_text()
        self.__email = self.entry_email.get_text()
        self.__telefone = self.entry_celular.get_text()
        self.__quantidade_diaria = self.dia #self.entry_quantidade_diaria.get_text()
        self.__quantidade_minutos = self.minuto
        self.__quantidade_horas = self.hora
        """if self.entry_quantidade_horas.get_text() == "":
            self.__quantidade_horas = "0"
        else:
            self.__quantidade_horas = self.entry_quantidade_horas.get_text()
        if self.entry_minutos.get_text() == "":
            self.__quantidade_minutos = "0"
        else:
            self.__quantidade_minutos = self.entry_minutos.get_text()"""
        if self.__nome == "":
            if self.language == "pt_BR":
                self.label_message_preencher_campos.set_text("PREENCHA TODOS OS CAMPOS")
            elif self.language == "en_US":
                self.label_message_preencher_campos.set_text("FILL IN ALL FIELDS")
            self.dialog_message_preencher_campos.show()
        elif self.__email == "":
            if self.language == "pt_BR":
                self.label_message_preencher_campos.set_text("PREENCHA TODOS OS CAMPOS")
            elif self.language == "en_US":
                self.label_message_preencher_campos.set_text("FILL IN ALL FIELDS")
            self.dialog_message_preencher_campos.show()
        elif self.__telefone == "":
            if self.language == "pt_BR":
                self.label_message_preencher_campos.set_text("PREENCHA TODOS OS CAMPOS")
            elif self.language == "en_US":
                self.label_message_preencher_campos.set_text("FILL IN ALL FIELDS")
            self.dialog_message_preencher_campos.show()
            """elif self.__quantidade_diaria == self.__quantidade_horas: #== self.__quantidade_minutos:
            if self.language == "pt_BR":
                self.label_message_preencher_campos.set_text("PREENCHA TODOS OS CAMPOS")
            elif self.language == "en_US":
                self.label_message_preencher_campos.set_text("FILL IN ALL FIELDS")
            self.dialog_message_preencher_campos.show()"""
        else:
            self.__armario = self.classe
            locacao = {
                "NOME"              : self.__nome, 
                "EMAIL"             : self.__email, 
                "TELEFONE"          : self.__telefone, 
                "QUANTIDADE_DIARIA" : self.__quantidade_diaria, 
                "QUANTIDADE_HORAS"  : self.__quantidade_horas, 
                "QUANTIDADE_MINUTOS": self.__quantidade_minutos, 
                "ARMARIO"           : self.__armario, 
                "LANGUAGE"          : self.language, 
                "VALOR_TOTAL"       : self.valor_total
            }
            
            #colocar em wait payment
            #self.window_payment.fullscreen()
            #self.window_payment.show()
            self.window_cadastro_usuario.hide()
            #WWP(locacao)
            print("locacao", self.__quantidade_diaria, self.__quantidade_horas, self.__quantidade_minutos)
            manager = Management()
            self.__result = manager.locacao(self.__nome, self.__email, self.__telefone, self.__quantidade_diaria, self.__quantidade_horas, self.__quantidade_minutos, self.__armario, self.language, self.valor_total)
            
            count = 0
            #self.__result = self.__result[0]
            print("self.__result total cadastro usuario ",self.__result[0])
            #print("self.__result cadastro usuario ", self.__result[0]["message"])
            if self.__result[0]["message"] == "locacao concluida com sucesso":
                dia_inicio_locacao = self.__result[0]["data_locacao"]
                print("dia_inicio cadastro usuario", dia_inicio_locacao)
                hora_inicio_locacao = self.__result[0]["hora_locacao"]
                print("hora_inicio cadastro usuario", hora_inicio_locacao)
                data_fim_locacao = self.__result[0]["data_locada"]
                print("data_fim cadastro usuario", data_fim_locacao)
                hora_fim_locacao = self.__result[0]["hora_locada"]
                print("hora_fim cadastro usuario", hora_fim_locacao)
                self.senha = self.__result[0]["senha"]
                print("__senha cadastro usuario", self.senha)
                compartimento = self.__result[0]["compartimento"]
                print("compartimento cadastro usuario", compartimento)
                
            
                self.label_date_inicio_locacao.set_text(dia_inicio_locacao)
                self.label_date_fim_locacao.set_text(data_fim_locacao)
                self.label_hour_inicio_locacao.set_text(hora_inicio_locacao[:2])
                self.label_hour_inicio_locacao1.set_text(hora_inicio_locacao[3:])
                self.label_hour_fim_locacao.set_text(hora_fim_locacao[:2])
                self.label_hour_fim_locacao1.set_text(hora_fim_locacao[3:])
                self.label_senha0.set_text(self.senha[0])
                self.label_senha1.set_text(self.senha[1])
                self.label_senha2.set_text(self.senha[2])
                self.label_senha3.set_text(self.senha[3])
                self.label_compartimento.set_text(str(compartimento))
                self.id_armario = manager.localiza_id_armario(self.senha)
                #return self.id_armario
                #self.window_payment.hide()
                self.window_cadastro_usuario.hide()
                self.window_conclusao.show()
            elif self.__result[0] == "armario da classe escolhida indisponível":
                if self.language == "pt_BR":
                    self.label_retorno_cadastro.set_text("tamanho de armario\n  escolhido indisponível")
                    self.dialog_retorno_cadastro.show()
                elif self.language == "en_US":
                    self.label_retorno_cadastro.set_text("chosen cabinet\n size unavailable")
                    self.dialog_retorno_cadastro.show()
            else:
                self.window_payment.hide()
                self.label_window_erro_pagamentos.set_text(self.__result[0])
                self.window_erro_pagamento()

    
    def window_erro_pagamento(self):
        self.window_payment.hide()
        self.window_erro_pagamentos.show()
    
    def on_btn_tente_novamente_window_erro_pagamentos_button_press_event(self, widget, event):
        self.window_erro_pagamentos.hide()
        #self.window_select_cartao.fullscreen()
        #self.window_select_cartao.show()
        self.select_cartao()

    def on_btn_cancelar_window_erro_pagamentos_button_press_event(self, widget, event):
        self.window_erro_pagamentos.hide()
        self.window_payment.hide()
        self.window_select_cartao.hide()
        

        
    
    def on_btn_limpar_entrada_numeros_button_press_event(self, widget, event):
        self.entry_entrada_numeros.set_text("")

    def on_btn_backspace_button_press_event(self, widget, event):
        self.texto = self.entry_entrada_dados.get_text()
        self.texto = self.texto[:-1]
        self.entry_entrada_dados.set_text(self.texto)
        self.entry_entrada_dados.set_position(-1)
    def on_btn_finalizar_sessao_button_press_event(self, widget, event):
        self.window_conclusao.hide()
        #self.window_payment.hide()
        self.dialog_instrucao_fecha_armario.show()
        time.sleep(5.0)
        self.dialog_instrucao_fecha_armario.hide()
    
    def on_btn_dialog_preencher_campos_pressed_event(self, event, args):
        self.dialog_message_preencher_campos.hide()
        CadastroUsuarios(self.valor_total, self.language, self.classe, self.dia, self.hora, self.minuto)

    def on_btn_ok_dialog_retorno_cadastro_pressed(self, widget, event):
        self.dialog_retorno_cadastro.hide()
        self.window_cadastro_usuario.destroy()

    def on_btn_confirmar_button_press_event(self, widget, event):
        #self.wait_payment()
        #self.window_select_cartao.show()
        self.window_cadastro_usuario.hide()
        self.select_cartao()
    def select_cartao(self):
        if self.language == "pt_BR":
            
            self.btn_credito.set_label("CRÉDITO")
            self.btn_debito.set_label("DÉBITO")
            self.btn_cancelar_escolha.set_label("CANCELA")

        elif self.language == "en_US":
            self.btn_credito.set_label("CREDIT")
            self.btn_debito.set_label("DEBIT")
            self.btn_cancelar_escolha.set_label("CANCEL")
        self.window_select_cartao.fullscreen()   
        self.window_select_cartao.show()   
        
    """def on_btn_window_payment_wait_button_press_event(self, widget, event):
        if self.tempo_locacao == "horas":
                self.entry_quantidade_diaria.set_text("0")
        elif self.tempo_locacao == "diaria":
            self.entry_quantidade_horas.set_text("0")
            #self.entry_minutos.set_text("0")
        
        self.__nome = self.entry_nome.get_text()
        self.__email = self.entry_email.get_text()
        self.__telefone = self.entry_celular.get_text()
        self.__quantidade_diaria = self.entry_quantidade_diaria.get_text()
        self.__quantidade_minutos = "0"
        if self.entry_quantidade_horas.get_text() == "":
            self.__quantidade_horas = "0"
        else:
            self.__quantidade_horas = self.entry_quantidade_horas.get_text()
        if self.entry_minutos.get_text() == "":
            self.__quantidade_minutos = "0"
        else:
            self.__quantidade_minutos = self.entry_minutos.get_text()
        if self.__nome == "":
            if self.language == "pt_BR":
                self.label_message_preencher_campos.set_text("PREENCHA TODOS OS CAMPOS")
            elif self.language == "en_US":
                self.label_message_preencher_campos.set_text("FILL IN ALL FIELDS")
            self.dialog_message_preencher_campos.show()
        elif self.__email == "":
            if self.language == "pt_BR":
                self.label_message_preencher_campos.set_text("PREENCHA TODOS OS CAMPOS")
            elif self.language == "en_US":
                self.label_message_preencher_campos.set_text("FILL IN ALL FIELDS")
            self.dialog_message_preencher_campos.show()
        elif self.__telefone == "":
            if self.language == "pt_BR":
                self.label_message_preencher_campos.set_text("PREENCHA TODOS OS CAMPOS")
            elif self.language == "en_US":
                self.label_message_preencher_campos.set_text("FILL IN ALL FIELDS")
            self.dialog_message_preencher_campos.show()
        elif self.__quantidade_diaria == self.__quantidade_horas: #== self.__quantidade_minutos:
            if self.language == "pt_BR":
                self.label_message_preencher_campos.set_text("PREENCHA TODOS OS CAMPOS")
            elif self.language == "en_US":
                self.label_message_preencher_campos.set_text("FILL IN ALL FIELDS")
            self.dialog_message_preencher_campos.show()
        else:
            
            self.__armario = self.classe
            print("locacao", self.__quantidade_diaria, self.__quantidade_horas, self.__quantidade_minutos)
            manager = Management()
            self.__result =  manager.locacao(self.__nome, self.__email, self.__telefone, self.__quantidade_diaria, self.__quantidade_horas, self.__quantidade_minutos, self.__armario, self.language, self.valor_total)
            count = 0
            #self.__result = self.__result[0]
            print("self.__result cadastro usuario payment", self.__result[0])
            if self.__result[0][0] == "locacao concluida com sucesso":
                dia_inicio_locacao = self.__result[0][1]
                print("dia_inicio cadastro usuario", dia_inicio_locacao)
                hora_inicio_locacao = self.__result[0][2]
                print("hora_inicio cadastro usuario", hora_inicio_locacao)
                data_fim_locacao = self.__result[0][3]
                print("data_fim cadastro usuario", data_fim_locacao)
                hora_fim_locacao = self.__result[0][4]
                print("hora_fim cadastro usuario", hora_fim_locacao)
                self.senha = self.__result[0][5]
                print("__senha cadastro usuario", self.senha)
                compartimento = self.__result[0][6]
                print("compartimento cadastro usuario", compartimento)
                
            
                self.label_date_inicio_locacao.set_text(dia_inicio_locacao)
                self.label_date_fim_locacao.set_text(data_fim_locacao)
                self.label_hour_inicio_locacao.set_text(hora_inicio_locacao)
                self.label_hour_fim_locacao.set_text(hora_fim_locacao)
                self.label_senha.set_text(str(self.senha))
                self.label_compartimento.set_text(str(compartimento))
                
                
                self.window_conclusao.show()
                self.window_cadastro_usuario.hide()
                #self.window_payment.hide()
                self.id_armario = manager.localiza_id_armario(self.senha)
                return self.id_armario
                
                
            elif self.__result[0] == "armario da classe escolhida indisponível":
                if self.language == "pt_BR":
                    self.label_retorno_cadastro.set_text("tamanho de armario\n  escolhido indisponível")
                    self.dialog_retorno_cadastro.show()
                elif self.language == "en_US":
                    self.label_retorno_cadastro.set_text("chosen cabinet\n size unavailable")
                    self.dialog_retorno_cadastro.show()
            else:
                pass"""
     


    """def wait_payment(self, tipo):
        #process_threading = threading.Thread(target=self.show_payment)
        #process_threading.start()
        self.window_payment.fullscreen()
        self.window_payment.show()
        sleep(1)
        print(tipo)
        total = self.valor_total #"%.2f"%(self.valor_total)
        #print("total para json", total)
        total = total.replace(',','')
        total = total.replace('.','')
        print("total para json formatado", total)
        with open("engine/paygoWeb/comprovantes/valor_venda.json", "w+") as f:
            f.write('\n{  \n')
            f.write('"TOTAL": "%s",  \n'%(total))
            f.write('"LANGUAGE": "%s",  \n'%(self.language))
            f.write('"PWINFO_CARDTYPE": "%s"  \n'%(tipo))
            f.write('\n}  \n')
        
        if self.tempo_locacao == "horas":
                self.entry_quantidade_diaria.set_text("0")
        elif self.tempo_locacao == "diaria":
            self.entry_quantidade_horas.set_text("0")
            #self.entry_minutos.set_text("0")
        
        self.__nome = self.entry_nome.get_text()
        self.__email = self.entry_email.get_text()
        self.__telefone = self.entry_celular.get_text()
        self.__quantidade_diaria = self.entry_quantidade_diaria.get_text()
        self.__quantidade_minutos = "0"
        if self.entry_quantidade_horas.get_text() == "":
            self.__quantidade_horas = "0"
        else:
            self.__quantidade_horas = self.entry_quantidade_horas.get_text()
        if self.entry_minutos.get_text() == "":
            self.__quantidade_minutos = "0"
        else:
            self.__quantidade_minutos = self.entry_minutos.get_text()
        if self.__nome == "":
            if self.language == "pt_BR":
                self.label_message_preencher_campos.set_text("PREENCHA TODOS OS CAMPOS")
            elif self.language == "en_US":
                self.label_message_preencher_campos.set_text("FILL IN ALL FIELDS")
            self.dialog_message_preencher_campos.show()
        elif self.__email == "":
            if self.language == "pt_BR":
                self.label_message_preencher_campos.set_text("PREENCHA TODOS OS CAMPOS")
            elif self.language == "en_US":
                self.label_message_preencher_campos.set_text("FILL IN ALL FIELDS")
            self.dialog_message_preencher_campos.show()
        elif self.__telefone == "":
            if self.language == "pt_BR":
                self.label_message_preencher_campos.set_text("PREENCHA TODOS OS CAMPOS")
            elif self.language == "en_US":
                self.label_message_preencher_campos.set_text("FILL IN ALL FIELDS")
            self.dialog_message_preencher_campos.show()
        elif self.__quantidade_diaria == self.__quantidade_horas: #== self.__quantidade_minutos:
            if self.language == "pt_BR":
                self.label_message_preencher_campos.set_text("PREENCHA TODOS OS CAMPOS")
            elif self.language == "en_US":
                self.label_message_preencher_campos.set_text("FILL IN ALL FIELDS")
            self.dialog_message_preencher_campos.show()
        else:
            
            self.__armario = self.classe
            print("locacao", self.__quantidade_diaria, self.__quantidade_horas, self.__quantidade_minutos)
            manager = Management()
            self.__result =  manager.locacao(self.__nome, self.__email, self.__telefone, self.__quantidade_diaria, self.__quantidade_horas, self.__quantidade_minutos, self.__armario, self.language, self.valor_total)
            count = 0
            #self.__result = self.__result[0]
            print("self.__result cadastro usuario wait_payment ", self.__result[0])
            if self.__result[0][0] == "locacao concluida com sucesso":
                dia_inicio_locacao = self.__result[0][1]
                print("dia_inicio cadastro usuario", dia_inicio_locacao)
                hora_inicio_locacao = self.__result[0][2]
                print("hora_inicio cadastro usuario", hora_inicio_locacao)
                data_fim_locacao = self.__result[0][3]
                print("data_fim cadastro usuario", data_fim_locacao)
                hora_fim_locacao = self.__result[0][4]
                print("hora_fim cadastro usuario", hora_fim_locacao)
                self.senha = self.__result[0][5]
                print("__senha cadastro usuario", self.senha)
                compartimento = self.__result[0][6]
                print("compartimento cadastro usuario", compartimento)
                
            
                self.label_date_inicio_locacao.set_text(dia_inicio_locacao)
                self.label_date_fim_locacao.set_text(data_fim_locacao)
                self.label_hour_inicio_locacao.set_text(hora_inicio_locacao)
                self.label_hour_fim_locacao.set_text(hora_fim_locacao)
                self.label_senha0.set_text(str(self.senha[0]))
                self.label_senha1.set_text(str(self.senha[1]))
                self.label_senha2.set_text(str(self.senha[2]))
                self.label_senha3.set_text(str(self.senha[3]))
                self.label_compartimento.set_text(str(compartimento))
                
                self.window_payment.hide()
                self.window_cadastro_usuario.hide()
                self.window_conclusao.show()
                
                
                self.id_armario = manager.localiza_id_armario(self.senha)
                return self.id_armario
                
                
            elif self.__result[0] == "armario da classe escolhida indisponível":
                if self.language == "pt_BR":
                    self.label_retorno_cadastro.set_text("tamanho de armario\n  escolhido indisponível")
                    self.dialog_retorno_cadastro.show()
                elif self.language == "en_US":
                    self.label_retorno_cadastro.set_text("chosen cabinet\n size unavailable")
                    self.dialog_retorno_cadastro.show()
            else:
                self.window_payment.hide()
                self.label_window_erro_pagamentos.set_text(self.__result[0])
                self.window_erro_pagamento()"""
    

    
    def on_btn_retornar_button_press_event(self, widget, event):
        self.window_cadastro_usuario.hide()
        OpcaoHoraDiaria(self.classe, self.language)
        
    
    def on_entry_nome_button_press_event(self, widget, event):
        if self.language == "pt_BR":
            self.label_entrada_dados.set_text("NOME")
        elif self.language == "en_US":
            self.label_entrada_dados.set_text("NAME")
        self.entry_entrada_dados.set_text("")
        self.window_entrada_dados.show()
        return (self.entry, self.label_entrada_dados)
    
    def on_entry_email_button_press_event(self, widget, event):
        self.label_entrada_dados.set_text("EMAIL")
        self.entry_entrada_dados.set_text("")
        self.window_entrada_dados.show()
        return self.entry
    
    def on_entry_celular_button_press_event(self, widget, event):
        if self.language == "pt_BR":
            self.label_entrada_numeros.set_text("CELULAR")
        elif self.language == "en_US":
            self.label_entrada_numeros.set_text("PHONE ")
        self.entry_entrada_numeros.set_text("")
        self.window_entrada_numeros.show()
        
    
    def on_entry_quantidade_diaria_button_press_event(self, widget, event):
        if self.language == "pt_BR":
            self.label_entrada_numeros.set_text("QUANTIDADE DIÁRIA")
        elif self.language == "en_US":
            self.label_entrada_numeros.set_text("QUANTITY DAYS")
            
        self.window_entrada_numeros.show()
        
    
    def on_entry_quantidade_horas_button_press_event(self, widget, event):
        if self.language == "pt_BR":
            self.label_entrada_numeros.set_text("QUANTIDADE HORAS")
        elif self.language == "en_US":
            self.label_entrada_numeros.set_text("QUANTITY HOURS")
        self.window_entrada_numeros.show()
        

    """def on_entry_minutos_button_press_event(self, widget, event):
        if self.language == "pt_BR":
            self.label_entrada_numeros.set_text("QUANTIDADE MINUTOS")
        elif self.language == "en_US":
            self.label_entrada_numeros.set_text("QUANTITY MINUTES")
        self.window_entrada_numeros.show()"""
        
    
    def on_btn_limpar_nome_button_press_event(self, widget, event):
        self.entry_nome.set_text("")
        self.entry_nome.set_position(0)
    
    def on_btn_limpar_email_button_press_event(self, widget, event):
        self.entry_email.set_text("")
        self.entry_email.set_position(0)
    
    def on_btn_limpar_celular_button_press_event(self, widget, event):
        self.entry_celular.set_text("")
        self.entry_celular.set_position(0)
    
    def on_btn_limpar_quantidade_diaria_button_press_event(self, widget, event):
        self.entry_quantidade_diaria.set_text("")
        self.entry_quantidade_diaria.set_position(0)
    
    def on_btn_limpar_horas_button_press_event(self, widget, event):
        self.entry_quantidade_horas.set_text("")
        self.entry_quantidade_horas.set_position(0)
    
    """""def on_btn_limpar_minutos_button_press_event(self, widget, event):
        self.entry_minutos.set_text("")
        self.entry_minutos.set_position(0)"""
    
    def on_btn_retornar_entrada_dados_button_press_event(self, widget, event):
        self.entry_entrada_dados.set_text("")
        self.entry_entrada_dados.set_position(-1)
        self.window_entrada_dados.hide()
    
    def on_entry_entrada_dados_button_press_event(self, widget):
        self.widget = widget
        self.value = self.widget.get_label()
        print("self.value entrada de dados ===> ",self.value)
        self.text_entrada = self.entry_entrada_dados.get_text() + self.value
        self.entry_entrada_dados.set_text(self.text_entrada)
        self.entry_entrada_dados.set_position(-1)
        
        
    def on_btn_confirmar_entrada_dados_button_press_event(self, widget, event):
        self.text_entrada = self.entry_entrada_dados.get_text()
        print(self.label_entrada_dados.get_text())
        if self.label_entrada_dados.get_text() == "NOME" or self.label_entrada_dados.get_text() == "NAME":
            self.entry_nome.set_text(self.text_entrada)
            self.entry_nome.set_position(-1)
        elif self.label_entrada_dados.get_text() == "EMAIL":
            self.entry_email.set_text(self.text_entrada)
            self.entry_email.set_position(-1)
        

        self.entry_entrada_dados.set_text("")
        self.entry_entrada_dados.set_position(0)
        self.window_entrada_dados.hide()
    
    def on_btn_confirmar_entrada_numero_button_press_event(self, widget, event):
        if self.label_entrada_numeros.get_text() == "CELULAR" or self.label_entrada_numeros.get_text() == "PHONE ":
            self.ddd = self.combobox_flags_ddd.get_active()
            
            print("self ddd", self.ddd)
            self.entry_celular.set_text(str(DDD[self.ddd]) + " " +str(self.text_entrada))
            self.entry_celular.set_position(-1)
            self.window_entrada_numeros.hide()
        
    def on_btn_retornar_entrada_numeros_button_press_event(self, widget, event):
        self.window_entrada_numeros.hide()
    
    def on_entry_entrada_numeros_button_press_event(self, widget):
        self.widget =  widget
        self.ddd = self.combobox_flags_ddd.get_active()
        if str(DDD[self.ddd]) == "+55":
            if self.entry_entrada_numeros.get_text() == "":
                self.value = "( " + self.widget.get_label()
            elif len(self.entry_entrada_numeros.get_text()) == 3:
                self.value = self.widget.get_label() + " ) "
            else:
                self.value = self.widget.get_label()
        else:
            self.value = self.widget.get_label()
        self.text_entrada = self.entry_entrada_numeros.get_text() + self.value
        self.entry_entrada_numeros.set_text(self.text_entrada)
        self.entry_entrada_numeros.set_position(-1)
    
    def on_button_fechar_armario_button_press_event(self, *args):
        print("args button fechar cadastro usuario", args)
        manager = Management()
        id_armario = manager.localiza_id_armario(self.senha)
        manager.fechar_armario(id_armario)
        #self.dialog_instrucao_fecha_armario.hide()


class WindowLogin(Gtk.Window):
    def __init__(self, *args):
        self.opcao = args[0]
        self.language = args[1]
        self.screen = Gdk.Screen.get_default()
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/window_login.glade")
        #self.builder.add_from_file("ui/window_select_cartao.glade")
        self.manager = Management()
        self.value = ''
        self.entrada = ''
        # alfabeto para gerar o teclado
        self.alfa = list(string.ascii_uppercase)
        # números para o teclado numérico
        self.num = list(map(lambda x: x, range(1,10)))
        self.builder.connect_signals({
            "on_btn_retornar_entrada_dados_pressed": self.on_btn_retornar_entrada_dados_pressed,
            "on_btn_backspace_button_press_event": self.on_btn_backspace_button_press_event,
            "on_btn_efetuar_pagamento_button_press_event": self.on_btn_efetuar_pagamento_button_press_event,
            #"on_btn_window_payment_wait_button_press_event": self.on_btn_window_payment_wait_button_press_event,
            #"on_button_fechar_armario_button_press_event": self.on_button_fechar_armario_button_press_event,
            "on_btn_tente_novamente_window_erro_pagamentos_button_press_event": self.on_btn_tente_novamente_window_erro_pagamentos_button_press_event,
            "on_btn_cancelar_window_erro_pagamentos_button_press_event": self.on_btn_cancelar_window_erro_pagamentos_button_press_event
        })
        # ================ DIALOGS ==============================
        #self.dialog_cobranca = self.builder.get_object("dialog_cobranca")
        self.dialog_senha_incorreta = self.builder.get_object("dialog_senha_incorreta")
        self.dialog_instrucao_fecha_armario = self.builder.get_object("dialog_instrucao_fecha_armario")

        # ======== BOTOES DO TECLADO ============================
        for alfabet in self.alfa:
            self.alfabet = self.builder.get_object(alfabet)
            self.alfabet.connect("clicked", self.on_entry_button_press_event)
        for num in self.num:
            self.number = self.builder.get_object("num_"+str(num))
            self.number.connect("clicked", self.on_entry_button_press_event)

        self.btn_backspace = self.builder.get_object("btn_backspace")

        # ==============================================
        # ============================== BUTTONS =========================================

        #self.button_fechar_armario = self.builder.get_object("button_fechar_armario")
        #self.button_fechar_armario.connect("button_press_event", self.on_button_fechar_armario_button_press_event)

        self.btn_efetuar_pagamento = self.builder.get_object("btn_efetuar_pagamento")
        self.btn_efetuar_pagamento.connect("button_press_event", self.on_btn_efetuar_pagamento_button_press_event)
        self.btn_encerrar_sessao = self.builder.get_object("btn_encerrar_sessao")

        self.entry_entrada_dados = self.builder.get_object("entry_entrada_dados")
        self.btn_confirmar_entrada_dados = self.builder.get_object("btn_confirmar_entrada_dados")
        self.btn_retornar_entrada_dados = self.builder.get_object("btn_retornar_entrada_dados")
        self.btn_retornar_entrada_dados.connect("clicked", self.on_btn_retornar_entrada_dados_pressed)
        self.btn_confirmar_entrada_dados.connect("clicked", self.on_btn_confirmar_entrada_dados_pressed)

        #self.btn_window_payment_wait = self.builder.get_object("btn_window_payment_wait")
        #self.btn_window_payment_wait.connect("button_press_event", self.on_btn_window_payment_wait_button_press_event)
        self.btn_tentar_dialog_senha_incorreta = self.builder.get_object("btn_tentar_dialog_senha_incorreta")
        self.btn_tentar_dialog_senha_incorreta.connect("clicked", self.on_btn_tentar_dialog_senha_incorreta)
        self.btn_dialog_cancelar_senha_incorreta = self.builder.get_object("btn_dialog_cancelar_senha_incorreta")
        self.btn_dialog_cancelar_senha_incorreta.connect("clicked", self.on_btn_dialog_cancelar_senha_incorreta)

        # ========= LABELS =========================
        self.lbl_message = self.builder.get_object("lbl_message")
        self.label_dialog_senha_incorreta = self.builder.get_object("label_dialog_senha_incorreta")
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
        self.label_tempo_extra_days = self.builder.get_object("label_tempo_extra_days")
        self.label_tempo_extra_hours = self.builder.get_object("label_tempo_extra_hours")
        self.label_tempo_extra_minutes = self.builder.get_object("label_tempo_extra_minutes")

        self.label_entrada_dados = self.builder.get_object("label_entrada_dados")

        self.label_instrucao = self.builder.get_object("label_instrucao")

        self.label_window_erro_pagamentos = self.builder.get_object("label_window_erro_pagamentos")
        self.label_window_erro_pagamentos.set_line_wrap(True)

        self.label_menu = self.builder.get_object("label_menu")

        # ======================== BOTOES window_erro_pagamentos =================
        self.btn_tente_novamente_window_erro_pagamentos = self.builder.get_object("btn_tente_novamente_window_erro_pagamentos")
        self.btn_tente_novamente_window_erro_pagamentos.connect("button-press-event", self.on_btn_tente_novamente_window_erro_pagamentos_button_press_event)
        self.btn_cancelar_window_erro_pagamentos = self.builder.get_object("btn_cancelar_window_erro_pagamentos")
        self.btn_cancelar_window_erro_pagamentos.connect("button-press-event", self.on_btn_cancelar_window_erro_pagamentos_button_press_event )

        # ======================== BOTOES TELA OPCAO CARTAO ======================
        self.btn_credito = self.builder.get_object("btn_credito")
        self.btn_credito.connect("button-press-event", self.on_btn_credito_button_press_event)
        self.btn_debito = self.builder.get_object("btn_debito")
        self.btn_debito.connect("button-press-event", self.on_btn_debito_button_press_event)
        self.btn_cancelar_escolha = self.builder.get_object("btn_cancelar_escolha")
        self.btn_cancelar_escolha.connect("button-press-event", self.on_btn_cancelar_button_press_event)

        # ========================= FIM OPCOES CARTAO ================================

        # ================== SET LANGUAGE ===================================

        if self.language == "pt_BR":
            self.label_dialog_senha_incorreta.set_text("SENHA INCORRETA,\n TENTE NOVAMENTE")
            self.label_locacao_inicial.set_text("LOCAÇÃO INICIAL")
            self.label_locacao_encerrada.set_text("LOCAÇÃO ENCERRADA ÀS")
            self.label_tempo_extra.set_text("TEMPO EXTRA")
            self.label_valor_extra.set_text("VALOR EXTRA")
            self.label_entrada_dados.set_text("SENHA")
            self.btn_efetuar_pagamento.set_label("EFETUAR PAGAMENTO")
            self.btn_confirmar_entrada_dados.set_label("CONFIRMAR")
            self.btn_retornar_entrada_dados.set_label("RETORNAR TELA ANTERIOR")
            self.btn_dialog_cancelar_senha_incorreta.set_label("CANCELAR")
            self.btn_tentar_dialog_senha_incorreta.set_label("TENTAR NOVAMENTE")
            #self.button_fechar_armario.set_label("FECHAR ARMÁRIO")
            self.btn_tente_novamente_window_erro_pagamentos.set_label("TENTE NOVAMENTE")
            self.btn_cancelar_window_erro_pagamentos.set_label("CANCELAR")
            self.label_menu.set_text(" SELECIONE A OPÇÃO DE PAGAMENTO ")
            self.btn_credito.set_label("CRÉDITO")
            self.btn_debito.set_label("DÉBITO")
            self.btn_cancelar_escolha.set_label("CANCELAR")
            self.label_instrucao.set_text("Obigado por utilizar nossos serviços! Lhe desejamos um dia incrível!")

        elif self.language == "en_US":
            self.label_dialog_senha_incorreta.set_text("WRONG PASSWORD,\n TRY AGAIN")
            self.label_locacao_inicial.set_text("START DATE OF LEASE")
            self.label_locacao_encerrada.set_text("FINAL DATE OF LEASE")
            self.label_tempo_extra.set_text("TIME OVER")
            self.label_valor_extra.set_text("OVERTIME CHARGE")
            self.label_entrada_dados.set_text("PASSWORD")
            self.btn_efetuar_pagamento.set_label("PAYMENT")
            self.btn_confirmar_entrada_dados.set_label("CONFIRM")
            self.btn_retornar_entrada_dados.set_label("PREVIOUS SCREEN")
            self.btn_dialog_cancelar_senha_incorreta.set_label("CANCEL")
            self.btn_tentar_dialog_senha_incorreta.set_label("TRY AGAIN")
            #self.button_fechar_armario.set_label("CLOSE CABINET")
            self.btn_tente_novamente_window_erro_pagamentos.set_label("TRY AGAIN")
            self.btn_cancelar_window_erro_pagamentos.set_label("CANCEL")
            self.label_menu.set_text(" SELECT A PAYMENT OPTION ")
            self.btn_credito.set_label("CREDIT")
            self.btn_debito.set_label("DEBIT")
            self.btn_cancelar_escolha.set_label("CANCEL")
            self.label_instrucao.set_text("Thanks for using our services. We desired an awesome day!")
        

        #self.window_payment = self.builder.get_object("window_payment_wait")
        self.window_pagamento_extra = self.builder.get_object("window_pagamento_extra")
        self.window_select_cartao = self.builder.get_object("window_select_cartao_login")
        self.window_erro_pagamentos = self.builder.get_object("window_erro_pagamento")
        self.window_login = self.builder.get_object("window_login")
        self.window_login.show()

    def window_erro_pagamento(self):
        #self.window_payment.hide()
        self.window_erro_pagamentos.show()
    
    def on_btn_tente_novamente_window_erro_pagamentos_button_press_event(self, widget, event):
        self.window_erro_pagamentos.hide()
        #self.window_select_cartao.fullscreen()
        self.window_select_cartao.show()

    def on_btn_cancelar_window_erro_pagamentos_button_press_event(self, widget, event):
        self.window_erro_pagamentos.hide()
        self.window_payment.hide()
        self.window_select_cartao.hide()

    def on_entry_button_press_event(self, widget):
        self.value = widget.get_label()
        self.text_entrada = self.entry_entrada_dados.get_text() + self.value
        self.entry_entrada_dados.set_text(self.text_entrada)
        self.entry_entrada_dados.set_position(-1)

    def on_btn_confirmar_entrada_dados_pressed(self, event):
        self.message = ''
        result = ''
        self.__senha = self.entry_entrada_dados.get_text()
        print(self.__senha)
        self.id_armario = self.manager.localiza_id_armario(self.__senha)
        
        if self.id_armario == []:
            result == 'senha incorreta, tente novamente'
        print("id_armario window login abrir", self.id_armario)
        if self.opcao == "abrir":
            #result = self.manager.abre_armario(self.id_armario)
            result = self.manager.abre_armario(self.__senha)
            if result == 'armario liberado':
                self.window_login.hide()
                self.entry_entrada_dados.set_text('')
                print('abrir')
                #self.dialog_instrucao_fecha_armario.show()
            elif result == 'senha incorreta, tente novamente':
                # self.window_login.hide()
                self.entry_entrada_dados.set_text('')
                self.dialog_senha_incorreta.show()

            else:

                print("result window_login", result)
                # self.window_login.close()
                #result = dict(zip(result))
                self.__total = result["total"]
                #print(self.__total, result)

                locacao = result["data_locacao"]
                limite = result["tempo_locado"]
                print("locacao window_login", locacao)
                print(type(locacao))

                __dia_da_semana_locacao = result["dia_locacao"]
                __dia_da_semana_locado = result["dia_limite"]
                __hora_locacao = result["hora_locacao"]
                __hora_locado = result["hora_locado"]
                __dia_extra = result["dia_extra"]
                __hora_extra = result["hora_extra"]
                __minuto_extra = result["minuto_extra"]
                self.label_data_locacao_inicial.set_text(__dia_da_semana_locacao + " " +
                                                        str(locacao))  # locacao)[8:10] + "/" + str(locacao)[5:7])
                self.label_data_locacao_encerrada.set_text(__dia_da_semana_locado + " " +
                                                        str(limite))  # [8:10] + "/" + str(limite)[5:7])
                self.label_hour_locacao_inicial.set_text(str(__hora_locacao))
                self.label_hour_locacao_encerrada.set_text(str(__hora_locado))
                self.label_tempo_extra_days.set_text(str(__dia_extra))
                self.label_tempo_extra_hours.set_text(str(__hora_extra))
                self.label_tempo_extra_minutes.set_text(str(__minuto_extra))
                self.label_valor_extra_value.set_text("R$ " + result["total"])
                if float(result["total"]) <= 0.00:
                    resultado = self.manager.finalizar(self.__senha)
                    if resultado == "armario liberado":
                        self.window_login.hide()
                        self.entry_entrada_dados.set_text('')
                        print('abrir')
                        self.dialog_instrucao_fecha_armario.show() # adicionar instrucao de fim de locacao
                else:
                    self.window_pagamento_extra.show()
            
        elif self.opcao == "encerrar":
            result = self.manager.finalizar(self.__senha)
            print('result login encerrar', result)
            if result == 'armario liberado':
                self.window_login.hide()
                self.entry_entrada_dados.set_text('')
                print('abrir')
                self.dialog_instrucao_fecha_armario.show()
                time.sleep(5.0)
                self.dialog_instrucao_fecha_armario.hide()
            elif result == 'senha incorreta, tente novamente':
                # self.window_login.hide()
                self.entry_entrada_dados.set_text('')
                self.dialog_senha_incorreta.show()

            else:

                print("result window_login", result)
                # self.window_login.close()
                #result = dict(zip(result))
                self.__total = result["total"]
                #print(self.__total, result)

                locacao = result["data_locacao"]
                limite = result["tempo_locado"]
                print("locacao window_login", locacao)
                print(type(locacao))

                __dia_da_semana_locacao = result["dia_locacao"]
                __dia_da_semana_locado = result["dia_limite"]
                __hora_locacao = result["hora_locacao"]
                __hora_locado = result["hora_locado"]
                __dia_extra = result["dia_extra"]
                __hora_extra = result["hora_extra"]
                __minuto_extra = result["minuto_extra"]
                self.label_data_locacao_inicial.set_text(__dia_da_semana_locacao + " " +
                                                        str(locacao))  # locacao)[8:10] + "/" + str(locacao)[5:7])
                self.label_data_locacao_encerrada.set_text(__dia_da_semana_locado + " " +
                                                        str(limite))  # [8:10] + "/" + str(limite)[5:7])
                self.label_hour_locacao_inicial.set_text(str(__hora_locacao))
                self.label_hour_locacao_encerrada.set_text(str(__hora_locado))
                self.label_tempo_extra_days.set_text(str(__dia_extra))
                self.label_tempo_extra_hours.set_text(str(__hora_extra))
                self.label_tempo_extra_minutes.set_text(str(__minuto_extra))
                self.label_valor_extra_value.set_text("R$ " + result["total"])

                self.window_login.hide()
                self.window_pagamento_extra.show()
                #return (self.__senha, self.id_armario)

    def on_btn_efetuar_pagamento_button_press_event(self, widget, event):
        #self.window_select_cartao.fullscreen()
        self.window_select_cartao.show()
        

    def on_btn_retornar_entrada_dados_pressed(self, event):
        self.entry_entrada_dados.set_text("")
        self.window_login.hide()


    def on_btn_backspace_button_press_event(self, widget, event):
        self.texto = self.entry_entrada_dados.get_text()
        self.texto = self.texto[:-1]
        self.entry_entrada_dados.set_text(self.texto)
        self.entry_entrada_dados.set_position(-1)

    """def on_btn_window_payment_wait_button_press_event(self, widget, event):
        #self.window_payment.hide()
        self.window_pagamento_extra.hide()
        self.window_login.hide()
        #self.dialog_instrucao_fecha_armario.show()"""

    def on_btn_tentar_dialog_senha_incorreta(self, widget):
        self.dialog_senha_incorreta.hide()

    def on_btn_dialog_cancelar_senha_incorreta(self, widget):
        self.dialog_senha_incorreta.hide()
        self.window_login.hide()


    """def on_button_fechar_armario_button_press_event(self, *args):
        print("args button fechar window login", args)
        #manager = Management()
        #id_armario = manager.localiza_id_armario(self.__senha)
        #manager.fechar_armario(self.id_armario)
        self.dialog_instrucao_fecha_armario.hide()"""
    
    def select_cartao(self):
        if self.language == "pt_BR":
            
            self.btn_credito.set_label("CRÉDITO")
            self.btn_debito.set_label("DÉBITO")
            self.btn_cancelar_escolha.set_label("CANCELA")

        elif self.language == "en_US":
            self.btn_credito.set_label("CREDIT")
            self.btn_debito.set_label("DEBIT")
            self.btn_cancelar_escolha.set_label("CANCEL")
            
        self.window_select_cartao.show()
    def on_btn_credito_button_press_event(self, event, args):
        #self.send_tipo_cartao("CREDITO")
        self.window_select_cartao.hide()
        #self.window_payment.show()
        self.send_tipo_cartao("CREDITO")
        
        sleep(0.5)       

    def on_btn_debito_button_press_event(self, event, args):
        #self.send_tipo_cartao("DEBITO")
        self.window_select_cartao.hide()
        #self.window_payment.show()
        self.send_tipo_cartao("DEBITO")
        
        sleep(0.5)
         

    def on_btn_cancelar_button_press_event(self, event, args):
        self.window_select_cartao.hide()

    def send_tipo_cartao(self, tipo):
        
        print(tipo)
        #total = self.label_valor_extra_value.get_label()
        print("total send tipo cartao window login", self.__total)
        print("total para json", self.__total)
        total = self.__total.replace('.','')
        total = total.replace(',','')
        print("total para json formatado", total)
        with open("/opt/paygoWeb/comprovantes/valor_venda.json", "w+") as f:
            f.write('\n{  \n\n')
            f.write('"TOTAL": "%s",  \n'%(total))
            f.write('"LANGUAGE": "%s",  \n'%(self.language))
            f.write('"PWINFO_CARDTYPE": "%s"  \n'%(tipo))
            f.write('\n}  \n')
        #self.wait_payment()
        

       
        pagamento_extra = {
            "SENHA"         : self.__senha, 
            "VALOR_TOTAL"   : self.__total
        }
        self.window_select_cartao.hide()
        self.window_login.hide()
        self.window_pagamento_extra.hide()
        result = self.manager.pagamento_extra(self.__total, self.__senha)
        if 'pagamento ok' in result.lower():
            self.dialog_instrucao_fecha_armario.show()
            time.sleep(5.0)
            self.dialog_instrucao_fecha_armario.hide()
        else:
            self.label_window_erro_pagamentos.set_text(result)
            self.window_erro_pagamento()
            print(result)

class WindowSelectCartao:
    def __init__(self):
        self.build = Gtk.Builder()
        self.build.add_from_file("ui/window_select_cartao.glade")
        self.build.connect_signals(
            {
                "gtk_main_quit": Gtk.main_quit,
                "on_btn_credito_button_press_event": self.on_btn_credito_button_press_event,
                "on_btn_debito_button_press_event": self.on_btn_debito_button_press_event,
                "on_btn_cancelar_button_press_event": self.on_btn_cancelar_button_press_event
            }
        )
        self.btn_credito = self.build.get_object("btn_credito")
        self.btn_credito.connect("button-press-event", self.on_btn_credito_button_press_event)
        self.btn_debito = self.build.get_object("btn_debito")
        #self.btn_debito.connect("button-press-event", self.on_btn_debito_button_press_event)
        self.btn_cancelar = self.build.get_object("btn_cancelar")
        #self.btn_cancelar.connect("button-press-event", self.on_btn_cancelar_button_press_event)
        self.tipo_cartao = ''

        self.window_select_cartao = self.build.get_object(
            "window_select_cartao")
        self.window_select_cartao.show()

    def on_btn_credito_button_press_event(self, event, args):
        # print("1")
        self.send_tipo_cartao("CREDITO")
        sleep(0.5)
        
        

    def on_btn_debito_button_press_event(self, event, args):
        # print("2")
        self.send_tipo_cartao("DEBITO")
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
    

if __name__ == "__main__":
    app = CollBagSafe()
    Gtk.main()