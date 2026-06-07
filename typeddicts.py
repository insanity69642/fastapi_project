from pydantic import BaseModel
from dataclasses import dataclass


@dataclass
class BaseUser(BaseModel):
    def __getitem__(self, key: str):
        if key == "name":
            return self.name
        elif key == "age":
            return self.age
        else:
            raise KeyError("That key does not exist")

    name: str
    age: int