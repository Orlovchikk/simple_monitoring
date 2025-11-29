#!/usr/bin/env bash

# Проверка, что у сценария есть root права для исполнения команд
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# Получение ответа от пользователя, нужно ли устанавливать тестовый сервер для проверки мониторинга
echo "Do you want to install test server to try the simple monitoring in work? (Y/N)"
read answer

# Импорт переменных из .env
source .env

# Создание директории и копирование в нее файлов
mkdir -p /opt/simple_monitoring
cp *.py /opt/simple_monitoring
cp install.sh /opt/simple_monitoring
cp pyproject.toml /opt/simple_monitoring
cp simple_monitoring.service /opt/simple_monitoring

# Копирование файлов сервера, если пользователь ответил, что ему нужен сервер
if [[ $answer =~ ^[Yy]$ ]]; then
    cp server/simple_server.py /opt/simple_monitoring
    cp server/simple_server.service /opt/simple_monitoring
fi

# Проверка, что файл с переменными был создан, если нет, то используется тестовый файл
if [[ -f ".env" ]]; then
    cp .env /opt/simple_monitoring/
else
    echo ".env not found, using example.env instead"
    cp example.env /opt/simple_monitoring/.env
fi

# Установка poetry
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"

cd /opt/simple_monitoring
# Создание виртуального окружения и установка зависимостей
poetry config virtualenvs.in-project true
poetry install
VENV_PATH=$(poetry env info --path)/bin/python

# Замена placeholder'ов в .service, чтобы python запускался из виртуального окружения
sed "s|{{VENV_PATH}}|$VENV_PATH|g" simple_monitoring.service > /etc/systemd/system/simple_monitoring.service

if [[ $answer =~ ^[Yy]$ ]]; then
    sed "s|{{VENV_PATH}}|$VENV_PATH|g" simple_server.service > /etc/systemd/system/simple_server.service
fi

# Перезагрузка systemd, чтобы он увидел новые сервисы
systemctl daemon-reload
# Снятие защиты с файла
systemctl unmask simple_monitoring.service
# Выставление настройки, чтобы сервис включался при запуске системы и запустился прямо сейчас
systemctl enable --now simple_monitoring.service

if [[ $answer =~ ^[Yy]$ ]]; then
    # Снятие защиты с файла
    systemctl unmask simple_server.service
    # Выставление настройки, чтобы сервис включался при запуске системы и запустился прямо сейчас
    systemctl enable --now simple_server.service
fi

# Вывод сообщения об успешной установке
echo "Simple monitoring installed successfully"