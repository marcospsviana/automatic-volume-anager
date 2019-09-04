import os
import locale
import gettext
__all__ = ["engine", "controllers", "gui"]


current_locale, encoding = locale.getdefaultlocale()
locale_path = "../raspcontrol/locale" + current_locale + "/LC_MESSAGES/"
t = gettext.translation("main_raspcontrol", locale_path, [current_locale])
t.install()
_ = t.ugettext