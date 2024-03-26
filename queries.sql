-- Queries for creating the database tables:

-- Adanced Query #1:
CREATE TABLE Users (
        UserID INT AUTO_INCREMENT PRIMARY KEY,
        Username VARCHAR(255) NOT NULL,
        Email VARCHAR(255) NOT NULL UNIQUE CHECK (Email LIKE '%@%.%'),
        Phone VARCHAR(20) CHECK (Phone LIKE '_+___-___-____'),
        PasswordHash VARCHAR(255) NOT NULL
    );

CREATE TABLE FamilyTrees (
        TreeID INT AUTO_INCREMENT PRIMARY KEY,
        TreeName VARCHAR(255) NOT NULL,
        OwnerUserID INT NOT NULL,
        FOREIGN KEY (OwnerUserID) REFERENCES Users(UserID)
    );

CREATE TABLE TreeAccess (
        UserID INT,
        TreeID INT,
        AccessRole ENUM('Editor', 'Viewer') NOT NULL,
        FOREIGN KEY (UserID) REFERENCES Users(UserID),
        FOREIGN KEY (TreeID) REFERENCES FamilyTrees(TreeID)
    );

CREATE TABLE FamilyMembers (
        MemberID INT AUTO_INCREMENT PRIMARY KEY,
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
    );

CREATE TABLE Relationships (
        RelationshipID INT AUTO_INCREMENT PRIMARY KEY,
        TreeID INT NOT NULL,
        FOREIGN KEY (TreeID) REFERENCES FamilyTrees(TreeID)
    );

CREATE TABLE Marriages (
        MarriageID INT AUTO_INCREMENT PRIMARY KEY,
        RelationshipID INT NOT NULL,
        Spouse1MemberID INT NOT NULL,
        Spouse2MemberID INT NOT NULL,
        FOREIGN KEY (RelationshipID) REFERENCES Relationships(RelationshipID),
        FOREIGN KEY (Spouse1MemberID) REFERENCES FamilyMembers(MemberID),
        FOREIGN KEY (Spouse2MemberID) REFERENCES FamilyMembers(MemberID)
    );

CREATE TABLE ParentChild (
        ParentChildID INT AUTO_INCREMENT PRIMARY KEY,
        RelationshipID INT NOT NULL,
        ParentMemberID INT,
        ChildMemberID INT NOT NULL,
        FOREIGN KEY (RelationshipID) REFERENCES Relationships(RelationshipID),
        FOREIGN KEY (ParentMemberID) REFERENCES FamilyMembers(MemberID),
        FOREIGN KEY (ChildMemberID) REFERENCES FamilyMembers(MemberID)
    );

CREATE TABLE Hobbies (
        HobbyID INT AUTO_INCREMENT PRIMARY KEY,
        MemberID INT NOT NULL,
        HobbyName VARCHAR(255) NOT NULL,
        FOREIGN KEY (MemberID) REFERENCES FamilyMembers(MemberID)
    );

CREATE TABLE SearchHistory (
        SearchID INT AUTO_INCREMENT PRIMARY KEY,
        UserID INT NOT NULL,
        SearchQuery VARCHAR(255) NOT NULL,
        SearchDate DATETIME NOT NULL,
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    );

CREATE TABLE AccessLogs (
        LogID INT AUTO_INCREMENT PRIMARY KEY,
        UserID INT NOT NULL,
        ActionType VARCHAR(255) NOT NULL,
        ActionTimestamp DATETIME NOT NULL,
        ActionDetails VARCHAR(255) NOT NULL,
        FOREIGN KEY (UserID) REFERENCES Users(UserID)
    );

-- Advanced Query #2:
CREATE TRIGGER EditorAuto 
AFTER INSERT ON FamilyTrees
FOR EACH ROW 
INSERT INTO TreeAccess (UserID, TreeID, AccessRole) VALUES(NEW.OwnerUserID, NEW.TreeID, "Editor");

--Queries used for populating the tables:

INSERT INTO Users (Username, Email, Phone, PasswordHash) VALUES ("username01", "username01@virginia.email", "1+703-567-1234", "password");
INSERT INTO Users (Username, Email, Phone, PasswordHash) VALUES ("username02", "username02@virginia.email", "1+703-567-1234", "password");
INSERT INTO Users (Username, Email, Phone, PasswordHash) VALUES ("username03", "username03@virginia.email", "1+703-567-1234", "password");
INSERT INTO Users (Username, Email, Phone, PasswordHash) VALUES ("username04", "username04@virginia.email", "1+703-567-1234", "password");
INSERT INTO Users (Username, Email, Phone, PasswordHash) VALUES ("username05", "username05@virginia.email", "1+703-567-1234", "password");
INSERT INTO Users (Username, Email, Phone, PasswordHash) VALUES ("username06", "username06@virginia.email", "1+703-567-1234", "password");
INSERT INTO Users (Username, Email, Phone, PasswordHash) VALUES ("username07", "username07@virginia.email", NULL, "password");
INSERT INTO Users (Username, Email, Phone, PasswordHash) VALUES ("username08", "username08@virginia.email", NULL, "password");
INSERT INTO Users (Username, Email, Phone, PasswordHash) VALUES ("username01", "username09@virginia.email", NULL, "password");
INSERT INTO Users (Username, Email, Phone, PasswordHash) VALUES ("username10", "username10@virginia.email", NULL, "password");
INSERT INTO Users (Username, Email, Phone, PasswordHash) VALUES ("john", "john@gmail.com", "1+703-567-1234", "password");
INSERT INTO Users (Username, Email, Phone, PasswordHash) VALUES ("mary", "mary@example.mail", "1+703-567-1234", "password");
INSERT INTO Users (Username, Email, Phone, PasswordHash) VALUES ("bob", "bob@virginia.edu", "1+703-567-1234", "password");
INSERT INTO Users (Username, Email, Phone, PasswordHash) VALUES ("sam", "sam12324r@adfa.dsfd", "1+703-567-1234", "password");
INSERT INTO Users (Username, Email, Phone, PasswordHash) VALUES ("frederick", "frederick@virginia.email", "1+703-567-1234", "password");
INSERT INTO Users (Username, Email, Phone, PasswordHash) VALUES ("kaitie", "mail@virginia.email", "1+703-567-1234", "password");
INSERT INTO Users (Username, Email, Phone, PasswordHash) VALUES ("leila", "virginia@virginia.email", "1+703-567-1234", "password");
INSERT INTO Users (Username, Email, Phone, PasswordHash) VALUES ("dillon", "sdafs@virginia.email", "1+703-567-1234", "password");
INSERT INTO Users (Username, Email, Phone, PasswordHash) VALUES ("sam", "sam1@virginia.email", "1+703-567-1234", "password");
INSERT INTO Users (Username, Email, Phone, PasswordHash) VALUES ("myst", "fbi@ggggg.a", "1+111-111-1111", "!~!#%YGA^*()");
INSERT INTO FamilyTrees (TreeName, OwnerUserID) VALUES("tree", 1);
INSERT INTO FamilyTrees (TreeName, OwnerUserID) VALUES("tree", 2);
INSERT INTO FamilyTrees (TreeName, OwnerUserID) VALUES("tree", 3);
INSERT INTO FamilyTrees (TreeName, OwnerUserID) VALUES("tree", 4);
INSERT INTO FamilyTrees (TreeName, OwnerUserID) VALUES("tree", 5);
INSERT INTO FamilyTrees (TreeName, OwnerUserID) VALUES("tree", 6);
INSERT INTO FamilyTrees (TreeName, OwnerUserID) VALUES("My Tree", 12);
INSERT INTO FamilyTrees (TreeName, OwnerUserID) VALUES("Family Tree", 13);
INSERT INTO FamilyTrees (TreeName, OwnerUserID) VALUES("Family", 14);
INSERT INTO FamilyTrees (TreeName, OwnerUserID) VALUES("Database Family", 15);
INSERT INTO FamilyTrees (TreeName, OwnerUserID) VALUES("Wear", 16);
INSERT INTO FamilyTrees (TreeName, OwnerUserID) VALUES("Tree", 17);
INSERT INTO FamilyTrees (TreeName, OwnerUserID) VALUES("sdfggfa", 18);
INSERT INTO FamilyTrees (TreeName, OwnerUserID) VALUES("fadgfa", 19);
INSERT INTO FamilyTrees (TreeName, OwnerUserID) VALUES("1234 fmkka f", 20);
INSERT INTO TreeAccess VALUES (10, 2, "Viewer");
INSERT INTO TreeAccess VALUES (14, 3, "Viewer");
INSERT INTO TreeAccess VALUES (15, 11, "Viewer");
INSERT INTO TreeAccess VALUES (11, 14, "Viewer");
INSERT INTO FamilyMembers (TreeID, FullName, DateOfBirth) VALUES(11, 'Jimmy Bob', "1967-02-27");
INSERT INTO FamilyMembers (TreeID, FullName, DateOfBirth) VALUES(11, "Mary Bob", "1937-01-01");
INSERT INTO FamilyMembers (TreeID, FullName, DateOfBirth) VALUES(11, "Uncle Jim", "1974-06-12");
INSERT INTO FamilyMembers (TreeID, FullName, DateOfBirth) VALUES(11, "Uncle Mary", "1964-12-15");
INSERT INTO FamilyMembers (TreeID, FullName, DateOfBirth) VALUES(11, "Brian Bob", "2001-05-07");
INSERT INTO FamilyMembers (TreeID, FullName, DateOfBirth) VALUES(11, "Bob Bob", "2000-06-01");
INSERT INTO FamilyMembers (TreeID, FullName, DateOfBirth, DateOfDeath) VALUES(12, 'Jimmy Bob 2', "1967-02-27", "1971-03-24");
INSERT INTO FamilyMembers (TreeID, FullName, DateOfBirth, StreetAddress, City, State, Country, ZIPCode) VALUES(12, "Mary Bob 2", "1937-01-01", "250 street", "san francisco", "california", "canada", "22333");
INSERT INTO FamilyMembers (TreeID, FullName, DateOfBirth, Email) VALUES(12, "Uncle Jim 2", "1974-06-12", "email@gmail.com");
INSERT INTO FamilyMembers (TreeID, FullName, DateOfBirth, Phone) VALUES(12, "Uncle Mary 2", "1964-12-15", "202-344-5022");
INSERT INTO FamilyMembers (TreeID, FullName, DateOfBirth, Email, Phone) VALUES(12, "Brian Bob 2", "2001-05-07", "21324@3142.132", "123456-134-13455");
INSERT INTO FamilyMembers (TreeID, FullName, DateOfBirth) VALUES(12, "Bob Bob 2", "2000-06-01");
INSERT INTO Relationships (TreeID) VALUES (11);
INSERT INTO Relationships (TreeID) VALUES (11);
INSERT INTO Relationships (TreeID) VALUES (11);
INSERT INTO Relationships (TreeID) VALUES (11);
INSERT INTO Relationships (TreeID) VALUES (12);
INSERT INTO Relationships (TreeID) VALUES (12);
INSERT INTO Relationships (TreeID) VALUES (12);
INSERT INTO Relationships (TreeID) VALUES (12);
INSERT INTO Marriages (RelationshipID, Spouse1MemberID, Spouse2MemberID) VALUES (1, 1, 2);
INSERT INTO Marriages (RelationshipID, Spouse1MemberID, Spouse2MemberID) VALUES (2, 3 , 4);
INSERT INTO Marriages (RelationshipID, Spouse1MemberID, Spouse2MemberID) VALUES (3, 7, 8);
INSERT INTO Marriages (RelationshipID, Spouse1MemberID, Spouse2MemberID) VALUES (4, 9, 10);
INSERT INTO ParentChild (RelationshipID, ParentMemberID, ChildMemberID) VALUES (5, 1, 5);
INSERT INTO ParentChild (RelationshipID, ParentMemberID, ChildMemberID) VALUES (6, 1, 6);
INSERT INTO ParentChild (RelationshipID, ParentMemberID, ChildMemberID) VALUES (7, 7, 11);
INSERT INTO ParentChild (RelationshipID, ParentMemberID, ChildMemberID) VALUES (8, 7, 12);
INSERT INTO SearchHistory (UserID, SearchQuery, SearchDate) VALUES (4, 'bobby', '2024-03-19 15:30:00');
INSERT INTO SearchHistory (UserID, SearchQuery, SearchDate) VALUES (5, 'timothy', '2024-03-22 15:30:00');
INSERT INTO SearchHistory (UserID, SearchQuery, SearchDate) VALUES (6, 'eric', '2024-03-24 15:30:00');
INSERT INTO SearchHistory (UserID, SearchQuery, SearchDate) VALUES (8, 'johnny', '2024-01-25 15:30:00');
INSERT INTO SearchHistory (UserID, SearchQuery, SearchDate) VALUES (8, 'johnny appleseed', '2024-02-25 15:30:00');
INSERT INTO SearchHistory (UserID, SearchQuery, SearchDate) VALUES (8, 'johnny appleseed', '2024-03-25 15:30:00');
INSERT INTO Hobbies (MemberID, HobbyName) VALUES (1, "tennis");
INSERT INTO Hobbies (MemberID, HobbyName) VALUES (1, "golf");
INSERT INTO Hobbies (MemberID, HobbyName) VALUES (1, "watching TV");
INSERT INTO Hobbies ( MemberID, HobbyName) VALUES (1, "playing chess");
INSERT INTO Hobbies (MemberID, HobbyName) VALUES (2, "jetskiing");
INSERT INTO Hobbies ( MemberID, HobbyName) VALUES (2, "parasailing");
INSERT INTO Hobbies (MemberID, HobbyName) VALUES (2, "eating exotic foods");
INSERT INTO Hobbies (MemberID, HobbyName) VALUES (3, "geocaching");
INSERT INTO AccessLogs (UserID, ActionType, ActionTimestamp, ActionDetails) VALUES (1, 'Login', NOW(), 'User logged in successfully'); 
INSERT INTO AccessLogs (UserID, ActionType, ActionTimestamp, ActionDetails) VALUES (2, 'Logout', NOW(), 'User logged out');
INSERT INTO AccessLogs (UserID, ActionType, ActionTimestamp, ActionDetails) VALUES (3, 'Data Update', '2024-03-25 15:30:00', 'Updated record with ID 1234');
INSERT INTO AccessLogs (UserID, ActionType, ActionTimestamp, ActionDetails) VALUES (3, 'Data Update', '2024-03-26 15:30:00', 'Updated record with ID 1234');
INSERT INTO AccessLogs (UserID, ActionType, ActionTimestamp, ActionDetails) VALUES (3, 'Data Update', '2024-03-23 15:30:00', 'Updated record with ID 1234');
INSERT INTO AccessLogs (UserID, ActionType, ActionTimestamp, ActionDetails) VALUES (4, 'Login', NOW(), 'User logged in successfully');
INSERT INTO AccessLogs (UserID, ActionType, ActionTimestamp, ActionDetails) VALUES (5, 'Logout', NOW(), 'User logged out successfully');

--Truncate tables for databases:
SET FOREIGN_KEY_CHECKS=0
TRUNCATE TABLE TreeAccess;
TRUNCATE TABLE Users;
TRUNCATE TABLE FamilyTrees;
TRUNCATE TABLE Relationships;
TRUNCATE TABLE Marriages;
TRUNCATE TABLE FamilyMembers;
TRUNCATE TABLE ParentChild;
TRUNCATE TABLE SearchHistory;
TRUNCATE TABLE Hobbies;
TRUNCATE TABLE AccessLogs;
SET FOREIGN_KEY_CHECKS=1;