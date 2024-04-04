from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from pydantic import BaseModel, ValidationError
import mimetypes
import request_db as db

class User(BaseModel):
    userid: str
    username: str
    email: str
    phone: str
    password: str

app = Flask(__name__)
# CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/tree')
def tree():
    return render_template('tree.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/add_family_member')
def add_family_member():
    return render_template('add_family_member.html')


@app.route("/users/createuser/", methods=["POST"])
def create_user():
    username = request.json.get("username")
    email = request.json.get("email")
    phone = request.json.get("phone")
    password = request.json.get("password")
    conpassword = request.json.get("conpassword")
    
    if password != conpassword:
        return jsonify({"detail": "Passwords don't match."}), 401
    hash_password = hash(password)
    db.add_user(username, email, phone, hash_password)
    return jsonify({"message": "Sign up successful"})

@app.route("/users/getuser/<username>", methods=["GET"])
def get_user(username):
    user = db.get_user(username)
    if user is None:
        return jsonify({"detail": "User not found"}), 404
    return jsonify(user)

@app.route("/users/login/", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    user = db.get_user(username)
    hashed_password = hash(password)
    
    if user is None or user.password != hashed_password:
        return jsonify({"detail": "Invalid username or password"}), 401
    return jsonify({"message": "Login successful"})


@app.route("/generatetree/<username>", methods=["GET"])
def generate_tree(username):
    try:
        treeID = db.getTreeIDfromUserName(username)
        # list of memberIDs
        family_members = db.getFamilyMemberIDsfromTreeID(treeID)
        # list of relationshipIDs
        relationshipIds = db.getRelationshipIDsfromTreeID(treeID)

        connections = []
        for rel in relationshipIds:
            rel_tuple = db.getMarriagefromRelationshipID(rel)
            if rel_tuple is not None:  # this means the relationship is a marriage
                new_connection = {}
                new_connection["type"] = "marriage"
                new_connection["source"] = rel_tuple[2]
                new_connection["target"] = rel_tuple[3]
                connections.append(new_connection)
            else:
                rel_tuple = db.getParentChildfromRelationshipID(rel)
                if rel_tuple is None:
                    return jsonify({"detail": "Invalid relationship"}), 500
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

        return jsonify({"nodes": nodes, "connections": connections})
    except Exception as e:
        return jsonify({"detail": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)