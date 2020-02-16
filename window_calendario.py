from cadastro_usuarios import CadastroUsuarios
from controllers import Management
from taxas import *
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import string
import time
import locale
from datetime import datetime, timedelta
import calendar
from time import sleep


class WindowCalendario:
    def __init__(self, *args):
        #op_and_language = args
        #print("op diaria", teste)
        self.tempo_locacao = args[0]
        self.classe = args[1][0]
        self.language = args[2]
        if self.classe == "A" and self.tempo_locacao == "diaria":
            self.taxa = TaxAndRates.TAXA_DIARIA_A.value
        elif self.classe == "B" and self.tempo_locacao == "diaria":
            self.taxa = TaxAndRates.TAXA_DIARIA_B.value
        
        elif self.classe == "C" and self.tempo_locacao == "diaria":
            self.taxa = TaxAndRates.TAXA_DIARIA_C.value
        
        elif self.classe == "D" and self.tempo_locacao == "diaria":
            self.taxa = TaxAndRates.TAXA_DIARIA_D.value
        
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
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
                "on_btn_confirmar_button_press_event"     : self.on_btn_confirmar_button_press_event,
                "on_btn_cancelar_button_press_event"      : self.on_btn_cancelar_button_press_event,
                "gtk_main_quit"                           : self.on_window_calendario_quit,
            }
        )
        self.window_calendario = self.builder.get_object("window_calendario")

        # ===================== LABELS ========================
        self.label_month = self.builder.get_object("label_month")
        self.label_year = self.builder.get_object("label_year")
        self.label_valor_total = self.builder.get_object("label_valor_total")


        #===================== BUTTONS ========================
        self.btn_previous_mont = self.builder.get_object("btn_previous_mont")
        self.btn_next_mont = self.builder.get_object("btn_next_mont")
        self.btn_previous_year = self.builder.get_object("btn_previous_year")
        self.btn_next_year = self.builder.get_object("btn_next_year")

        self.btn_confirmar = self.builder.get_object("btn_confirmar")
        self.btn_confirmar.connect("button_press_event", self.on_btn_confirmar_button_press_event)

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
        self.label_year.set_label(str(self.ano))
        calendar.setfirstweekday(calendar.SUNDAY)
        



        
        self.set_calendario(self.data.year, self.data.month)

        self.window_calendario.fullscreen()
        self.window_calendario.show()
    def on_btn_cancelar_button_press_event(self, widget, event):
        self.label_valor_total.set_text("")
        self.window_calendario.hide()
    def on_btn_confirmar_button_press_event(self, widget, event):
        self.total = self.label_valor_total.get_label()
        CadastroUsuarios(self.total , self.language)

    def on_btn_button_press_event(self, widget, args):
        self.widget = widget.get_label()
        data = datetime(self.data.year, self.data.month, self.data.day, self.data.hour, self.data.minute)
        mes_escolhido = self.meses_indices[self.label_month.get_label()]
        ano_escolhido = int(self.label_year.get_label())
        data2 = datetime(ano_escolhido, mes_escolhido, int(self.widget), self.data.hour, self.data.minute )
        resultado_dias = abs((data2 - data).days)
        total = self.taxa * resultado_dias #(int(self.widget) - self.data.day)
        print("total = %.2f"%(total))
        self.label_valor_total.set_text("%.2f"%(total))
        print(self.widget)

        
    def set_calendario(self, ano, mes):
        
        self.mes = calendar.monthcalendar(ano, mes)
        self.month = mes
        self.label_month.set_label(self.meses[mes])
        self.label_year.set_label(str(ano))

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
        
        for i in range(len(self.dias_meses)):
            for d in range(len(self.dias_meses[i])):
                self.dias_meses[i][d].set_label("")
        for i in range(len(self.mes)):
            for j,d in zip(self.mes[i], range(7)):
                if self.mes[i][d] == 0 or self.mes[i][d] == None:
                    self.dias_meses[i][d].set_label("")
                else:
                    self.dias_meses[i][d].set_label(str(self.mes[i][d]))
        
        for i in range(len(self.mes)):
            for j,d in zip(self.mes[i], range(7)):
                if self.dias_meses[i][d].get_label() == '0':
                    self.dias_meses[i][d].set_label("")
                    self.dias_meses[i][d].set_sensitive(False)
                else:
                    self.dia = self.dias_meses[i][d].get_label()
                
                """if self.dia == "" or (self.label_month.get_label() < self.meses[self.data.month] and int(self.dia) < self.data.day):
                    print("dias messess",self.dias_meses[i][d].get_label())
                    #self.dias_meses[i][d].set_sensitive(False)
                    self.dias_meses[i][d].set_name("dia_passado")"""
                if self.label_month.get_label() != self.meses[self.data.month] and self.dias_meses[i][d] not in(self.dias_dom):
                    print("dias normais",self.dias_meses[i][d].get_label())
                    #self.dias_meses[i][d].set_sensitive(False)
                    self.dias_meses[i][d].set_name("btn_calendario")
                if self.dias_meses[i][d] in(self.dias_dom):
                    self.dias_meses[i][d].set_name("btn_calendario_dom")
        teste = self.meses_indices[self.label_month.get_label()]
        print("teste", teste)
        teste2 = self.label_month.get_label()
        print("teste2", teste2)
        if self.meses_indices[self.label_month.get_label()] == self.data.month:
            self.btn_previous_mont.set_sensitive(False)
        else:
            self.btn_previous_mont.set_sensitive(True)

        if int(self.label_year.get_label()) == self.data.year:
            self.btn_previous_year.set_sensitive(False) 
        else:
            self.btn_previous_year.set_sensitive(True)    

        
    
    def on_btn_previous_mont_button_press_event(self, event, args):
        self.label_valor_total.set_text("")
        self.mes_atual = self.meses_indices[self.label_month.get_label()]
        print("self.mes_atual", self.mes_atual)
        self.ano_atual = self.data.year
        if self.mes_atual == 1:
            self.mes_atual = 12
            self.ano_atual = self.ano_atual - 1
        else:
            self.mes_atual =  self.mes_atual - 1
            
            
        self.set_calendario(self.ano_atual, self.mes_atual) 
       
       
    
    def on_btn_next_month_button_press_event(self, event, args):
        self.label_valor_total.set_text("")
        self.mes_atual = self.meses_indices[self.label_month.get_label()]
        print("self.mes_atual", self.mes_atual)
        self.ano_atual = self.data.year
        if self.mes_atual == 12:
            self.mes_atual = 1
            self.ano_atual = self.ano_atual + 1
        else:
            self.mes_atual =  self.mes_atual + 1
            
            
        self.set_calendario(self.ano_atual, self.mes_atual) 
    
    def on_btn_previous_year_button_press_event(self, event, args):
        self.label_valor_total.set_text("")
        self.mes_atual = self.meses_indices[self.label_month.get_label()]
        print("self.mes_atual", self.mes_atual)
        self.ano_atual = int(self.label_year.get_label())
       
        self.ano_atual = self.ano_atual - 1

        self.set_calendario(self.ano_atual, self.mes_atual)
    
    def on_btn_next_year_button_press_event(self, event, args):
        self.label_valor_total.set_text("")
        self.mes_atual = self.meses_indices[self.label_month.get_label()]
        print("self.mes_atual", self.mes_atual)
        self.ano_atual = int(self.label_year.get_label())
       
        self.ano_atual = self.ano_atual + 1

        self.set_calendario(self.ano_atual, self.mes_atual)

    def on_window_calendario_quit(self):
        self.window_calendario.destroy()
    
    def gtk_style(self):
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


if __name__ == "__main__":
    app = WindowCalendario()
    Gtk.main()
        