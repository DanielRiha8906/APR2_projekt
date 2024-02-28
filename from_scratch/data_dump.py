import random
from pymongo import MongoClient

#Just a file for creating dummy data, not essential
client = MongoClient("mongodb://admin:admin@localhost:27017", connect=False)
db_name = client['APR2']
collection = db_name['QR_code']

json_objects = []
for i in range(100):
    userID = str(i+2000)
    qr_code = str(i)
    isTaken = str(random.choice([0,1]))
    json_object = {
        "_id": userID,
        "qr_code": qr_code,
        "Is_taken": isTaken,
    }
    json_objects.append(json_object)

collection.insert_many(json_objects)