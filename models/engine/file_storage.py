#!/usr/bin/python3

"""
The storage system for this project is defined in this file
The method deployed here is JSON serialization adn deserialization
"""

import json
from json.decoder import JSONDecodeError
from models.base_model import BaseModel


class FileStorage:
    """
    This is  will serve as the database
    """

    """private class varaibles"""
    __objects: dict = {}
    __file_path: str = 'file.json'

    def all(self):
        """Intended to return all instances stored"""
        return FileStorage.__objects

    def new(self, obj):
        """Intended to store a new Object"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj
        return key

    def save(self):
        """serializes objects stored and persist in file"""
        serialized = {
            key: val.to_dict()
            for key, val in self.__objects.items()
        }
        with open(FileStorage.__file_path, "w") as f:
            f.write(json.dumps(serialized))

    def reload(self):
        """de-serialize persisted objects"""
        try:
            deserialized = {}
            with open(FileStorage.__file_path, "r") as f:
                deserialized = json.loads(f.read())
            FileStorage.__objects = {
                key:
                    eval(obj["__class__"])(**obj)
                    for key, obj in deserialized.items()}
        except (FileNotFoundError, JSONDecodeError):
            # There would be no need for error
            pass
