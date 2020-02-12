from controllers import Management
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import string
import time
from datetime import datetime
import calendar
from time import sleep


class WindowCalendario:
    def __init__(self):
        #teste = args
        #print("op diaria", teste)
        #self.classe = args[0]
        #self.language = args[1]
        self.builder = Gtk.Builder()
        self.gtk_style()
        self.builder.add_from_file("ui/window_calendario.glade")
        self.builder.connect_signals(
            {
                "on_btn_button_press_event"               : self.on_btn_button_press_event,
                "on_btn_previous_mont_button_press_event" : self.on_btn_previous_mont_button_press_event,
                "on_btn_next_month_button_press_event"    : self.on_btn_next_month_button_press_event,
                "on_btn_previous_year_button_press_event" : self.on_btn_previous_year_button_press_event,
                "on_btn_next_year_button_press_event"     : self.on_btn_next_year_button_press_event,
                "gtk_main_quit"                           : self.on_window_calendario_quit,
            }
        )
        self.window_calendario = self.builder.get_object("window_calendario")

        # ===================== LABELS ========================
        self.label_month = self.builder.get_object("label_month")
        self.label_year = self.builder.get_object("label_year")


        #===================== BUTTONS ========================
        self.btn_previous_mont = self.builder.get_object("btn_previous_mont")
        self.btn_next_mont = self.builder.get_object("btn_next_mont")
        self.btn_previous_year = self.builder.get_object("btn_previous_year")
        self.btn_next_year = self.builder.get_object("btn_next_year")

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



        self.date_calendar = calendar.Calendar()
        data = datetime.now()
        self.weekdays = ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
        self.meses = ["Janeiro","Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        self.ano = data.year
        self.label_month.set_label(str(self.meses[data.month]))
        self.label_year.set_label(str(self.ano))
        calendar.setfirstweekday(calendar.SUNDAY)
        self.mes = calendar.monthcalendar(data.year, data.month)

        dias_meses = [  [self.btn0, self.btn1, self.btn2, self.btn3, self.btn4, self.btn5,self.btn6],
                        [self.btn7, self.btn8, self.btn9, self.btn10,self.btn11,self.btn12,self.btn13],
                        [self.btn14,self.btn15,self.btn16,self.btn17,self.btn18,self.btn19, self.btn20],
                        [self.btn21,self.btn22,self.btn23,self.btn24, self.btn25,self.btn26,self.btn27],
                        [self.btn28,self.btn29, self.btn30,self.btn31,self.btn32,self.btn33,self.btn34]
                    ]
        dias_dom = [self.btn6, self.btn13, self.btn20, self.btn27, self.btn34]
        for i in range(len(self.mes)):
            for j,d in zip(self.mes[i], range(7)):
                dias_meses[i][d].set_label(str(j))
        for i in range(len(dias_meses)):
             for d in range(7):
                if dias_meses[i][d].get_label() == '0':
                    dias_meses[i][d].set_label("")
                    dias_meses[i][d].set_sensitive(False)
                if dias_meses[i][d].get_label() == str(data.day):
                    print("dias messess",dias_meses[i][d].get_label())
                    dias_meses[i][d].gtk_style("border: 1px solid #05878b")
        

        #self.window_calendario.fullscreen()
        self.window_calendario.show()

    def on_btn_button_press_event(self, event, args):
        print("clicou")
    
    def on_btn_previous_mont_button_press_event(self, event, args):
        print("voltar mes")
    
    def on_btn_next_month_button_press_event(self, event, args):
        print("avancar mes")
    
    def on_btn_previous_year_button_press_event(self, event, args):
        print("voltar ano")
    
    def on_btn_next_year_button_press_event(self, event, args):
        print("avancar ano")

    def on_window_calendario_quit(self):
        self.window_calendario.destroy()
    
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


if __name__ == "__main__":
    app = WindowCalendario()
    Gtk.main()
        