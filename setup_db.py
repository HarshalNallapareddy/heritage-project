# ONLY HAVE TO CALL THIS ONCE!!!!!!

import connect_db as db

conn = db.create_connection()
cursor = conn.cursor()

# Execute each SQL command to create tables
sql_commands = [
    """
    CREATE TABLE Users (
        UserID INT AUTO_INCREMENT PRIMARY KEY UNIQUE,
        Username VARCHAR(255) NOT NULL,
        Email VARCHAR(255) NOT NULL UNIQUE,
        Phone VARCHAR(20),
        PasswordHash VARCHAR(255) NOT NULL
    )
    """,
    """
    CREATE TABLE FamilyTrees (
        TreeID INT AUTO_INCREMENT PRIMARY KEY UNIQUE,
        TreeName VARCHAR(255) NOT NULL,
        OwnerUserID INT NOT NULL,
        FOREIGN KEY (OwnerUserID) REFERENCES Users(UserID)
    )
    """,
    """
    CREATE TABLE TreeAccess (
        UserID INT,
        TreeID INT,
        AccessRole ENUM('Editor', 'Viewer') NOT NULL,
        FOREIGN KEY (UserID) REFERENCES Users(UserID),
        FOREIGN KEY (TreeID) REFERENCES FamilyTrees(TreeID)
    )
    """,
    """
    CREATE TABLE FamilyMembers (
        MemberID INT AUTO_INCREMENT PRIMARY KEY UNIQUE,
        TreeID INT NOT NULL,
        FullName VARCHAR(255) NOT NULL,
        DateOfBirth DATE NOT NULL,
        DateOfDeath DATE,
        PictureURL VARCHAR(255),
        StreetAddress VARCHAR(255),
        City VARCHAR(255),
        State VARCHAR(255),
        Country VARCHAR(255),
        ZIPCode VARCHAR(255),
        Email VARCHAR(255),
        Phone VARCHAR(20),
        FOREIGN KEY (TreeID) REFERENCES FamilyTrees(TreeID)
    )
    """,
    """
    CREATE TABLE Relationships (
        RelationshipID INT AUTO_INCREMENT PRIMARY KEY,
        TreeID INT NOT NULL,
        FOREIGN KEY (TreeID) REFERENCES FamilyTrees(TreeID)
    )
    """,
    """
    CREATE TABLE Marriages (
        MarriageID INT AUTO_INCREMENT PRIMARY KEY,
        RelationshipID INT NOT NULL,
        Spouse1MemberID INT NOT NULL,
        Spouse2MemberID INT NOT NULL,
        FOREIGN KEY (RelationshipID) REFERENCES Relationships(RelationshipID),
        FOREIGN KEY (Spouse1MemberID) REFERENCES FamilyMembers(MemberID),
        FOREIGN KEY (Spouse2MemberID) REFERENCES FamilyMembers(MemberID)
    )
    """,
    """
    CREATE TABLE ParentChild (
        ParentChildID INT AUTO_INCREMENT PRIMARY KEY,
        RelationshipID INT NOT NULL,
        ParentMemberID INT,
        ChildMemberID INT NOT NULL,
        FOREIGN KEY (RelationshipID) REFERENCES Relationships(RelationshipID),
        FOREIGN KEY (ParentMemberID) REFERENCES FamilyMembers(MemberID),
        FOREIGN KEY (ChildMemberID) REFERENCES FamilyMembers(MemberID)
    )
    """,
    """
    CREATE TABLE Hobbies (
        HobbyID INT AUTO_INCREMENT PRIMARY KEY,
        MemberID INT NOT NULL,
        HobbyName VARCHAR(255) NOT NULL,
        FOREIGN KEY (MemberID) REFERENCES FamilyMembers(MemberID)
    )
    """,
    """
    CREATE TABLE SearchHistory (
        SearchID INT AUTO_INCREMENT PRIMARY KEY,
        UserID INT NOT NULL,
        SearchQuery VARCHAR(255) NOT NULL,
        SearchDate DATETIME NOT NULL,
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    )
    """,
    """
    CREATE TABLE AccessLogs (
        LogID INT AUTO_INCREMENT PRIMARY KEY,
        UserID INT NOT NULL,
        ActionType VARCHAR(255) NOT NULL,
        ActionTimestamp DATETIME NOT NULL,
        ActionDetails VARCHAR(255) NOT NULL,
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    )
    """
]

for command in sql_commands:
    cursor.execute(command)

# Commit the changes and close the connection
conn.commit()
conn.close()