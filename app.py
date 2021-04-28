from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import psycopg2
from psycopg2 import Error

app = Flask(__name__)

SQLALCHEMY_TRACK_MODIFICATIONS = False

## Im still figuring this out.. dont trust the below line
#app.config['DATABASE_URL'] = 'postgres://hqlekupiwiodgw:e02966a8d4c287b73338f72e099e751c240f11ed6434aa6c5d626e1a11cd2b8c@ec2-3-217-219-146.compute-1.amazonaws.com:5432/d3duhguvo7sdom'


try:
    # Connect to an existing database
    connection = psycopg2.connect(user="jodywinters",
                                  password="NonaGrey11",
                                  host="localhost",
                                  port="5432",
                                  database="postgres")

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    insert_query ="""INSERT INTO orders(customer_username, pizza_crust, pizza_topping1, pizza_topping2) VALUES('jody12', 'thin crust', 'pepperoni', 'cheese');"""
    cursor.execute(insert_query)
    connection.commit()
    print("1 record inserted successfully")
    cursor.execute("SELECT * FROM orders")
    records = cursor.fetchall()
    print("Results ", records)

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

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

@app.route('/work-orders')
def workOrder():
  return render_template('work-orders.html')

@app.route('/register-login')
def registerLogin():
      return render_template("register-login.html")

@app.route('/menu', methods=['POST', 'GET'])
def menu():
  return render_template('cmenu.html')


if __name__ == '__main__':
  app.run(debug=True)
