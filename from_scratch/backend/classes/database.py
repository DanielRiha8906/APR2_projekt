import pymongo

class DB:

    def __init__(self,qr):
        self.qr = qr
    #testing purpose only
    def add_student(self, username, qr_code):
        existing_doc = self.qr.find_one({"qr_code": qr_code})
        if existing_doc:
            self.qr.update_one({"qr_code": qr_code}, {"$set": {"Is_taken": username}})
            print("Updated document")
        else:
        # Insert a new document because of testing
            self.qr.insert_one({"qr_code": qr_code, "Is_taken": username})
            print("Inserted document")
        return 0
    #Signing out ain't implemented -> proof of concept
    def remove_student(self, qr_code):
        self.qr.update_one({"qr_code": qr_code}, {"$set": {"Is_taken": "0"}})
        return 0

    #Login
    def login_user(self, username, qr_code):
        available_qr = self.qr.find_one({"qr_code": str(qr_code)})
        if not available_qr:
            return None
        if available_qr['Is_taken'] == "0":
            self.qr.update_one({"qr_code": qr_code}, {"$set": {"Is_taken": username}})
            user = self.qr.find_one({"qr_code": str(qr_code)})
            return user
        else:
            return False
    def reset_database(self):
        self.qr.update_many({}, {"$set": {"Is_taken": "0"}})
        print("Database reset completed")