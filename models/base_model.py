#!/usr/bin/python3

from uuid import uuid4
from datetime import datetime

class BaseModeel:
    def __init__(self):
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.update_at = datetime.now()

    def __str__(self):
        pass
