#!/usr/bin/python3

"""
The storage system for this project is defined in this file
The method deployed here is JSON serialization adn deserialization
"""

import json
from json.decoder import JSONDecodeError
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


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
            json.dump(serialized, f)

    def reload(self):
        """de-serialize persisted objects"""
        try:
            deserialized = {}
            with open(FileStorage.__file_path, "r") as f:
                deserialized = json.load(f)
            for key, obj in deserialized.items():
                cls_name = obj["__class__"]
                if cls_name == "BaseModel":
                    FileStorage.__objects[key] = BaseModel(**obj)
                elif cls_name == "User":
                    FileStorage.__objects[key] = User(**obj)
                elif cls_name == "State":
                    FileStorage.__objects[key] = State(**obj)
                elif cls_name == "City":
                    FileStorage.__objects[key] = City(**obj)
                elif cls_name == "Amenity":
                    FileStorage.__objects[key] = Amenity(**obj)
                elif cls_name == "Place":
                    FileStorage.__objects[key] = Place(**obj)
                elif cls_name == "Review":
                    FileStorage.__objects[key] = Review(**obj)
        except (FileNotFoundError, JSONDecodeError):
            pass
