#!/usr/bin/env python3
""" Session Authentication """

from typing import Dict
from flask.globals import session
import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """ Session  auth class"""
    user_id_by_session_id = {}
    def create_session(self, user_id: str = None) -> str:
        """ Create Session """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ get session _id """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id, None)
    def current_user(self, request=None):
        """ return current user"""
        cookie = self.session_cookie(request)
        session_user_id = self.user_id_for_session_id(cookie)
        user_id = User.get(session_user_id)
        return user_id
    def destroy_session(self, request=None):
        """ deletes session """
        cookie_data = self.session_cookie(request)
        if cookie_data is None:
            return False
        if not self.user_id_for_session_id(cookie_data):
            return False
        del self.user_id_by_session_id[cookie_data]
        return True
