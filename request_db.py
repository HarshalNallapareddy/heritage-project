import connect_db as db
import mysql.connector

# For the users table:
def add_user(username, email, phone, password_hash):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Users (Username, Email, Phone, PasswordHash) VALUES (%s, %s, %s, %s)",
                       (username, email, phone, password_hash))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None

def add_tree(treeid, treename, ownerUserID):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO FamilyTrees (TreeID, TreeName, OwnerUserID) VALUES (%s, %s, %s)",
                       (treeid, treename, ownerUserID))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
    
def add_tree_access(userid, treeid, accessrole):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO TreeAccess (UserID, TreeID, AccessRole) VALUES (%s, %s, %s)",
                       (userid, treeid, accessrole))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
    
def add_family_member(treeid, fullname, dateofbirth, dateofdeath="NULL", pictureurl="NULL", streetaddress="NULL", city="NULL", state="NULL", country="NULL", zipcode="NULL", email="NULL", phone="NULL"):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO FamilyMembers (TreeID, FullName, DateOfBirth, DateOfDeath, PictureURL, StreetAddress, City, State, Country, ZIPCode, Email, Phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (treeid, fullname, dateofbirth, dateofdeath, pictureurl, streetaddress, city, state, country, zipcode, email, phone))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
    
def add_relationship(treeid):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Relationships (TreeID) VALUES (%s)",
                       (treeid))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
    
def add_marriagerelationship(treeid, member1id, member2id):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO MarriageRelationship (TreeID, Member1ID, Member2ID) VALUES (%s, %s, %s)",
                       (treeid, member1id, member2id))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
    
def add_parentchildrelationship(treeid, parentid, childid):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO ParentChildRelationship (TreeID, ParentID, ChildID) VALUES (%s, %s, %s)",
                       (treeid, parentid, childid))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
    
def add_hobbies(treeid, memberid, hobby):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Hobbies (TreeID, MemberID, Hobby) VALUES (%s, %s, %s)",
                       (treeid, memberid, hobby))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
                       
def add_searchhistory(userid, searchterm):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO SearchHistory (UserID, SearchTerm) VALUES (%s, %s)",
                       (userid, searchterm))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None

def add_accesslogs(userid, actiontype, actiontimestamp, actiondetails):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO AccessLogs (UserID, ActionType, ActionTimestamp, ActionDetails) VALUES (%s, %s, %s, %s)",
                       (userid, actiontype, actiontimestamp, actiondetails))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None

