#ID DA IMAGEM UBUNTU 16.04 i386
FROM i386/ubuntu:16.04
MAINTAINER Marcos Paulo 

COPY paygoWeb/ /paygoWeb
RUN apt update && apt-get install -y --no-install-recommends apt-utils

RUN apt-get install build-essential -y

#BIBLIOTECAS IMPORTANTES
RUN apt-get install zlib1g-dev -y
RUN apt-get install libncurses5-dev -y
RUN apt-get install libgdbm-dev -y
RUN apt-get install libnss3-dev -y
RUN apt-get install libssl-dev -y 
RUN apt-get install libreadline-dev -y 
RUN apt-get install libffi-dev wget -y
RUN apt-get install python3 -y

#RUN if [ python --version =! "" ]; \
    #then echo "python instalado"; \
    #else cd /tmp \#\\\\\
##&& wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tar.xz  \ 
    #&& tar -xf Python-3.7.2.tar.xz \
    #&&chmod a+x -R Python-3.7.2 \
    #&& cd Python-3.7.2  \
    #&& ./configure --enable-optmizations \
    #&& make -j 8 \
    #&& make install; \
    #fi;

#CRIANDO DIRETORIO QUE SERA MAPEADO 

RUN cd paygoWeb
#CMD ["python3.7", "/paygoWeb/paygoWeb.py"]



