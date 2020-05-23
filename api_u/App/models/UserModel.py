# coding=utf-8
import hashlib

from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from flask import abort
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from App.ext import db
from App.models.ModelUtil import BaseModel
from datetime import datetime
import jwt
import time

skey = 'top secret!'
token_serializer = Serializer(skey, expires_in=3600)
auth = HTTPTokenAuth('Bearer')


# 权限判定
# 读
READ = 1
# 赞
PRAISE = 2
# 写
WRITE = 4


# Table
class Labs(BaseModel, db.Model):
    __tablename__ = 'Labs'

    lab_id = db.Column(db.Integer(), primary_key=True)
    lab_name = db.Column(db.String(50))
    lab_info = db.Column(db.String(1000))
    lab_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_delete = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Labs %r>' % self.lab_name


class Mentors(BaseModel, db.Model):
    __tablename__ = 'Mentors'

    mentor_id = db.Column(db.Integer(), primary_key=True)
    mentor_name = db.Column(db.String(50))
    mentor_password = db.Column(db.String(128))
    lab_id = db.Column(db.Integer(), db.ForeignKey('Labs.lab_id'))
    is_delete = db.Column(db.Boolean, default=False)
    #is_login =  db.Column(db.Boolean, default=False)


    def men_password(self, password):
        self.mentor_password = generate_password_hash(password)
        return self.mentor_password

    def generate_auth_token(self, expires_in=600):
        return token_serializer.dumps({'id': self.mentor_id}).decode('utf-8')

    @auth.verify_token
    def verify_auth_token(token):
        try:
            data = token_serializer.loads(token)
            # data = jwt.decode(token, secret_key, algorithms=['HS256'])
        except:
            return False
        if 'id' in data:
            return Mentors.query.get(data['id'])

    # 验证密码
    def verify_password(self, password):
        return check_password_hash(self.mentor_password, password)

    # 权限判定
    def check_permission(self, permission):
        return self.mentor_password & permission == permission

    def __repr__(self):
        return '<Mentors %r>' % self.mentor_name


class Students(BaseModel, db.Model):
    __tablename__ = 'Students'

    student_id = db.Column(db.Integer(), primary_key=True)
    student_name = db.Column(db.String(50))
    student_password = db.Column(db.String(128))
    lab_id = db.Column(db.Integer(), db.ForeignKey('Labs.lab_id'))
    admin = db.Column(db.Boolean, default=False)
    is_delete = db.Column(db.Boolean, default=False)
    #is_login = db.Column(db.Boolean, default=False)

    @property
    def stu_password(self):
        return self.student_password

    @stu_password.setter
    def stu_password(self, password):
        self.student_password = generate_password_hash(password)

    # 验证密码
    def verify_password(self, password):
        return check_password_hash(self.student_password, password)

    # 权限判定
    def check_permission(self, permission):
        return self.stu_permission & permission == permission

    def __repr__(self):
        return '<Students %r>' % self.student_name