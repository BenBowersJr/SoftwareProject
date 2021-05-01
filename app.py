from flask import Flask, render_template, redirect, url_for, request, session, flash
import psycopg2, time

app = Flask(__name__)
#connecting to heroku database 
con = psycopg2.connect(
  host = "ec2-3-217-219-146.compute-1.amazonaws.com",
  database= "d3duhguvo7sdom",
  user="hqlekupiwiodgw",
  password="e02966a8d4c287b73338f72e099e751c240f11ed6434aa6c5d626e1a11cd2b8c"
)
cur = con.cursor()

secret_key="secret"


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
    connection = psycopg2.connect(user="jodywinters",
                                  password="NonaGrey11",
                                  host="localhost",
                                  port="5432",
                                  database="postgres")
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
      connection = psycopg2.connect(user="jodywinters",
                                    password="NonaGrey11",
                                    host="localhost",
                                    port="5432",
                                    database="postgres")
      cursor = connection.cursor()
      deletequery = ("""delete from orders where customer_username = '{}'""".format(username))
      cursor.execute(deletequery)
      connection.commit()
      cursor.execute("SELECT * FROM orders")
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
  app.secret_key = "the greatest key"
  app.run(debug=True)
