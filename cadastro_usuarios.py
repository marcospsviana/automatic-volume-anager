import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf, GObject
import datetime
import time
from time import sleep
import calendar
import string
from controllers import Management
import PIL
from PIL import Image
from decimal import Decimal

class CadastroUsuarios(object):
    def __init__(self, *args):
        global TAXA_HORA_A, TAXA_HORA_B, TAXA_HORA_C, TAXA_HORA_D, DDD
        global TAXA_DIARIA_A, TAXA_DIARIA_B, TAXA_DIARIA_C, TAXA_DIARIA_D
        self.senha = ''
        TAXA_DIARIA_A = 37.5
        TAXA_DIARIA_B = 24.5
        TAXA_DIARIA_C = 14.5
        TAXA_DIARIA_D = 9.0
        TAXA_HORA_A = 2.10
        TAXA_HORA_B = 1.56
        TAXA_HORA_C = 1.05
        TAXA_HORA_D = 0.6
        teste = args
        print(teste)
        self.tempo_locacao = args[0]
        self.classe = args[1][0]
        self.language = args[2]
        print(self.classe)
        print(self.tempo_locacao)
        print(self.language)
        self.alfa = list(string.ascii_uppercase) # alfabeto para gerar o teclado
        self.num = list(map(lambda x: x, range(10))) # números para o teclado numérico
        self.entry = ""
        self.dia = self.hora = self.minuto = 0
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
            "on_btn_window_payment_wait_button_press_event": self.on_btn_window_payment_wait_button_press_event,
            "on_button_fechar_armario_button_press_event": self.on_button_fechar_armario_button_press_event,
            #"on_btn_credito_button_press_event": self.on_btn_credito_button_press_event,
            #"on_btn_debito_button_press_event": self.on_btn_debito_button_press_event,
            #"on_btn_cancelar_button_press_event": self.on_btn_cancelar_button_press_event
        })
        self.builder.add_from_file("ui/cadastro_usuario.glade")
        self.window_cadastro_usuario = self.builder.get_object("window_cadastro_usuario")
        self.window_payment = self.builder.get_object("window_payment_wait")
        self.window_entrada_dados = self.builder.get_object("window_entrada_dados")
        self.window_entrada_numeros = self.builder.get_object("window_entrada_numeros")
        self.window_select_cartao = self.builder.get_object("window_select_cartao")
        self.dialog_retorno_cadastro = self.builder.get_object("dialog_retorno_cadastro")
        self.dialog_message_preencher_campos = self.builder.get_object("dialog_message_preencher_campos")
        self.dialog_instrucao_fecha_armario = self.builder.get_object(
            "dialog_instrucao_fecha_armario")
        self.window_conclusao  = self.builder.get_object("window_conclusao")
        

        """ =================LABELS ====================="""

        self.label_nome = self.builder.get_object("label_nome")
        self.label_email = self.builder.get_object("label_email")
        self.label_telefone = self.builder.get_object("label_celular")
        self.label_quantidade_diaria = self.builder.get_object("label_quantidade_diaria")
        self.label_quantidade_horas = self.builder.get_object("label_quantidade_horas")
        #self.label_quantidade_minutos = self.builder.get_object("label_quantidade_minutos")
        self.label_total = self.builder.get_object("label_total")
        self.label_valor_da_locacao = self.builder.get_object("label_valor_da_locacao")
        
        self.label_senha = self.builder.get_object("label_senha")
        self.label_compartimento_titulo = self.builder.get_object("label_compartimento_titulo")
        self.label_compartimento = self.builder.get_object("label_compartimento")
        self.label_inicio_locacao_titulo = self.builder.get_object("label_inicio_locacao_titulo")
        self.label_date_inicio_locacao = self.builder.get_object("label_date_inicio_locacao")
        self.label_hour_inicio_locacao = self.builder.get_object("label_hour_inicio_locacao")
        self.label_minute_inicio_locacao = self.builder.get_object("label_minute_inicio_locacao")
        self.label_fim_locacao_titulo = self.builder.get_object("label_fim_locacao_titulo")
        self.label_date_fim_locacao = self.builder.get_object("label_date_fim_locacao")
        self.label_hour_fim_locacao = self.builder.get_object("label_hour_fim_locacao")
        self.label_minute_fim_locacao = self.builder.get_object("label_minute_fim_locacao")
        self.label_message_envio_email = self.builder.get_object("label_message_envio_email")
        self.label_senha = self.builder.get_object("label_senha")
        

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
        self.label_aguarde_pagamento = self.builder.get_object("label_aguarde_pagamento")

        """ ================FIM LABELS==================="""
        self.spinner = self.builder.get_object("spinner")

        """ ================= ENTRYS ===================="""

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
        self.btn_confirmar = self.builder.get_object("btn_confirmar")
        self.btn_confirmar.connect("button_press_event", self.on_btn_confirmar_button_press_event)
        self.btn_retornar = self.builder.get_object("btn_retornar")
        self.btn_retornar.connect("button_press_event", self.on_btn_retornar_button_press_event)
        self.btn_limpar_entrada_numeros = self.builder.get_object("btn_limpar_entrada_numeros")
        self.btn_limpar_entrada_numeros.connect("button_press_event", self.on_btn_limpar_entrada_numeros_button_press_event)

        #self.btn_finalizar_sessao = self.builder.get_object("btn_finalizar_sessao")

        self.btn_window_payment_wait = self.builder.get_object("btn_window_payment_wait")
        self.btn_window_payment_wait.connect("button_press_event", self.on_btn_window_payment_wait_button_press_event)

        " ----------- BOTOES ENTRADA_DADOS --------------- "
        self.btn_confirmar_entrada_dados = self.builder.get_object("btn_confirmar_entrada_dados")
        self.btn_confirmar_entrada_dados.connect("button_press_event", self.on_btn_confirmar_entrada_dados_button_press_event)
        self.btn_retornar_entrada_dados = self.builder.get_object("btn_retornar_entrada_dados")
        self.btn_retornar_entrada_dados.connect("button_press_event", self.on_btn_retornar_entrada_dados_button_press_event)
        self.btn_backspace = self.builder.get_object("btn_backspace")
        self.btn_backspace.connect("button_press_event", self.on_btn_backspace_button_press_event)

        """ ================FIM BOTOES==================== """
        " ----------- BOTOES TELA ENTRADA NUMEROS --------- "
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

        """ =================== BOTÕES DIALOGOS ===================="""
        self.btn_ok_dialog_retorno_cadastro = self.builder.get_object("btn_ok_dialog_retorno_cadastro")
        self.btn_ok_dialog_retorno_cadastro.connect("button_press_event", self.on_btn_ok_dialog_retorno_cadastro_pressed)
        self.btn_dialog_preencher_campos = self.builder.get_object("btn_dialog_preencher_campos")
        self.btn_dialog_preencher_campos.connect("button_press_event", self.on_btn_dialog_preencher_campos_pressed_event)
        self.btn_finalizar_sessao = self.builder.get_object("btn_finalizar_sessao")
        self.btn_finalizar_sessao.connect("button_press_event", self.on_btn_finalizar_sessao_button_press_event)
        self.button_fechar_armario = self.builder.get_object(
            "button_fechar_armario")
        self.button_fechar_armario.connect(
            "button_press_event", self.on_button_fechar_armario_button_press_event)
        # ======================== BOTOES TELA OPCAO CARTAO ======================
        self.btn_credito = self.builder.get_object("btn_credito")
        self.btn_credito.connect("button-press-event", self.on_btn_credito_button_press_event)
        self.btn_debito = self.builder.get_object("btn_debito")
        self.btn_debito.connect("button-press-event", self.on_btn_debito_button_press_event)
        self.btn_cancelar_escolha = self.builder.get_object("btn_cancelar_escolha")
        self.btn_cancelar_escolha.connect("button-press-event", self.on_btn_cancelar_button_press_event)

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
        """========== fim elementos do teclado  """
        """ ========= lista combobox ========= """
       
        
        self.combobox_flags_ddd = self.builder.get_object("combobox_flags_ddd")
        self.combobox_flags_ddd.set_wrap_width(12)
        
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
        
        
        
    

        if self.tempo_locacao == "diaria":
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
            self.btn_limpar_quantidade_diaria.hide()
        
        if self.language == "pt_BR":
            self.label_aguarde_pagamento.set_text("AGUARDE PAGAMENTO")
            self.label_nome.set_text("NOME")
            self.label_telefone.set_text("CELULAR")
            self.label_quantidade_diaria.set_text("QUANTIDADE\n DIÁRIA") #daily amount
            self.label_quantidade_horas.set_text("QUANTIDADE\n HORAS") #quantity of hours
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
            self.label_instrucao.set_text("""Após guardar todo o volume necessário, \n
                                           empurre a porta sem forçar até encostar na trava,\n 
                                           depois para finalizar clique no botão abaixo com nome: FECHAR ARMÁRIO.\n
                                           Observação: A responsabilidade de fechar o armário é do usuário,\n
                                           caso esqueça de fechá-lo a empresa não se responsabilizará por perdas!"""
                                           )
            
        elif self.language == "en_US":
            self.label_aguarde_pagamento.set_text("WAIT FOR PAYMENT")
            self.label_nome.set_text("NAME")
            self.label_telefone.set_text("PHONE")
            self.label_quantidade_diaria.set_text("QUANTITY\n DAYS") 
            self.label_quantidade_horas.set_text("QUANTITY\n HOURS") 
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
            self.label_instrucao.set_text("""After saving all the required volume,\n
                                            push the door without force until it touches the lock,\n
                                            then to finish click the button below with name: CLOSET CLOSER.\n
                                            Note: It is the responsibility of the user to close the cabinet,\n
                                            if you forget to close it the company will not be responsible for any losses!"""
                                            )
        

         

        
        self.window_cadastro_usuario.fullscreen()
        self.window_cadastro_usuario.show()
    def on_btn_credito_button_press_event(self, event, args):
        self.send_tipo_cartao("CREDITO")
        sleep(0.5)
        
        

    def on_btn_debito_button_press_event(self, event, args):
        self.send_tipo_cartao("DEBITO")
        sleep(0.5)
        
        

    def on_btn_cancelar_button_press_event(self, event, args):
        self.window_select_cartao.hide()

    def send_tipo_cartao(self, tipo):
        print(tipo)
        total = "%.2f"%(self.valor_total)
        print("total para json", total)
        total = total.replace('.','')
        print("total para json formatado", total)
        with open("engine/paygoWeb/comprovantes/valor_venda.json", "w+") as f:
            f.write('\n{  \n\n')
            f.write('"TOTAL": "%s",  \n'%(total))
            f.write('"LANGUAGE": "%s",  \n'%(self.language))
            f.write('"PWINFO_CARDTYPE": "%s"  \n'%(tipo))
            f.write('\n}  \n')
        #self.wait_payment()
        self.window_select_cartao.hide()
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
        """if self.entry_minutos.get_text() == "":
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
        elif self.__quantidade_diaria == self.__quantidade_horas: #== self.__quantidade_minutos:
            if self.language == "pt_BR":
                self.label_message_preencher_campos.set_text("PREENCHA TODOS OS CAMPOS")
            elif self.language == "en_US":
                self.label_message_preencher_campos.set_text("FILL IN ALL FIELDS")
            self.dialog_message_preencher_campos.show()
        else:
            self.window_payment.show()
            self.__armario = self.classe
            print("locacao", self.__quantidade_diaria, self.__quantidade_horas, self.__quantidade_minutos)
            manager = Management()
            self.__result =  manager.locacao(self.__nome, self.__email, self.__telefone, self.__quantidade_diaria, self.__quantidade_horas, self.__quantidade_minutos, self.__armario, self.language, self.valor_total)
            count = 0
            #self.__result = self.__result[0]
            print("self.__result cadastro usuario ", self.__result[0])
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
                
                self.window_payment.hide()
                self.window_conclusao.show()
                self.window_cadastro_usuario.hide()
                
                self.id_armario = manager.localiza_id_armario(self.senha)
                return self.id_armario
                
                
            elif self.__result[0] == "armario da classe escolhida indisponível":
                if self.language == "pt_BR":
                    self.label_retorno_cadastro.set_text("tamanho de armario\n  escolhido indisponível")
                    self.dialog_retorno_cadastro.show()
                elif self.language == "en_US":
                    self.label_retorno_cadastro.set_text("chosen cabinet\n size unavailable")
                    self.dialog_retorno_cadastro.show()
        
    
    def on_btn_limpar_entrada_numeros_button_press_event(self, widget, event):
        self.entry_entrada_numeros.set_text("")

    def on_btn_backspace_button_press_event(self, widget, event):
        self.texto = self.entry_entrada_dados.get_text()
        self.texto = self.texto[:-1]
        self.entry_entrada_dados.set_text(self.texto)
        self.entry_entrada_dados.set_position(-1)
    def on_btn_finalizar_sessao_button_press_event(self, widget, event):
        self.window_conclusao.hide()
        self.window_payment.hide()
        self.dialog_instrucao_fecha_armario.show()
    
    def on_btn_dialog_preencher_campos_pressed_event(self, widget, event):
        self.dialog_message_preencher_campos.hide()

    def on_btn_ok_dialog_retorno_cadastro_pressed(self, widget, event):
        self.dialog_retorno_cadastro.hide()
        self.window_cadastro_usuario.destroy()

    def on_btn_confirmar_button_press_event(self, widget, event):
        #self.wait_payment()
        #self.window_select_cartao.show()
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
            
        self.window_select_cartao.show()   
        
    def on_btn_window_payment_wait_button_press_event(self, widget, event):
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
        """if self.entry_minutos.get_text() == "":
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
            print("self.__result cadastro usuario ", self.__result[0])
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
                self.window_payment.hide()
                self.id_armario = manager.localiza_id_armario(self.senha)
                return self.id_armario
                
                
            elif self.__result[0] == "armario da classe escolhida indisponível":
                if self.language == "pt_BR":
                    self.label_retorno_cadastro.set_text("tamanho de armario\n  escolhido indisponível")
                    self.dialog_retorno_cadastro.show()
                elif self.language == "en_US":
                    self.label_retorno_cadastro.set_text("chosen cabinet\n size unavailable")
                    self.dialog_retorno_cadastro.show()        


    def wait_payment(self):
        self.window_payment.show()
        if self.language == "pt_BR":
            self.label_entrada_numeros.set_text("QUANTIDADE DIÁRIA")
        elif self.language == "en_US":
            self.label_entrada_numeros.set_text("QUANTITY DAYS")
        
    def on_btn_retornar_button_press_event(self, widget, event):
        self.window_cadastro_usuario.hide()
        
    
    def on_entry_nome_button_press_event(self, widget, event):
        if self.language == "pt_BR":
            self.label_entrada_dados.set_text("NOME")
        elif self.language == "en_US":
            self.label_entrada_dados.set_text("NAME")
        self.window_entrada_dados.show()
        return (self.entry, self.label_entrada_dados)
    
    def on_entry_email_button_press_event(self, widget, event):
        self.label_entrada_dados.set_text("EMAIL")
        self.window_entrada_dados.show()
        return self.entry
    
    def on_entry_celular_button_press_event(self, widget, event):
        if self.language == "pt_BR":
            self.label_entrada_numeros.set_text("CELULAR")
        elif self.language == "en_US":
            self.label_entrada_numeros.set_text("PHONE")
        
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
        if self.label_entrada_numeros.get_text() == "CELULAR" or self.label_entrada_numeros.get_text() == "PHONE":
            self.ddd = self.combobox_flags_ddd.get_active()
            
            print("self ddd", self.ddd)
            self.entry_celular.set_text(str(DDD[self.ddd]) + " " +str(self.text_entrada))
            self.entry_celular.set_position(-1)
        elif self.label_entrada_numeros.get_text() == "QUANTIDADE DIÁRIA" or self.label_entrada_numeros.get_text() == "QUANTITY DAYS":
            
            self.entry_quantidade_diaria.set_text(self.text_entrada)
            print("entry qtd diaria ===>",self.entry_quantidade_diaria.get_text())
            self.entry_quantidade_diaria.set_position(-1)
            
        elif self.label_entrada_numeros.get_text() == "QUANTIDADE HORAS" or self.label_entrada_numeros.get_text() == "QUANTITY HOURS":
            self.entry_quantidade_horas.set_text(self.text_entrada)
            print("entry qtd horas ===>",self.entry_quantidade_horas.get_text())
            self.entry_quantidade_horas.set_position(-1)
        """elif self.label_entrada_numeros.get_text() == "QUANTIDADE MINUTOS":
            self.entry_minutos.set_text(self.text_entrada)
            self.entry_minutos.set_position(-1)"""
        
        
        self.dia = self.entry_quantidade_diaria.get_text() + ".0"
        self.dia = float(self.dia)
        
        self.hora = self.entry_quantidade_horas.get_text()
        self.hora = self.hora +".0"
        self.hora = float(self.hora) 
        
        self.minuto = 0.0
        
        if self.classe == "A":
            self.valor_total = ((self.dia * TAXA_DIARIA_A) + (self.hora * TAXA_HORA_A) + self.minuto * TAXA_HORA_A)
        elif self.classe == "B":
            self.valor_total = ((self.dia * TAXA_DIARIA_B) + (self.hora * TAXA_HORA_B) + self.minuto * TAXA_HORA_B)
        elif self.classe == "C":
            self.valor_total = ((self.dia * TAXA_DIARIA_C) + (self.hora * TAXA_HORA_C) + self.minuto * TAXA_HORA_c)
        elif self.classe == "D":
            self.valor_total = ((self.dia * TAXA_DIARIA_D) + (self.hora * TAXA_HORA_D) + self.minuto * TAXA_HORA_D)
        
        self.valor_total = float(Decimal(str(self.valor_total)).quantize(Decimal('1.00')))
        
        print("total para ver",self.valor_total)
        
        self.label_total.set_text("%.2f"%(self.valor_total))
        print("set label para ver","%.2f"%(self.valor_total))
        self.entry_entrada_numeros.set_text("")
        self.window_entrada_numeros.hide()
    
    def on_btn_retornar_entrada_numeros_button_press_event(self, widget, event):
        self.window_entrada_numeros.hide()
    
    def on_entry_entrada_numeros_button_press_event(self, widget):
        self.widget = widget
        self.value = self.widget.get_label()
        self.text_entrada = self.entry_entrada_numeros.get_text() + self.value
        self.entry_entrada_numeros.set_text(self.text_entrada)
        self.entry_entrada_numeros.set_position(-1)
    
    def on_button_fechar_armario_button_press_event(self, *args):
        print("args button fechar cadastro usuario", args)
        manager = Management()
        id_armario = manager.localiza_id_armario(self.senha)
        manager.fechar_armario(id_armario)
        self.dialog_instrucao_fecha_armario.hide()
        


if __name__ == "__main__":
    app = CadastroUsuarios()
    Gtk.main()


