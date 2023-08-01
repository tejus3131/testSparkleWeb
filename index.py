from SparkleWeb import Server
from datetime import datetime

server = Server()

server.setCss({
    "customCSS":"http://127.0.0.1:5300/static/custom.css",
    "bootstrap":"https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css",
    "Beginner":"https://fonts.googleapis.com/css2?family=Edu+SA+Beginner&display=swap"
    })

server.setJs({
    "customJS":"http://127.0.0.1:5300/static/custom.js",
    "bootstrap":"https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js"
    })

server.setIndex("start.html", 
                "SparkleWeb",
                {"time":datetime.now().isoformat()},
                ["customJS"])

if __name__ == "__main__":
    server.run()