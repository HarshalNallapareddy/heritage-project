from flask import Flask, request, redirect, session, jsonify, render_template, url_for, flash, send_file
import request_db as db
from flask_bcrypt import generate_password_hash, check_password_hash
from datetime import datetime
from datetime import date, datetime
import json
from io import BytesIO



class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


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


@app.route('/download_tree', methods=['GET'])
def download_tree():
    # Create a dictionary to be converted into a JSON object
    # Define the path for the temporary json file
    add_access_log("view-tree", "Viewing family tree")
    try:
        response = db.get_tree_data(session['treeid'])
        if len(response) == 0:
            return jsonify({"detail": "No data found"}), 404
        
        else:
            if "detail" in response:
                return jsonify(response), 500
            else:
                memory_file = BytesIO()
                memory_file.write(json.dumps(response, cls=CustomJSONEncoder).encode('utf-8'))
                # memory_file.write(jsonify(response))
                memory_file.seek(0)  # Go to the beginning of the BytesIO object
                return send_file(memory_file, as_attachment=True,download_name='family_tree.json' ,mimetype='application/json')
    
    except Exception as e:
        print("Uhhh ohhhh")
        print(e)
        print(str(e))
        return jsonify({"detail": str(e)}), 500


    # filename = 'data.json'
    # data = {"hello": ""}
    # # Writing JSON data
    # with open(filename, 'w') as f:
    #     json.dump(data, f)

    # # Return the file for download
    # return send_file(filename, as_attachment=True, download_name='data.json')


@app.route('/share_page')
def share_page():
    results = db.get_tree_access_by_treeid(session['treeid']) # the users who have access to your tree
    shared_by_you = []
    for user in results:
        shared_by_you.append({"username": user[1], "id": user[0]})
    

    shared_by_others = []
    results = db.get_shared_tree_access_by_userid(session['userid'])
    for tree in results:
        shared_by_others.append({"title": tree[1], "id": tree[0]})
    print(shared_by_others)

    
    return render_template('share.html', shared_by_you=shared_by_you, shared_by_others=shared_by_others)


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


@app.route('/delete_member', methods=['POST'])
def delete_member():
    # Logic to delete family member with memberID
        print("hello")
        id_to_delete = request.json.get('id_to_delete')

        print(id_to_delete)
        # first check to see if member is in the user's tree
        in_tree = db.check_member_in_tree( id_to_delete, session['treeid'],)
        print(in_tree)
        if not in_tree:
            print("not in tree")
            return jsonify({"message": "Member not in user's tree"}), 401

        print("BREAKING POINT")
        # check that the member is not in any relationships
        in_relationship = db.check_member_in_relationships(id_to_delete, session['treeid'])
        print("IN RELATIONSHIP: ", in_relationship)
        if in_relationship:
            return jsonify({"message": "Member is in a relationship"}), 401
        

        print("DELETING MEMBER")
        # Perform action to delete family member
        try:
            # delete hobbies
            db.delete_hobbies_by_memberid(id_to_delete)
            print("HELLO")
            # run delete for the member id
            x = db.delete_family_member(id_to_delete)
            print(x)
            return jsonify({"message": "Deleted"})
        
        except Exception as e:
            return jsonify({"message": "Something went wrong"}), 401



@app.route('/view_tree/<int:tree_id>', methods=['GET'])
def view_tree(tree_id):
    # check to see if given user has access to the tree using tree access
    if db.check_if_user_has_access_to_tree(session['userid'], tree_id):
        data = db.get_tree_data(tree_id)
        import json
        print(data)

        return render_template('view_tree.html', tree_data=data)
    
    return share_page()

    # if not, return to share page

    # if yes, return the tree data


    # Logic to view tree with tree_id
    return jsonify({'tree_id': tree_id})




@app.route('/revoke_access/<int:user_id>', methods=['GET'])
def revoke_access(user_id):
    # Logic to revoke access for user with user_id
    if request.method == 'GET':
        # Perform action to revoke access
        try:
            # run delete for the user's tree and specified user id
            x = db.delete_tree_access(session['treeid'], user_id)
            print(x)
            return share_page()
        
        except Exception as e:
            return share_page()
    



@app.route('/share_tree/', methods=['POST'])
def share_tree():
    if request.method == 'POST':
        username = request.form['username']
        results = db.get_user_by_username(username)
        print(results)

        if results is None:
            flash('Username does not exist', 'error')
            return share_page()
        
        userid = results[0]

        if db.check_if_user_has_access_to_tree(userid, session['treeid']):
            flash('User already has access to tree', 'error')
            return share_page()

        db.add_tree_access(userid, session['treeid'], "Viewer")


        # check to see if username exists
        # if db.get_user_by_username(username) is None:
        #     flash('Username does not exist', 'error')
        #     return redirect(url_for('share_page'))
    
        # add access to user
        # db.add_tree_access(session['treeid'], db.get_user_by_username(username)[0])


        # update TreeAccess table to make that username have access to the tree

        # Logic to share tree with user 'username'
        return share_page()
    else:
        return share_page()



@app.route('/add_family_member')
def add_family_member_page():
    # fetch json from generate_tree method
    return render_template('add_family_member.html')


@app.route('/add_family_relationship')
def add_family_relationship_page():
    # fetch json from generate_tree method
    return render_template('add_relationship.html')




@app.route('/accesslogs')
def accesslogs_page():
    return render_template('accesslogs.html')


@app.route("/getaccesslogs", methods=["GET"])
def get_access_logs():
    userid = session["userid"]
    logs = db.get_accesslogs_by_userid(userid)
    logs = logs[::-1]
    print(logs)
    return jsonify(logs)



@app.route("/getsearchhistory", methods=["GET"])
def get_search_history():
    userid = session["userid"]
    logs = db.get_search_history_by_user_id(userid)
    logs = logs[::-1]
    print(logs)
    return jsonify(logs)



@app.route("/deleterelationship", methods=["POST"])
def delete_relationship():
    try:
        rel_id = request.json.get("rel_id")

        # check to see if relationship is in the user's tree
        in_tree = db.check_relationship_in_tree(session['treeid'], rel_id)
        print("IN TREE: ", in_tree)
        if not in_tree:
            return jsonify({"message": "Relationship not in user's tree"}), 401

        print(f"\n\n\nDELETING {rel_id}")
        db.delete_relationship(rel_id)
        add_access_log("delete-relationship", f"Deleted relationship with ID {rel_id}")
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

        add_access_log("create-parent-child", f"Created relationship between {spouse1} and {spouse2}")


        return jsonify({"message": "Marriage Creation successful"})

    except:
        return jsonify({"message", "Database error. Relationship creation not successful."}), 401


# Internal function
def add_access_log(actiontype, actiondetails):
    userid = session['userid']
    time = datetime.now()
    db.add_accesslogs(userid, actiontype, time, actiondetails)




@app.route('/update_family_member/<int:memberID>', methods=["GET", "POST"])
def update_family_member_page(memberID):
    # TODO: check to see if memberID is in the user's tree
    # TODO: add hobbies
    if request.method == 'POST':
            try:

                # print("HELLLLOOOOO")
                # check to see if member is in the user's tree
                in_tree = db.check_member_in_tree( memberID, session['treeid'],)
                print("IN_TREE: ", in_tree)
                if not in_tree:
                    print("not in tree")
                    return jsonify({"message": "Member not in user's tree"}), 401


                # Extract form data
                full_name = request.form['fullname']
                date_of_birth = request.form['dateofbirth']
                date_of_death = request.form.get('dateofdeath')  # Using .get() to handle if the field is empty
                picture_url = request.form['pictureurl']
                street_address = request.form['streetaddress']
                city = request.form['city']
                state = request.form['state']
                country = request.form['country']
                zipcode = request.form['zipcode']
                email = request.form['email']
                phone = request.form['phone']


                hobbies = request.form['hobbies'].split(',')

                # Example: Update the database using SQLAlchemy or another database library
                print(f"Updating family member with ID {memberID} with the following data: {full_name}, {date_of_birth}, {date_of_death}, {picture_url}, {street_address}, {city}, {state}, {country}, {zipcode}, {email}, {phone}")
                
                if date_of_death == '':
                    date_of_death = None
                
                if picture_url == '':
                    picture_url = None
                
                if street_address == '':
                    street_address = None
                
                if city == '':
                    city = None
                
                if state == '':
                    state = None
                
                if country == '':
                    country = None

                if zipcode == '':
                    zipcode = None
                
                if email == '':
                    email = None
                
                last_row_id = db.update_family_member(memberID, full_name, date_of_birth, date_of_death, picture_url, street_address, city, state, country, zipcode, email, phone)
                                                    # memberid, fullname, dateofbirth, dateofdeath, pictureurl, streetaddress, city, state, country, zipcode, email, phone
                print(f"Last row ID: {last_row_id}")

                db.delete_hobbies_by_memberid(memberID)
                # print("DELETED HOBBIES")
                for hobby in hobbies:
                    # print(session["treeid"], memberID, hobby)
                    db.add_hobby(memberID, hobby)
                    print(f"HOBBY ADDED: {hobby}")
                flash('Family member updated successfully!', 'success')

                return redirect(url_for('tree'))
                
        
            except Exception as e:
                flash(f'An error occurred: {e}', 'error')
                return redirect(url_for('update_family_member_page', memberID=memberID))

        

    else:
        in_tree = db.check_member_in_tree( memberID, session['treeid'],)
        print("IN_TREE: ", in_tree)
        if not in_tree:
            print("not in tree")
            return jsonify({"message": "Member not in user's tree"}), 401
        member_dict = db.get_family_member(memberID)
        hobbies = db.getHobbyNamesfromMemberID(memberID)
        # print(hobbies)

        member_dict['hobbies'] = ",".join(hobbies)
        print(member_dict['hobbies'])

        # convert all Null values to None
        member_dict = {key: '' if value == 'NULL' or value == None else value for key, value in member_dict.items()}
        return render_template('update_family_member.html', member_id=memberID, member_dict=member_dict)




@app.route("/createparentchild", methods=["POST"])
def create_parent_child():
    try:
        parent = request.json.get("parent_id")
        child = request.json.get("child_id")
        
        add_access_log("create-parent-child", f"Created relationship between {parent} and {child}")

        familymemberids = db.getFamilyMemberIDsfromTreeID(session['treeid'])
        familymemberids = [x[0] for x in familymemberids]

        print(parent, child, familymemberids)
        if parent not in familymemberids or child not in familymemberids:
            return jsonify({"message", "Parent and Child not found. Please enter their full names properly."}), 401
        
        db.add_parentchildrelationship(session['treeid'], parent, child)

        return jsonify({"message": "Parent-Child Creation successful"})

    except:
        return jsonify({"message", "Database error. Relationship creation not successful."}), 401





@app.route("/find_path", methods=["POST"])
def find_path():
    try:
        print("\n\n\n\n")

        # get grah data
        graph_data = db.get_tree_data(session['treeid'])
        if len(graph_data) == 0:
            return jsonify({"detail": "No data found"}), 404
        
        # get source and target
        source = request.json.get("source")
        target = request.json.get("target")


        # check to see if source and target are in the tree
        familymemberids = db.getFamilyMemberIDsfromTreeID(session['treeid'])
        familymemberids = [x[0] for x in familymemberids]

        if source not in familymemberids or target not in familymemberids:
            return jsonify({"message", "Source and Target not found. Please enter their full names properly."}), 401


        print("SOURCE: ", source)
        print("TARGET: ", target)

        nodes = graph_data["nodes"]
        connections = graph_data["connections"]

        id_to_name = {}
        for node in nodes:
            print(node["id"], node["name"])
            id_to_name[node["id"]] = node["name"]

        print("source name: ", id_to_name[source])
        print("target name: ", id_to_name[target])

        db.add_searchhistory(session['userid'], "Search between {} - {}".format(id_to_name[source], id_to_name[target]))

        
        graph = {}
        for connection in connections:
            source_x = connection["source"]
            target_x = connection["target"]
            rel_type = connection["type"]


            x_name = id_to_name[source_x]
            y_name = id_to_name[target_x]

            print("1", source_x, x_name)
            print("2", target_x, y_name)

            
            if source_x not in graph:
                graph[source_x] = []

            print("x-y", x_name, y_name)
            graph[source_x].append((target_x, f"{x_name}" +" is married to " + f"{y_name}\n" if rel_type == "marriage" else f"{x_name}" + " is the parent of " + f"{y_name}\n"))
            
            if target_x not in graph:
                graph[target_x] = []

            graph[target_x].append((source_x, f"{y_name}" + " is married to " + f"{x_name}\n" if rel_type == "marriage" else f"{y_name}" + " is the child of " + f"{x_name}\n"))
            # print("HELLO")


        visited = set()

        start = (source, [])
        queue = [start]


        print("GRAPH", graph)
        # print("START", start)

        while len(queue) > 0:

            current, path = queue[0]
            queue = queue[1:]
            visited.add(current)

            if current == target:
                return jsonify({"path": path})
            
            for neighbor, relation in graph[current]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [relation]))

        print("\n\n\n\n")
        return jsonify({"path": ["No path found"]})


    except Exception as e:
        print(e)
        return jsonify({"message": str(e)}), 401


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
    add_access_log("create-user", "New user created!")




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
        add_access_log("login", "login successful")


        # return redirect(url_for('tree'))
        return jsonify({"message": "Login successful"})

    else:
        print("Invalid username or password")
        return jsonify({"detail": "Invalid username or password"}), 401



@app.route("/generatetree/", methods=["GET"])
def generate_tree():
    add_access_log("view-tree", "Viewing family tree")
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




@app.route("/addfamilymember/", methods=["POST"])
def add_family_member():
    data = request.json
    # treeid = session["treeid"] <-- uncomment this line when session is implemented

    # print("DATA: ", data)
    member = FamilyMember(session['treeid'], data["fullname"], data["dateofbirth"], data["dateofdeath"], data["pictureurl"], data["streetaddress"], data["city"], data["state"], data["country"], data["zipcode"], data["email"], data["phone"])
    default_values = {
        "dateofdeath": None,
        "pictureurl": None,
        "streetaddress": "NULL",
        "fullname": "NULL",
        "city": "NULL",
        "state": "NULL",
        "country": "NULL",
        "zipcode": "NULL",
        "email": "NULL",
    }
    member_sanitized = {key: default_values[key] if value=='' else value for key, value in vars(member).items()}
    print("DATA: ", member_sanitized)
    memberid = db.add_family_member(session["treeid"], fullname=member_sanitized['fullname'], dateofbirth=member_sanitized['dateofbirth'], dateofdeath=member_sanitized['dateofdeath'], pictureurl=member_sanitized['pictureurl'], streetaddress=member_sanitized['streetaddress'], city=member_sanitized['city'], state=member_sanitized['state'], country=member_sanitized['country'], zipcode=member_sanitized['zipcode'], email=member_sanitized['email'], phone=member_sanitized['phone'])
    add_access_log("add-family-member", "Family member " + str(member_sanitized["fullname"]) + " added")

    hobbies = data["hobbies"].split(',')
    print(hobbies)

    print("MEMBERID: ", memberid)
    for hobby in hobbies:
        db.add_hobby(memberid, hobby)
        print(f"HOBBY ADDED: {hobby}")
    



    return jsonify({"message": "Family member added successfully"})

if __name__ == "__main__":
    app.secret_key = "super secret"
    app.json_encoder = CustomJSONEncoder

    app.run(debug=True)