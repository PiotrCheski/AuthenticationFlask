from flask import Blueprint, render_template

logs = Blueprint('logs', __name__)

@logs.route("/")
@logs.route("/logs")
def logshome():
    return render_template("logs/logs.html")