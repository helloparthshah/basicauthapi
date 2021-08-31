from werkzeug.security import generate_password_hash
import uuid


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password, method='sha256')
        self.publicId = str(uuid.uuid4())
        self.homes = []

    def toJSON(self):
        return {
            'username': self.username,
            'password': self.password,
            'public_Id': self.publicId,
            'homes': self.homes,
        }

    def addHome(self, home):
        self.homes.append(home)
