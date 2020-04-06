from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from ..app import db
from .user import User

class Instance(db.Model):
    __tablename__ = 'instances'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String())
    public_ip = db.Column(db.String())
    private_ip = db.Column(db.String())
    state = db.Column(db.String())
    key_name = db.Column(db.String())
    region_name = db.Column(db.String())

    user_ids = db.Column(db.ARRAY(db.Integer), ForeignKey('users.id'))

    # defining relationships
    instance = relationship('User', backref=backref('users', cascade='save-update, merge, delete, delete-orphan'))

    def __init__(self):
        pass

    def add_instance(self, id, name, state, public_ip, private_ip, key_name, region_name):
        self.id = id
        self.name = name
        self.state = state
        self.public_ip = public_ip
        self.private_ip = private_ip
        self.key_name = key_name
        self.region_name = region_name
        db.session.add(self)
        db.session.commit()

    # get all instance based on region name
    def get_all_instances(self):
        instanceList = []
        all_instance = db.session.query(Instance)

        for instance in all_instance:
            instanceDict = {
                "Id": instance.id,
                "Name": instance.name,
                "State": instance.state,
                "PublicIP": instance.public_ip,
                "PrivateIP": instance.private_ip,
                "KeyName": instance.key_name,
            }
            instanceList.append(instanceDict)
        return instanceList

    def get_instances_with_owner(self):
        # getting all users
        # instances = db.session.query(Instance).filter(User.ins_id == Instance.id)
        all_instances = db.session.query(Instance)
        all_users = db.session.query(User)

        instanceList = []
        for user in all_users:
            for instance in all_instances:
                if instance.id == user.ins_id:
                    instanceDict = {
                        "Id": instance.id,
                        "Name": instance.name,
                        "State": instance.state,
                        "PublicIP": instance.public_ip,
                        "PrivateIP": instance.private_ip,
                        "Owner": user.name,
                    }
                    print(instanceDict)
                    instanceList.append(instanceDict)
        return instanceList

    #
    # def assign_instance_to_user(self, username, ins_id):
    #     db.session.query(User).filter(User.name == username).update({User.ins_id : ins_id})
    #     db.session.commit()


    def __repr__(self):
        return '<id {}>'.format(self.id)
