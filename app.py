from flask import Flask, request, redirect, render_template
from models import db, connect_db, Users, Posts

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.debug = True

connect_db(app)

# db.create_all()

@app.route('/')
def home():
    users = Users.query.all()
    for user in users:
        print(user.first_name)
    return render_template('index.html', users=users)

@app.route('/', methods=["POST"])
def make_user(): 
    return redirect('/new_user')

@app.route("/new_user", methods=["POST"])
def add_user():
    """Add pet and redirect to list."""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url= request.form['image_url']
    if not image_url:
        image_url = 'https://www.freeiconspng.com/uploads/profile-icon-9.png'

    user = Users(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect(f"/{user.id}")

@app.route("/new_user")
def new_user():
    return render_template('new_user.html')


@app.route('/<int:id>')
def user(id):
    user = Users.query.get_or_404(id)
    return render_template('user.html', user=user)

@app.route('/<int:id>', methods=["POST"])
def go_to_edit(id):
    return redirect(f'/edit/{id}')

@app.route('/edit/<int:id>')
def edit_user(id):
    user = Users.query.get_or_404(id)
    return render_template('edit.html', user=user)

@app.route('/edit/<int:id>', methods=["POST"])
def edit_user_post(id):
    user = Users.query.get_or_404(id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    db.session.commit()
    return redirect(f'/{id}')

@app.route("/delete/<int:id>", methods=["POST"])
def delete_user(id):
    user = Users.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')