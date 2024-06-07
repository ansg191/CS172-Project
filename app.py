import flask
import json
from flask import Flask, Response
from flask_cors import CORS

from index import Index

app = Flask(__name__)
CORS(app)

index = Index()
with app.app_context():
    index.build_index()


@app.route("/")
def main():
    return flask.redirect(flask.url_for("web", path="index.html"))


@app.route("/<path:path>")
def web(path):
    return flask.send_from_directory("web/dist", path)


@app.route("/query")
def query():
    q = flask.request.args.get("q")
    print(q)

    results = index.query(q)
    return Response(json.dumps(results), mimetype="application/json")

