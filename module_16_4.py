from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get('/users')
async def get_() -> list[User]:
    return users


@app.post('/user/{username}/{age}')
async def post_(message: User) -> str:
    if len(users) == 0:
        message.id = 1
    else:
        last_user = users[-1]
        message.id = last_user.id+1
    users.append(message)
    return f'User {message.id} is registered'


@app.put('/user/{user_id}/{username}/{age}')
async def put_(user_id: int, message: User) -> str:
    try:
        edit_user = users[user_id-1]
        edit_user.username = message.username
        edit_user.age = message.age
        return f'The user {user_id} has been updated'
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def delete_(user_id: int) -> str:
    try:
        delete_user = users[user_id-1]
        users.remove(delete_user)
        return f'User {user_id} has been deleted'
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')
