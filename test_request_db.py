import request_db as db

print(db.getTreeIDfromUserName('john'))
print(len(db.getFamilyMembersfromTreeID(11)))