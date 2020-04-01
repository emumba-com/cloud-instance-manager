from sqlalchemy import ForeignKey, update
from sqlalchemy.orm import relationship, backref
from ..app import db

class User(db.Model):
    __tablename__ = 'users'
    # __table_args__ = {"schema": "keldan"}

    id = db.Column(db.Integer, primary_key=True)
    ins_id = db.Column(db.String(), ForeignKey('instances.id'))
    name = db.Column(db.String())
    password = db.Column(db.String())
    # defining relationships
    user = relationship('Instance', backref=backref('users', cascade='save-update, merge, delete, delete-orphan'))


    def get_all_users(self):
        userList = []
        all_users = db.session.query(User)
        for user in all_users:
            userDict = {
                "Id": user.id,
                "Name": user.name,
            }
            userList.append(userDict)
        return userList

    def addUser(self, username, password):
        self.name = username
        self.password = password
        # print(username, password)
        db.session.add(self)
        db.session.commit()

    def assign_instance_to_user(self, username, ins_id):
        db.session.query(User).filter(User.name == username).update({User.ins_id : ins_id})
        db.session.commit()

    def unassign_instance_from_user(self, userId):
        db.session.query(User).filter(User.ins_id == userId).delete()
        db.session.commit()

    def deleteUser(self, userId):
        db.session.query(User).filter(User.id == userId).delete()
        db.session.commit()


db.create_all()
db.session.commit()
