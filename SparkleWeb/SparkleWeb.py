from flask import jsonify, render_template, request, render_template_string, Flask, Blueprint
from flask_cors import CORS
import json


'''

`SparkleWeb.Server`
~~~~
This is a class for creating an instance of Flask-based SparkleWeb server.
::
~~~~
`Directory Structure` =>
>>> .
... ├── main.py
... ├── static
... │   ├── Your_CSS_files.css
... │   ├── Your_JS_files.js
... ├── templates
... │   ├── Your_templates.html

::
~~~~

`Initilization` =>
>>> from SparkleWeb import Server
>>> app = Server()

::
~~~~
`Methods` =>
>>> app.setIndex()
>>> app.setCss()
>>> app.setJs()
>>> app.run()

'''



def makeApp(base_config) -> None:
    '''
    Constructor to initialize the server instance and set up the necessary configurations.
    '''
    app = Flask(__name__)
    CORS(app)
    app.jinja_env.filters['load'] = load
    app.add_url_rule('/', 'index', index, methods=['GET'])
    app.add_url_rule('/', 'response', response, methods=['POST'])

    indexPage = '''<!DOCTYPE html>
<html lang="en">

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://sparkleweb.vercel.app/static/script.js"></script>
<link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon">
<script>
    var siteData = {{ json_data| safe }};
    var start_data = {{ start_data| safe }}
    init(siteData.route, siteData.cssDict, siteData.jsDict);
    start(start_data.template, start_data.title, start_data.args, start_data.reload);
</script>
<link rel="stylesheet" href="https://sparkleweb.vercel.app/static/styles.css">
</head>

<body>
<div id="mainServerBody"></div>
</body>

</html>'''
    config(base_config, index=indexPage)

    return app

def setIndex(base_config, template:str , title:str | None = "Home", args:dict |None = {}, reload:list | None = []):
    '''
    `setIndex()`
    ~~~~
    Sets the base configuration for the starting page.
    ::
    ~~~~

    `Setting up the starting page` =>
    >>> app.setIndex("index.html")

    Parameters:
        template (str): The template to be used for the starting page.
        title (str, optional): The title of the starting page. Defaults to "Home".
        args (dict, optional): Arguments to be passed to the template. Defaults to {}.
        reload (list, optional): List of elements that should trigger a page reload. Defaults to [].
    '''
    base_config["template"] = template
    base_config["title"] = title
    base_config["args"] = args
    base_config["reload"] = reload

def setCss(base_config, cssDict:dict | None = {}):
    '''
    `setCss()`
    ~~~~
    Sets the CSS configuration for the server.
    ::
    ~~~~
    `Setting up the CSS` =>
    >>> cssDict = {
    ...     "mainCSS":"http://127.0.0.1:5300/static/main.css",
    ...     "extraCSS":"http://127.0.0.1:5300/static/extra.css"
    ... }
    >>> app.setCss(cssDict)
    '''
    base_config["cssDict"] = cssDict

def setJs(base_config, jsDict:dict | None = {}):
    '''
    `setJs()`
    ~~~~
    Sets the JavaScript configuration for the server.
    ::
    ~~~~
    `Setting up the JavaScript` =>
    >>> jsDict = {
    ...     "mainJS":"http://127.0.0.1:5300/static/main.js",
    ...     "extraJS":"http://127.0.0.1:5300/static/extra.js"
    ... }
    >>> app.setJs(jsDict)
    '''
    base_config["jsDict"] = jsDict

def config(base_config, **kwags):
    '''
    Configures the server with the provided key-value pairs.

    Parameters:
        **kwags (dict): Key-value pairs for configuring the server.
    '''
    for key in kwags:
        if key in base_config:
            base_config[key] = kwags[key]
        else:
            raise Exception(f"Invalid Config Key {key}")
        
def get_base_config():
    '''
    Returns the base configuration of the server.

    Returns:
        dict: The base configuration of the server.
    '''
    return base_config

def set_base_config(config):
    '''
    Sets the base configuration of the server.

    Parameters:
        base_config (dict): The base configuration of the server.
    '''
    global base_config
    base_config = config

def index():
    '''
    Renders the starting page of the server.

    Returns:
        str: The HTML content of the starting page.
    '''
    base_config = get_base_config()
    if base_config["template"] is None:
        return f'''<div style="text-align: center;">
<h1>Invalid Syntax</h1>
<br>
No Starting page set.<br>Set Starting page by using setIndex Function.
</div>'''
    siteData = {
        "route": request.base_url,
        "cssDict": base_config["cssDict"],
        "jsDict": base_config["jsDict"]
    }
    startData = {
        "template": base_config["template"],
        "title": base_config["title"],
        "args": base_config["args"],
        "reload": base_config["reload"]
    }
    return render_template_string(base_config["index"], json_data=json.dumps(siteData), start_data=json.dumps(startData))

def response():
    '''
    Handles the response from the server.

    Returns:
        Response: The JSON response containing the status, template, and other data.
    '''
    data = request.get_json()
    if data.get("request") == "page":
        response = jsonify({
            "status": "success",
            "title": data.get("title"),
            "template": render_template(data.get("template"), args=data.get("args")),
            "reloadRequired": data.get("reloadRequired")
        })
    elif data.get("request") == "section":
        return jsonify({
            "status": "success",
            "template": render_template(data.get("template"), args=data.get("args")),
            "reloadRequired": data.get("reloadRequired"),
            "title": data.get("title")
        })
    else:
        response = jsonify({
            "status": "error",
            "message": "Invalid Request"
        })
    return response

def load(requestType, **data):
    '''
    Loads a template or section using a JavaScript function.

    Parameters:
        requestType (str): Type of request (page or section).
        **data (dict): Additional data required for the request.

    Returns:
        str: JavaScript function to load the specified template or section.
    '''
    if requestType == "page":
        return 'loadPage({"request":"page", '+f'"template" : "{data["template"]}", "title" : "{data["title"]}", "args":{data["args"]},"reloadRequired" : {data["reload"]}'+'})'

    elif requestType == "section":
        return 'loadPage({"request":"section", '+f'"title" : "{data["title"]}", "template" : "{data["template"]}", "args":{data["args"]},"reloadRequired" : {data["reload"]}'+'}, body_id = '+f'"{data["target_id"]}")'

    elif requestType == "error":
        return 'loadPage({"request":"page", "template" : "error.html", "title" : "ERROR", "args":{"error": "' + data['error'] + '"},"reloadRequired" : [] }, "mainServerBody", "https://sparkleweb.vercel.app/error")'

    else:
        return 'loadPage({"request":"page", "template" : "error.html", "title" : "ERROR", "args":{"error": "Invalid Request Type :- request type must be page or section not ' + requestType + '"},"reloadRequired" : [] }, "mainServerBody", "https://sparkleweb.vercel.app/error")'
