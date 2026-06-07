from typing import TypedDict, NotRequired

class ClientConnectProps(TypedDict):
    url: str
    key: str

class User(TypedDict, total = True):
    person_id: NotRequired[int]
    name: str
    age: int