"""
This module contains the API routes for user-related operations.
Routes:
- GET /users: Retrieves a list of all users.
- POST /users: Creates a new user.
- GET /users/{user_id}: Retrieves a specific user.
- PUT /users/{user_id}: Updates a specific user.
- DELETE /users/{user_id}: Deletes a specific user.
"""

from fastapi import APIRouter, Response, status
from config.db import conn
from schemas.user import userEntity, usersEntity
from models.user import User
from passlib.hash import sha256_crypt as sha256

from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT 

user = APIRouter()

@user.get('/users', response_model=list[User], tags=["users"])
async def find_all_users():
    # print(list(conn.users.user.find()))
    return usersEntity(conn.users.user.find())

@user.post('/users', response_model=User, tags=["users"])
async def create_user(user: User):
    new_user = dict(user)
    new_user["password"] = sha256.encrypt(new_user["password"])
    del new_user["id"]
    id = conn.users.user.insert_one(new_user).inserted_id
    user = conn.users.user.find_one({"_id": id})
    return userEntity(user)

@user.get('/users/{user_id}',response_model=User, tags=["users"])
def find_user(user_id: str):
    return userEntity(conn.users.user.find_one({"_id": ObjectId(user_id)}))

@user.put('/users/{user_id}',response_model=User, tags=["users"])
def update_user(user_id: str, user: User):
    conn.users.user.find_one_and_update({"_id": ObjectId(user_id)}, {"$set": dict(user)})
    return userEntity(conn.users.user.find_one({"_id": ObjectId(user_id)}))

@user.delete('/users/{user_id}',status_code=HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(user_id: str,):
    userEntity(conn.users.user.find_one_and_delete({"_id": ObjectId(user_id)}))
    return Response(status_code=HTTP_204_NO_CONTENT)