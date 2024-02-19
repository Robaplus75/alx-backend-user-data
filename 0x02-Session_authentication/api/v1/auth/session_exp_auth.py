#!/usr/bin/env python3
"""
contains sessionExpAuth class
"""
from datetime import datetime, timedelta, timedelta
from api.v1.auth.session_auth import SessionAuth
from os import getenv


class SessionExpAuth(SessionAuth):
    """ sessionExpAuth class """

    def __init__(self):
        """ initailization """
        try:
            session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            session_duration = 0
        self.session_duration = session_duration

    def create_session(self, user_id=None):
        """ returns session Id """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {'user_id': user_id, 'created_at': datetime.now()}
        SessionAuth.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ for Returning user_id for a session_id """
        if session_id is None:
            return None
        if session_id not in SessionAuth.user_id_by_session_id.keys():
            return None
        session_dictionary = SessionAuth.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dictionary["user_id"]
        if "created_at" not in session_dictionary.keys():
            return None
        create_time = session_dictionary["created_at"]
        time_delta = timedelta(seconds=self.session_duration)
        if (create_time + time_delta) < datetime.now():
            return None
        return session_dictionary["user_id"]
