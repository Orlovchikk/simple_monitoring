import requests
import logging
import time
import subprocess
import sys

from config import AppConfig

config = AppConfig()

# Настройка формата логирования и записи в файл "monitoring.log"
logging.basicConfig(
    level=logging.INFO, format="%(levelname)s - %(message)s", stream=sys.stdout
)

if __name__ == "__main__":
    logging.info(f"Starting monitor {config.APP_URL}")

    # Бесконечный цикл проверки доступности веб-приложения
    while True:
        try:
            # Ожидание N секунд для проверки веб-приложения
            time.sleep(config.CHECK_INTERVAL)

            # Посылание запроса в веб-приложение
            result = requests.get(config.APP_URL, timeout=config.TIMEOUT)

            # Проверка статуса ответа веб-приложения
            if result.status_code == 200:
                # Ответ 200 = с приложением все ок
                logging.info(f"Service {config.APP_URL} is OK")
            else:
                # Любой другой ответ, значит что-то не так
                raise Exception(
                    f"Service responded with status code: {result.status_code}"
                )

        # Обработка ошибок, если веб-приложение не отвечает со статусом 200
        except Exception as e:
            # Вывод критической ошибки
            logging.critical(
                f"Service failure. Tried to get {config.APP_URL} and got error: {e}"
            )
            logging.critical(f"Executing restart command {config.RESTART_COMMAND}")

            try:
                # Перезапуск веб-приложения через команду RESTART_COMMAND
                restart_process = subprocess.run(
                    config.RESTART_COMMAND,
                    shell=True,
                    capture_output=True,
                    timeout=30,
                )

                # Проверка кода ответа команды перезапуска веб-приложения
                if restart_process.returncode == 0:
                    logging.info("Restart command success")
                else:
                    logging.error(f"Restart failed. stderr: {restart_process.stderr}")
                time.sleep(config.CHECK_INTERVAL)

            # Обработка ошибок, если веб-приложение не перезапускается
            except subprocess.TimeoutExpired:
                # Ошибка, если команда перезапуска не отвечала больше 30 секунд
                logging.error("Restart command timed out")
            except Exception as e:
                # Все остальные ошибки, которые могли произойти при перезапуске веб-приложения
                logging.error(f"Failed to run restart command: {e}")

            time.sleep(config.CHECK_INTERVAL)
