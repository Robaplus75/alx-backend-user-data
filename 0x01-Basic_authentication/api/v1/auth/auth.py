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
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Request Flask Object """
        if request is None or 'Authorization' not in request.headers:
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ flask request object"""
        return None
