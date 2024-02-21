#!/usr/bin/env python3
""" Authentication methods """

import bcrypt


def _hash_password(password: str):
    """ for hashing the password """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
