from flask import Flask, url_for, request, redirect
from flask import render_template as rt
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

NumberOfTodo = 0;
NumberOfCompTodo = 0;

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable = False)
    isDone = db.Column(db.Boolean, nullable = True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Task %r>" % self.id

@app.route("/add-todo", methods=["POST", "GET"])
def add_todo():
    global NumberOfTodo

    NumberOfTodo += 1
    if request.method == "POST":
        text = request.form["text"]
        task = Task(text = text, isDone = False)

        try:
            db.session.add(task)
            db.session.commit()
            return redirect("/home")
        except:
            return rt("Произошла ошибка!")
    else:
        return rt("home.html", task=task)

@app.route("/<int:id>/delete-todo")
def delete_todo(id):
    global NumberOfTodo, NumberOfCompTodo

    task = Task.query.get_or_404(id)
    if task.isDone == True:
        NumberOfCompTodo -= 1
    elif task.isDone == False:
        NumberOfTodo -= 1

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect("/home")
    except:
        return rt("Произошла ошибка!")

@app.route("/<int:id>/complete-todo")
def complete_todo(id):
    global NumberOfTodo, NumberOfCompTodo

    task = Task.query.get_or_404(id)
    NumberOfTodo -= 1
    NumberOfCompTodo += 1
    try:
        task.isDone = True
        db.session.add(task)
        db.session.commit()
        return redirect("/home")
    except:
        return rt("Произошла ошибка!")

@app.route("/")
@app.route("/home")
def home():
    tasks = Task.query.order_by(Task.date.desc()).all()
    return rt("home.html", tasks = tasks, NumberOfTodo = NumberOfTodo, NumberOfCompTodo=NumberOfCompTodo)

if __name__ == "__main__":
    app.run(debug=True)
