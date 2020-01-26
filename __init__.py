from raspcontrol.cadastro_usuarios import CadastroUsuarios
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, Gio, GdkPixbuf, GObject

import os
import locale
import gettext

__all__ = ["engine", "controllers", "gui", "raspcontrol"]

current_locale, encoding = locale.getdefaultlocale()
locale_path = "../raspcontrol/locale" + current_locale + "/LC_MESSAGES/"
t = gettext.translation("main_raspcontrol", locale_path, [current_locale])
t.install()
_ = t.ugettext
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

