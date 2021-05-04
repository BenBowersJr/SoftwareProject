from flask import Flask, render_template, redirect, url_for, request, session
import os
from flask_sqlalchemy import SQLAlchemy
import psycopg2, time
from psycopg2 import Error
from sqlalchemy import *
# Initialization

app = Flask(__name__)



con = psycopg2.connect(
  host = "ec2-3-217-219-146.compute-1.amazonaws.com",
  database= "d3duhguvo7sdom",
  user="hqlekupiwiodgw",
  password="e02966a8d4c287b73338f72e099e751c240f11ed6434aa6c5d626e1a11cd2b8c"
)
cur = con.cursor()

app.secret_key = os.urandom(12)

mode = 'dev'

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
  return render_template('homepage.html')

@app.route('/work-menu')
def workMenu():
  return render_template('work-menu.html')

@app.route('/pay-stubs')
def payStubs():
  return render_template('pay-stubs.html')

@app.route('/messages')
def messages():
  return render_template('messages.html')

@app.route('/time-off')
def timeOff():
  return render_template('time-off.html')

@app.route('/work-orders', methods=['POST', 'GET'])
def workOrder():
  try:
    # Connect to an existing database
    if mode == 'dev':
      connection = psycopg2.connect(user="jodywinters",
                                    password="NonaGrey11",
                                    host="localhost",
                                    port="5432",
                                    database="postgres")
    else:
      connection = psycopg2.connect(
        host = "ec2-3-217-219-146.compute-1.amazonaws.com",
        database= "d3duhguvo7sdom",
        user="hqlekupiwiodgw",
        password="e02966a8d4c287b73338f72e099e751c240f11ed6434aa6c5d626e1a11cd2b8c"
      )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM orders order by customer_username asc")
    records = cursor.fetchall()

  except (Exception, Error) as error:
      print("Error while connecting to PostgreSQL", error)
  finally:
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
  return render_template('work-orders.html', records = records)

@app.route('/submit', methods=['POST', 'GET'])
def deletingOrder():
  if request.method == 'POST':
    username = request.form['username']
    try:
      # Connect to an existing database
      if mode == 'dev':
        connection = psycopg2.connect(user="jodywinters",
                                    password="NonaGrey11",
                                    host="localhost",
                                    port="5432",
                                    database="postgres")
      else:
        connection = psycopg2.connect(
          host = "ec2-3-217-219-146.compute-1.amazonaws.com",
          database= "d3duhguvo7sdom",
          user="hqlekupiwiodgw",
          password="e02966a8d4c287b73338f72e099e751c240f11ed6434aa6c5d626e1a11cd2b8c"
        )
      cursor = connection.cursor()
      deletequery = ("""delete from orders where customer_username = '{}'""".format(username))
      cursor.execute(deletequery)
      connection.commit()
      cursor.execute("SELECT * FROM orders order by customer_username asc")
      records = cursor.fetchall()

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
      if (connection):
          cursor.close()
          connection.close()
          print("PostgreSQL connection is closed")
    return render_template("work-orders.html", records = records)

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
          return render_template('cmenu.html', message='Logged in successful!')
      else:
        return render_template('login.html', message='Incorrect username or password. Please register if an account does not exist.')
    else:
      cursor.execute("""SELECT * FROM workerlogin WHERE Worker_username = %s AND Worker_password = %s AND Employee_id = %s""", (username, password, employeeID ))
      result = cursor.fetchone()
      if result:
          session['logged_in'] = True
          return render_template('work-menu.html', message='Logged in successful!')
      else:
        return render_template('login.html', message='Incorrect username/employeeID or password. Please register if an account does not exist.')
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
      cursor.execute("""SELECT * FROM customerlogin WHERE Customer_username = %s AND Customer_password = %s""", (username, password ))
      cursor.execute("""SELECT * FROM workerlogin WHERE Worker_username = %s AND Worker_password = %s AND Employee_id = %s""", (username, password, employeeID ))
      result = cursor.fetchone()
      if result:
        return render_template('register.html', message='Account already exists!')
      elif employeeID == '':
        cursor.execute("""INSERT INTO customerlogin VALUES (%s, %s)""", (username, password ))
        con.commit()
        cursor.execute("SELECT * FROM customerlogin")
        result = cursor.fetchall()
        if result:
          return render_template('login.html', message='You have successfully registered !')
      else :
        cursor.execute("""INSERT INTO workerlogin VALUES (%s, %s, %s)""", (username, password, employeeID ))
        con.commit()
        cursor.execute("SELECT * FROM workerlogin")
        result = cursor.fetchall()
        if result:
          return render_template('login.html', message='You have successfully registered !')
      cursor.close()
      con.close()
    return render_template('register.html')

@app.route('/customer-menu', methods=['POST', 'GET'])
def menu():
  ### Connecting the database ###
  con = psycopg2.connect(
  host = "ec2-3-217-219-146.compute-1.amazonaws.com",
  database= "d3duhguvo7sdom",
  user="hqlekupiwiodgw",
  password="e02966a8d4c287b73338f72e099e751c240f11ed6434aa6c5d626e1a11cd2b8c")
  cur = con.cursor()

  #### Getting menu from database #####
  cur.execute('SELECT * FROM pizzasizes')
  allSizes = cur.fetchall()
  cur.execute('SELECT * FROM pizzatoppings')
  allToppings = cur.fetchall()
  cur.execute('SELECT * FROM pizzacrust')
  allCrusts = cur.fetchall()

  ##### this is converting the tuples returned from the SQL query into strings so they display cleanly on the menu#####
  global fixedCrusts, fixedToppings, fixedSizes

  fixedToppings = []
  for tup in allToppings:
    for char in tup:
      fixedToppings.append(char)
  fixedSizes = []
  for tup in allSizes:
    for char in tup:
      fixedSizes.append(char)
  fixedCrusts = []
  for tup in allCrusts:
    for char in tup:
      fixedCrusts.append(char)

  if request.method == 'POST':
    #create a Dict of the new item, time is just for a unique ID
    newCartItem = { f"{time.time()}": {
      'size': request.form['size'],
      'crust': request.form['crust'],
      'toppings': request.form.getlist('toppings')
      }
    }
    ### if there is already an item in the cart
    if 'cart' in session:
      ### merge the new cart item with the current cart
      session['cart'] = session['cart'] | newCartItem
    else:
      ### make the cart
      session['cart'] = newCartItem

    cur.close()
    con.close()
    return render_template('cmenu.html', crusts=fixedCrusts, sizes=fixedSizes, toppings=fixedToppings)

  if request.method == 'GET':

    cur.close()
    con.close()

    return render_template('cmenu.html', crusts=fixedCrusts, sizes=fixedSizes, toppings=fixedToppings)

@app.route('/clear', methods=['POST'])
def clear():
  global fixedCrusts, fixedToppings, fixedSizes
  session.clear()
  return redirect(url_for('menu'))

@app.route('/checkout')
def checkout():
  return "not done yet"



#disconnects the database and cursor
cur.close()
con.close()

if __name__ == '__main__':
  app.run(debug=True)
