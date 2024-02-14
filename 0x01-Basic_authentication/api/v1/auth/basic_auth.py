#!/usr/bin/env python3
""" Basic authentication Class """

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic Auth class """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ extract the authorization header """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        elif 'Basic' not in authorization_header:
            return None
        return authorization_header[6:] 
