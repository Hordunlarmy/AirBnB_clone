#!/usr/bin/env python3
from uuid import uuid4 as id
from datetime import datetime
import models


class BaseModel:
    """ The Birth Of BaseModel """

    def __init__(self, *args, **kwargs):
        """ Inintialization Of Instances """

        if kwargs is not None and len(kwargs) != 0:
            for key in kwargs:
                time = datetime.now().isoformat()
                if key == "created_at":
                    self.__dict__["created_at"] = datetime.fromisoformat(
                        time)
                elif key == "updated_at":
                    self.__dict__["updated_at"] = datetime.fromisoformat(
                        time)
                else:
                    self.__dict__[key] = kwargs[key]

        else:
            self.id = str(id())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """Format string based on [<class name>] (<self.id>) <self.__dict__>"""

        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        updates the public instance attribute updated_at with the current
        datetime
        """

        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        returns a dictionary containing all keys/values of __dict__ of the
        instance
        """

        to_dict = self.__dict__.copy()
        to_dict["__class__"] = self.__class__.__name__
        to_dict["created_at"] = datetime.now().isoformat()
        to_dict["updated_at"] = datetime.now().isoformat()

        return (to_dict)
