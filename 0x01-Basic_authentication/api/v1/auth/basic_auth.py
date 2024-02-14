#!/usr/bin/env python3
""" Basic authentication Class """

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic Auth class """
    def extract_base64_authorization_header(self, authorization_h: str) -> str:
        """ extract the authorization header """
        if authorization_h is None or not isinstance(authorization_h, str):
            return None
        elif 'Basic' not in authorization_h:
            return None
        return authorization_h[6:]
