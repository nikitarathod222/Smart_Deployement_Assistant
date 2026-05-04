import subprocess
import sys

from flask import Flask, redirect, render_template, request

app = Flask(__name__)

DEFAULT_PROJECT_TYPE = "Python"
DEFAULT_INPUT_TYPE = "GitHub URL"
STREAMLIT_URL = "http://localhost:8501"


@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == "admin" and password == "1234":
            return redirect("/dashboard")
        error = "Use the demo credentials to access the dashboard."
    return render_template("login.html", error=error)


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    selected_project_type = request.form.get("project_type", DEFAULT_PROJECT_TYPE)
    selected_input_type = request.form.get("input_type", DEFAULT_INPUT_TYPE)
    launched = False

    if request.method == "POST":
        subprocess.Popen([sys.executable, "-m", "streamlit", "run", "app.py"])
        launched = True

    return render_template(
        "dashboard.html",
        launched=launched,
        launch_url=STREAMLIT_URL,
        selected_project_type=selected_project_type,
        selected_input_type=selected_input_type,
    )


if __name__ == "__main__":
    app.run(debug=True)
