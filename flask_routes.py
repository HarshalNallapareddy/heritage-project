from flask import Flask, request, redirect, session, jsonify, render_template, url_for
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
    def __init__(self, treeid, fullname, dateofbirth, dateofdeath, pictureurl, streetaddress, city, state, country, zipcode, email, phone):
        self.treeid = treeid
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


@app.route('/logout')
def logout():
    session.pop("username", None) # clear username variable from session
    return render_template('login.html')



@app.route('/tree')
def tree():
    # json_data = generate_tree("john")
    return render_template('tree.html')



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




@app.route("/deleterelationship", methods=["POST"])
def delete_relationship():
    try:
        rel_id = request.json.get("rel_id")
        print(f"\n\n\nDELETING {rel_id}")
        db.delete_relationship(rel_id)
        return jsonify({"message": "Relationship deleted successfully"})
    except:
        return jsonify({"message": "Database error. Relationship deletion not successful."}), 401
    


@app.route("/createmarriage", methods=["POST"])
def create_marriage():
    try:
        spouse1 = request.json.get("spouse1_id")
        spouse2 = request.json.get("spouse2_id")

        familymemberids = db.getFamilyMemberIDsfromTreeID(session['treeid'])
        familymemberids = [x[0] for x in familymemberids]

        if spouse1 not in familymemberids or spouse2 not in familymemberids:
            return jsonify({"message", "Spouse 1 and Spouse 2 not found. Please enter their full names properly."}), 401
        
        db.add_marriagerelationship(session['treeid'], spouse1, spouse2)

        return jsonify({"message": "Marriage Creation successful"})

    except:
        return jsonify({"message", "Database error. Relationship creation not successful."}), 401




@app.route("/createparentchild", methods=["POST"])
def create_parent_child():
    try:
        parent = request.json.get("parent_id")
        child = request.json.get("child_id")

        familymemberids = db.getFamilyMemberIDsfromTreeID(session['treeid'])
        familymemberids = [x[0] for x in familymemberids]



        print(parent, child, familymemberids)
        if parent not in familymemberids or child not in familymemberids:
            return jsonify({"message", "Parent and Child not found. Please enter their full names properly."}), 401
        
        db.add_parentchildrelationship(session['treeid'], parent, child)

        return jsonify({"message": "Parent-Child Creation successful"})

    except:
        return jsonify({"message", "Database error. Relationship creation not successful."}), 401





@app.route("/users/createuser/", methods=["POST"])
def create_user():
    username = request.json.get("username")
    email = request.json.get("email")
    phone = request.json.get("phone")
    password = request.json.get("password")
    conpassword = request.json.get("conpassword")

    # make sure user is not already in session
    if 'username' in session:
        return jsonify({"detail": "User already logged in"}), 401

    if password != conpassword:
        return jsonify({"detail": "Passwords don't match."}), 401
    # hash_password = hash(password)
    
    hash_password = generate_password_hash(password).decode('utf-8')
    # print(hash_password)
    db.add_user(username, email, phone, hash_password)

    print(f"Created user successfully: {username, email, phone}")
    # add user to session
    session['username'] = username
    session['userid'] = db.get_user_by_username(username)[0]

    # create a tree for the user
    session['treeid'] = db.add_tree(f'{username}_tree', session['userid'])

    print("-------------------------------")
    print("CREATED USER!!!")
    print(session['username'], session['userid'], session['treeid'])
    print("-------------------------------")



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
        session["username"] = username
        session["userid"] = db.get_user_by_username(username)[0]
        session["treeid"] = db.getTreeIDfromUserName(username)
        print("-------------------")
        print(session["username"], session["userid"], session["treeid"])

        # return redirect(url_for('tree'))
        return jsonify({"message": "Login successful"})

    else:
        print("Invalid username or password")
        return jsonify({"detail": "Invalid username or password"}), 401



@app.route("/generatetree/", methods=["GET"])
def generate_tree():
    try:
        response = db.get_tree_data(session['treeid'])
        if len(response) == 0:
            return jsonify({"detail": "No data found"}), 404
        
        else:
            if "detail" in response:
                return jsonify(response), 500
            else:
                return jsonify(response)
    
    except Exception as e:
        print("Uhhh ohhhh")
        print(e)
        print(str(e))
        return jsonify({"detail": str(e)}), 500




# @app.route("/generatetree/", methods=["GET"])
# def generate_tree():
#     try:
#         # treeID = db.getTreeIDfromUserName(session.user)
#         # list of memberIDs
#         print("session", session)
#         family_members = db.getFamilyMemberIDsfromTreeID(session['treeid'])
#         # list of relationshipIDs
#         relationshipIds = db.getRelationshipIDsfromTreeID(session['treeid'])

#         connections = []
#         for rel in relationshipIds:
#             print("rel", rel)
#             rel_tuple = db.getMarriagefromRelationshipID(rel[0])
#             if rel_tuple is not None:  # this means the relationship is a marriage
#                 new_connection = {}
#                 new_connection["type"] = "marriage"
#                 new_connection["rel_id"] = rel_tuple[1]
#                 new_connection["source"] = rel_tuple[2]
#                 new_connection["target"] = rel_tuple[3]
#                 connections.append(new_connection)
#             else:
#                 rel_tuple = db.getParentChildfromRelationshipID(rel[0])
#                 if rel_tuple is None:
#                     return jsonify({"detail": "Invalid relationship"}), 500
#                 print("rel2", rel_tuple)
          
#                 new_connection = {}
#                 new_connection["type"] = "parent-child"
#                 new_connection["rel_id"] = rel_tuple[1]
#                 new_connection["source"] = rel_tuple[2]
#                 new_connection["target"] = rel_tuple[3]

#                 connections.append(new_connection)
#             print(connections)

#         nodes = []
#         for memberId in family_members:
#             new_node = {}
#             member = db.get_family_member(memberId[0])

#             new_node["id"] = memberId[0]
#             new_node["name"] = member[2]
#             new_node["dateOfBirth"] = member[3]
#             new_node["hobbies"] = db.getHobbyNamesfromMemberID(memberId[0])


#             nodes.append(new_node)

#         return_dict = {"nodes": nodes, "connections": connections}
#         print(return_dict)
#         return jsonify(return_dict)
    
#     except Exception as e:
#         print("Uhhh ohhhh")
#         print(e)
#         print(str(e))
#         return jsonify({"detail": str(e)}), 500
    

@app.route("/deleteuser/<username>", methods=["DELETE"])
def delete_user(username):
    userid = db.get_user_by_username(username)
    if userid is None:
        return jsonify({"detail": "User not found"}), 404
    db.delete_user(userid)


@app.route("/addfamilymember/", methods=["POST"])
def add_family_member():
    data = request.json
    # treeid = session["treeid"] <-- uncomment this line when session is implemented
    member = FamilyMember(session['treeid'], data["fullname"], data["dateofbirth"], data["dateofdeath"], data["pictureurl"], data["streetaddress"], data["city"], data["state"], data["country"], data["zipcode"], data["email"], data["phone"])
    default_values = {
        "dateofdeath": None,
        "pictureurl": None,
        "streetaddress": "NULL",
        "city": "NULL",
        "state": "NULL",
        "country": "NULL",
        "zipcode": "NULL",
        "email": "NULL",
    }
    member_sanitized = {key: default_values[key] if value=='' else value for key, value in vars(member).items()}
    print(member_sanitized)
    db.add_family_member(treeid=member_sanitized['treeid'], fullname=member_sanitized['fullname'], dateofbirth=member_sanitized['dateofbirth'], dateofdeath=member_sanitized['dateofdeath'], pictureurl=member_sanitized['pictureurl'], streetaddress=member_sanitized['streetaddress'], city=member_sanitized['city'], state=member_sanitized['state'], country=member_sanitized['country'], zipcode=member_sanitized['zipcode'], email=member_sanitized['email'], phone=member_sanitized['phone'])
    return jsonify({"message": "Family member added successfully"})

if __name__ == "__main__":
    app.secret_key = "super secret"
    app.run(debug=True)