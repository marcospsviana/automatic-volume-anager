#!/usr/bin/python3
# -*- coding: utf-8 -*- 
import sys, os
import subprocess
import gi, gobject
import numpy as np
import string, encodings.unicode_escape
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from controllers import Management
from login import Login
from encerrar import Encerrar
#from locacao import Locacao


class RaspControl(object):
    def __init__(self):
        self.manager = Management()
        self.text = ''
        self.value = ''
        self.values = ''
        self.entrada = '1'
        self.total = 0.0
        self.armario = ''
        self.lbl_armario = ''
        self.dia = self.hora = self.minuto = 0.0
        self.alfa = list(string.ascii_lowercase) # alfabeto para gerar o teclado
        self.num = False
        #folha de estilo das interfaces
        self.gtk_style()
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/index.glade")
        self.builder.connect_signals({
        "on_btn_encerrar_clicked": self.on_btn_encerrar_clicked,
        #"on_btn_login_clicked": self.on_btn_login_clicked,
        "on_btn_campo_branco_clicked": self.on_btn_campo_branco_clicked,
        "on_btn_A_clicked": self.on_btn_A_clicked,
        "on_btn_B_clicked": self.on_btn_B_clicked,
        "on_btn_C_clicked": self.on_btn_C_clicked,
        "on_btn_D_clicked": self.on_btn_D_clicked,
        "btn_locar_clicked_cb": self.btn_locar_clicked_cb,
        "on_entry_button_press_event": self.on_entry_button_press_event,
        "on_entry_nome": self.on_entry_nome,
        "on_entry_telefone": self.on_entry_telefone,
        "on_entry_email": self.on_entry_email,
        "on_entry_dias": self.on_entry_dias,
        "on_entry_horas": self.on_entry_horas,
        "on_entry_minutos": self.on_entry_minutos,
        "gtk_widget_destroy": self.gtk_widget_destroy,
        "on_locacao_destroy": self.on_locacao_destroy,
        "on_btn_proximo_button_press_event": self.on_btn_proximo_button_press_event,
        "on_onpen": self.abrir,
        "on_space_clicked": self.on_space_clicked,
        "on_btn_dialog_confirmar_clicked": self.on_btn_dialog_confirmar_clicked,
        "on_btn_dialog_cancelar_clicked": self.on_btn_dialog_cancelar_clicked,
        "btn_abrir_clicked_cb": self.btn_abrir_clicked_cb,
        #"on_btn_login_clicked": self.on_btn_login_clicked,
        "on_num_button_press_event": self.on_num_button_press_event,
        "on_btn_cancelar_button_press_event": self.on_btn_cancelar_button_press_event,
        "gtk_main_quit": Gtk.main_quit
        })
        
        #adicionando os elementos do teclado =======================
        self.a = self.builder.get_object("a")
        self.a.connect("clicked", self.on_entry_button_press_event)
        self.b = self.builder.get_object("b")
        self.b.connect("clicked", self.on_entry_button_press_event)
        self.c = self.builder.get_object("c")
        self.c.connect("clicked", self.on_entry_button_press_event)
        self.d = self.builder.get_object("d")
        self.d.connect("clicked", self.on_entry_button_press_event)
        self.e = self.builder.get_object("e")
        self.e.connect("clicked", self.on_entry_button_press_event)
        self.f = self.builder.get_object("f")
        self.f.connect("clicked", self.on_entry_button_press_event)
        self.g = self.builder.get_object("g")
        self.g.connect("clicked", self.on_entry_button_press_event)
        self.h = self.builder.get_object("h")
        self.h.connect("clicked", self.on_entry_button_press_event)
        self.i = self.builder.get_object("i")
        self.i.connect("clicked", self.on_entry_button_press_event)
        self.j = self.builder.get_object("j")
        self.j.connect("clicked", self.on_entry_button_press_event)
        self.k = self.builder.get_object("k")
        self.k.connect("clicked", self.on_entry_button_press_event)
        self.l = self.builder.get_object("l")
        self.l.connect("clicked", self.on_entry_button_press_event)
        self.m = self.builder.get_object("m")
        self.m.connect("clicked", self.on_entry_button_press_event)
        self.n = self.builder.get_object("n")
        self.n.connect("clicked", self.on_entry_button_press_event)
        self.o = self.builder.get_object("o")
        self.o.connect("clicked", self.on_entry_button_press_event)
        self.p = self.builder.get_object("p")
        self.p.connect("clicked", self.on_entry_button_press_event)
        self.q = self.builder.get_object("q")
        self.q.connect("clicked", self.on_entry_button_press_event)
        self.r = self.builder.get_object("r")
        self.r.connect("clicked", self.on_entry_button_press_event)
        self.s = self.builder.get_object("s")
        self.s.connect("clicked", self.on_entry_button_press_event)
        self.t = self.builder.get_object("t")
        self.t.connect("clicked", self.on_entry_button_press_event)
        self.u = self.builder.get_object("u")
        self.u.connect("clicked", self.on_entry_button_press_event)
        self.v = self.builder.get_object("v")
        self.v.connect("clicked", self.on_entry_button_press_event)
        self.w = self.builder.get_object("w")
        self.w.connect("clicked", self.on_entry_button_press_event)
        self.x = self.builder.get_object("x")
        self.x.connect("clicked", self.on_entry_button_press_event)
        self.y = self.builder.get_object("y")
        self.y.connect("clicked", self.on_entry_button_press_event)
        self.z = self.builder.get_object("z")
        self.z.connect("clicked", self.on_entry_button_press_event)
        self.space = self.builder.get_object("space")
        #========== fim elementos do teclado 
        
        
        #=========== dialog cobranca ===========
        self.btn_cobranca_ok = self.builder.get_object("btn_cobranca_ok")
        self.btn_cobranca_ok.connect("clicked", self.btn_cobranca_ok_clicked)


        #========= dialog escolha ==============
        self.dialog_escolha = self.builder.get_object('dialog_escolha')
        self.lbl_a = self.builder.get_object('lbl_a')
        self.lbl_b = self.builder.get_object('lbl_b')
        self.lbl_c = self.builder.get_object('lbl_c')
        self.lbl_d = self.builder.get_object('lbl_d')
        self.label_message_escolha = self.builder.get_object("label_message_escolha")
        #self.btn_escolha_cancela = self.builder.get_object('btn_escolha_cancela')
        self.btn_escolha_ok = self.builder.get_object('btn_escolha_ok')
        self.btn_escolha_ok.connect("clicked", self.on_btn_escolha_ok_destroy)

        # ========= dialog confirma ============
        self.dialog = self.builder.get_object("dialogConfirm")
        #===== tela de login =======================
        
        # ============= tela locar e botoes de escolha de armarios
        self.locar = self.builder.get_object("locar_window")
        self.locar.fullscreen()
        self.btn_A = self.builder.get_object("btn_A")
        self.btn_B = self.builder.get_object("btn_B")
        self.btn_C = self.builder.get_object("btn_C")
        self.btn_Dsup = self.builder.get_object("btn_DSup")
        self.btn_Dinf = self.builder.get_object("btn_DInf")
        self.btn_A.connect_object("clicked",self.on_show_locacao, self.on_btn_A_clicked)
        self.btn_B.connect_object("clicked",self.on_show_locacao, self.on_btn_B_clicked)
        self.btn_C.connect_object("clicked",self.on_show_locacao, self.on_btn_C_clicked)
        self.btn_Dsup.connect_object("clicked",self.on_show_locacao, self.on_btn_D_clicked)
        self.btn_Dinf.connect_object("clicked",self.on_show_locacao, self.on_btn_D_clicked)
        # ============ fim tela locar =======================
        
        self.window = self.builder.get_object("main_window")
        self.window.fullscreen()
        
        self.teclado = self.builder.get_object("teclado")
        self.grid_teclado = self.builder.get_object("grid_teclado")
        #elementos janela locacao
        self.locacao = self.builder.get_object("locacao") #janela
        self.locacao.fullscreen()
        self.btn_cancelar = self.builder.get_object("btn_cancelar")
        self.btn_proximo = self.builder.get_object("btn_proximo")
        ## adicionando os elementos do form locacao com cadastro
        self.entry_nome = self.builder.get_object("entry_nome")
        self.entry_telefone = self.builder.get_object("entry_telefone")
        self.entry_email = self.builder.get_object("entry_email")
        self.entry_dias = self.builder.get_object("entry_dias")
        self.entry_horas = self.builder.get_object("entry_horas")
        self.entry_minutos = self.builder.get_object("entry_minutos")
        self.text_total = self.builder.get_object("text_total")
        self.btn_delete = self.builder.get_object("DELETE")

        ##elementos label dialog
        self.lbl_nome = self.builder.get_object("lbl_nome")
        self.lbl_email = self.builder.get_object("lbl_email")
        self.lbl_telefone = self.builder.get_object("lbl_telefone")
        self.lbl_dias = self.builder.get_object("lbl_dias")
        self.lbl_armario = self.builder.get_object("lbl_armario")
        self.lbl_horas = self.builder.get_object("lbl_horas")
        self.lbl_minutos = self.builder.get_object("lbl_minutos")
        self.lbl_total = self.builder.get_object("lbl_total")
        self.btn_dialog_confirmar = self.builder.get_object("btn_dialog_confirmar")
        self.btn_dialog_cancelar = self.builder.get_object("btn_dialog_cancelar")
        self.dialog_campo_em_branco = self.builder.get_object("dialog_campo_em_branco")
        self.btn_campo_branco = self.builder.get_object("btn_campo_branco")
        self.dialogConfirm = self.builder.get_object("dialogConfirm")
        #entradas de campos tela login ===========
        self.entry_nome_login = self.builder.get_object("entry_nome_login")
        self.entry_senha = self.builder.get_object("entry_senha")
        self.dialog_cobranca = self.builder.get_object("dialog_cobranca")
        self.lbl_message = self.builder.get_object("lbl_message")
        self.btn_num = self.builder.get_object("num")

        #conectando as entradas aos eventos de teclado
        self.entry_nome.connect('button-press-event', self.on_entry_nome)
        self.entry_telefone.connect('button-press-event', self.on_entry_telefone)
        self.entry_email.connect('button-press-event', self.on_entry_email)
        self.entry_dias.connect('button-press-event', self.on_entry_dias)
        self.entry_horas.connect('button-press-event', self.on_entry_horas)
        self.entry_minutos.connect('button-press-event', self.on_entry_minutos) 
        #conectando os botões aos eventos
        self.btn_delete.connect("clicked", self.on_entry_backspace)
        
        self.space.connect("clicked", self.on_space_clicked)
        #self.btn_campo_branco.connect("clicked", self.on_btn_campo_clicked)
        # ==== exibe janela principal com todos os elementos =================
        self.window.show()
    
    def on_num_button_press_event(self, widget, event):
        if self.num == False:
            self.num = True
            self.a.set_label('a')
            self.b.set_label('b')
            self.c.set_label('c')
            self.d.set_label('d')
            self.e.set_label('e')
            self.f.set_label('f')
            self.g.set_label('g')
            self.h.set_label('h')
            self.i.set_label('i')
            self.j.set_label('j')
            self.k.set_label('k')
            self.l.set_label('l')
            self.m.set_label('m')
            self.n.set_label('n')
            self.o.set_label('o')
            self.p.set_label('p')
            self.q.set_label('q')
            self.r.set_label('r')
            self.s.set_visible(True)
            self.t.set_visible(True)
            self.u.set_visible(True)
            self.v.set_visible(True)
            self.w.set_visible(True)
            self.x.set_visible(True)
            self.y.set_visible(True)
            self.z.set_visible(True)
            
            self.btn_num.set_label('123..')
        else:
            self.num = False
            self.a.set_label('0')
            self.b.set_label('1')
            self.c.set_label('2')
            self.d.set_label('3')
            self.e.set_label('4')
            self.f.set_label('5')
            self.g.set_label('6')
            self.h.set_label('7')
            self.i.set_label('8')
            self.j.set_label('9')
            self.k.set_label('@')
            self.l.set_label('_')
            self.m.set_label('-')
            self.n.set_label('.')
            self.o.set_label('.com')
            self.p.set_label('@gmail')
            self.q.set_label('@outlook')
            self.r.set_label('@yahoo')
            self.s.set_visible(False)
            self.t.set_visible(False)
            self.u.set_visible(False)
            self.v.set_visible(False)
            self.w.set_visible(False)
            self.x.set_visible(False)
            self.y.set_visible(False)
            self.z.set_visible(False)
            self.btn_num.set_label('abc..')
    
    def on_btn_encerrar_clicked(self, event):
        Encerrar()
    


    def btn_cobranca_ok_clicked(self, event):
        self.dialog_cobranca.hide()
        self.entry_nome_login.set_text('')
        self.entry_senha.set_text('')
        

    def on_btn_campo_branco_clicked(self, widget):
        self.dialog_campo_em_branco.hide()
        self.locacao.show()

    def btn_abrir_clicked_cb(self, widget):
        Login()
        #self.window_login.show()
        
        

    def on_btn_escolha_ok_destroy(self, event):
        self.dialog_escolha.hide()


    def on_btn_A_clicked(self, event):
        self.lbl_armario.set_text("A")
        print('setado lbl_armario para A')
        return self.lbl_armario


    def on_btn_B_clicked(self, event):
        self.lbl_armario.set_text("B")
        print('setado lbl_armario para B')
        return self.lbl_armario
    
    def on_btn_C_clicked(self, event):
        self.lbl_armario.set_text("C")
        print('setado lbl_armario para C') 
        return self.lbl_armario
    
    def on_btn_D_clicked(self, event):
        self.lbl_armario.set_text("D")
        print('setado lbl_armario para D')
        return self.lbl_armario
        
    def on_entry_nome(self, widget, event):
        self.entrada = '1'
        return self.entrada
    
    def on_entry_email(self, widget, event):
        self.entrada = '2'
        return self.entrada
    
    def on_entry_telefone(self, widget, event):
        self.entrada = '3'
        return self.entrada
    
    def on_entry_dias(self, widget, event):
        self.entrada = '4'
        return self.entrada
    
    def on_entry_horas(self, widget, event):
        self.entrada = '5'
        return self.entrada
    
    def on_entry_minutos( self, widget, event):
        self.entrada = '6'
        return self.entrada
    def on_entry_nome_login(self, widget, event):
        self.entrada = '7'
        return self.entrada
    
    def on_entry_senha(self, widget, event):
        self.entrada = '8'
        return self.entrada


    def on_space_clicked(self, widget):
        
        if self.entrada == '1':
            self.text_nome = self.entry_nome.get_text()
            self.text_nome = self.text_nome.replace(self.text_nome, self.text_nome+" ")
            self.entry_nome.set_text(self.text_nome)
            self.entry_nome.set_position(0)
    
    def on_btn_dialog_confirmar_clicked(self, event):
        manager = Management()
        self.nome = self.lbl_nome.get_label()
        self.email = self.lbl_email.get_label()
        self.telefone = self.lbl_telefone.get_label()
        self.dias = self.lbl_dias.get_label()
        self.horas = self.lbl_horas.get_label()
        self.minutos = self.lbl_minutos.get_label()
        self.armario = self.lbl_armario.get_label()
        self.total = self.lbl_total.get_label()
        
        result = manager.locacao(self.nome, self.email, self.telefone, self.dias, self.horas, self.minutos, self.armario )
        print("result on_btn_confirmar", result)
        
        if result[0] == "armario locado com sucesso":
            self.dialog.hide()
            self.locacao.hide()
    
    def on_btn_dialog_cancelar_clicked(self, widget):
        self.lbl_total.set_text('0,00')
        self.lbl_nome.set_text('')
        self.lbl_email.set_text('')
        self.lbl_telefone.set_text('')
        self.lbl_dias.set_text('0')
        self.lbl_horas.set_text('0')
        self.lbl_horas.set_text('')
        self.lbl_minutos.set_text('0')
        self.dialogConfirm.hide()

        
    

    def on_entry_button_press_event(self, widget):
        self.widget = widget
        self.armario = self.lbl_armario.get_label()
        self.lbl_armario.set_text(self.armario)
        self.value =  self.widget.get_label()
        
        if self.entrada == '1':
            
            self.text_nome = self.entry_nome.get_text() + self.value
            if self.text_nome.isalpha() or (self.text_nome.isalpha and string.whitespace):
                self.entry_nome.set_text(self.text_nome)
                self.lbl_nome.set_text(self.text_nome)
                self.entry_nome.set_position(-1)
                
            
        elif self.entrada == '2':
            self.text_email = self.entry_email.get_text() + self.value
            self.entry_email.set_text(self.text_email)
            self.lbl_email.set_text(self.text_email)
            self.entry_email.set_position(-1)

        elif self.entrada == '3':
            self.text_telefone = self.entry_telefone.get_text() + self.value
            if self.text_telefone.isnumeric():
                self.entry_telefone.set_text(self.text_telefone)
                self.lbl_telefone.set_text(self.text_telefone)
                self.entry_telefone.set_position(-1)
                
        
        elif self.entrada == '4':
            self.text_dias = self.entry_dias.get_text() + self.value
            if self.text_dias.isnumeric():
                self.entry_dias.set_text(self.text_dias)
                self.lbl_dias.set_text(self.text_dias)
                self.entry_dias.set_position(-1)
                self.taxa = 0.15
                self.dia = self.entry_dias.get_text()
                print('preço total')
                self.dia = self.dia + ".0"
                self.dia = float(self.dia)
                self.dia = self.dia * 50
                self.hora = self.entry_horas.get_text()
                self.hora = self.hora +".0"
                self.hora = float(self.hora) 
                self.hora = self.hora * 60 * 0.15
                self.minuto = self.entry_minutos.get_text()
                self.minuto = self.minuto + ".0"
                self.minuto = float(self.minuto) 
                self.minuto = self.minuto * 0.15
                self.total =  self.dia + self.hora + self.minuto
                print(self.total)
                self.text_total.set_text(str(self.total))
                self.lbl_total.set_text(str(self.total))
        
        elif self.entrada == '5':
            if self.entry_horas.get_text() > '23':
                self.entry_horas.set_text('23')
            
    
            
            self.text_horas = self.entry_horas.get_text() + self.value
            
            
            if self.text_horas.isnumeric():
                self.entry_horas.set_text(self.text_horas)
                self.lbl_horas.set_text(self.text_horas[:2])
                self.entry_horas.set_position(-1)
                self.taxa = 0.15
                self.dia = self.entry_dias.get_text()
                
                print('preço total')
                self.dia = self.dia + ".0"
                self.dia = float(self.dia)
                self.dia = self.dia * 50
                self.hora = self.entry_horas.get_text()
                self.hora = self.hora +".0"
                self.hora = float(self.hora)
                self.hora = self.hora * 60 * 0.15
                self.minuto = self.entry_minutos.get_text()
                self.minuto = self.minuto + ".0"
                self.minuto = float(self.minuto) 
                self.minuto = self.minuto * 0.15
                self.total =  self.dia + self.hora + self.minuto
                print(self.total)
                self.text_total.set_text(str(self.total))
                self.lbl_total.set_text(str(self.total))
        
        elif self.entrada == '6':
            if self.entry_minutos.get_text() > '59':
                self.entry_minutos.set_text('59')
            self.text_minutos = self.entry_minutos.get_text() + self.value
            
            if self.text_minutos.isnumeric():
                self.entry_minutos.set_text(self.text_minutos)
                self.lbl_minutos.set_text(self.text_minutos[:2])
                self.entry_minutos.set_position(-1)
                self.taxa = 0.15
                self.dia = self.entry_dias.get_text()
                self.dia = self.dia + ".0"
                self.dia = float(self.dia)
                self.dia = self.dia * 50
                self.hora = self.entry_horas.get_text()
                self.hora = self.hora +".0"
                self.hora = float(self.hora) 
                self.hora = self.hora * 60 * 0.15
                self.minuto = self.entry_minutos.get_text()
                self.minuto = self.minuto + ".0"
                self.minuto = float(self.minuto) 
                self.minuto = self.minuto * 0.15
                self.total =  self.dia + self.hora + self.minuto
                print(self.total)
                self.text_total.set_text(str(self.total))
                self.lbl_total.set_text(str(self.total))
                return self.minuto
        elif self.entrada == '7':
            
            self.text_nome = self.entry_nome.get_text() + self.value
            if self.text_nome.isalpha() or (self.text_nome.isalpha and string.whitespace):
                self.entry_nome.set_text(self.text_nome)
                self.entry_nome.set_position(-1)
                
            
        elif self.entrada == '8':
            self.text_senha = self.entry_senha.get_text() + self.value
            self.entry_senha.set_text(self.text_senha)
            self.entry_senha.set_position(-1)

    def on_entry_backspace(self, widget):
        
        if self.entrada == '1':
            self.texto = ''
            self.texto = self.entry_nome.get_text()
            self.texto = self.texto[:-1]
            self.entry_nome.set_text(self.texto)
            self.entry_nome.set_position(-1)
            self.lbl_nome.set_text(self.entry_nome.get_text())
        elif self.entrada == '2':
            self.texto = ''
            self.texto = self.entry_email.get_text()
            self.texto = self.texto[:-1]
            self.entry_email.set_text(self.texto)
            self.entry_email.set_position(-1)
        elif self.entrada == '3':
            self.texto = ''
            self.texto = self.entry_telefone.get_text()
            self.texto = self.texto[:-1]
            self.entry_telefone.set_text(self.texto)
            self.entry_telefone.set_position(-1)
        elif self.entrada == '4':
            self.texto = ''
            self.texto = self.entry_dias.get_text()
            self.texto = self.texto[:-1]
            self.entry_dias.set_text(self.texto)
            self.entry_dias.set_position(-1)
            self.taxa = 0.15
            self.dia = self.entry_dias.get_text()
            print('preço total')
            self.dia = self.dia + ".0"
            self.dia = float(self.dia)
            self.dia = self.dia * 50
            self.hora = self.entry_horas.get_text()
            self.hora = self.hora +".0"
            self.hora = float(self.hora) 
            self.hora = self.hora * 60 * 0.15
            self.minuto = self.entry_minutos.get_text()
            self.minuto = self.minuto + ".0"
            self.minuto = float(self.minuto) 
            self.minuto = self.minuto * 0.15
            self.total =  self.dia + self.hora + self.minuto
            print(self.total)
            self.text_total.set_text(str(self.total))
            self.lbl_total.set_text(str(self.total))
        elif self.entrada == '5':
            self.texto = ''
            self.texto = self.entry_horas.get_text()
            self.texto = self.texto[:-1]
            self.entry_horas.set_text(self.texto)
            self.entry_horas.set_position(-1)
            self.taxa = 0.15
            self.dia = self.entry_dias.get_text()
            print('preço total')
            self.dia = self.dia + ".0"
            self.dia = float(self.dia)
            self.dia = self.dia * 50
            self.hora = self.entry_horas.get_text()
            self.hora = self.hora +".0"
            self.hora = float(self.hora) 
            self.hora = self.hora * 60 * 0.15
            self.minuto = self.entry_minutos.get_text()
            self.minuto = self.minuto + ".0"
            self.minuto = float(self.minuto) 
            self.minuto = self.minuto * 0.15
            self.total =  self.dia + self.hora + self.minuto
            print(self.total)
            self.text_total.set_text(str(self.total))
            self.lbl_total.set_text(str(self.total))
            
            
        
        elif self.entrada == '6':
            self.texto = ''
            self.texto = self.entry_minutos.get_text()
            self.texto = self.texto[:-1]
            self.entry_minutos.set_text(self.texto)
            self.entry_minutos.set_position(-1)
            self.taxa = 0.15
            self.dia = self.entry_dias.get_text()
            print('preço total')
            self.dia = self.dia + ".0"
            self.dia = float(self.dia)
            self.dia = self.dia * 50
            self.hora = self.entry_horas.get_text()
            self.hora = self.hora +".0"
            self.hora = float(self.hora) 
            self.hora = self.hora * 60 * 0.15
            self.minuto = self.entry_minutos.get_text()
            self.minuto = self.minuto + ".0"
            self.minuto = float(self.minuto)
            self.minuto = self.minuto * 0.15
            self.total =  self.dia + self.hora + self.minuto
            print(self.total)
            self.text_total.set_text(str(self.total))
            self.lbl_total.set_text(str(self.total))
    

    def on_btn_cancelar_button_press_event(self, widget, event):
        self.lbl_armario.set_text('')
        self.lbl_dias.set_text('')
        self.lbl_email.set_text('')
        self.lbl_horas.set_text('')
        self.lbl_nome.set_text('')
        self.lbl_total.set_text('')
        self.lbl_minutos.set_text('')
        self.lbl_telefone.set_text('')
        self.entry_dias.set_text('')
        self.entry_email.set_text('')
        self.entry_horas.set_text('')
        self.entry_minutos.set_text('')
        self.entry_nome.set_text('')
        self.entry_telefone.set_text('')
        self.entry_dias.set_text('')
        self.entry_email.set_text('')
        self.entry_horas.set_text('')
        self.entry_minutos.set_text('')
        self.entry_nome.set_text('')
        self.entry_telefone.set_text('')
        self.locacao.hide()           
            
   

    def gtk_widget_destroy(self, widget):
        self.locar.hide()
        #self.window_login(self.builder, None)
       
    
    def btn_locar_clicked_cb(self, widget):
        #Locacao().locar_window

        
        self.locar.show()
    # ====== janela locacao =======
    def on_show_locacao(self, widget):
        manager = Management()
        self.armario = self.lbl_armario.get_label()
        print('self.armario main', self.armario)
        classe = manager.select_armario(self.armario)
        print('classe selecionada' ,classe)
        
        listar = manager.lista_armarios()
        if "A" in np.array(listar):
            self.lbl_a.set_text("A")
        if "B" in np.array(listar):
            self.lbl_b.set_text("B")
        if "C" in np.array(listar):
            self.lbl_c.set_text("C")
        if "D" in np.array(listar):
            self.lbl_b.set_text("D")
        if self.armario in np.array(classe):
            self.locacao.show()
        else:
            self.dialog_escolha.show()
        print('listar classes mainwindow', listar)
        
        
    
    def on_locacao_destroy(self, widget, event):
        self.locacao.hide()
    def on_btn_proximo_button_press_event(self, widget, event):
        if self.entry_dias.get_text == '':
            self.lbl_dias.set_text('0')
        elif self.entry_horas.get_text() == '':
            self.lbl_horas.set_text('0')
        elif self.entry_minutos.get_text() == '':
            self.lbl_minutos.set_text('0')
        self.dialog.show()
        self.text_total.set_text("0,00")
        self.entry_dias.set_text('')
        self.entry_email.set_text('')
        self.entry_horas.set_text('')
        self.entry_minutos.set_text('')
        self.entry_nome.set_text('')
        self.entry_telefone.set_text('')
        
            
            
    
            
    def abrir(self, widget):
        pass
    
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
    
    def dialog(self):
        pass
   

    
if __name__ == "__main__":
    app = RaspControl()

    Gtk.main()
