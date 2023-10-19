### CONFIGURAÇOES BÁSIXAS PARA COMUNICAÇÃO SERIAL RASPBERRY PI 3 B+ E ARDUINO

Para configurar a serial é preciso editar o arquivo “inittab”, localizado em “/etc/inittab”. Para habilitar a serial deve-se comentar a linha “T0:23:respawn:/sbin/getty -L ttyAMA0 115200 vt100”. Para abrir este arquivo digite o seguinte comando no LX Terminal:
~~~
$ sudo nano /etc/inittab
~~~

Caso não se consiga encontrar este arquivo no sistema operacional da sua Raspberry PI, que foi  o meu caso, deve-se realizar o seguinte comando:
~~~
$ sudo nano /boot/config.txt
~~~

Quando abrir este arquivo acrescente no final a seguinte linha **“enable_uart=1”**.

Em seguida desabilite a serial com os seguintes comandos:
~~~
$ sudo systemctl stop serial-getty@ttyS0.service
$ sudo systemctl disable serial-getty@ttyS0.service
~~~
Em seguida execute o comando abaixo:
~~~
$ sudo nano /boot/cmdline.txt
~~~

E remova a linha **“console=serial0,115200”**, salve o arquivo e realize o “Reboot” da Raspberry PI.

Pronto, a Raspberry PI está configurada e pronta para se utilizar as portas seriais com protocolo UART.