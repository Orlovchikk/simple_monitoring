import requests
import logging
import time
import subprocess
import sys

from config import AppConfig

config = AppConfig()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


if __name__ == "__main__":
    logging.info(f"Starting monitor {config.APP_URL}")

    while True:
        try:
            result = requests.get(config.APP_URL, timeout=config.TIMEOUT)

            if result.status_code == 200:
                logging.info(f"Service {config.APP_URL} is OK")
            else:
                logging.warning(
                    f"Service responded with status code: {result.status_code}"
                )
            time.sleep(config.CHECK_INTERVAL)

        except Exception as e:
            logging.critical(
                f"Service failure. Tried to get {config.APP_URL} and got error: {e}"
            )
            logging.critical(f"Executing restart command {config.RESTART_COMMAND}")

            try:
                restart_process = subprocess.run(
                    config.RESTART_COMMAND,
                    shell=True,
                    capture_output=True,
                    timeout=30,
                )

                if restart_process.returncode == 0:
                    logging.info("Restart command success")
                else:
                    logging.error(f"Restart failed. stderr: {restart_process.stderr}")

            except subprocess.TimeoutExpired:
                logging.error("Restart command timed out")
            except Exception as e:
                logging.error(f"Failed to run restart command: {e}")

            time.sleep(config.CHECK_INTERVAL)
