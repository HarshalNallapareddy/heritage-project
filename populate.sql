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
INSERT INTO TreeAccess VALUES (2, 1, "Editor");
INSERT INTO TreeAccess VALUES (2, 1, "Editor");
INSERT INTO TreeAccess VALUES (3, 2, "Editor");
INSERT INTO TreeAccess VALUES (4, 3, "Editor");
INSERT INTO TreeAccess VALUES (5, 4, "Editor");
INSERT INTO TreeAccess VALUES (6, 5, "Editor");
INSERT INTO TreeAccess VALUES (12, 6, "Editor");
INSERT INTO TreeAccess VALUES (13, 7, "Editor");
INSERT INTO TreeAccess VALUES (14, 8, "Editor");
INSERT INTO TreeAccess VALUES (15, 9, "Editor");
INSERT INTO TreeAccess VALUES (16, 10, "Editor");
INSERT INTO TreeAccess VALUES (17, 11, "Editor");
INSERT INTO TreeAccess VALUES (18, 12, "Editor");
INSERT INTO TreeAccess VALUES (19, 13, "Editor");
INSERT INTO TreeAccess VALUES (20, 14, "Editor");
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
INSERT INTO FamilyMembers (TreeID, FullName, DateOfBirth, DateOfDeath) VALUES(12, 'Jimmy Bob', "1967-02-27", "1971-03-24");
INSERT INTO FamilyMembers (TreeID, FullName, DateOfBirth, StreetAddress, City, State, Country, ZIPCode) VALUES(12, "Mary Bob", "1937-01-01", "250 street", "san francisco", "california", "canada", "22333");
INSERT INTO FamilyMembers (TreeID, FullName, DateOfBirth, Email) VALUES(12, "Uncle Jim", "1974-06-12", "email@gmail.com");
INSERT INTO FamilyMembers (TreeID, FullName, DateOfBirth, Phone) VALUES(12, "Uncle Mary", "1964-12-15", "202-344-5022);






