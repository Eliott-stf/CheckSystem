from flask import Blueprint, render_template, request

from ..services.command_service import execute_command

web_blueprint = Blueprint("web", __name__)

@web_blueprint.route("/", methods=["GET", "POST"])
def index():
  result = ""
  command= ""
  if request.method == "POST":
    command = request.form["cmd"].strip()
    result = execute_command(command)
  return render_template("index.html", result=result, command=command)