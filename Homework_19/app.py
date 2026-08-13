import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from db import db
from models import User, Note
from forms import RegisterForm, LoginForm, NoteForm

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SECRET_KEY"] = os.urandom(24)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    os.makedirs(app.instance_path, exist_ok=True)
    db.create_all()

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("მომხმარებლის სახელი უკვე დაკავებულია. გთხოვთ, აირჩიოთ სხვა.", "danger")
            return redirect(url_for("register"))

        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("რეგისტრაცია წარმატებით დასრულდა! შეგიძლიათ შეხვიდეთ.", "success")
        return redirect(url_for("login"))
    
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("notes"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("notes"))
        else:
            flash("არასწორი მომხმარებლის სახელი ან პაროლი!", "danger")

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required 
def logout():
    logout_user() 
    flash("თქვენ გამოხვედით სისტემიდან.", "info")
    return redirect(url_for("login"))


@app.route("/")
@app.route("/notes")
@login_required
def notes():
    user_notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template("notes.html", notes=user_notes)


@app.route("/add_note", methods=["GET", "POST"])
@login_required
def add_note():
    form = NoteForm()
    if form.validate_on_submit():
        new_note = Note(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id
        )
        db.session.add(new_note)
        db.session.commit()
        
        flash("ჩანაწერი წარმატებით დაემატა!", "success")
        return redirect(url_for("notes"))
        
    return render_template("add_note.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)