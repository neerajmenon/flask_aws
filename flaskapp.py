from flask import Flask,redirect,url_for,render_template,request,flash,send_file,session
import sqlite3, json


app = Flask(__name__)
app.config['SECRET_KEY'] = "thisisasecret!!!!"


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route('/')
def hello_world():
  return render_template('home.html')


@app.route('/dashboard')
def dashboard():
  if "username" not in session:
    return redirect(url_for("login"))
  data = json.dumps({})
  if 'data' in request.args:
    data = request.args['data']
  
  return render_template('dashboard.html',data=json.loads(data))

def count_words(filename):
  number_of_words = 0
  with open(filename,'r') as file:
    data = file.read()
    lines = data.split()
    number_of_words += len(lines)
    return number_of_words
  
@app.route('/download')
def download():
  return send_file("Limerick.txt",as_attachment=True)


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
            session['username'] = f_name
            wcount = count_words('Limerick.txt')
            data = json.dumps({'username':f_name,
                               'email':f_email,
                               'fname':f_fname,
                               'lname':f_lname,
                               'wcount':wcount})
            return redirect(url_for('dashboard',data=data))
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
        uploaded_file = request.files['file']
        print(uploaded_file)
        if uploaded_file.filename != '':
          uploaded_file.save(uploaded_file.filename)
        
        
        
        return redirect(url_for('login'))

    return render_template('register.html')


if __name__ == '__main__':
  app.run(debug=True)
