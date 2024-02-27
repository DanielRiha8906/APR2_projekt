import pymongo

class DB:

    def __init__(self, users, qr):
        self.users = users
        self.qr = qr

    def add_student(self, username, qr_code):
        existing_doc = self.qr.find_one({"qr_code": qr_code})

        if existing_doc:
            self.qr.update_one({"qr_code": qr_code}, {"$set": {"Is_taken": username}})
        else:
        # Insert a new document because of testing
            self.qr.insert_one({"qr_code": qr_code, "Is_taken": username})
        return 0
    def remove_student(self, qr_code):
        self.qr.update_one({"qr_code": qr_code}, {"$set": {"Is_taken": "0"}})
        return 0

    def login_user(self, username, qr_code):
        available_qr = self.qr.find_one({"qr_code": qr_code, "is_taken": "0"})
        if available_qr:
            self.qr.update_one({"qr_code": qr_code}, {"$set": {"is_taken": username}})
            return True
        else:
            return False
