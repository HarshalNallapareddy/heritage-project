import connect_db as db
import mysql.connector

# ------------------- ADD ---------------------------------------

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

def add_tree(treename, ownerUserID):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO FamilyTrees (TreeName, OwnerUserID) VALUES (%s, %s)",
                       (treename, ownerUserID))
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
    
def add_family_member(treeid, fullname, dateofbirth, dateofdeath, pictureurl, streetaddress, city, state, country, zipcode, email, phone):
    conn = db.create_connection()
    cursor = conn.cursor()
    print("about to submit now....")
    print("INSERT INTO FamilyMembers (TreeID, FullName, DateOfBirth, DateOfDeath, PictureURL, StreetAddress, City, State, Country, ZIPCode, Email, Phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (treeid, fullname, dateofbirth, dateofdeath, pictureurl, streetaddress, city, state, country, zipcode, email, phone))
    try:
        # cursor.execute("INSERT INTO FamilyMembers (TreeID, FullName, DateOfBirth, DateOfDeath, PictureURL, StreetAddress, City, State, Country, ZIPCode, Email, Phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        #                (treeid, fullname, dateofbirth, dateofdeath, pictureurl, streetaddress, city, state, country, zipcode, email, phone))
        cursor.execute("INSERT INTO FamilyMembers (TreeID, FullName, DateOfBirth, DateOfDeath, PictureURL, StreetAddress, City, State, Country, ZIPCode, Email, Phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (treeid, fullname, dateofbirth, dateofdeath, pictureurl, streetaddress, city, state, country, zipcode, email, phone))
        conn.commit()
        print("Family member added")
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
    
def add_relationship(treeid):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Relationships (TreeID) VALUES (%s)",
                       (treeid,))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
    
def add_marriagerelationship(treeid, member1id, member2id):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        relationship_id = add_relationship(treeid) # first add relationship to super table
        cursor.execute("INSERT INTO Marriages (RelationshipID, Spouse1MemberID, Spouse2MemberID) VALUES (%s, %s, %s)",
                       (relationship_id, member1id, member2id))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
    
def add_parentchildrelationship(treeid, parentid, childid):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        relationship_id = add_relationship(treeid) # first add relationship to super table
        cursor.execute("INSERT INTO ParentChild (RelationshipID, ParentMemberID, ChildMemberID) VALUES (%s, %s, %s)",
                       (relationship_id, parentid, childid))
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
    
# ------------------- UPDATE ---------------------------------------
    
def update_user(userid, username, email, phone):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Users SET Username = %s, Email = %s, Phone = %s WHERE UserID = %s",
                       (username, email, phone, userid))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
    
def update_tree(treeid, treename):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE FamilyTrees SET TreeName = %s WHERE TreeID = %s",
                       (treename, treeid))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
    
def update_tree_access(userid, treeid, accessrole):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE TreeAccess SET AccessRole = %s WHERE UserID = %s AND TreeID = %s",
                       (accessrole, userid, treeid))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None

def update_family_member(memberid, treeid, fullname, dateofbirth, dateofdeath, pictureurl, streetaddress, city, state, country, zipcode, email, phone):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE FamilyMembers SET TreeID = %s, FullName = %s, DateOfBirth = %s, DateOfDeath = %s, PictureURL = %s, StreetAddress = %s, City = %s, State = %s, Country = %s, ZIPCode = %s, Email = %s, Phone = %s WHERE MemberID = %s",
                       (treeid, fullname, dateofbirth, dateofdeath, pictureurl, streetaddress, city, state, country, zipcode, email, phone, memberid))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None

def update_relationship(relationshipId, treeId):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Relationships SET TreeID = %s WHERE RelationshipID = %s",
                       (treeId, relationshipId))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
    
def update_marriagerelationship(marriageId, relationshipId, member1Id, member2Id):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Marriages SET RelationshipID = %s, Spouse1MemberID = %s, Spouse2MemberID = %s WHERE MarriageID = %s",
                       (relationshipId, member1Id, member2Id, marriageId))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
    
def update_parentchildrelationship(parentchildId, relationshipId, parentId, childId):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE ParentChild SET RelationshipID = %s, ParentMemberID = %s, ChildMemberID = %s WHERE ParentChildID = %s",
                       (relationshipId, parentId, childId, parentchildId))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
    
def update_hobbies(hobbyId, memberId, hobby):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Hobbies SET MemberID = %s, HobbyName = %s WHERE HobbyID = %s",
                       (memberId, hobby, hobbyId))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
    
def update_searchhistory(searchId, userId, searchTerm, searchDate):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE SearchHistory SET UserID = %s, SearchQuery = %s, SearchDate = %s WHERE SearchID = %s",
                       (userId, searchTerm, searchDate, searchId))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
    
def update_accesslogs(logId, userId, actionType, actionTimestamp, actionDetails):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE AccessLogs SET UserID = %s, ActionType = %s, ActionTimestamp = %s, ActionDetails = %s WHERE LogID = %s",
                       (userId, actionType, actionTimestamp, actionDetails, logId))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
    
# ------------------- DELETE ---------------------------------------
    
def delete_user(userid):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Users WHERE UserID = %s",
                       (userid,))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
    
def delete_tree(treeid):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM FamilyTrees WHERE TreeID = %s",
                       (treeid,))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
    
def delete_tree_access(userid, treeid):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM TreeAccess WHERE UserID = %s AND TreeID = %s",
                       (userid, treeid))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
    
def delete_family_member(memberid):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM FamilyMembers WHERE MemberID = %s",
                       (memberid,))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
    


def delete_relationship(relationshipId):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:

                # delete all marriages and parent-child relationships associated with this relationship
        cursor.execute("DELETE FROM Marriages WHERE RelationshipID = %s",
                       (relationshipId,))
        cursor.execute("DELETE FROM ParentChild WHERE RelationshipID = %s",
                          (relationshipId,))
        
        cursor.execute("DELETE FROM Relationships WHERE RelationshipID = %s",
                       (relationshipId,))
        

        print(f"HELLOOOOOO {relationshipId}\n\n\n\n\n\n")
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
    
def delete_marriagerelationship(marriageId):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Marriages WHERE MarriageID = %s",
                       (marriageId,))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
    
def delete_parentchildrelationship(parentchildId):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM ParentChild WHERE ParentChildID = %s",
                       (parentchildId,))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
    
def delete_hobbies(hobbyId):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Hobbies WHERE HobbyID = %s",
                       (hobbyId,))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
    
def delete_searchhistory(searchId):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM SearchHistory WHERE SearchID = %s",
                       (searchId,))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
    
def delete_accesslogs(logId):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM AccessLogs WHERE LogID = %s",
                       (logId,))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None
    
# ------------------- SELECT ---------------------------------------
    
def get_user(userid):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Users WHERE UserID = %s",
                       (userid,))
        return cursor.fetchone()
    except mysql.connector.Error as e:
        print(e)
        return None
    
def get_user_by_username(username):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Users WHERE Username = %s",
                       (username,))
        return cursor.fetchone()
    except mysql.connector.Error as e:
        print(e)
        return None
    
def get_tree(treeid):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM FamilyTrees WHERE TreeID = %s",
                       (treeid,))
        return cursor.fetchone()
    except mysql.connector.Error as e:
        print(e)
        return None
    
def get_tree_access(userid, treeid):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM TreeAccess WHERE UserID = %s AND TreeID = %s",
                       (userid, treeid))
        return cursor.fetchone()
    except mysql.connector.Error as e:
        print(e)
        return None
    
def get_family_member(memberid):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM FamilyMembers WHERE MemberID = %s",
                       (memberid,))
        return cursor.fetchone()
    except mysql.connector.Error as e:
        print(e)
        return None
    
def get_relationship(relationshipId):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Relationships WHERE RelationshipID = %s",
                       (relationshipId,))
        return cursor.fetchone()
    except mysql.connector.Error as e:
        print(e)
        return None
    
def get_marriagerelationship(marriageId):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Marriages WHERE MarriageID = %s",
                       (marriageId,))
        return cursor.fetchone()
    except mysql.connector.Error as e:
        print(e)
        return None
    
def get_parentchildrelationship(parentchildId):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM ParentChild WHERE ParentChildID = %s",
                       (parentchildId,))
        return cursor.fetchone()
    except mysql.connector.Error as e:
        print(e)
        return None
    
def get_hobbies(hobbyId):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Hobbies WHERE HobbyID = %s",
                       (hobbyId,))
        return cursor.fetchone()
    except mysql.connector.Error as e:
        print(e)
        return None
    
def get_searchhistory(searchId):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM SearchHistory WHERE SearchID = %s",
                       (searchId,))
        return cursor.fetchone()
    except mysql.connector.Error as e:
        print(e)
        return None
    
def get_accesslogs(logId):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM AccessLogs WHERE LogID = %s",
                       (logId,))
        return cursor.fetchone()
    except mysql.connector.Error as e:
        print(e)
        return None
    
def get_all_users():
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Users")
        return cursor.fetchall()
    except mysql.connector.Error as e:
        print(e)
        return None

def getTreeIDfromUserName(username):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT UserID FROM Users WHERE Username = %s",
                       (username,))
        userid = cursor.fetchone()[0] #tuple object
        cursor.fetchall()
        cursor.execute("SELECT TreeID FROM FamilyTrees WHERE OwnerUserID = %s",
                       (userid,))
        return cursor.fetchone()[0]
    except mysql.connector.Error as e:
        print(e)
        return None
    
    
def getFamilyMemberIDsfromTreeID(treeid):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT MemberID FROM FamilyMembers WHERE TreeID = %s",
                       (treeid,))
        return cursor.fetchall()
    except mysql.connector.Error as e:
        print(e)
        return None
    

def getHobbyNamesfromMemberID(memberid):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT HobbyName FROM Hobbies WHERE MemberID = %s",
                       (memberid,))
        hobbyname_tuples = cursor.fetchall()
        return [hobbyname[0] for hobbyname in hobbyname_tuples]

    except mysql.connector.Error as e:
        print(e)
        return None
    
def getRelationshipIDsfromTreeID(treeid):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT RelationshipID FROM Relationships WHERE TreeID = %s",
                       (treeid,))
        return cursor.fetchall()
    except mysql.connector.Error as e:
        print(e)
        return None
    
def getMarriagefromRelationshipID(relationshipid):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Marriages WHERE RelationshipID = %s",
                       (relationshipid,))
        result = cursor.fetchone()
        return result
    except mysql.connector.Error as e:
        print(e)
        return None

def getParentChildfromRelationshipID(relationshipid):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM ParentChild WHERE RelationshipID = %s",
                       (relationshipid,))
        return cursor.fetchone()
    except mysql.connector.Error as e:
        print(e)
        return None