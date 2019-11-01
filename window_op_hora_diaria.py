import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from datetime import datetime, date
from cadastro_usuarios import CadastroUsuarios

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
        self.codigos_ddd = ["""
        ###+27	 África do Sul,
        +49	 Alemanha	Europa,
        +966	 Arábia Saudita	Ásia,
        +213	 Argélia	África,
        +54	 Argentina	América do Sul,
        +374	 Armênia	Ásia,
        +61	 Austrália	Oceania,
        +43	 Áustria	Europa,
        +973	 Bahrein	Ásia,
        +32	 Bélgica	Europa,

        +1	 Bermudas	América Central,

        +591	 Bolívia	América do Sul,
        +55	 Brasil	América do Sul,
        +237	 Camarões	África,
        +1	 Canadá	América do Norte,
        +56	 Chile	América do Sul,
        +86	 República Popular da China	Ásia,
        +57	 Colômbia	América do Sul,
        +82	 Coreia do Sul	Ásia,
        +506	 Costa Rica	América Central,
        +45	 Dinamarca	Europa,
        +20	 Egipto	África/Ásia,
        +503	 El Salvador	América Central,
        +971	 Emirados Árabes Unidos	Ásia,
        +593	 Equador	América do Sul,
        +34	 Espanha	Europa,
        +1	 Estados Unidos	América do Norte,
        +358	 Finlândia	Europa,
        +33	 França	Europa,
        +350	 Gibraltar	Europa,
        +30	 Grécia	Europa,
        +299	 Groenlândia	América do Norte,
        +502	 Guatemala	América Central,
        +592	 Guiana	América do Sul,
        +594	 Guiana Francesa	América do Sul,
        +224	 Guiné	África,
        +245	 Guiné-Bissau	África,
        +240	 Guiné Equatorial	África,
        +509	 Haiti	América Central,
        +504	 Honduras	América Central,
        +852	 Hong Kong	Ásia,
        +91	 Índia	Ásia,
        +62	 Indonésia	Ásia/Oceania,
        +98	 Irã	Ásia,
        +964	 Iraque	Ásia,
        +353	 Irlanda	Europa,
        +354	 Islândia	Europa,
        +972	 Israel	Ásia,
        +39	 Itália	Europa,
        +81	 Japão	Ásia,
        +60	 Malásia	Ásia,        
        +52	 México	América do Norte,
       
        +373	 Moldávia	Europa,
        +377	 Mônaco	Europa,
        +505	 Nicarágua	América Central,
        
        +47	 Noruega	Europa,
     
        +64	 Nova Zelândia	Oceania,
        
        
        
        +507	 Panamá	América Central,
     
       
        +595	 Paraguai	América do Sul,
        +51	 Peru	América do Sul,
      
        +48	 Polônia	Europa,
        +1	 Porto Rico	América Central,
        +351	 Portugal	Europa,
        +974	 Qatar	Ásia,
        +254	 Quênia	África,
        
        +44	 Reino Unido	Europa,
       
        +1	 República Dominicana	América Central,
        
        +40	 Romênia	Europa,
        
        +7	 Rússia	Europa/Ásia,
        
        
        
        +65	 Singapura	Ásia,
       
        
        +46	 Suécia	Europa,
        +41	 Suíça	Europa,
        +597	 Suriname	América do Sul,
        
        +66	 Tailândia	Ásia,
        +886	 República da China	Ásia,
        
        
        +670	 Timor-Leste	Ásia,
       
        +1	 Trinidad e Tobago	América Central,
     
        
        +90	 Turquia	Ásia//Europa,
        
       
        +598	 Uruguai	América do Sul,
      
        
       
        +58	 Venezuela	América do Sul,"""
        ]
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

        self.window_hora_diaria.show()
    
    def on_btn_loc_hora_button_press_event(self, widget, event):
        tempo_locacao = "horas"
        CadastroUsuarios(tempo_locacao, self.classe, self.language)
        self.window_hora_diaria.hide()
    
    def on_btn_loc_diaria_button_press_event(self, widget, event):
        tempo_locacao = "diaria"
        CadastroUsuarios(tempo_locacao, self.classe, self.language)
        self.window_hora_diaria.hide()
    
    def on_btn_tela_hora_diaria_button_press_event(self, widget, event):
        self.window_hora_diaria.hide()
    
    def on_change_language_br(self, event):
        self.language = "pt_BR"
        self.label_por_hora.set_text("POR HORA")
        self.label_por_diaria.set_text("POR DIÁRIA")
        self.btn_tela_hora_diaria.set_label("RETORNAR TELA ANTERIOR")
    
    def on_change_language_usa(self, event):
        self.language = "en_US"
        self.label_por_hora.set_text("HOURLY")
        self.label_por_diaria.set_text("DAILY")
        self.btn_tela_hora_diaria.set_label("RETURN TO THE\n PREVIOUS SCREEN")

if __name__ == "__main__":
    app = OpcaoHoraDiaria()
    Gtk.main()