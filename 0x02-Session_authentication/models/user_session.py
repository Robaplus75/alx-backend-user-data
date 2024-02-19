#!/usr/bin/env python3
""" User Session"""
from os import path
import json
import uuid
from models.base import Base
from typing import TypeVar, List, Iterable


class UserSession(Base):
    """ UserSession Class """
    def __init__(self, *args: list, **kwargs: dict):
        """ Initialization  """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
