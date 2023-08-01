from SparkleWeb import makeServer
from datetime import datetime

Css = {
    "customCSS":"http://127.0.0.1:5000/static/custom.css",
    "bootstrap":"https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css",
    "Beginner":"https://fonts.googleapis.com/css2?family=Edu+SA+Beginner&display=swap"
    }

Js = {
    "customJS":"http://127.0.0.1:5000/static/custom.js",
    "bootstrap":"https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js"
    }

Index = ["start.html", 
                "SparkleWeb",
                {"time":datetime.now().isoformat()},
                ["customJS"]]

server = makeServer(Css, Js, Index)


if __name__ == "__main__":
    server.run(debug=True)