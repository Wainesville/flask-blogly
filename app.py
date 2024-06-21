"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'password123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def root():
    return redirect('/users')


@app.route('/users')
def users_list():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/list.html', users = users)

@app.route('/users/new', methods=["GET"])
def new_user_form():
    return render_template('users/new.html')

@app.route('/users/new', methods=['POST'])
def new_user():

    new_user= User(
        first_name = request.form["first_name"],
        last_name = request.form["last_name"],
        image_url = request.form["image_url"] or None)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>')
def user_details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/detail.html', user=user)

@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def users_update(user_id):

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

# @app.route('/edit_user')
# def edit_user()