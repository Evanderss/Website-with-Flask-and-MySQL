from flask import Flask
from flask import render_template, request, redirect, send_from_directory
from flaskext.mysql import MySQL
from datetime import datetime
import os


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


@app.get("/img/<imagen>")
def images(imagen):
    print(imagen)
    return send_from_directory(os.path.join("templates/site/img"),imagen)



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
    cursor = cone.cursor()
    cursor.execute("SELECT * FROM `books`")
    books = cursor.fetchall()
    cone.commit()
    print(books)
    return render_template("admin/books.html", books=books)


@app.route("/admin/books/saved", methods=["POST"])
def admin_books_saved():
    _name = request.form["name"]
    _url = request.form["url"]
    _file = request.files["image"]
    time = datetime.now()
    houractual = time.strftime("%Y%H%M%S")
    if _file.filename != "":
        newname = houractual + "_" + _file.filename
        _file.save("templates/site/img/" + newname)
    sql = "INSERT INTO `books` (`id`, `name`, `image`, `url`) VALUES (NULL, %s, %s, %s);"
    dates = (_name, newname, _url)
    cone = mysql.connect()
    cursor = cone.cursor()
    cursor.execute(sql, dates)
    cone.commit()
    print(_name)
    print(_url)
    print(_file)
    return redirect("/admin/books")


@app.route("/admin/books/delete", methods=["POST"])
def admin_books_delete():
    _id = request.form["txtID"]
    print(_id)
    cone = mysql.connect()
    cursor = cone.cursor()
    cursor.execute("SELECT * FROM `books` WHERE id=%s", (_id))
    book = cursor.fetchall()
    cone.commit()
    print(book)
    
    cone = mysql.connect()
    cursor = cone.cursor()
    cursor.execute("DELETE FROM `books` WHERE id=%s", (_id))
    cone.commit()
    return redirect("/admin/books")


if __name__ == "__main__":
    app.run(debug=True)