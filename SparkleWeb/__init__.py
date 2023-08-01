from .SparkleWeb import Server


def makeServer(css, js, index):
    app = Server()
    app.setCss(css)
    app.setJs(js)
    print(index)
    app.setIndex(index[0], index[1], index[2], index[3])
    return app.app