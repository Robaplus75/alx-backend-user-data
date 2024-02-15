#!/usr/bin/env python3
"""
    API Authentication System
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """ Authentication Class """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ ture or false"""
        if path is None:
            return True
        elif excluded_paths is None or not len(excluded_paths):
            return True
        if path[-1] != '/':
            path += '/'
        if excluded_paths[-1] != '/':
            excluded_paths += '/'

        astericks = [stars[:-1]
                     for stars in excluded_paths if stars[-1] == '*']

        for stars in astericks:
            if path.startswith(stars):
                return False
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Request Flask Object """
        if request is None or 'Authorization' not in request.headers:
            return None
        else:
            return request.headers.get('Authorization')

    def session_cookie(self, request=None):
        """ gets session cookie """
        if request is None:
            return None
        cookie = getenv('SESSION_NAME')
        return request.cookies.get(cookie)

    def current_user(self, request=None) -> TypeVar('User'):
        """ flask request object"""
        return None
