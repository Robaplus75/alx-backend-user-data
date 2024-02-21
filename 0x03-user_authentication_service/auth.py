#!/usr/bin/env python3
"""Athentication module"""

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import bcrypt
import uuid
from db import DB
from user import User


def _generate_uuid() -> str:
    """generates id"""
    return str(uuid.uuid4())


def _hash_password(password: str) -> str:
    """returns hashed password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Class for authenticating"""

    def __init__(self):
        """Initialization"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers User"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists.".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def create_session(self, email: str) -> str:
        """creates a session"""
        session_id = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None
    
    def valid_login(self, email: str, password: str) -> bool:
        """checks if its a valid Login"""
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
        except NoResultFound:
            pass
        return False

    def get_user_from_session_id(self, session_id: str) -> str:
        """gets the user from a sessin id"""
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user.email
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys a session"""
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            return None

    def update_password(self, reset_token: str, password: str) -> str:
        """Updates Password"""
        if reset_token is None or password is None:
            return None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password,
                             reset_token=None)
    
    def get_reset_password_token(self, email: str) -> str:
        """resets password token"""
        updated_token = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, reset_token=updated_token)
            return updated_token
        except NoResultFound:
            raise ValueError
