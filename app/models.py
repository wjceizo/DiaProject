from datetime import datetime
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

class Permission:
    USER = 1
    ADMIN = 2


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')
    permissions = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 1

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name




class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    name = db.Column(db.String(64), nullable=False)
    location = db.Column(db.String(128), nullable=False)
    lang = db.Column(db.String(32), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    token = db.Column(db.text, nullable=False)
    user_logs = db.relationship('Userlog', backref='auth')
    user_word_rels = db.relationship('Userwordrel', backref='auth')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role_id is None:
            self.role_id = 2


    def __repr__(self):
        return '<User %r>' % self.name

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Userlog(db.Model):
    __tablename__ = 'user_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    location = db.Column(db.String(128))
    created_at = db.Column(db.DateTime(), default=datetime.now)

    def __repr__(self):
        return '<Userlog %r>' % self.name


class Userwordrel(db.Model):
    __tablename__ = 'user_word_rels'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    word_id = db.Column(db.String(128), db.ForeignKey('words.id'))
    snd_path = db.Column(db.String(128))
    snd_abs = db.Column(db.String(128))
    created_at = db.Column(db.DateTime(), default=datetime.now)
    update_at = db.Column(db.DateTime())

    # diffs = db.relationship('Diff', backref='user_word_rel')

    def __repr__(self):
        return '<Userwordrel %r>' % self.name


class Word(db.Model):
    __tablename__ = 'words'
    id = db.Column(db.Integer, primary_key=True)
    stem = db.Column(db.String(128), unique=True, index=True, nullable=False)
    meaning = db.Column(db.String(128))
    comm = db.Column(db.Text())
    user_word_rels = db.relationship('Userwordrel', backref='word')

    def __repr__(self):
        return '<Word %r>' % self.name


class Diff(db.Model):
    __tablename__ = 'diffs'
    id = db.Column(db.Integer, primary_key=True)
    uwr_id1 = db.Column(db.Integer, db.ForeignKey('user_word_rels.id'))
    uwr_id2 = db.Column(db.Integer, db.ForeignKey('user_word_rels.id'))
    value = db.Column(db.Float)
    diff_type = db.Column(db.Integer, db.ForeignKey('difftypes.id'))
    uwr1 = db.relationship('Userwordrel', foreign_keys=uwr_id1)
    uwr2 = db.relationship('Userwordrel', foreign_keys=uwr_id2)

    def __repr__(self):
        return '<Diff %r>' % self.name


class Difftype(db.Model):
    __tablename__ = 'difftypes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True, nullable=False)
    diffs = db.relationship('Diff', backref='difftype')

    def __repr__(self):
        return '<Difftype %r>' % self.name
