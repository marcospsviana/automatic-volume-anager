# -*- coding: utf-8 -*-
import subprocess
import gi, gobject
import numpy as np
import string, encodings.unicode_escape
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from controllers import Management


class RaspControl(object):
    def __init__(self):
        self.text = ''
        self.value = ''
        self.values = ''
        self.entrada = '1'
        self.total = 0.0
        self.armario = ''
        self.lbl_armario = ''
        self.dia = self.hora = self.minuto = 0.0
        self.alfa = list(string.ascii_lowercase) # alfabeto para gerar o teclado
        self.num = list(map(lambda x: x, range(10))) # números para o teclado numérico
        #folha de estilo das interfaces
        self.gtk_style()
        builder = Gtk.Builder()
        builder.add_from_file("index.glade")
        builder.connect_signals({
        "on_btn_A_clicked": self.on_btn_A_clicked,
        "on_btn_B_clicked": self.on_btn_B_clicked,
        "on_btn_C_clicked": self.on_btn_C_clicked,
        "on_btn_D_clicked": self.on_btn_B_clicked,
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
        #"gtk_widget_show": self.on_show_locacao,
        "on_btn_cancelar_button_press_event": self.on_btn_cancelar_button_press_event,
        "gtk_main_quit": Gtk.main_quit
        })
        
        #adicionando os elementos do teclado =======================
        for a in self.alfa:
            self.a = builder.get_object("%s"%a)
            self.a.connect("clicked", self.on_entry_button_press_event)
        for n in self.num:
            self.n = builder.get_object("%s"%n)
            self.n.connect("clicked", self.on_entry_button_press_event)

        self.arroba = builder.get_object("arroba")
        self.dot = builder.get_object("dot")
        self.under = builder.get_object("under")
        self.dash = builder.get_object("dash")
        self.dotCom = builder.get_object("dotCom")
        self.gmail = builder.get_object("gmail")
        self.yahoo = builder.get_object("yahoo")
        self.outlook  = builder.get_object("outlook")
        self.space = builder.get_object("space")
        #========== fim elementos do teclado

        #========= dialog escolha ==============
        self.dialog_escolha = builder.get_object('dialog_escolha')
        self.lbl_a = builder.get_object('lbl_a')
        self.lbl_b = builder.get_object('lbl_b')
        self.lbl_c = builder.get_object('lbl_c')
        self.lbl_d = builder.get_object('lbl_d')
        self.btn_escolha_cancela = builder.get_object('btn_escolha_cancela')
        self.btn_escolha_ok = builder.get_object('btn_escolha_ok')
        self.btn_escolha_ok.connect("clicked", self.on_btn_escolha_ok_destroy)

        # ========= dialog confirma ============
        self.dialog = builder.get_object("dialogConfirm")
        # ============= tela locar e botoes de escolha de armarios
        self.locar = builder.get_object("locar_window")
        self.btn_A = builder.get_object("btn_A")
        self.btn_B = builder.get_object("btn_B")
        self.btn_C = builder.get_object("btn_C")
        self.btn_Dsup = builder.get_object("btn_DSup")
        self.btn_Dinf = builder.get_object("btn_DInf")
        self.btn_A.connect_object("clicked",self.on_show_locacao, self.on_btn_A_clicked)
        self.btn_B.connect_object("clicked",self.on_show_locacao, self.on_btn_B_clicked)
        self.btn_C.connect_object("clicked",self.on_show_locacao, self.on_btn_C_clicked)
        self.btn_Dsup.connect_object("clicked",self.on_show_locacao, self.on_btn_D_clicked)
        self.btn_Dinf.connect_object("clicked",self.on_show_locacao, self.on_btn_D_clicked)
        # ============ fim tela locar =======================
        
        self.window = builder.get_object("main_window")
        self.window.fullscreen()
        
        self.teclado = builder.get_object("teclado")
        self.grid_teclado = builder.get_object("grid_teclado1")
        #elementos janela locacao
        self.locacao = builder.get_object("locacao") #janela
        self.btn_cancelar = builder.get_object("btn_cancelar")
        self.btn_proximo = builder.get_object("btn_proximo")
        ## adicionando os elementos do form locacao com cadastro
        self.entry_nome = builder.get_object("entry_nome")
        self.entry_telefone = builder.get_object("entry_telefone")
        self.entry_email = builder.get_object("entry_email")
        self.entry_dias = builder.get_object("entry_dias")
        self.entry_horas = builder.get_object("entry_horas")
        self.entry_minutos = builder.get_object("entry_minutos")
        self.text_total = builder.get_object("text_total")
        self.btn_delete = builder.get_object("DELETE")

        ##elementos label dialog
        self.lbl_nome = builder.get_object("lbl_nome")
        self.lbl_email = builder.get_object("lbl_email")
        self.lbl_telefone = builder.get_object("lbl_telefone")
        self.lbl_dias = builder.get_object("lbl_dias")
        self.lbl_armario = builder.get_object("lbl_armario")
        self.lbl_horas = builder.get_object("lbl_horas")
        self.lbl_minutos = builder.get_object("lbl_minutos")
        self.lbl_total = builder.get_object("lbl_total")
        self.btn_dialog_confirmar = builder.get_object("btn_dialog_confirmar")
        self.btn_dialog_cancelar = builder.get_object("btn_dialog_cancelar")
        

        #conectando as entradas aos eventos de teclado
        self.entry_nome.connect('button-press-event', self.on_entry_nome)
        self.entry_telefone.connect('button-press-event', self.on_entry_telefone)
        self.entry_email.connect('button-press-event', self.on_entry_email)
        self.entry_dias.connect('button-press-event', self.on_entry_dias)
        self.entry_horas.connect('button-press-event', self.on_entry_horas)
        self.entry_minutos.connect('button-press-event', self.on_entry_minutos)
        
        #conectando os botões aos eventos
        self.btn_delete.connect("clicked", self.on_entry_backspace)
        self.arroba.connect("clicked", self.on_entry_button_press_event)
        self.dotCom.connect("clicked", self.on_entry_button_press_event)
        self.dot.connect("clicked", self.on_entry_button_press_event)
        self.dash.connect("clicked", self.on_entry_button_press_event)
        self.under.connect("clicked", self.on_entry_button_press_event)
        self.yahoo.connect("clicked", self.on_entry_button_press_event)
        self.gmail.connect("clicked", self.on_entry_button_press_event)
        self.outlook.connect("clicked", self.on_entry_button_press_event)
        self.space.connect("clicked", self.on_space_clicked)
        
        # ==== exibe janela principal com todos os elementos =================
        self.window.show()
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
    
    def on_btn_dialog_cancelar_clicked(self, event):
        self.dialog_escolha.hide()

        
    

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

    def on_entry_backspace(self, widget):
        
        if self.entrada == '1':
            self.texto = ''
            self.texto = self.entry_nome.get_text()
            self.texto = self.texto[:-1]
            self.entry_nome.set_text(self.texto)
            self.entry_nome.set_position(-1)
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
       
    
    def btn_locar_clicked_cb(self, widget):

        #self.locar.fullscreen()
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
    def on_btn_proximo_button_press_event(self, widget):
        self.text_total.set_text("0,00")
        
        #self.locacao.hide()
        self.entry_dias.set_text('')
        self.entry_email.set_text('')
        self.entry_horas.set_text('')
        self.entry_minutos.set_text('')
        self.entry_nome.set_text('')
        self.entry_telefone.set_text('')
        self.dialog.show()
        
    def abrir(self, widget):
        pass
    
    def gtk_style(self):
        css = b"""
        #btn_locar { color: #000000;  font-size: 32px;}
        #btn_abrir { color: #000000;  font-size: 32px;}
        #btn_encerrar { color: #000000;  font-size: 32px;}
        
        #btn_num{ background-color: red; font-size: 22px}
        #grid_teclado { font-size: 15px}
        #btn_proximo { font-size: 20px; background-color: #008cc3; color: #fff }
        #btn_cancelar { font-size: 20px; background-color: red; color: #fff }
        #label { font-size: 22px; }
        #entry { font-size: 22px; color: #000000}
       
        #tecla { font-size: 22px;}
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
