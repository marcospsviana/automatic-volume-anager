from controllers import Management
from gi.repository import Gtk, Gdk
import gi
gi.require_version('Gtk', '3.0')


class MainWindowCad():
    def __init__(self, *args, **kwargs):
        self.gtk_style()
        builder = Gtk.Builder()
        builder.add_from_file("ui/cadastros_armarios.glade")
        builder.connect_signals(
            {
                "gtk_main_quit": Gtk.main_quit,
                "on_btn_cadastrar_armario_button_press_event": self.on_btn_cadastrar_armario_button_press_event,
            }
        )

        self.window_cad = builder.get_object("cad_armarios_window")
        self.combo_classe = builder.get_object("combobox_classe")
        self.combo_coluna = builder.get_object("combobox_coluna")
        self.combo_nivel = builder.get_object("combobox_nivel")
        self.combo_terminal = builder.get_object("combobox_terminal")

        self.btn_cadastrar = builder.get_object("btn_cadastrar_armario")
        self.lbl_resultado = builder.get_object("lbl_resultado")
        self.btn_cadastrar.connect(
            "clicked", self.on_btn_cadastrar_armario_button_press_event)
        self.CLASSES = ["A", "B", "C", "D"]
        self.NIVEIS = ["SUPERIOR", "INFERIOR", "SUPERIOR DIREITA",
            "SUPERIOR ESQUERDA", "INFERIOR DIREITA", "INFERIOR ESQUERDA"]
        self.COLUNAS = list(map(lambda x: x, range(1, 17)))
        self.TERMINAIS = ["OTHON PALACE HOTEL", "PORTO FUTURO HOTEL"]
        self.PORTAS = list(map(lambda x: x, range(1, 101)))
        PORTAS_ALFA = ["A0", "A1", "A2", "A3", "A4"]
        for ports, i in zip(PORTAS_ALFA, range(len(PORTAS_ALFA))):
            self.PORTAS.insert(i, ports)

        self.REGISTROS = []
        self.COMPARTIMENTOS = [
            'A01', 'A02', 'A03', 'A04', 'A05', 'A06',
            'A07', 'A08', 'A09', 'A10', 'A11', 'A12',
            'A13', 'A14', 'A15', 'A16', 'A17', 'A18',
            'A19', 'A20', 'A21', 'A22', 'A23', 'A24',
            'A25', 'A26', 'A27', 'A28', 'A29', 'A30',
            'A31', 'A32', 'A33', 'A34', 'A35', 'A36',
            'A37', 'A38', 'A39', 'A40', 'A41', 'A42',
            'A43', 'A44', 'A45', 'A46', 'A47', 'A48',
            'A49', 'A50', 'A51', 'A52', 'A53', 'A54',
            'A55', 'A56', 'A57', 'A58', 'A59', 'A60',
            'A61', 'A62', 'A63', 'A64', 'A65', 'A66',
            'A67', 'A68', 'A69', 'A70', 'A71', 'A72',
            'A73', 'A74', 'A75', 'A76', 'A77', 'A78',
            'A79', 'A80', 'A81', 'A82', 'A83', 'A84',
            'A85', 'A86', 'A87', 'A88', 'A89', 'A90',
            'A91', 'A92', 'A93', 'A94', 'A95', 'A96',
            'A97', 'A98', 'A99', 'A100', 'B01', 'B02',
            'B03', 'B04', 'B05', 'B06', 'B07', 'B08',
            'B09', 'B10', 'B11', 'B12', 'B13', 'B14',
            'B15', 'B16', 'B17', 'B18', 'B19', 'B20',
            'B21', 'B22', 'B23', 'B24', 'B25', 'B26',
            'B27', 'B28', 'B29', 'B30', 'B31', 'B32',
            'B33', 'B34', 'B35', 'B36', 'B37', 'B38',
            'B39', 'B40', 'B41', 'B42', 'B43', 'B44',
            'B45', 'B46', 'B47', 'B48', 'B49', 'B50',
            'B51', 'B52', 'B53', 'B54', 'B55', 'B56',
            'B57', 'B58', 'B59', 'B60', 'B61', 'B62',
            'B63', 'B64', 'B65', 'B66', 'B67', 'B68',
            'B69', 'B70', 'B71', 'B72', 'B73', 'B74',
            'B75', 'B76', 'B77', 'B78', 'B79', 'B80',
            'B81', 'B82', 'B83', 'B84', 'B85', 'B86',
            'B87', 'B88', 'B89', 'B90', 'B91', 'B92',
            'B93', 'B94', 'B95', 'B96', 'B97', 'B98',
            'B99', 'B100', 'C01', 'C02', 'C03', 'C04',
            'C05', 'C06', 'C07', 'C08', 'C09', 'C10',
            'C11', 'C12', 'C13', 'C14', 'C15', 'C16',
            'C17', 'C18', 'C19', 'C20', 'C21', 'C22',
            'C23', 'C24', 'C25', 'C26', 'C27', 'C28',
            'C29', 'C30', 'C31', 'C32', 'C33', 'C34',
            'C35', 'C36', 'C37', 'C38', 'C39', 'C40',
            'C41', 'C42', 'C43', 'C44', 'C45', 'C46',
            'C47', 'C48', 'C49', 'C50', 'C51', 'C52',
            'C53', 'C54', 'C55', 'C56', 'C57', 'C58',
            'C59', 'C60', 'C61', 'C62', 'C63', 'C64',
            'C65', 'C66', 'C67', 'C68', 'C69', 'C70',
            'C71', 'C72', 'C73', 'C74', 'C75', 'C76',
            'C77', 'C78', 'C79', 'C80', 'C81', 'C82', 
            'C83', 'C84', 'C85', 'C86', 'C87', 'C88', 
            'C89', 'C90', 'C91', 'C92', 'C93', 'C94', 
            'C95', 'C96', 'C97', 'C98', 'C99', 'C100', 
            'D01', 'D02', 'D03', 'D04', 'D05', 'D06', 
            'D07', 'D08', 'D09', 'D10', 'D11', 'D12', 
            'D13', 'D14', 'D15', 'D16', 'D17', 'D18', 
            'D19', 'D20', 'D21', 'D22', 'D23', 'D24', 
            'D25', 'D26', 'D27', 'D28', 'D29', 'D30', 
            'D31', 'D32', 'D33', 'D34', 'D35', 'D36', 
            'D37', 'D38', 'D39', 'D40', 'D41', 'D42', 
            'D43', 'D44', 'D45', 'D46', 'D47', 'D48', 
            'D49', 'D50', 'D51', 'D52', 'D53', 'D54', 
            'D55', 'D56', 'D57', 'D58', 'D59', 'D60', 
            'D61', 'D62', 'D63', 'D64', 'D65', 'D66', 
            'D67', 'D68', 'D69', 'D70', 'D71', 'D72', 
            'D73', 'D74', 'D75', 'D76', 'D77', 'D78', 
            'D79', 'D80', 'D81', 'D82', 'D83', 'D84', 
            'D85', 'D86', 'D87', 'D88', 'D89', 'D90', 
            'D91', 'D92', 'D93', 'D94', 'D95', 'D96', 
            'D97', 'D98', 'D99', 'D100'
            ]

        
        for c in self.CLASSES:
            for p in self.PORTAS:
                self.REGISTROS.append(c+str(p))
        self.registros= Gtk.ListStore(str)
        for r in self.REGISTROS:
            self.registros.append([r])
        

        self.portas_arduino = Gtk.ListStore(str)
        self.compartimentos = Gtk.ListStore(str)
        for cp in self.COMPARTIMENTOS:
            self.compartimentos.append([cp])
        for p in self.PORTAS:
            self.portas_arduino.append([str(p)])

        """self.combobox_numeracao= builder.get_object("combobox_numeracao")
        self.combobox_numeracao.set_model(self.registros)"""
        self.combobox_compartimentos = builder.get_object("combobox_compartimentos")
        self.combobox_compartimentos.set_model(self.compartimentos)
        self.combobox_portas = builder.get_object("combobox_portas")
        self.combobox_portas.set_model(self.portas_arduino)

        # self.combobox_numeracao.connect("changed", self.on_change_combobox_numeracao)
        self.window_cad.show()

    def on_btn_cadastrar_armario_button_press_event(self, event):



        self.classe= self.CLASSES[self.combo_classe.get_active()] # obter o conteú e não o indice da lista do combobox
        print(self.classe)
        self.nivel= self.NIVEIS[self.combo_nivel.get_active()]
        self.coluna= self.COLUNAS[self.combo_coluna.get_active()]
        self.terminal= self.TERMINAIS[self.combo_terminal.get_active()]
        compartimentos = self.COMPARTIMENTOS[self.combobox_compartimentos.get_active()]
        portas_arduino = self.PORTAS[self.combobox_portas.get_active()]
        print(self.classe, self.nivel, self.coluna, self.terminal)
        manager= Management()
        result = manager.cad_armarios(self.classe, self.terminal, self.coluna, self.nivel, portas_arduino, compartimentos)
        print("reuslt cad armarios", result)
        self.lbl_resultado.set_text(str(result))
        print(compartimentos)
    
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
    app= MainWindowCad()
    Gtk.main()
