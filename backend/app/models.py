from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
import jwt
from flask_jwt_extended import create_access_token, get_jwt_identity
import datetime as dat


class Permission:
    USER = 1
    MEMBER = 2
    ADMIN = 4


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role")
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
        return self.name


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    name = db.Column(db.String(64), nullable=False)
    location = db.Column(db.String(128), nullable=False)
    lang = db.Column(db.String(32), nullable=False)
    sex = db.Column(db.String(32), nullable=False)
    work = db.Column(db.String(32))
    comm1 = db.Column(db.String(64))
    comm2 = db.Column(db.String(64))
    created_at = db.Column(db.DateTime(), default=datetime.now)
    user_logs = db.relationship("Userlog", backref="auth")
    user_word_rels = db.relationship("Userwordrel", backref="auth")

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role_id is None:
            self.role_id = 3


    def __repr__(self):
        return self.username

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def encode_auth_token(user_id):
        try:
            return create_access_token(identity=user_id)
        except Exception as e:
            return e


class Userlog(db.Model):
    __tablename__ = "user_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    location = db.Column(db.String(128))
    created_at = db.Column(db.DateTime(), default=datetime.now)

    def __repr__(self):
        return "<Userlog %r>" % self.name


class Word(db.Model):
    __tablename__ = "words"
    id = db.Column(db.Integer, primary_key=True)
    stem = db.Column(db.String(128), unique=True, index=True, nullable=False)
    meaning = db.Column(db.String(128))
    lang = db.Column(db.String(32), nullable=False)
    prompt = db.Column(db.String(128))
    comm = db.Column(db.String(64))
    image_path = db.Column(db.String(128))
    translation = db.Column(db.String(128))
    user_word_rels = db.relationship("Userwordrel", backref="word")
    survey_word_rels = db.relationship("Surveywordrel", backref="word")

    def __repr__(self):
        return self.stem


class Userwordrel(db.Model):
    __tablename__ = "user_word_rels"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    word_id = db.Column(db.Integer, db.ForeignKey("words.id"), index=True)
    transcript = db.Column(db.String(128))
    audio_path = db.Column(db.String(128), unique=True)
    audio_feat = db.Column(db.String(128))
    created_at = db.Column(db.DateTime(), default=datetime.now)
    update_at = db.Column(db.DateTime(), default=datetime.now)

    def __repr__(self):
        return "(%s, %s, %s, %s)" % (self.id, self.user_id, self.word_id, self.audio_path)


class Survey(db.Model):
    __tablename__ = "surveys"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    initiator_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    description = db.Column(db.String(128))
    created_at = db.Column(db.DateTime(), default=datetime.now)
    update_at = db.Column(db.DateTime(), default=datetime.now)
    survey_word_rels = db.relationship("Surveywordrel", backref="survey")

    def __repr__(self):
        return self.name


class Surveywordrel(db.Model):
    __tablename__ = "survey_word_rels"
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey("surveys.id"), index=True)
    word_id = db.Column(db.Integer, db.ForeignKey("words.id"), index=True)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    update_at = db.Column(db.DateTime(), default=datetime.now)

    def __repr__(self):
        return "(%s, %s, %s)" % (self.id, self.survey_id, self.word_id)


class Diff(db.Model):
    __tablename__ = "diffs"
    id = db.Column(db.Integer, primary_key=True)
    uwr_id1 = db.Column(db.Integer, db.ForeignKey("user_word_rels.id"))
    uwr_id2 = db.Column(db.Integer, db.ForeignKey("user_word_rels.id"))
    value = db.Column(db.Float)
    diff_type = db.Column(db.Integer, db.ForeignKey("difftypes.id"))
    uwr1 = db.relationship("Userwordrel", foreign_keys=uwr_id1)
    uwr2 = db.relationship("Userwordrel", foreign_keys=uwr_id2)

    def __repr__(self):
        return self.value


class Difftype(db.Model):
    __tablename__ = "difftypes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True, nullable=False)
    diffs = db.relationship("Diff", backref="difftype")

    def __repr__(self):
        return "<Difftype %r>" % self.name


class Province(db.Model):
    __tablename__ = "province"
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    province_id = db.Column(db.String(64))

    def __repr__(self):
        return "<Province_name %r>" % self.name

    def to_dict(self):
        return {"name": self.name, "id": self.province_id}


class City(db.Model):
    __tablename__ = "city"
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    province_id = db.Column(db.String(64))
    city_id = db.Column(db.String(64))

    def __repr__(self):
        return "<City_name %r>" % self.name

    def to_dict(self):
        return {"name": self.name, "id": self.city_id}


class County(db.Model):
    __tablename__ = "county"
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    city_id = db.Column(db.String(64))
    county_id = db.Column(db.String(64))

    def __repr__(self):
        return "<County_name %r>" % self.name

    def to_dict(self):
        return {"name": self.name, "id": self.county_id}


class Town(db.Model):
    __tablename__ = "town"
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    county_id = db.Column(db.String(64))
    town_id = db.Column(db.String(64))

    def __repr__(self):
        return "<Town_name %r>" % self.name

    def to_dict(self):
        return {"name": self.name, "id": self.town_id}
