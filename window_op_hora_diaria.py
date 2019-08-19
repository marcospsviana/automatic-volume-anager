import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from datetime import datetime, date

class OpcaoHoraDiaria(object):
    def __init__(self):
        self.build = Gtk.Builder()
        self.build.add_from_file("ui/locacar_hora_diaria.glade")
        self.window_hora_diaria = self.build.get_object("window_op_hora_diaria")
        self.list_store_flags = self.build.get_object("list_store_flags")
        self.build.connect_signals(
            {
                "gtk_main_quit": Gtk.main_quit,
                "on_btn_loc_hora_button_press_event": self.on_btn_loc_hora_button_press_event,
                "on_btn_loc_diaria_button_press_event": self.on_btn_loc_diaria_button_press_event,
            }
        )
        self.codigos_ddd = ["+93"	 Afeganistão	Ásia,
+27	 África do Sul	África,
+355	 Albânia	Europa,
+49	 Alemanha	Europa,
+376	 Andorra	Europa,
+244	 Angola	África,
+1	 Anguilla	América Central,
+1	 Antígua e Barbuda	América Central,
+599	 Antilhas Holandesas	América Central,
+966	 Arábia Saudita	Ásia
+213	 Argélia	África
+54	 Argentina	América do Sul
+374	 Armênia	Ásia
+297	 Aruba	América Central
+247	Flag of Ascension Island.svg Ascensão	África
+61	 Austrália	Oceania
+43	 Áustria	Europa
+994	 Azerbaijão	Ásia
+1	 Bahamas	América Central
+880	 Bangladesh	Ásia
+1	 Barbados	América Central
+973	 Bahrein	Ásia
+32	 Bélgica	Europa
+501	 Belize	América Central
+229	 Benim	África
+1	 Bermudas	América Central
+375	 Bielorrússia	Europa
+591	 Bolívia	América do Sul
+387	 Bósnia e Herzegovina	Europa
+267	 Botswana	África
+55	 Brasil	América do Sul
+673	 Brunei	Ásia
+359	 Bulgária	Europa
+226	 Burkina Faso	África
+257	 Burundi	África
+975	 Butão	Ásia
+238	 Cabo Verde	África
+237	 Camarões	África
+855	 Camboja	Ásia
+1	 Canadá	América do Norte
+7	 Cazaquistão	Ásia
+235	 Chade	África
+56	 Chile	América do Sul
+86	 República Popular da China	Ásia
+357	 Chipre	Europa
+57	 Colômbia	América do Sul
+269	 Comores	África
+242	 Congo-Brazzaville	África
+243	 Congo-Kinshasa	África
+850	 Coreia do Norte	Ásia
+82	 Coreia do Sul	Ásia
+225	 Costa do Marfim	África
+506	 Costa Rica	América Central
+385	 Croácia	Europa
+53	 Cuba	América Central
+45	 Dinamarca	Europa
+253	 Djibuti	África
+1	 Dominica	América Central
+20	 Egipto	África/Ásia
+503	 El Salvador	América Central
+971	 Emirados Árabes Unidos	Ásia
+593	 Equador	América do Sul
+291	 Eritreia	África
+421	 Eslováquia	Europa
+386	 Eslovénia	Europa
+34	 Espanha	Europa
+1	 Estados Unidos	América do Norte
+372	 Estónia	Europa
+251	 Etiópia	África
+679	 Fiji	Oceania
+63	 Filipinas	Ásia
+358	 Finlândia	Europa
+33	 França	Europa
+241	 Gabão	África
+220	 Gâmbia	África
+233	 Gana	África
+995	 Geórgia	Ásia
+350	 Gibraltar	Europa
+1	 Granada	América Central
+30	 Grécia	Europa
+299	 Groenlândia	América do Norte
+590	 Guadalupe	América Central
+671	 Guam	Oceania
+502	 Guatemala	América Central
+592	 Guiana	América do Sul
+594	 Guiana Francesa	América do Sul
+224	 Guiné	África
+245	 Guiné-Bissau	África
+240	 Guiné Equatorial	África
+509	 Haiti	América Central
+504	 Honduras	América Central
+852	 Hong Kong	Ásia
+36	 Hungria	Europa
+967	 Iêmen	Ásia
+1	 Ilhas Cayman	América Central
+672	 Ilha Christmas	Oceania
+672	 Ilhas Cocos	Oceania
+682	 Ilhas Cook	Oceania
+298	 Ilhas Féroe	Europa
+672	 Ilha Heard e Ilhas McDonald	Oceania
+960	 Maldivas	Ásia
+500	 Ilhas Malvinas	América do Sul
+1	 Ilhas Marianas do Norte	Oceania
+692	 Ilhas Marshall	Oceania
+672	 Ilha Norfolk	Oceania
+677	 Ilhas Salomão	Oceania
+1	 Ilhas Virgens Americanas	América Central
+1	 Ilhas Virgens Britânicas	América Central
+91	 Índia	Ásia
+62	 Indonésia	Ásia/Oceania
+98	 Irã	Ásia
+964	 Iraque	Ásia
+353	 Irlanda	Europa
+354	 Islândia	Europa
+972	 Israel	Ásia
+39	 Itália	Europa
+1	 Jamaica	América Central
+81	 Japão	Ásia
+962	 Jordânia	Ásia
+686	 Kiribati	Oceania
+383	 Kosovo	Europa
+965	 Kuwait	Ásia
+856	 Laos	Ásia
+266	 Lesoto	África
+371	 Letônia	Europa
+961	 Líbano	Ásia
+231	 Libéria	África
+218	 Líbia	África
+423	 Liechtenstein	Europa
+370	 Lituânia	Europa
+352	 Luxemburgo	Europa
+853	 Macau	Ásia
+389	 República da Macedônia	Europa
+261	 Madagascar	África
+60	 Malásia	Ásia
+265	 Malawi	África
+223	 Mali	África
+356	 Malta	Europa
+212	 Marrocos	África
+596	 Martinica	América Central
+230	 Maurícia	África
+222	 Mauritânia	África
+269	 Mayotte	África
+52	 México	América do Norte
+691	 Estados Federados da Micronésia	Oceania
+258	 Moçambique	África
+373	 Moldávia	Europa
+377	 Mônaco	Europa
+976	 Mongólia	Ásia
+382	 Montenegro	Europa
+1	 Montserrat	América Central
+95	 Myanmar	Ásia
+264	 Namíbia	África
+674	 Nauru	Oceania
+977	 Nepal	Ásia
+505	 Nicarágua	América Central
+227	 Níger	África
+234	 Nigéria	África
+683	 Niue	Oceania
+47	 Noruega	Europa
+687	 Nova Caledônia	Oceania
+64	 Nova Zelândia	Oceania
+968	 Omã	Ásia
+31	 Países Baixos	Europa
+680	 Palau	Oceania
+970	 Palestina	Ásia
+507	 Panamá	América Central
+675	 Papua-Nova Guiné	Oceania
+92	 Paquistão	Ásia
+595	 Paraguai	América do Sul
+51	 Peru	América do Sul
+689	 Polinésia Francesa	Oceania
+48	 Polônia	Europa
+1	 Porto Rico	América Central
+351	 Portugal	Europa
+974	 Qatar	Ásia
+254	 Quênia	África
+996	 Quirguistão	Ásia
+44	 Reino Unido	Europa
+236	 República Centro-Africana	África
+1	 República Dominicana	América Central
+420	 República Tcheca	Europa
+262	 Reunião	África
+40	 Romênia	Europa
+250	 Ruanda	África
+7	 Rússia	Europa/Ásia
+212	 Saara Ocidental	África
+685	 Samoa	Oceania
+1	 Samoa Americana	Oceania
+290	 Santa Helena (território)	África
+1	 Santa Lúcia	América Central
+1	 São Cristóvão e Nevis	América Central
+378	 São Marinho	Europa
+508	 Saint-Pierre e Miquelon	América do Norte
+239	 São Tomé e Príncipe	África
+1	 São Vicente e Granadinas	América Central
+248	 Seicheles	África
+221	 Senegal	África
+232	 Serra Leoa	África
+381	 Sérvia	Europa
+65	 Singapura	Ásia
+963	 Síria	Ásia
+252	 Somália	África
+94	 Sri Lanka	Ásia
+268	 Suazilândia	África
+249	 Sudão	África
+211	 Sudão do Sul	África
+46	 Suécia	Europa
+41	 Suíça	Europa
+597	 Suriname	América do Sul
+992	 Tadjiquistão	Ásia
+66	 Tailândia	Ásia
+886	 República da China	Ásia
+255	 Tanzânia	África
+246	 Território Britânico do Oceano Índico	África
+670	 Timor-Leste	Ásia
+228	 Togo	África
+690	 Tokelau	Oceania
+676	 Tonga	Oceania
+1	 Trinidad e Tobago	América Central
+216	 Tunísia	África
+1	 Turcas e Caicos	América Central
+993	 Turquemenistão	Ásia
+90	 Turquia	Ásia//Europa
+688	 Tuvalu	Oceania
+380	 Ucrânia	Europa
+256	 Uganda	África
+598	 Uruguai	América do Sul
+998	 Uzbequistão	Ásia
+678	 Vanuatu	Oceania
+379	 Vaticano	Europa
+58	 Venezuela	América do Sul
+84	 Vietnã	Ásia
+681	 Wallis e Futuna	Oceania
+260	 Zâmbia	África
+263]
        self.window_hora_diaria.show()
    
    def on_btn_loc_hora_button_press_event(self, widget, event):
        pass
    
    def on_btn_loc_diaria_button_press_event(self, widget, event):
        pass


if __name__ == "__main__":
    app = OpcaoHoraDiaria()
    Gtk.main()