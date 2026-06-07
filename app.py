from dotenv import load_dotenv
from copy import deepcopy
from typing import *
from typeddicts import *
import fastapi as fapi
import supabase as sb
import postgrest as sbt
import os

def includes(a: str, b: str) -> bool:
    return a.find(b) != -1

load_dotenv()

client: sb.Client = sb.create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
table: sbt.SyncRequestBuilder = client.from_("persons")
app = fapi.FastAPI()

type Status = Literal["success", "error"]
type Data = tuple[Status, Optional[str]]

def add_user(user: BaseUser) -> Data:
    try:
        table.insert({"name": user["name"], "age": user["age"]}).execute()
        return ("success", None)
    except Exception as e:
        return ("error", str(e))
    
def lmf(seq: Sequence[Any], lim: int) -> Sequence[Any]:
    new_seq: Sequence[Any] = []

    try:
        for idx in range(0, lim):
            new_seq.append(seq[idx])
    except IndexError:
        new_seq = deepcopy(seq)

    return new_seq

@app.get("/persons/get/")
def get_users(name: Optional[str] = None, age: Optional[str] = None, limit: Optional[int] = None):
    users: Union[sbt.APIResponse, Sequence[Any]] = table.select("*").execute()
    users = users.data
    
    if name:
        users = list(filter(lambda x: includes(x["name"].lower(), name.lower()), users)) # name is not null, but type-checker thinks its nullable
        if age:
            users = list(filter(lambda x: x["age"] == age, users))
            if limit:
                users = lmf(users, limit)
                return users
            return users
        if limit:
            users = lmf(users, limit)
            if age:
                users = list(filter(lambda x: x["age"] == age, users))
                return users
            return users
        return users
    
    if age:
        users = list(filter(lambda x: x["age"] == age, users))
        if limit:
            users = lmf(users, limit)
            if name:
                users = list(filter(lambda x: includes(x["name"].lower(), name.lower()), users))
                return users
            return users
        if name:
            users = list(filter(lambda x: includes(x["name"].lower(), name.lower()), users))
            if limit:
                users = lmf(users, limit)
                return users
            return users

        return users
    
    if limit:
        users = lmf(users, limit)
        if name:
            users = list(filter(lambda x: includes(x["name"].lower(), name.lower()), users))
            if age:
                users = list(filter(lambda x: x["age"] == age, users))
                return users
            return users
        if age:
            users = list(filter(lambda x: x["age"] == age, users))
            if name:
                users = list(filter(lambda x: includes(x["name"].lower(), name.lower()), users))
            return users
        return users
    return users

@app.post("/persons/add")
def post_user(user: BaseUser | list[Any]):
    if isinstance(user, BaseUser):
        return add_user(user)
    else:
        results: Mapping[str, Data] = {}

        for _user in user:
            result = add_user(_user)

            results[_user["name"]] = (result[0], result[1])
        
        return results
        