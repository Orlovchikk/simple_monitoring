#!/usr/bin/env bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

echo "Do you want to install test server to try the simple monitoring in work? (Y/N)"
read answer

source .env

mkdir -p /opt/simple_monitoring
cp *.py /opt/simple_monitoring
cp install.sh /opt/simple_monitoring
cp pyproject.toml /opt/simple_monitoring
cp simple_monitoring.service /opt/simple_monitoring

if [[ $answer =~ ^[Yy]$ ]]; then
    cp server/simple_server.py /opt/simple_monitoring
    cp server/simple_server.service /opt/simple_monitoring
fi

if [[ -f ".env" ]]; then
    cp .env /opt/simple_monitoring/
else
    echo ".env not found, using example.env instead"
    cp example.env /opt/simple_monitoring/.env
fi


curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"

cd /opt/simple_monitoring
poetry config virtualenvs.in-project true
poetry install
VENV_PATH=$(poetry env info --path)/bin/python

sed "s|{{VENV_PATH}}|$VENV_PATH|g" simple_monitoring.service > /etc/systemd/system/simple_monitoring.service

if [[ $answer =~ ^[Yy]$ ]]; then
    sed "s|{{VENV_PATH}}|$VENV_PATH|g" simple_server.service > /etc/systemd/system/simple_server.service
fi

systemctl daemon-reload
systemctl unmask simple_monitoring.service
systemctl enable --now simple_monitoring.service

if [[ $answer =~ ^[Yy]$ ]]; then
    systemctl unmask simple_server.service
    systemctl enable --now simple_server.service
fi

echo "Simple monitoring installed successfully"