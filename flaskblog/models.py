from flaskblog import db, login_manager
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    u_preference = db.relationship('UserPreferences', backref='users preference', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.img_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.content}', '{self.date_posted}')"


class PerfumeInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    top = db.Column(db.String(100), nullable=False)
    heart = db.Column(db.String(100), nullable=False)
    base = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    group = db.Column(db.String(50), nullable=False)
    #p_scent = db.relationship('PerfumeScents', backref='perfume scent pi', lazy=True)
    p_preference = db.relationship('UserPreferences', backref='perfume preference', lazy=True)

    def __repr__(self):
        return f"({self.id},{self.name},{self.brand})"

    def get_info(self):
        return (self.id, self.name, self.brand)

    def get_type(self):
        return self.group


class UserPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    perfume_id = db.Column(db.Integer, db.ForeignKey('perfume_info.id'), nullable=False)

    def __repr__(self):
        return f"({self.id}, {self.user_id}, {self.perfume_id})"


class Scents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    group = db.Column(db.String(50), nullable=False)
    #prefume_scent = db.relationship('PerfumeScents', backref='perfume scent s', lazy=True)

    def __repr__(self):
        return f"({self.id},{self.name})"
    
    def get_info(self):
        return (self.id, self.name)


#class PerfumeScents(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    perfume_id = db.Column(db.Integer, db.ForeignKey('perfume_info.id'), nullable=False)
#    scent_id = db.Column(db.Integer, db.ForeignKey('scents.id'), nullable=False)