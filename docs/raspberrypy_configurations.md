## RAPBERRYPY CONFIG

Para que a Raspberry Pi consiga realizar a comunicação serial via protocolo UART é 
necessário configurar o pino 8 como porta transmissora (TX) e o pino 10 como porta receptora (RX).
 
Todos os comandos de configuração e para abrir arquivos serão realizados no “LX Terminal”
Para configurar a serial é preciso editar o arquivo “inittab”, localizado em “/etc/inittab”. Para habilitar a serial deve-se comentar a linha “T0:23:respawn:/sbin/getty -L ttyAMA0 115200 vt100”.

Para abrir este arquivo digite o seguinte comando no LX Terminal:
~~~shell
$ sudo leafpad /etc/inittab
~~~

Caso não se consiga encontrar este arquivo no sistema operacional da sua Raspberry PI, 
deve-se realizar o seguinte comando:
~~~shell
$ sudo leafpad /boot/config.txt
~~~

Quando abrir este arquivo acrescente no final a seguinte linha “enable_uart=1”

### *Em seguida desabilite a serial com os seguintes comandos*:

~~~shell
$ sudo systemctl stop serial-getty@ttyS0.service
~~~
~~~shell
$ sudo systemctl disable serial-getty@ttyS0.service
~~~

### *Em seguida execute o comando abaixo*:

~~~shell
$ sudo leafpad /boot/cmdline.txt
~~~
E remova a linha “console=serial0,115200”, 
salve o arquivo e realize o “Reboot” da Raspberry PI.

Comandos  - Raspberry PI - Python
---

~~~html
   Os comandos Python utilizados para realizar a comunicação serial na Raspberry Pi fazem parte da biblioteca “serial” da linguagem e devemos usar o comando import  para utilizá-lo nos nossos códigos. Como utilizar o comando import é demonstrado na seção “Código”.
 
serial.Serial(): É uma classe usada para configurar a porta serial. Cria uma instância para essa classe, no projeto ela recebe o nome de “serial”, mas poderia receber qualquer outro nome.
~~~
Sintaxe:
----
~~~
serial  = serial.Serial(Port, Baudrate)
~~~
**Parâmetros**: 

Port: nome da porta serial, no projeto é usado "/dev/ttyS0".

Baudrate: taxa de baudrate tais como 9600, 38400 e 115200.
 
**Exemplo**: 
~~~
ser = serial.Serial(“dev/ttyS0”, 9600)
 ~~~

read(): Essa função é usada para ler os dados na porta serial.
 
**Sintaxe**: 
~~~
received_data = ser.read(Size)
~~~

**Parâmetros**:

Size: número de bytes a serem lidos. O tamanho padrão 1.
 
**Retorno**:

Bytes lidos da porta serial.
 
inWaiting():  
*Verifica se ainda há bytes restantes no buffer de recepção da porta serial.*
 
**Sintaxe**: 
~~~
data_left = ser.inWainting()
~~~
 
**Retorno**:

#### *Retorna os bytes armazenados no buffer.*
 
write(): Essa função é usada para transmitir/enviar dados da porta serial.
 
**Sintaxe**:
~~~
ser.write(Data)
~~~
  

**Parâmetros**:

**Data**:

são os dados a serem enviados pela porta serial.
 
**Retorno**:

Número de bytes escritos/enviados.

~~~
close(): # Finaliza a transmissão serial.
~~~

