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
        
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)