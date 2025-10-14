from flask import Flask, render_template
from flask import jsonify

app = Flask(__name__)

@app.route("/")
def root():
    return render_template("home.html")

@app.route("/json")
def hello_json():
    return jsonify(message="Hello, JSON!")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/error")
def error():
    return render_template("error.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)