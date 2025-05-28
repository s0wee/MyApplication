from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'myDatabase'

mysql = MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM dogs")
    dogs = cur.fetchall()
    cur.close()

    return render_template('index.html', dogs=dogs)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        breed = request.form['breed']
        owner = request.form['owner']
        name = request.form['name']
        color = request.form['color']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO dogs (breed, owner, name, color) VALUES (%s, %s, %s, %s)", (breed, owner, name, color))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        breed = request.form['breed']
        owner = request.form['owner']
        name = request.form['name']
        color = request.form['color']
        cur.execute("UPDATE dogs SET breed=%s, owner=%s, name=%s, color=%s WHERE id=%s", (breed, owner, name, color, id))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))
    else:
        cur.execute("SELECT * FROM dogs WHERE id = %s", (id,))
        dog = cur.fetchone()
        cur.close()

        return render_template('edit_add.html', dog=dog)

@app.route('/new')
def new():
    return render_template('edit_add.html', dog=None)

@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM dogs WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
