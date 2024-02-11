from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


    
# MODELS GO HERE

class Users(db.Model):
    '''User model'''
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(50),
                        nullable=False)
    last_name = db.Column(db.String(50),
                          nullable=False)
    
    image_url = db.Column(db.String,
                          nullable=True,
                          default='https://www.freeiconspng.com/uploads/profile-icon-9.png')
    
    def __repr__(self):
        u = self
        return f'<User {u.id} {u.first_name} {u.last_name} {u.image_url}>'
        
class Posts(db.Model):
    """Post model with a user fk"""
    
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer,
                     primary_key=True,
                     autoincrement=True)
    title = db.Column(db.String(100),
                      nullable=False)
    content = db.Column(db.String,
                        nullable=False)
    created_at = db.Column(db.DateTime,
                          nullable=False,
                          default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    users = db.relationship('Users', backref='posts')

class Post_tag(db.Model):
    """Post_tag model with a post fk and a tag fk"""
    
    __tablename__ = 'post_tag'
    
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    
class Tags(db.Model):
    """Tag model"""
    
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    
    posts = db.relationship('Posts', secondary='post_tag', backref='tags')
    
     
        
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)