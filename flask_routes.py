from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from pydantic import BaseModel, ValidationError
import mimetypes
import request_db as db
from flask_bcrypt import generate_password_hash, check_password_hash

class User(BaseModel):
    userid: str
    username: str
    email: str
    phone: str
    password: str


class FamilyMember:
    def __init__(self, treeid, memberid, fullname, dateofbirth, dateofdeath, pictureurl, streetaddress, city, state, country, zipcode, email, phone):
        self.treeid = treeid
        self.memberid = memberid
        self.fullname = fullname
        self.dateofbirth = dateofbirth
        self.dateofdeath = dateofdeath
        self.pictureurl = pictureurl
        self.streetaddress = streetaddress
        self.city = city
        self.state = state
        self.country = country
        self.zipcode = zipcode
        self.email = email
        self.phone = phone




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
    json_data = generate_tree("john")
    print(json_data)
    print(json_data)
    return render_template('tree.html', json_data=json_data)

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/add_family_member')
def add_family_member_page():
    # fetch json from generate_tree method
    return render_template('add_family_member.html')

@app.route('/add_family_relationship')
def add_family_relationship_page():
    # fetch json from generate_tree method
    return render_template('add_relationship.html')


@app.route("/users/createuser/", methods=["POST"])
def create_user():
    username = request.json.get("username")
    email = request.json.get("email")
    phone = request.json.get("phone")
    password = request.json.get("password")
    conpassword = request.json.get("conpassword")


    print(username, email, phone, password, conpassword)

    print("hello")

    if password != conpassword:
        return jsonify({"detail": "Passwords don't match."}), 401
    # hash_password = hash(password)
    hash_password = generate_password_hash(password).decode('utf-8')
    # print(hash_password)
    db.add_user(username, email, phone, hash_password)
    print(f"Created user successfully: {username, email, phone}")
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

    # print("username: ", username)
    # print("password: ", password)
    user = db.get_user_by_username(username)
    print(user)
    if user is None:
        return jsonify({"detail": "Invalid username or password"}), 401

    stored_hashed_password = user[-1]

    if check_password_hash(stored_hashed_password, password):
        print("Login successful")
        return jsonify({"message": "Login successful"})
    else:
        print("Invalid username or password")
        return jsonify({"detail": "Invalid username or password"}), 401



@app.route("/generatetree/<username>", methods=["GET"])
def generate_tree(username):
    try:
        treeID = db.getTreeIDfromUserName(username)
        # list of memberIDs
        family_members = db.getFamilyMemberIDsfromTreeID(treeID)
        # list of relationshipIDs
        relationshipIds = db.getRelationshipIDsfromTreeID(treeID)

        print(treeID)
        print(family_members)
        print(relationshipIds)

        print("br 1")

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

        return_dict = {"nodes": nodes, "connections": connections}
        print(return_dict)
        return jsonify(return_dict)
    
    except Exception as e:
        print("Uhhh ohhhh")
        return jsonify({"detail": str(e)}), 500
    

@app.route("/deleteuser/<username>", methods=["DELETE"])
def delete_user(username):
    userid = db.get_user_by_username(username)
    if userid is None:
        return jsonify({"detail": "User not found"}), 404
    db.delete_user(userid)


@app.route("/addfamilymember/", methods=["POST"])
def add_family_member():
    data = request.json
    member = FamilyMember(data["treeid"], data["memberid"], data["fullname"], data["dateofbirth"], data["dateofdeath"], data["pictureurl"], data["streetaddress"], data["city"], data["state"], data["country"], data["zipcode"], data["email"], data["phone"])
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
    db.add_family_member(treeid=member_sanitized.treeid, fullname=member_sanitized.fullname, dateofbirth=member_sanitized.dateofbirth, dateofdeath=member_sanitized.dateofdeath, pictureurl=member_sanitized.pictureurl, streetaddress=member_sanitized.streetaddress, city=member_sanitized.city, state=member_sanitized.state, country=member_sanitized.country, zipcode=member_sanitized.zipcode, email=member_sanitized.email, phone=member_sanitized.phone)
    return jsonify({"message": "Family member added successfully"})


if __name__ == "__main__":
    app.run(debug=True)