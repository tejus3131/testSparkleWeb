from .SparkleWeb import makeApp, setCss, setIndex, setJs, set_base_config


def makeServer(css, js, index):
    base_config = {
        "template": None,
        "title": None,
        "args": None,
        "reload": None,
        "cssDict":{},
        "jsDict":{},
        "index":None
    }
    app = makeApp(base_config)
    setCss(base_config, css)
    setJs(base_config, js)
    print(index)
    setIndex(base_config, index[0], index[1], index[2], index[3])
    set_base_config(base_config)
    return app