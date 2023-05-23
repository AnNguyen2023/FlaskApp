from flask import Flask, render_template, redirect, url_for, request
from app import app, db
from app.models import Todo

@app.route('/')
def index():
    todo_list = Todo.query.all()
    total_todo = Todo.query.count()
    completed_todo = Todo.query.filter_by(complete=True).count()
    uncompleted_todo = total_todo - completed_todo
    return render_template('dashboard/index.html', **locals())
# return render_template('dashboard/index.html', todo_list=todo_list, total_todo=total_todo, completed_todo=completed_todo)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>')
def update(id):
    todo = Todo.query.filter_by(id=id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    todo = Todo.query.get(id)
    if request.method == 'POST':
        todo.title = request.form['title']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template ('dashboard/edit.html', todo=todo)


@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

# @app.route('/export_completed_jobs/<int:id>', methods=['GET', 'POST'])
# def export(id):
#     todo = Todo.query.get(id)
#     if request.method == 'POST':
#         todo.title = request.form['title']
#         db.session.commit()
#         return redirect(url_for('index'))
#     return render_template ('dashboard/export.html', todo=todo)
@app.route('/export_completed_jobs')
def export_completed_jobs():
    completed_jobs = Todo.query.filter_by(complete=True).all()
    return render_template('dashboard/export.html', todos=completed_jobs)


@app.route('/about')
def about():
    return render_template('dashboard/about.html')


if __name__ == "__main__":
    app.run(debug=True)
