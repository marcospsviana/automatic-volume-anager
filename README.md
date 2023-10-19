## Controle e gerenciamento de Armarios em GTK PyGObject, RaspberryPi e Arduino

Este é um projeto desenvolvido em python com GTK, aplicado em um raspberrypi com Ubuntu

#### problems and solutions
~~~
$ pip install pygobject 

$  ERROR: Could not build wheels for pygobject, which is required to install pyproject.toml-based projects

$ python3 -m pip install --no-use-pep517  pygobject

$ error: from _ctypes import Union, Structure, Array ImportError: libffi.so.7: cannot open shared object file: No such file or directory

$ sudo find /usr/lib -name "libffi.so*"

/usr/lib/libffi.so
/usr/lib/libffi.so.8.1.0
/usr/lib/libffi.so.8

$ sudo apt install libgirepository1.0-dev # resolve  ERROR: Failed building wheel for pygobject

$ sudo ln -s /usr/lib/libffi.so.8 /usr/lib/libffi.so.7
$ pip install PyGObject
Command '('pkg-config', '--print-errors', '--exists', 'gobject-introspection-1.0 >= 1.56.0')' returned non-zero exit status 1.
install gobject-introspection
~~~
### FLUXOGRAMA

![Alt text](/docs/image.png)

