import os
from app import db
from passlib.apps import custom_app_context as pwd_context


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


class User(db.Model, AddUpdateDelete):
    """Defines the user model"""
    __tablename__ = "users"
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        """returning a printable version for the object"""
        return "<UserModel: {}>".format(self.username)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

        # Hash password
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

        # Verify password
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


class BucketListItems(db.Model, AddUpdateDelete):
    """Defines the bucketlist item model"""
    __tablename__ = "bucketlistitems"
    item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp()
                              , onupdate=db.func.current_timestamp())
    bucketlist_id = db.Column(db.Integer, db.ForeignKey("bucketlist.id"))

    done = db.Column(db.Boolean, default=False)

    def __init__(self, name, bucketlist_id):
        self.name = name
        self.bucketlist_id = bucketlist_id


class BucketList(db.Model, AddUpdateDelete):
    """Defines the bucketlist model"""
    __tablename__ = "bucketlist"
    list_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    created_by = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    name = db.Column(db.String(50), nullable=False)
    items = db.relationship(BucketListItems, backref="bucketlist",
                            cascade='all,delete', lazy='dynamic',
                            viewonly=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp()
                              , onupdate=db.func.current_timestamp())

    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by
