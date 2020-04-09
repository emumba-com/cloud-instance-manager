from ..app import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from ..models.user import User


class Instance(db.Model):
    __tablename__ = 'instances'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String())
    state = db.Column(db.String())
    public_ip = db.Column(db.String())
    private_ip = db.Column(db.String())
    key_name = db.Column(db.String())
    user_ids = db.Column(db.ARRAY(db.Integer), ForeignKey('users.id'))
    region_name = db.Column(db.String())
    # defining relationships
    user = relationship('User')

    # , backref = backref('users', cascade='save-update, merge, delete, delete-orphan'

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
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            pass

    # get all instance based on region name from db
    def get_all_instances(self, region_name):
        instanceList = []
        all_instance = db.session.query(Instance)
        for instance in all_instance:
            if instance.region_name == region_name:
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
                if instance.id == user.id:
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

    def get_user_instances(self, user_id):
        instance_detail = []
        instances = db.session.query(Instance)
        for instance in instances:
            users = instance.user_ids
            try:
                for user in len(users):
                    if user_id == user:
                        instanceDict = {
                            "Id": instance['id'],
                            "Name": instance['name'],
                            "State": instance['state'],
                            "PublicIP": instance['public_ip'],
                            "PrivateIP": instance['private_ip'],
                            "KeyName": instance['key_name'],
                            "RegionName": instance['region_name'],
                        }
                        instance_detail.append(instanceDict)

            except Exception as e:
                pass
        return instance_detail

    def assign_instance_to_user(slef, userId, ins_Id):
        print(userId, "userid")
        instance = db.session.query(Instance).filter(Instance.id == ins_Id)
        for i in instance:
            if i.id == ins_Id:
                db.session.execute
                print(i.key_name)
                db.session.query(Instance).filter(Instance.id == ins_Id).update({Instance.user_ids: Instance.user_ids.insert(0, userId)})
                db.session.commit()
        # typeof(instance.user_ids)
        # db.session.query(Instance).filter(Instance.id == ins_Id).update(
        #     {Instance.user_ids: instance.user_ids.insert(0, userId)})
        # db.session.commit()

    def __repr__(self):
        return '<id {}>'.format(self.id)
