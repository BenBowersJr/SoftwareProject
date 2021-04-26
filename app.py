from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

## Im still figuring this out.. dont trust the below line
app.config['DATABASE_URL'] = 'postgres://hqlekupiwiodgw:e02966a8d4c287b73338f72e099e751c240f11ed6434aa6c5d626e1a11cd2b8c@ec2-3-217-219-146.compute-1.amazonaws.com:5432/d3duhguvo7sdom'

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

@app.route('/menu', methods=['POST', 'GET'])
def menu():
  return render_template('cmenu.html')



if __name__ == '__main__':
  app.run(debug=True)