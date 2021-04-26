from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def homepage():
  return render_template('homepage.html')

@app.route('/work-menu')
def workMenu():
  return render_template('work-menu.html')

@app.route('/work-orders')
def workOrder():
  return render_template('work-orders.html')

if __name__ == '__main__':
  app.run(debug=True)