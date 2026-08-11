from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    course = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Student {self.id} - {self.name} ({self.course})>"


@app.route('/')
def index():
    students = Student.query.order_by(Student.id).all()
    return render_template('index.html', students=students)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        grade = request.form['grade']

        new_student = Student(
            name=name,
            email=email,
            course=course,
            grade=float(grade)
        )

        try:
            db.session.add(new_student)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return f"შეცდომა დამატებისას: {e}"

    return render_template('add.html')


@app.route('/delete/<int:id>')
def delete(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
