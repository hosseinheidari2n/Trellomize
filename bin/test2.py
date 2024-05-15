import os
import tempfile
from typing import List

class User:
    def __init__(self, username: str):
        self.UserName = username

class Update:
    def __init__(self, title: str, content: str, creator: User):
        self.title = title
        self.content = content
        self.creator = creator

