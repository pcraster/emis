# from flask import g, jsonify
# from flask.ext.httpauth import HTTPBasicAuth
# from ..model import User, AnonymousUser
# from . import api
# from .error import unauthorized, forbidden
# 
# 
# auth = HTTPBasicAuth()
# 
# 
# @auth.verify_password
# def verify_password(
#         email_or_token,
#         password):
# 
#     status = False
# 
#     if email_or_token == "":
#         g.current_user = AnonymousUser()
#         status = True
#     else:
#         if password == "":
#             g.current_user = User.verify_auth_token(email_or_token)
#             g.token_used = True
#             status = g.current_user is not None
#         else:
#             user = User.query.filter_by(email=email_or_token).first()
# 
#             if user:
#                 g.current_user = user
#                 g.token_used = False
#                 status = user.verify_password(password)
# 
#     return status
# 
# 
# @auth.error_handler
# def auth_error():
#     return unauthorized("Invalid credentials")
# 
# 
# @api.before_request
# @auth.login_required
# def before_request():
#     if not g.current_user.is_anonymous and \
#             not g.current_user.confirmed:
#         return forbidden("Unconfirmed account")
# 
# 
# @api.route("/token")
# def get_token():
#     if g.current_user.is_anonymous or g.token_used:
#         return unauthorized("Invalid credentials")
#     return jsonify({
#             "token": g.current_user.generate_auth_token(expiration=3600),
#             "expiration": 3600
#         })
