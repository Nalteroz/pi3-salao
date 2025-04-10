from flask import jsonify 
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, create_access_token, set_access_cookies, set_refresh_cookies, current_user

from bcrypt import hashpw, gensalt, checkpw

from resources.data import system_db
from resources.models import UserModel, UserSchema, UserRoleEnum

UserBlueprint = Blueprint('user', __name__, url_prefix='/api/user')

@UserBlueprint.route('/')
class RootUserMethodView(MethodView):
    """
        Root route, for user creation and listing.
    """
    @jwt_required()
    @UserBlueprint.response(200, UserSchema(many=True))
    def get(self):
        """
            Return all users on the system, depending on the user's role.
        """
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get users information.')

        users = UserModel.query.all()
        return users

    @jwt_required()
    @UserBlueprint.arguments(UserSchema)
    @UserBlueprint.response(201, UserSchema)
    def post(self, new_user):
        """
            Create a new user.

            Arguments:
            ------------
            new_user : dictionary of user information
        """
        if UserModel.query.filter_by(email=new_user['email']).first():
            abort(409, message='User already exists. If you want to reactivate and you are an admin, update the user instead.')

        new_user['password'] = hashpw(new_user['password'].encode('utf-8'), gensalt())
        user = UserModel(**new_user) 

        system_db.session.add(user)
        system_db.session.commit()

        return user

@UserBlueprint.route('/<int:user_id>')
class SingleUserMethod(MethodView):
    """
        Route for a single user operations.
    """
    @jwt_required()
    @UserBlueprint.response(200, UserSchema)
    def get(self, user_id):
        """
            Get a user by id.
        """
        if current_user.role != UserRoleEnum.ADMIN and current_user.id != user_id:
            abort(403, message='You are an admin, or are not allowed to see this user.')

        user = UserModel.query.get(user_id)
        if not user:
            abort(404, message='User not found.')

        return user
    
    @jwt_required()
    @UserBlueprint.arguments(UserSchema(partial=True))
    @UserBlueprint.response(200, UserSchema)
    def patch(self, user, user_id):
        """
            Update a user by id.

            Arguments:
            ------------
            user : dictionary of user information
        """
        if current_user.role != UserRoleEnum.ADMIN and current_user.id != user_id:
            abort(403, message='You are an admin, or are not allowed to update this user.')

        dbUser = UserModel.query.get(user_id)
        if not dbUser:
            abort(404, message='User not found.')

        if dbUser.deleted_at:
            abort(403, message='The user was deleted.')

        if 'role' in user:
            if current_user.role != UserRoleEnum.ADMIN:
                abort(403, message='You are not an admin, or are not allowed to update this user.')
            else:
                dbUser.role = user['role']

        if 'email' in user:
            if UserModel.query.filter_by(email=user['email']).first():
                abort(409, message='Email is already in use.')
            else:
                dbUser.email = user['email']

        if 'password' in user:
            dbUser.password = hashpw(user['password'].encode('utf-8'), gensalt())

        if 'name' in user:
            dbUser.name = user['name']

        dbUser.updated_by = current_user.id
        system_db.session.add(dbUser)
        system_db.session.commit()

        return dbUser
    
    @jwt_required()
    @UserBlueprint.response(200, UserSchema)
    def delete(self, user_id):
        """
            Delete a user by id.
        """
        if current_user.role != UserRoleEnum.ADMIN and current_user.id != user_id:
            abort(403, message='You are an admin, or are not allowed to delete this user.')

        dbUser = UserModel.query.get(user_id)
        if not dbUser:
            abort(404, message='User not found.')

        system_db.session.delete(dbUser)
        system_db.session.commit()

        return dbUser

@UserBlueprint.route('/login')
class LoginMethod(MethodView):
    @UserBlueprint.arguments(UserSchema(only=('email', 'password')))
    @UserBlueprint.response(200, "Successfully logged in.")
    def post(self, user):
        """
            User login procedure.
        """
        dbUser = UserModel.query.filter_by(email=user['email']).first()
        if not dbUser:
            abort(404, message='User not found.')

        if not checkpw(user['password'].encode('utf-8'), dbUser.password):
            abort(401, message='Invalid password.')

        acess_token = create_access_token(identity=dbUser, expires_delta=False)
        refresh_token = create_access_token(identity=dbUser, fresh=True)
        resp = jsonify({'login': True})
        set_access_cookies(resp, acess_token)
        set_refresh_cookies(resp, refresh_token)

        return resp
    
@UserBlueprint.route('/refreshtoken')
class RefreshTokenMethod(MethodView):
    @jwt_required(refresh=True)
    @UserBlueprint.response(200, "Successfully refreshed token.")
    def post(self):
        """
            Refresh token procedure.
        """
        # Create the new access token
        access_token = create_access_token(identity=current_user)

        # Set the JWT access cookie in the response
        resp = jsonify({'refresh': True})
        set_access_cookies(resp, access_token)
        return resp
    