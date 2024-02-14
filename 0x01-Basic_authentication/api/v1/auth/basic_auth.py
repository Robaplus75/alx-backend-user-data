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

    def decode_base64_authorization_header(self, b64_auth_header: str) -> str:
        """ Decodes base64 authorization """
        if b64_auth_header is None or not isinstance(b64_auth_header, str):
            return None
        try:
            b64 = base64.b64decode(b64_auth_header)
            b64_decode = b64.decode('utf-8')
        except Exception:
            return None
        return b64_decode
