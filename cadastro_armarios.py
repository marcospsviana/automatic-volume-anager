import gi


from controllers import Management
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk, Gtk


class MainWindowCad:
    def __init__(self, *args, **kwargs):
        self.gtk_style()
        builder = Gtk.Builder()
        builder.add_from_file('ui/cadastros_armarios.glade')
        builder.connect_signals(
            {
                'gtk_main_quit': Gtk.main_quit,
                'on_btn_cadastrar_armario_button_press_event': self.on_btn_cadastrar_armario_button_press_event,
            }
        )

        self.window_cad = builder.get_object('cad_armarios_window')
        self.combo_classe = builder.get_object('combobox_classe')
        # self.combo_classe.set_wrap_width(10)
        self.combo_coluna = builder.get_object('combobox_coluna')
        # self.combo_coluna.set_wrap_width(10)
        self.combo_nivel = builder.get_object('combobox_nivel')
        # self.combo_nivel.set_wrap_width(10)
        self.combo_terminal = builder.get_object('combobox_terminal')
        self.combo_terminal.set_wrap_width(10)

        self.btn_cadastrar = builder.get_object('btn_cadastrar_armario')
        self.lbl_resultado = builder.get_object('lbl_resultado')
        self.btn_cadastrar.connect('clicked', self.on_btn_cadastrar_armario_button_press_event)
        self.CLASSES = ['A', 'B', 'C', 'D']
        self.NIVEIS = [
            'SUPERIOR',
            'INFERIOR',
            'SUPERIOR DIREITA',
            'SUPERIOR ESQUERDA',
            'INFERIOR DIREITA',
            'INFERIOR ESQUERDA',
        ]
        self.COLUNAS = list(map(lambda x: x, range(1, 17)))
        self.TERMINAIS = [
            '',
            'CBS',
        ]
        self.PORTAS = list(map(lambda x: x, range(1, 101)))
        PORTAS_ALFA = ['A0', 'A1', 'A2', 'A3', 'A4']
        for ports, i in zip(PORTAS_ALFA, range(len(PORTAS_ALFA))):
            self.PORTAS.insert(i, ports)

        self.REGISTROS = []
        self.COMPARTIMENTOS = [
            'A01',
            'A02',
            'A03',
            'A04',
            'A05',
            'A06',
            'A07',
            'A08',
            'A09',
            'A10',
            'A11',
            'A12',
            'A13',
            'A14',
            'A15',
            'A16',
            'A17',
            'A18',
            'A19',
            'A20',
            'A21',
            'A22',
            'A23',
            'A24',
            'A25',
            'A26',
            'A27',
            'A28',
            'A29',
            'A30',
            'A31',
            'A32',
            'A33',
            'A34',
            'A35',
            'A36',
            'A37',
            'A38',
            'A39',
            'A40',
            'A41',
            'A42',
            'A43',
            'A44',
            'A45',
            'A46',
            'A47',
            'A48',
            'A49',
            'A50',
            'B01',
            'B02',
            'B03',
            'B04',
            'B05',
            'B06',
            'B07',
            'B08',
            'B09',
            'B10',
            'B11',
            'B12',
            'B13',
            'B14',
            'B15',
            'B16',
            'B17',
            'B18',
            'B19',
            'B20',
            'B21',
            'B22',
            'B23',
            'B24',
            'B25',
            'B26',
            'B27',
            'B28',
            'B29',
            'B30',
            'B31',
            'B32',
            'B33',
            'B34',
            'B35',
            'B36',
            'B37',
            'B38',
            'B39',
            'B40',
            'B41',
            'B42',
            'B43',
            'B44',
            'B45',
            'B46',
            'B47',
            'B48',
            'B49',
            'B50',
            'C01',
            'C02',
            'C03',
            'C04',
            'C05',
            'C06',
            'C07',
            'C08',
            'C09',
            'C10',
            'C11',
            'C12',
            'C13',
            'C14',
            'C15',
            'C16',
            'C17',
            'C18',
            'C19',
            'C20',
            'C21',
            'C22',
            'C23',
            'C24',
            'C25',
            'C26',
            'C27',
            'C28',
            'C29',
            'C30',
            'C31',
            'C32',
            'C33',
            'C34',
            'C35',
            'C36',
            'C37',
            'C38',
            'C39',
            'C40',
            'C41',
            'C42',
            'C43',
            'C44',
            'C45',
            'C46',
            'C47',
            'C48',
            'C49',
            'D01',
            'D02',
            'D03',
            'D04',
            'D05',
            'D06',
            'D07',
            'D08',
            'D09',
            'D10',
            'D11',
            'D12',
            'D13',
            'D14',
            'D15',
            'D16',
            'D17',
            'D18',
            'D19',
            'D20',
            'D21',
            'D22',
            'D23',
            'D24',
            'D25',
            'D26',
            'D27',
            'D28',
            'D29',
            'D30',
            'D31',
            'D32',
            'D33',
            'D34',
            'D35',
            'D36',
            'D37',
            'D38',
            'D39',
            'D40',
            'D41',
            'D42',
            'D43',
            'D44',
            'D45',
            'D46',
            'D47',
            'D48',
            'D49',
            'D50',
        ]

        self.terminais = Gtk.ListStore(str)
        for t in self.TERMINAIS:
            self.terminais.append([t])
        for c in self.CLASSES:
            for p in self.PORTAS:
                self.REGISTROS.append(c + str(p))
        self.registros = Gtk.ListStore(str)
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
        self.combobox_compartimentos = builder.get_object('combobox_compartimentos')
        self.combobox_compartimentos.set_wrap_width(10)
        self.combobox_compartimentos.set_model(self.compartimentos)
        self.combobox_portas = builder.get_object('combobox_portas')
        self.combobox_portas.set_wrap_width(10)
        self.combobox_portas.set_model(self.portas_arduino)
        self.combo_terminal.set_model(self.terminais)

        # self.combobox_numeracao.connect("changed", self.on_change_combobox_numeracao)
        self.window_cad.show()

    def on_btn_cadastrar_armario_button_press_event(self, event):

        self.classe = self.CLASSES[self.combo_classe.get_active()]   # obter o conteú e não o indice da lista do combobox
        print(self.classe)
        self.nivel = self.NIVEIS[self.combo_nivel.get_active()]
        self.coluna = self.COLUNAS[self.combo_coluna.get_active()]
        self.terminal = self.TERMINAIS[self.combo_terminal.get_active()]
        compartimentos = self.COMPARTIMENTOS[self.combobox_compartimentos.get_active()]
        portas_arduino = self.PORTAS[self.combobox_portas.get_active()]
        print(self.classe, self.nivel, self.coluna, self.terminal)
        manager = Management()
        result = manager.cad_armarios(
            self.classe,
            self.terminal,
            self.coluna,
            self.nivel,
            portas_arduino,
            compartimentos,
        )
        print('reuslt cad armarios', result)
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
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )


if __name__ == '__main__':
    app = MainWindowCad()
    Gtk.main()
