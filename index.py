from SparkleWeb import Server
from flask import Flask

base = {
    "template": "index.html",
    "title": "Index",
    "args": {},
    "reloadRequired": []
}

cssDict = {
    "main": "http://127.0.0.1:5300/static/main.css"
}

jsDict = {
    "main": "http://127.0.0.1:5300/static/main.js"
}

flask_app = Flask(__name__)
app = Server(flask_app, base, cssDict, jsDict)

if __name__ == "__main__":
    flask_app.run(port=5300)