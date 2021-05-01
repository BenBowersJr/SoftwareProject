from flask import Flask, render_template, redirect, url_for, request, session
import os
from config import Config
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from psycopg2 import Error
from sqlalchemy import *
# Initialization

app = Flask(__name__)
## Im still figuring this out.. dont trust the below line
db = app.config['DATABASE_URL'] = 'postgres://hqlekupiwiodgw:e02966a8d4c287b73338f72e099e751c240f11ed6434aa6c5d626e1a11cd2b8c@ec2-3-217-219-146.compute-1.amazonaws.com:5432/d3duhguvo7sdom'

db = SQLAlchemy(app)

class menu(db.Model):
  __tablename__ = 'menu'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(20))

  def __init__(self, name):
    self.name = name

@app.route('/')
def homepage():
  if not session.get('logged_in'):
  return render_template('homepage.html')

@app.route('/work-menu')
def workMenu():
  return render_template('work-menu.html')

@app.route('/work-orders')
def workOrder():
  return render_template('work-orders.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    employeeID = request.form['employeeID']
    con = psycopg2.connect(
    host = "ec2-3-217-219-146.compute-1.amazonaws.com",
    database= "d3duhguvo7sdom",
    user="hqlekupiwiodgw",
    password="e02966a8d4c287b73338f72e099e751c240f11ed6434aa6c5d626e1a11cd2b8c"
    )
    cursor = con.cursor()
    if employeeID == '':

      cursor.execute("""SELECT * FROM customerlogin WHERE Customer_username = %s AND Customer_password = %s""", (username, password ))
      result = cursor.fetchone()
      if result:
          session['logged_in'] = True
          return render_template('login.html', message='Logged in successful!')
      else:
        return render_template('login.html', message='Incorrect username or password')
    else:
      cursor.execute("""SELECT * FROM workerlogin WHERE Worker_username = %s AND Worker_password = %s AND Employee_id = %s""", (username, password, employeeID ))
      result = cursor.fetchone()
      if result:
          session['logged_in'] = True
          return render_template('login.html', message='Logged in successful!')
      else:
        return render_template('login.html', message='Incorrect username/employeeID or password')
    cursor.close()
    con.commit()
    con.close()
  return render_template('login.html')

@app.route('/logout')
def logout():
  session['logged_in'] = False
    return redirect(url_for('login', message='Logged out successful!'))

@app.route('/register', methods =['GET', 'POST'])
def register():
    if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      employeeID = request.form['employeeID']
      if len(username) > 8 :
        return render_template('register.html', message='Username is too long.')

      con = psycopg2.connect(
        host = "ec2-3-217-219-146.compute-1.amazonaws.com",
        database= "d3duhguvo7sdom",
        user="hqlekupiwiodgw",
        password="e02966a8d4c287b73338f72e099e751c240f11ed6434aa6c5d626e1a11cd2b8c"
      )
      cursor = con.cursor()
      if employeeID == '':

        cursor.execute("""INSERT INTO customerlogin VALUES (%s, %s)""", (username, password ))
        cursor.execute("SELECT * FROM customerlogin")
        result = cursor.fetchall()
        for r in result:
          print (r)
          message = 'You have successfully registered !'
      else :
        cursor.execute("""INSERT INTO workerlogin VALUES (%s, %s, %s)""", (username, password, employeeID ))
        cursor.execute("SELECT * FROM workerlogin")
        result = cursor.fetchall()
        for r in result:
          print (r)
          message = 'You have successfully registered !'
      cursor.close()
      con.commit()
      con.close()
    return render_template('register.html')

@app.route('/menu', methods=['POST', 'GET'])
def menu():
  return render_template('cmenu.html')


if __name__ == '__main__':
  app.secret_key = os.urandom(12)
  app.run(debug=True)
