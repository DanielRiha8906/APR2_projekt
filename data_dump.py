import random
from pymongo import MongoClient

client = MongoClient("mongodb://admin:admin@localhost:27017", connect=False)
db_name = client['APR2']
collection = db_name['QR_code']

json_objects = []
for i in range(5):
    userID = random.randint(1,20)
    qr_code = str(random.randint(1000, 1020))
    isTaken = str(random.choice([0,1]))
    json_object = {
        "_id": userID,
        "qr_code": qr_code,
        "Is_taken": isTaken,
    }
    json_objects.append(json_object)

collection.insert_many(json_objects)