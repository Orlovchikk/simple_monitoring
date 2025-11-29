# simple_monitoring

Мониторинг веб-приложения.

## Структура проекта 

```text
.
├── config.py
├── example.env
├── install.sh
├── main.py
├── pyproject.toml
├── README.md
├── server
│   ├── simple_server.py
│   └── simple_server.service
└── simple_monitoring.service
```

## Требования

- OS: Debian/Ubuntu
- Python ^3.10
- Root права

## Установка и запуск

1. Клонировать репозиторий:

    ```sh
    git clone https://github.com/Orlovchikk/simple_monitoring.git
    ```

2. Перейти в папку репозитория:

    ```sh
    cd simple_monitoring
    ```

3. Создать файл `.env` на подобии `example.env` и изменить под свои нужды:
    Для теста приложения можно пропустить этот шаг, будут использоватся переменные из `example.env`

    ```sh
    mv example.env .env
    vim .env
    ```

4. Выполнить сценарий `install.sh` с root правами:

    ```sh
    sudo bash install.sh
    ```

5. Мониторинг запущен, для проверки статуса выполнить команду:

    ```sh
    systemctl status -u simple_monitoring
    ```

## Конфигурация

Мониторинг настраивается через `.env` файл, который располагается в `/opt/simple_monitoring`

Параметры:

- `APP_URL` — Адрес для проверки.
- `CHECK_INTERVAL` — Частота проверок в секундах.
- `RESTART_COMMAND` — Команда для перезагруки отслеживаемого веб-приложения
- `TIMEOUT` — Время ожидания ответа от веб-приложения.
- `RESTART_WAIT_TIME` — Время ожидания загрузки веб-приложения после перезагрузки.

## Описание технического решения

- *Веб-сервер:* Flask приложение, работающее как simple_service.service.
- *Мониторинг:* Python-скрипт (main.py), работающий как simple_monitoring.service. В бесконечном цикле следит за URL. При status_code != 200 или исключении выполняет RESTART_COMMAND.
- *Деплой:* Poetry используется для отслеживания и изоляции зависимостей. Systemd отвечает за автозапуск и управление процессами.

## Мониторинг и логирование

Для просмотра статуса:

```sh
systemctl status simple_monitoring.service
```

Для просмотра логов:

```sh
journalctl -u simple_monitoring.service
```
