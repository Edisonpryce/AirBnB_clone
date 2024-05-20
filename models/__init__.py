#!/usr/bin/python3

""" Initializes  the module global variables """

from models.engine.file_storage import FileStorage
""" Retrieving the storage instance """
storage = FileStorage()
storage.reload()
