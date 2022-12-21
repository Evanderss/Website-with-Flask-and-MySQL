from flask import Flask
from flask import render_template, request, redirect


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


@app.get("/admin")
def admin_index():
    return render_template("admin/index.html")


@app.get("/admin/login")
def admin_login():
    return render_template("admin/login.html")


@app.get("/admin/books")
def admin_books():
    return render_template("admin/books.html")


@app.post("/admin/books/saved")
def admin_books_saved():
    print(request.form["name"])
    return redirect("/admin/books")


if __name__ == "__main__":
    app.run(debug=True)