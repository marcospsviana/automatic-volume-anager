docker pull 32bit/ubuntu

docker container ls -a



docker export paygoweb | gzip > paygoweb.gz

zcat paygoweb.gz | docker import - paygoweb


### EXECUTAR DENTRO DO DIRETORIO /coolbag/raspcontrol/engine
~~~
docker run -it -t -e TZ=America/Fortaleza --privileged --rm -v /paygoWeb:/paygoWeb paygoweb bash 
~~~
### ////MODO ANTIGO/////

### LOCALIZACAO DO DOCKER EM PAYGOWEB EM PATH DEFAULT PYTHON
docker run -it -t -e TZ=America/Fortaleza --privileged --name paygoweb -v /usr/lib/python3.8/site-packages/coolbagsafe_system/paygoWeb:/paygoWeb paygoweb bash


### CRIACAO DOCKER COM CONEXAO HOST REMOTO
#docker run -it --name mariadb_king  mariadb mysql --user='{USERNAME}' --password='{PASSWORD}' --host='{HOST}' BANCO \
docker run -i --name ubuntu --volume=/usr/lib/python3.8/site-packages/coolbagsafe_system:/coolbagsafe_system IMAGE /bin/bash

