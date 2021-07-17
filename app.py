# flask minimal app
from datetime import datetime
from typing import DefaultDict
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# creat a database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    # it is only use for import
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(600), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    # it is only use for export
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/' , methods = ['GET','POST'])
def hello_world():
    #form submit 
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

       # data automatically going in the sql server
        todo = Todo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()

    # show the data in the webpage
    allTodo = Todo.query.all()
    print(allTodo)
    return  render_template('index.html', allTodo = allTodo) 

# make a different end point(endpotin means a different pages) in the flask server
# make a different pages for delete and update
@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'this is the products page'

@app.route('/update/<int:sno>',methods = ['GET','POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

       # data automatically going in the sql server for update
        todo  = Todo.query.filter_by(sno = sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')   
    todo = Todo.query.filter_by(sno = sno).first()
    return  render_template('update.html', todo = todo) 
    return 'this is the products page'


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno = sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')         

# if you want to change the port so add port in the bellow
if  __name__ == '__main__':
    app.run(debug=True , port=8000) 








    # check pip version = pip --version
    # python -m virtualenv venv for create a env. for flask
    # make env. venv tab scripts tab activste tab
    # pip install flask
    #https://inloop.github.io/sqlite-viewer/ 
    # sql

    # app reload code
     # data base run = from app import db
    #                   db.create_all()
    #                    exit()   

    # app frease code
    # pip install gunicorn
    # pip freeze > requirments.txt