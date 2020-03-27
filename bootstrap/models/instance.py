from ..app import db
from .user import User

class Instance(db.Model):
    __tablename__ = 'instances'
    # __table_args__ = {"schema": "keldan"}

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String())
    public_ip = db.Column(db.String())
    private_ip = db.Column(db.String())
    state = db.Column(db.String())
    key_name = db.Column(db.String())


    def __init__(self):
        pass

    def add_instance(self, id, name, state, public_ip, private_ip, key_name):
        self.id = id
        self.name = name
        self.state = state
        self.public_ip = public_ip
        self.private_ip = private_ip
        self.key_name = key_name
        db.session.add(self)
        db.session.commit()

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


    def __repr__(self):
        return '<id {}>'.format(self.id)
