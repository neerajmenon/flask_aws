from flask import Flask,redirect,url_for,render_template,request,flash
import sqlite3


app = Flask(__name__)
app.config['SECRET_KEY'] = "thisisasecret"


@app.route('/')
def hello_world():
  return render_template('home.html')


@app.route('/login',methods=['GET','POST'])
def login():
  if request.method == 'POST':
        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['username']
        password = request.form['password']
        command = "SELECT DISTINCT * from users where name='"+name+"';"
        print(command)
        cursor.execute(command)
        rows = cursor.fetchall()
        f_name = ""
        f_pswd = ""
        f_email = ""
        for row in rows:
          print(row)
        if len(rows)>0:
          print(len(rows[0]))
          f_name = rows[0][0]
          f_pswd = rows[0][1]
          f_email = rows[0][2]
          f_fname = rows[0][3]
          f_lname = rows[0][4]
        if f_name == name:
          if f_pswd == password:
            flash('You were successfully logged in!')
            return render_template('dashboard.html',username=f_name,password=f_pswd,email=f_email,fname=f_fname,lname=f_lname)
          else:
            flash("Incorrect password")
        else:
          flash("Username does not exist")
          
        
        return render_template('login.html')
  elif request.method == 'GET':
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
        return render_template('login.html')

    return render_template('register.html')


if __name__ == '__main__':
  app.run(debug=True)
