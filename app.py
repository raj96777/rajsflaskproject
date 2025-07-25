from flask import Flask,render_template,url_for,request, redirect,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)#it is an object of Flask.
app.secret_key = "rajkumar123"


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):#table_name
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Task %r>' %self.id

with app.app_context():
    db.create_all()
    print("✅ Database created successfully.")

@app.route('/', methods = ['POST','GET'])
def index():
    if request.method =='POST':
        task_content = request.form['content'].strip()#html content  , request.form [] is a dictionary.if you dont want to crash you can use request.form.get
        new_task = Todo(content = task_content)# todo content    content = "write a letter"
        if not task_content:
            flash("⚠️ Please enter some content before submitting.")
            return redirect('/')  # Redirect to show the message

        try:
            db.session.add(new_task)
            db.session.commit()#save
            return redirect('/')
        except:
            return "There was an issue adding your task."


    else:
        tasks = Todo.query.order_by(Todo.date_created).all()# .query is equivalent to: SELECT * FROM todos (in SQL).
        #SELECT * FROM todos ORDER BY date_created;

        return render_template('index.html', tasks = tasks)
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting the task."

@app.route('/update/<int:id>', methods = ['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)



    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There is an issue updating your task."

    else:
        return render_template("update.html", task = task)

if __name__ == "__main__":
    app.run(debug = True)