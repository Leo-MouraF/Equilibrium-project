from flask import Flask, render_template

app = Flask(__name__)

if __name__ == "__main__":
    app.run()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/suplementos")
def suplementos():
    return render_template("suplementos.html")

@app.route("/produtos_naturais")
def produtos_naturais():
    return render_template("produtos_naturais.html")