#!/usr/bin/env python3
"""The Flask app"""

from flask.helpers import make_response
from auth import Auth
from db import DB
from flask import Flask, request, abort, redirect, jsonify
from user import User

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """Welcome route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """sessions route"""
    user_request = request.form
    user_password = user_request.get('password', '')
    user_email = user_request.get('email', '')
    valid_log = AUTH.valid_login(user_email, user_password)
    if not valid_log:
        abort(401)
    response = make_response(jsonify({"email": user_email,
                                      "message": "logged in"}))
    response.set_cookie('session_id', AUTH.create_session(user_email))
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """Delete session route"""
    user_cookie = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(user_cookie)
    if user_cookie is None or user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """hands post request for /users route"""
    password = request.form.get('password')
    email = request.form.get('email')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """profile route"""
    user_cookie = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(user_cookie)
    if user_cookie is None or user is None:
        abort(403)
    return jsonify({"email": user}), 200


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """reset passoword put route"""
    reset_token = request.form.get('reset_token')
    user_email = request.form.get('email')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
    except Exception:
        abort(403)
    return jsonify({"email": user_email, "message": "Password updated"}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token_route() -> str:
    """reset password route"""
    user_request = request.form
    user_email = user_request.get('email', '')
    is_registered = AUTH.create_session(user_email)
    if not is_registered:
        abort(403)
    token = AUTH.get_reset_password_token(user_email)
    return jsonify({"email": user_email, "reset_token": token})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
