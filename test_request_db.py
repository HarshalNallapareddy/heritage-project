import request_db as db

# print(db.getTreeIDfromUserName('john'))
# print(db.getFamilyMemberIDsfromTreeID(11))
# print(db.getHobbyNamesfromMemberID(1))

db.add_family_member(
    treeid=5,
    fullname='Harshal Nallapareddy',
    dateofbirth='2003-02-14',
    dateofdeath='2100-02-14',
    pictureurl='https://www.shorturl.at/',
    streetaddress='825 Parkland Pl',
    city='Glen Allen',
    state='Virginia',
    country='USA',
    zipcode='23059',
    email='harshalreddyn@gmail.com',
    phone='8048336436'
)

