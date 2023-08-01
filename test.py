from SparkleWeb import Server

server = Server()

server.setCss({
    "customCSS":"http://127.0.0.1:5300/static/custom.css",
    "bootstrap":"https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css"
    })

server.setJs({
    "customJS":"http://127.0.0.1:5300/static/custom.js",
    "bootstrap":"https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js"
    })

server.setIndex("index.html")

if __name__ == "__main__":
    server.run(debug=True)