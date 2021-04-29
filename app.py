from flask import Flask, render_template, redirect, url_for, request
import psycopg2

app = Flask(__name__)
#connecting to heroku database 
con = psycopg2.connect(
  host = "ec2-3-217-219-146.compute-1.amazonaws.com",
  database= "d3duhguvo7sdom",
  user="hqlekupiwiodgw",
  password="e02966a8d4c287b73338f72e099e751c240f11ed6434aa6c5d626e1a11cd2b8c"
)
#creating cursor
cur = con.cursor()
#execting a query
cur.execute("select * from pizzatoppings")
#putting that query into a variable
rows = cur.fetchall()
#printing those out in the terminal
for r in rows:
  print(f"{r}")


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

@app.route('/customer-menu', methods=['POST', 'GET'])
def menu():
  if request.method == 'POST':
    toppings = request.form['toppings']
    print(toppings)
    return render_template('cmenu.html')
  if request.method == 'GET':
    return render_template('cmenu.html')

#disconnects the database and cursor
cur.close()
con.close()

if __name__ == '__main__':
  app.run(debug=True)
