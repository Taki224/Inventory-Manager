import json

class Employee:
    def __init__(self, id, username, email, password, genpassword, permission):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.genpassword = genpassword
        self.permission = permission

    def to_json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))



