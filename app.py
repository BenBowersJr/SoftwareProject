from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from psycopg2 import Error

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
  return render_template('homepage.html')

@app.route('/work-menu')
def workMenu():
  return render_template('work-menu.html')

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

@app.route('/register-login')
def registerLogin():
      return render_template("register-login.html")

@app.route('/menu', methods=['POST', 'GET'])
def menu():
  return render_template('cmenu.html')


if __name__ == '__main__':
  app.run(debug=True)
