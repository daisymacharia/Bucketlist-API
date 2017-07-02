import os.path
import sys
from inspect import getsourcefile

current_path = os.path.abspath(getsourcefile(lambda: 0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

sys.path.insert(0, parent_dir)
from app.__init__ import db
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.ext.declarative import declarative_base
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

secret = os.getenv('SECRET')


class AddUpdateDelete():

    def add(self, resource):
        """To add attributes passed"""
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        """To update attributes passed"""
        return db.session.commit()

    def delete(self, resource):
        """To delete attributes passed"""
        db.session.delete(resource)
        return db.session.commit()


Base = declarative_base()


class User(db.Model, AddUpdateDelete):
    """Defines the user model"""
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fullnames = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    bucketlist = db.relationship('BucketList',
                                 backref=db.backref("bucketlist"),
                                 order_by='User.user_id',
                                 cascade='all, delete-orphan')

    def __repr__(self):
        """returning a representation of the user instance"""
        return "<UserModel: {}>".format(self.fullnames)

    def __init__(self, fullnames, email, password):
        self.fullnames = fullnames
        self.email = email
        self.password = password

    def hash_password(self, password):
        """Hash the password"""
        self.password = pwd_context.encrypt(password)
        db.session.commit()

    def verify_password(self, password):
        """Verify password"""
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=600):
        # token default expiry time = 10 min
        s = Serializer(secret, expires_in=expiration)
        return s.dumps({'id': self.user_id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret)
        try:
            data = s.loads(token)
        except SignatureExpired:
            # valid token, but expired
            return 'Signature Expired. Try log in again'
        except BadSignature:
            return 'Invalid Token. Try log in again'  # invalid token
        user = User.query.get(data['id'])
        return user


class BucketListItems(db.Model, AddUpdateDelete):
    """Defines the bucketlist item model"""
    __tablename__ = "bucketlistitems"
    __table_args__ = {'extend_existing': True}
    item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    bucketlist_id = db.Column(db.Integer, db.ForeignKey("bucketlist.list_id"))

    done = db.Column(db.Boolean, default=False)

    def __init__(self, name, bucketlist_id):
        self.name = name
        self.bucketlist_id = bucketlist_id


class BucketList(db.Model, AddUpdateDelete):
    """Defines the bucketlist model"""
    __tablename__ = "bucketlist"
    __table_args__ = {'extend_existing': True}
    list_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    name = db.Column(db.String(50), nullable=False)
    items = db.relationship('BucketListItems', backref=db.backref("items"),
                            order_by='BucketList.list_id',
                            cascade='all, delete-orphan', lazy='dynamic',
                            viewonly=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by
