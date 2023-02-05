from flask import Flask,redirect,url_for,render_template,request,flash
import sqlite3


app = Flask(__name__)
app.config['SECRET_KEY'] = "thisisasecret"


@app.route('/')
def hello_world():
  return render_template('home.html')


@app.route('/login',methods=['GET','POST'])
def login():
    return render_template('login.html')


@app.route('/register',methods=['GET','POST'])
def register():

    if request.method == 'POST':
        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['username']
        password = request.form['password']
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        command = "INSERT INTO users VALUES('"+name+"','"+password+"','"+email+"','"+firstname+"','"+lastname+"')"
        print(command)
        cursor.execute(command)
        connection.commit()

    return render_template('register.html')


if __name__ == '__main__':
  app.run(debug=True)
