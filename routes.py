from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import mimetypes
import request_db as db
from datetime import date

class User(BaseModel):
    username: str
    email: str
    phone: str
    password: str

class FamilyMember(BaseModel):
    treeid: int
    fullname: str
    dateofbirth: str
    dateofdeath: str
    pictureurl: str
    streetaddress: str
    city: str
    state: str
    country: str
    zipcode: str
    email: str
    phone: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/users/createuser/")
async def create_user(user: User):
    print(user)
    user.password = hash(user.password)
    if db.get_user(user.username) is not None:
        raise HTTPException(status_code=400, detail="Username already exists")
    db.add_user(user.username, user.email, user.phone, user.password)

@app.get("/users/getuser/{username}")
async def get_user(username: str):
    user = db.get_user(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/login/")
async def login(username: str, password: str):
    user = db.get_user(username)
    hashed_password = hash(password)
    
    if user is None or user.password != hashed_password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}

@app.get("/generatetree/{username}")
async def generate_tree(username : str):
    treeID = db.getTreeIDfromUserName(username)
    # list of memberIDs
    family_members = db.getFamilyMemberIDsfromTreeID(treeID)
    # list of relationshipIDs
    relationshipIds = db.getRelationshipIDsfromTreeID(treeID)

    connections = []
    for rel in relationshipIds:
        rel_tuple = db.getMarriagefromRelationshipID(rel)
        if rel_tuple is not None: # this means the relationship is a marriage
            new_connection = {}
            new_connection["type"] = "marriage"
            new_connection["source"] = rel_tuple[2]
            new_connection["target"] = rel_tuple[3]
            connections.append(new_connection)
        else:
            rel_tuple = db.getParentChildfromRelationshipID(rel)
            if rel_tuple is None:
                raise HTTPException(status_code=500, detail="Invalid relationship")
            new_connection = {}
            new_connection["type"] = "parent-child"
            new_connection["source"] = rel_tuple[2]
            new_connection["target"] = rel_tuple[3]
            connections.append(new_connection)

    nodes = []
    for memberId in family_members:
        new_node = {}
        member = db.get_family_member(memberId)
        new_node["id"] = memberId
        new_node["name"] = member[2]
        new_node["dateOfBirth"] = member[3]
        new_node["hobbies"] = db.getHobbyNamesfromMemberID(memberId)
        nodes.append(new_node)

    return {"nodes": nodes, "connections": connections}

@app.delete("/deleteuser/{username}")
async def delete_user(username: str):
    userid = db.get_user_by_username(username)
    if userid is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete_user(userid)

@app.post("/addfamilymember/")
async def add_family_member(member: FamilyMember):
    default_values = {
        "dateofdeath": "NULL",
        "pictureurl": "NULL",
        "streetaddress": "NULL",
        "city": "NULL",
        "state": "NULL",
        "country": "NULL",
        "zipcode": "NULL",
        "email": "NULL",
    }
    member_sanitized = {key: default_values[key] if value is None else value for key, value in vars(member).items()}
    db.add_family_member(treeid=member_sanitized["treeid"], fullname=member_sanitized["fullname"], dateofbirth=member_sanitized["dateofbirth"], dateofdeath=member_sanitized["dateofdeath"], pictureurl=member_sanitized["pictureurl"], streetaddress=member_sanitized["streetaddress"], city=member_sanitized["city"], state=member_sanitized["state"], country=member_sanitized["country"], zipcode=member_sanitized["zipcode"], email=member_sanitized["email"], phone=member_sanitized["phone"])
            

    