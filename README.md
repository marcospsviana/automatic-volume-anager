#### problems and solutions
```bash
$ pip install pygobject 

$  ERROR: Could not build wheels for pygobject, which is required to install pyproject.toml-based projects

$ python3 -m pip install --no-use-pep517  pygobject

$ error: from _ctypes import Union, Structure, Array ImportError: libffi.so.7: cannot open shared object file: No such file or directory

$ sudo find /usr/lib -name "libffi.so*"

/usr/lib/libffi.so
/usr/lib/libffi.so.8.1.0
/usr/lib/libffi.so.8


$ sudo ln -s /usr/lib/libffi.so.8 /usr/lib/libffi.so.7