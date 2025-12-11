from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)

@app.route("/", methods=['GET', 'POST'])
def start_page():
    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        if content:
            new_todo = Todo(content=content)
            db.session.add(new_todo)
            db.session.commit()
        return redirect(url_for('start_page'))  #Sorgt dafür, dass ToDos nicht 2mal angezeigt werden wenn Seite neu geladen wird
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

# Neue Route zum Löschen eines ToDos
@app.route("/delete/<int:id>")
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('start_page'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
