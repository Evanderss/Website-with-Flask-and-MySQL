from flask import Flask
from flask import render_template, request, redirect, send_from_directory, session
from flaskext.mysql import MySQL
from datetime import datetime
import os


app = Flask(__name__)
app.secret_key = "evanderss"
mysql = MySQL()
app.config["MYSQL_DATABASE_HOST"]='localhost'
app.config["MYSQL_DATABASE_USER"]='root'
app.config["MYSQL_DATABASE_PASSWORD"]=''
app.config["MYSQL_DATABASE_DB"]='website'
mysql.init_app(app)


@app.get("/")
def start():
    return render_template("site/index.html")


@app.get("/img/<imagen>")
def images(imagen):
    print(imagen)
    return send_from_directory(os.path.join("templates/site/img"), imagen)


@app.get("/css/<filecss>")
def css_link(filecss):
    return send_from_directory(os.path.join("templates/site/css"), filecss)


@app.get("/books")
def books():
    cone = mysql.connect()
    cursor = cone.cursor()
    cursor.execute("SELECT * FROM `books`")
    books = cursor.fetchall()
    cone.commit()
    return render_template("site/books.html", books=books)


@app.get("/about")
def about():
    return render_template("site/about.html")


@app.get("/admin")
def admin_index():
    if not "login" in session:
        return redirect("/admin/login")
    return render_template("admin/index.html")


@app.get("/admin/login")
def admin_login():
    return render_template("admin/login.html")


@app.post("/admin/login")
def admin_login_post():
    _user = request.form["user"]
    _password = request.form["password"]
    print(_user)
    print(_password)
    if _user == "admin" and _password == "123":
        session["login"] = True
        session["user"] = "Evan"
        return redirect("/admin")
    return render_template("admin/login.html")


@app.get("/admin/logout")
def admin_logout():
    session.clear()
    return redirect("/")


@app.get("/admin/books")
def admin_books():
    if not "login" in session:
        return redirect("/admin/login")
    cone = mysql.connect()
    cursor = cone.cursor()
    cursor.execute("SELECT * FROM `books`")
    books = cursor.fetchall()
    cone.commit()
    print(books)
    return render_template("/admin/books.html", books=books)


@app.route("/admin/books/saved", methods=["POST"])
def admin_books_saved():
    if not "login" in session:
        return redirect("/admin/login")
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
    if not "login" in session:
        return redirect("/admin/login")
    _id = request.form["txtID"]
    print(_id)
    cone = mysql.connect()
    cursor = cone.cursor()
    cursor.execute("SELECT image FROM `books` WHERE id=%s", (_id))
    book = cursor.fetchall()
    cone.commit()
    print(book)
    if os.path.exists("templates/site/img/" + str(book[0][0])):
        os.unlink("templates/site/img/" + str(book[0][0]))
    cone = mysql.connect()
    cursor = cone.cursor()
    cursor.execute("DELETE FROM `books` WHERE id=%s", (_id))
    cone.commit()
    return redirect("/admin/books")


if __name__ == "__main__":
    app.run(debug=True)