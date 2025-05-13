#!/usr/bin/env bash

echo "Instalando Google Chrome..."

apt-get update

# Instala bibliotecas necessárias
apt-get install -y wget unzip curl fonts-liberation libappindicator3-1 \
libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 libdbus-1-3 \
libgdk-pixbuf2.0-0 libnspr4 libnss3 libxcomposite1 libxdamage1 \
libxrandr2 xdg-utils

# Baixa o Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# Instala o Chrome
dpkg -i google-chrome-stable_current_amd64.deb || apt-get -fy install

# Verifica se funcionou
google-chrome --version

echo "Google Chrome instalado com sucesso."
