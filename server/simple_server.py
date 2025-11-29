# Простое веб приложение на Flask, которое возвращает «Hello World!»
from flask import Flask

app = Flask(__name__)


# По пути "/" выдается страница «Hello World!»
@app.route("/")
def helloworld():
    return "Hello World!"


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
