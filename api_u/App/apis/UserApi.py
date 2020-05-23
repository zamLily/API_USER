# coding=utf-8
import uuid

from flask import abort, request
from flask_restful import Resource, reqparse, fields, marshal, marshal_with
from werkzeug.security import generate_password_hash, check_password_hash
from App.ext import cache

from App.models.UserModel import auth, Labs, Mentors, Students


# 输出参数
parser = reqparse.RequestParser()
parser.add_argument('user', required=True, help="请输入操作者身份mentors/students")
parser.add_argument('u_name', required=True, help="请输入用户名")
parser.add_argument('u_password', required=True, help="请输入密码")

# 比较常见的位置直接放在   ?action=login, register
parser.add_argument('action', required=True, help="请提供具体操作")


# 内层参数格式化
mentors_fields = {
    'mentor_name': fields.String,
    #'mentor_permission': fields.Integer,
}

# 外层输出参数格式化
response_mentors_fields = {
    'status': fields.Integer,
    'msg': fields.String,
    'data': fields.Nested(mentors_fields)
}


# 外层输出参数格式化  + token
response_mentors_token_fields = {
    'status': fields.Integer,
    'msg': fields.String,
    'token': fields.String,
    'data': fields.Nested(mentors_fields)
}



def login_mentors(user, u_password):

    if user:

        if not user.verify_password(u_password):

            data['status'] = 406
            data['msg'] = 'password fail'
            return data

        elif user.is_delete:
            data['status'] = 900
            data['msg'] = 'user is deleted'
            return data

        else:

            data['data'] = user

            token = user.generate_auth_token(600)
            #token = str(uuid.uuid4())  # token 需要转换为字符串

            # 将用户token 存到缓存中 可以根据token 找到用户id 也可以根据用户id 找到token
            # key: 使用token  值:用户id
            # 第一个参数是键，这个主要是用来获取这个缓存的值。第二个参数是值。第三个参数是秒
            #cache.set(token, user.mentor_id, timeout=60*60*24*7)
            #if not cache.get(token):
            #    abort(403, message="fail to set token")
            data['token'] = token

            return marshal(data, response_mentors_token_fields)

    else:
        data['status'] = 406
        data['msg'] = 'user not exist'
        return data


def register_mentors(user, u_name, u_password):

    user.mentor_name = u_name

    # 密码做数据安全处理
    # user.set_password(u_password)

    # 最终方法  密码做数据安全处理

    user.mentor_password = user.men_password(u_password)

    user.save()


# 用户注册登录 操作  其中密码做了数据安全
class UsersResource(Resource):

    def post(self):
        global user

        args = parser.parse_args()

        users = args.get("user")
        action = args.get("action")
        u_name = args.get("u_name")
        u_password = args.get("u_password")

        global data
        data = {
            "status": 201,
            "msg": 'ok'
        }

        if users == "mentors":

            #def login(User, u_name, u_password, data)
            if action == "login":       # 用户登录
                token = request.args.get("token")
                if token:
                    abort(401, message="User has already login.")
                else:
                    user = Mentors.query.filter(Mentors.mentor_name.__eq__(u_name)).one_or_none()

                    login_mentors(user, u_password)


            elif action == "register":   # 用户注册

                #def register(User, u_name, u_password)
                user = Mentors()
                register_mentors(user, u_name, u_password)


           # elif action == "logout":  # 用户登出
               # user = Mentors()
               # cache.


        else:
            pass

        data['data'] = user
        return marshal(data, response_mentors_token_fields)
        #return data

    def get(self):
        return marshal(data, response_mentors_token_fields)


"""
# 更新用户信息不更改用户名，只改密码
parser_user = reqparse.RequestParser()
parser_user.add_argument('u_password', required=True, help='请输入新密码')


# 单个用户数据操作  查询 修改 删除
class UserResource(Resource):
    # 根据 id 获取用户信息
    @marshal_with(response_user_fields)
    def get(self, id):

        user = User.query.get(id)

        data = {
            "status": 200,
            "msg": 'ok',
            'data': user,
        }
        return data

    # 根据 id 修改用户信息 --> 密码修改
    @marshal_with(response_user_fields)
    def post(self, id):

        args = parser_user.parse_args()

        u_password = args.get("u_password")

        user = User.query.get(id)

        user.u_password = u_password

        user.save()

        data = {
            "status": 200,
            "msg": 'password change ok',
            'data': user,
        }
        return data

    # 根据 id 删除某个用户   Model中应该设计一个字段 is_delete 来判断是否已删除
    @marshal_with(response_user_fields)
    def delete(self, id):

        user = User.query.get(id)

        user.is_delete = True       # is_delete = 1  表示删除用户

        user.save()

        data = {
            "status": 200,
            "msg": 'delete ok',
            "data": user,
        }
        return data
"""