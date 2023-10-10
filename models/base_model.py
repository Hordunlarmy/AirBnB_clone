#!/usr/bin/env python3
from uuid import uuid4 as id
from datetime import datetime


class BaseModel:
    """ The Birth Of BaseModel """

    def __init__(self, *args, **kwarg):
        """ Inintialization Of Instances """

        self.id = str(id())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __str__(self):
        """Format string based on [<class name>] (<self.id>) <self.__dict__>"""

        return f"{type(self).__name__} ({self.id}) {self.__dict__}"

    def save(self):
        """
        updates the public instance attribute updated_at with the current
        datetime
        """

        self.updated_at = datetime.now()

    def to_dict(self):
        """
        returns a dictionary containing all keys/values of __dict__ of the
        instance
        """

        to_dict = self.__dict__.copy()
        to_dict[__class__] = type(self).__name__
        to_dict["created_at"] = datetime.now().isoformat()
        to_dict["updated_at"] = datetime.now().isoformat()

        return (to_dict)
