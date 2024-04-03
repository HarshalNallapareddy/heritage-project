from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import mimetypes
import request_db as db
import hashlib

class User(BaseModel):
    userid: str
    username: str
    email: str
    phone: str
    password: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/users/createuser/")
async def login(user: User):
    print(user)
    password_bytes = user.password.encode('utf-8')
    user.password = hashlib.sha256(password_bytes).hexdigest()
    db.add_user(user.userid, user.username, user.email, user.phone, user.password)

@app.get("/users/getuser/{username}")
async def get_user(username: str):
    user = db.get_user(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/login/")
async def login(username: str, password: str):
    user = db.get_user(username)
    password_bytes = password.encode('utf-8')
    hashed_password = hashlib.sha256(password_bytes).hexdigest()
    
    if user is None or user.password != hashed_password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}

