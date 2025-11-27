# Простое веб приложение на Flask, которое возвращает «Hello World!»
from flask import Flask

# Библиотека для чтения переменных окружения из .env
from dotenv import load_dotenv
import os

load_dotenv()
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

app = Flask(__name__)


# По пути "/" будет выдаватся страница с «Hello World!»
@app.route("/")
def helloworld():
    return "Hello World!"


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
