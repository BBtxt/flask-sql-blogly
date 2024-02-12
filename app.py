from flask import Flask, request, redirect, render_template
from flask_migrate import Migrate
from models import db, connect_db, Users, Posts, Post_tag, Tags

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.debug = True
migrate = Migrate(app, db)

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
    posts = Posts.query.filter_by(user_id=id).all()
    return render_template('user.html', user=user, posts=posts)


@app.route('/<int:id>', methods=["POST"])
def go_to_edit(id):
    return redirect(f'/edit/{id}')

@app.route('/edit/<int:id>')
def edit_user(id):
    user = Users.query.get_or_404(id)
    return render_template('edit.html', user=user)

###########################Posts###############################

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
 
@app.route('/<int:id>/posts/new')
def new_post(id):
    user = Users.query.get_or_404(id)
    tags = Tags.query.all()
    return render_template('new_post.html', user=user, tags=tags)

@app.route('/<int:id>/posts/new', methods=["POST"])
def new_post_post(id):
    title = request.form['title']
    content = request.form['content']
    post = Posts(title=title, content=content, user_id=id)
    db.session.add(post)
    db.session.commit()
    return redirect(f'/{id}')

@app.route("/<int:u_id>/posts/<int:post_id>")
def post(u_id, post_id): 
    user = Users.query.get_or_404(u_id)
    post = Posts.query.get_or_404(post_id)
    date = post.created_at.strftime("%B %d, %Y")
    post_tags = Post_tag.query.filter_by(post_id=post_id).all()
    return render_template('post.html', post=post, user=user, date=date, post_tags=post_tags)

@app.route("/<int:u_id>/posts/<int:post_id>/edit")
def edit_post(u_id, post_id):
    user = Users.query.get_or_404(u_id)
    post = Posts.query.get_or_404(post_id)
    return render_template('edit_post.html', user=user, post=post)

@app.route("/<int:u_id>/posts/<int:post_id>/edit", methods=["POST"])
def edit_post_post(u_id, post_id):
    post = Posts.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.commit()
    return redirect(f'/{u_id}/posts/{post_id}')

@app.route("/<int:u_id>/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(u_id, post_id):
    post = Posts.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/{u_id}')

###########################Tags###############################


@app.route("/tags")
def all_tags():
    tags = Tags.query.all()
    return render_template('tags.html', tags=tags)

@app.route("/tags/new")
def create_tag():
    current_tags = Tags.query.all()
    return render_template('new_tag.html', current_tags=current_tags)

@app .route("/tags/new", methods=["POST"])
def create_tag_post():
    tag = Tags(name=request.form['name'])
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

@app.route("/<int:u_id>/posts/<int:post_id>/add_tags")
def add_tags(u_id, post_id):
    post = Posts.query.get_or_404(post_id)
    tags = Tags.query.all()
    return render_template('add_tags.html', post=post, tags=tags)

@app.route("/<int:u_id>/posts/<int:post_id>/add_tags", methods=["POST"])
def add_tags_post(u_id, post_id):
    tags = request.form.getlist('tags')
    for tag in tags:
        post_tag = Post_tag(post_id=post_id, tag_id=tag)
        db.session.add(post_tag)
        db.session.commit()
        
    return redirect(f'/{u_id}/posts/{post_id}')
