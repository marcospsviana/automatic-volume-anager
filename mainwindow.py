import subprocess
import gi 
import string
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class RaspControl(object):
    def __init__(self):
        self.text = ''
        self.value = ''
        self.values = ''
        self.entrada = '1'
        self.dia = self.hora = self.minuto = 0.0
        self.alfa = list(string.ascii_lowercase) # alfabeto para gerar o teclado
        self.num = list(map(lambda x: x, range(10))) # números para o teclado numérico

        self.gtk_style()
        builder = Gtk.Builder()
        builder.add_from_file("index.glade")
        builder.connect_signals({
        "btn_locar_clicked_cb": self.btn_locar_clicked_cb,
        "on_entry_button_press_event": self.on_entry_button_press_event,
        "gtk_widget_destroy": self.gtk_widget_destroy,
        "on_locacao_destroy": self.on_locacao_destroy,
        "on_btn_proximo_button_press_event": self.on_btn_proximo_button_press_event,
        "gtk_widget_show": self.on_show_locacao,
        "gtk_widget_hide": self.on_hide_cursor,
        "on_onpen": self.abrir,
        "on_text_total_focus": self.show_total,
        "gtk_main_quit": Gtk.main_quit
        })
        #adicionando os elementos do teclado
        for a in self.alfa:
            self.a = builder.get_object("%s"%a)
            self.a.connect("clicked", self.on_entry_button_press_event)
        for n in self.num:
            self.n = builder.get_object("%s"%n)
            self.n.connect("clicked", self.on_entry_button_press_event)


        self.window = builder.get_object("main_window")
        self.window.fullscreen()
        self.locar = builder.get_object("locar_window")
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
        

        #conectando as entradas aos eventos de teclado
        self.entry_nome.connect('button-press-event', self.on_entry_nome)
        self.entry_telefone.connect('button-press-event', self.on_entry_telefone)
        self.entry_email.connect('button-press-event', self.on_entry_email)
        self.entry_dias.connect('button-press-event', self.on_entry_dias)
        self.entry_horas.connect('button-press-event', self.on_entry_horas)
        self.entry_minutos.connect('button-press-event', self.on_entry_minutos)
        
        self.window.show()
    
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


    
        
    

    def on_entry_button_press_event(self, widget):
        self.widget = widget
        self.value =  self.widget.get_label()
        if self.entrada == '1':
            
            self.text_nome = self.entry_nome.get_text() + self.value
            self.entry_nome.set_text(self.text_nome)
            self.entry_nome.set_position(-1)
            
        elif self.entrada == '2':
            self.text_email = self.entry_email.get_text() + self.value
            self.entry_email.set_text(self.text_email)
            self.entry_email.set_position(-1)

        elif self.entrada == '3':
            self.text_telefone = self.entry_telefone.get_text() + self.value
            self.entry_telefone.set_text(self.text_telefone)
            self.entry_telefone.set_position(-1)
        
        elif self.entrada == '4':
            self.text_dias = self.entry_dias.get_text() + self.value
            self.entry_dias.set_text(self.text_dias)
            self.entry_dias.set_position(-1)
        
        elif self.entrada == '5':
            self.text_horas = self.entry_horas.get_text() + self.value
            self.entry_horas.set_text(self.text_horas)
            self.entry_horas.set_position(-1)
        
        elif self.entrada == '6':
            self.text_minutos = self.entry_minutos.get_text() + self.value
            self.entry_minutos.set_text(self.text_minutos)
            self.entry_minutos.set_position(-1)

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
        elif self.entrada == '5':
            self.texto = ''
            self.texto = self.entry_horas.get_text()
            self.texto = self.texto[:-1]
            self.entry_horas.set_text(self.texto)
            self.entry_horas.set_position(-1)
        
        elif self.entrada == '6':
            self.texto = ''
            self.texto = self.entry_minutos.get_text()
            self.texto = self.texto[:-1]
            self.entry_minutos.set_text(self.texto)
            self.entry_minutos.set_position(-1)
         
        
       
        
        '''self.entry_telefone.do_insert_at_cursor
        self.entry_telefone.set_text(self.value)
        self.taxa = 0.15
        self.dia = float(self.entry_dias.get_text()) * 50
        self.hora = float(self.entry_horas.get_text()) * 60 * 0.15
        self.minuto = float(self.entry_minutos.get_text()) * 0.15
        self.text =  str(self.dia + self.hora + self.minuto)
        self.text_total.set_text(str(self.text))'''
        
        #self.value = self.entry.get_text()
        print(self.value)
        return self.value
   

    def gtk_widget_destroy(self, widget):
        self.locar.hide()
        
    
    def btn_locar_clicked_cb(self, widget):
        self.locar.fullscreen()
        self.locar.show()
    # ====== janela locacao =======
    def on_show_locacao(self, widget):
        self.locacao.show()
    def on_locacao_destroy(self, widget):
        self.locacao.hide()
    def on_btn_proximo_button_press_event(self, widget):
        self.text_total.set_text("0,00")
        
        self.locacao.hide()
        self.entry_dias.set_text('')
        self.entry_email.set_text('')
        self.entry_horas.set_text('')
        self.entry_minutos.set_text('')
        self.entry_nome.set_text('')
        self.entry_telefone.set_text('')


    def show_total(self):
        print('ta indo')
        self.text_total.set_text( "ola")
        
    
    '''def entry_nome_activate_cb(self, widget):
        self.teclado.show()'''
        

    def on_hide_cursor(self, widget):
        self.teclado.hide()    
        
    def abrir(self, widget):
        pass
    
    def gtk_style(self):
        css = b"""
        #btn_locar { color: #000000;  font-size: 32px;}
        #btn_abrir { color: #000000;  font-size: 32px;}
        #btn_encerrar { color: #000000;  font-size: 32px;}
        #locar_window { background-color: #fff}
        #btn_num{ background-color: red; font-size: 22px}
        #grid_teclado { font-size: 15px}
        #btn_proximo { font-size: 20px; background-color: #008cc3; color: #fff }
        #btn_cancelar { font-size: 20px; background-color: red; color: #fff }
        #label { font-size: 22px; }
        #entry { font-size: 22px;}
        #tecla { font-size: 22px;}
        """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    



if __name__ == "__main__":
    app = RaspControl()
    Gtk.main()
