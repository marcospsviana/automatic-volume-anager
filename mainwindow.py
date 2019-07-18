import subprocess
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class RaspControl(object):
    def __init__(self):
        self.text = ''
        self.dia = self.hora = self.minuto = 0.0

        self.gtk_style()
        builder = Gtk.Builder()
        builder.add_from_file("index.glade")
        builder.connect_signals({
        "btn_locar_clicked_cb": self.btn_locar_clicked_cb,
        "entry_nome_activate_cb": self.entry_nome_activate_cb,
        "gtk_widget_destroy": self.gtk_widget_destroy,
        "on_locacao_destroy": self.on_locacao_destroy,
        "on_btn_proximo_button_press_event": self.on_btn_proximo_button_press_event,
        "gtk_widget_show": self.on_show_locacao,
        "gtk_widget_hide": self.on_hide_cursor,
        "on_onpen": self.abrir,
        "on_text_total_focus": self.show_total,
        "gtk_main_quit": Gtk.main_quit
        })
        self.window = builder.get_object("main_window")
        self.window.fullscreen()
        self.locar = builder.get_object("locar_window")
        self.teclado = builder.get_object("teclado")
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
        self.entry_nome.connect('focus-in-event', self.focus_in)
        self.entry_nome.connect('focus-out-event', self.focus_out)
        self.entry_telefone.connect('focus-in-event', self.focus_in)
        self.entry_telefone.connect('focus-out-event', self.focus_out)
        self.entry_email.connect('focus-in-event', self.focus_in)
        self.entry_email.connect('focus-out-event', self.focus_out)
        self.entry_dias.connect('focus-in-event', self.focus_in)
        self.entry_dias.connect('focus-out-event', self.focus_out) 
        self.entry_horas.connect('focus-in-event', self.focus_in)
        self.entry_horas.connect('focus-out-event', self.focus_out)
        self.entry_minutos.connect('focus-in-event', self.focus_in)
        self.entry_minutos.connect('focus-out-event', self.focus_out)
        self.window.show()

    def focus_out(self, entry, event):
        subprocess.Popen(["pkill", "onboard"]) 
        #self.teclado.hide()
    
    def focus_in(self, entry, event):
        subprocess.Popen("onboard")
        self.taxa = 0.15
        self.dia = float(self.entry_dias.get_text()) * 50
        self.hora = float(self.entry_horas.get_text()) * 60 * 0.15
        self.minuto = float(self.entry_minutos.get_text()) * 0.15
        self.text =  str(self.dia + self.hora + self.minuto)
        self.text_total.set_text(str(self.text))

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
        
    
    def entry_nome_activate_cb(self, widget):
        self.teclado.show()
        

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
        #btn_num{ background-color: red}
        #grid_teclado { font-size: 15px}
        #btn_proximo { font-size: 20px; background-color: #008cc3; color: #fff }
        #btn_cancelar { font-size: 20px; background-color: red; color: #fff }
        #label { font-size: 20px; }
        #entry { font-size: 20px;}
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
