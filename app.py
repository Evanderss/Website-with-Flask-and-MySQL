from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route("/")
def start():
    return render_template("site/index.html")


@app.get("/books")
def books():
    return render_template("site/books.html")


@app.get("/about")
def about():
    return render_template("site/about.html")


if __name__ == "__main__":
    app.run(debug=True)