from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL


app = Flask(__name__)
mysql = MySQL()
app.config["MYSQL_DATABASE_HOST"]='localhost'
app.config["MYSQL_DATABASE_USER"]='root'
app.config["MYSQL_DATABASE_PASSWORD"]=''
app.config["MYSQL_DATABASE_DB"]='website'
mysql.init_app(app)


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
    cone = mysql.connect()
    print(cone)
    return render_template("admin/books.html")


@app.route("/admin/books/saved", methods=["POST"])
def admin_books_saved():
    _name = request.form["name"]
    _url = request.form["url"]
    _file = request.files["image"]
    print(_name)
    print(_url)
    print(_file)
    return redirect("/admin/books")


if __name__ == "__main__":
    app.run(debug=True)