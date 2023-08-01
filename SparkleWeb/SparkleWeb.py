from flask import jsonify, render_template, request, render_template_string, Flask, Blueprint
from flask_cors import CORS
import json
import requests
import os

class Server():
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
    def __init__(self) -> None:
        '''
        Constructor to initialize the server instance and set up the necessary configurations.
        '''
        root_directory = os.getcwd()
        self.app = Flask(__name__, template_folder=os.path.join(root_directory, "templates"), static_folder=os.path.join(root_directory, "static"))
        CORS(self.app)
        self.app.jinja_env.filters['load'] = self.load
        self.app.add_url_rule('/', 'index', self.index, methods=['GET'])
        self.app.add_url_rule('/', 'response', self.response, methods=['POST'])
        self.base_config = {
            "template": None,
            "title": None,
            "args": None,
            "reload": None,
            "cssDict":{},
            "jsDict":{},
            "index":None
        }
        try:
            host = "https://sparkleweb.vercel.app/index"
            indexPage = requests.post(host).text
        except Exception as e:
            indexPage = f'''<div style="text-align: center;">
    <h1>Invalid Syntax</h1>
    <br>
    {host} is not responding currently<br><br>{str(e)}
</div>'''
        self.config(index=indexPage)

    def setIndex(self, template:str , title:str | None = "Home", args:dict |None = {}, reload:list | None = []):
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
        self.base_config["template"] = template
        self.base_config["title"] = title
        self.base_config["args"] = args
        self.base_config["reload"] = reload

    def setCss(self, cssDict:dict | None = {}):
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
        self.base_config["cssDict"] = cssDict

    def setJs(self, jsDict:dict | None = {}):
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
        self.base_config["jsDict"] = jsDict

    def config(self, **kwags):
        '''
        Configures the server with the provided key-value pairs.

        Parameters:
            **kwags (dict): Key-value pairs for configuring the server.
        '''
        for key in kwags:
            if key in self.base_config:
                self.base_config[key] = kwags[key]
            else:
                raise Exception(f"Invalid Config Key {key}")

    def run(self, debug:bool | None=False, port:int | None=5300):
        '''
        `run()`
        ~~~~
        Runs the server.
        ::
        ~~~~

        `Running the server` =>
        >>> if __name__ == "__main__":
        ...     app.run()

        Parameters:
            debug (bool, optional): Enable or disable debug mode. Defaults to False.
            port (int, optional): The port number to run the server on. Defaults to 5300.
        '''
        self.app.run(debug=debug, port=port)

    def index(self):
        '''
        Renders the starting page of the server.

        Returns:
            str: The HTML content of the starting page.
        '''
        if self.base_config["template"] is None:
            return f'''<div style="text-align: center;">
    <h1>Invalid Syntax</h1>
    <br>
    No Starting page set.<br>Set Starting page by using setIndex Function.
</div>'''
        siteData = {
            "route": request.base_url,
            "cssDict": self.base_config["cssDict"],
            "jsDict": self.base_config["jsDict"]
        }
        startData = {
            "template": self.base_config["template"],
            "title": self.base_config["title"],
            "args": self.base_config["args"],
            "reload": self.base_config["reload"]
        }
        return render_template_string(self.base_config["index"], json_data=json.dumps(siteData), start_data=json.dumps(startData))

    def response(self):
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

    def load(self, requestType, **data):
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
