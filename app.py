from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route("/")
def home():
    todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list)

@app.route("/add", methods=["POST"])
def addpage():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))



@app.route("/update/<int:todo_id>")
def updatepage(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def deletepage(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/newhome")
def newhome():
    todo_list = Todo.query.all()
    return render_template("index.html", todo_list=todo_list)

@app.route("/edit", methods=["POST"])
def editpage():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("newhome"))
    


@app.route("/do/<int:todo_id>")
def dopage(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("newhome"))
    

@app.route("/erase/<int:todo_id>")
def erasepage(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("newhome"))
    

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)



















def task(data, **kwargs):
   if '/add' in data: 
       addpage(**kwargs)
   if '/delete' in data: 
       deletepage(**kwargs)
   if '/update' in data: 
       updatepage(**kwargs)
   if '/' in data: 
       home(**kwargs)


def account(data, **kwargs):
   if '/edit' in data: 
       editpage(**kwargs)
   if '/do' in data: 
       dopage(**kwargs)
   if '/erase' in data: 
       erasepage(**kwargs)
