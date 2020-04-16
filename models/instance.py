import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))


from settings import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from models.user import User


class Instance(db.Model):
    __tablename__ = 'instances'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String())
    state = db.Column(db.String())
    public_ip = db.Column(db.String())
    private_ip = db.Column(db.String())
    key_name = db.Column(db.String())
    user_ids = db.Column(db.ARRAY(db.Integer))
    region_name = db.Column(db.String())
    # defining relationships


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
        row = Instance.query.filter_by(id=id).first()
        if row:
            db.session.merge(self)
            db.session.commit()
        else:
            db.session.add(self)
            db.session.commit()

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
                    "RegionName": instance.region_name,
                    "KeyName": instance.key_name,
                }
                instanceList.append(instanceDict)
        return instanceList

    # get all instance based on region name from db
    def get_all_instances_from_db(self):
        instanceList = []
        all_instance = db.session.query(Instance)
        for instance in all_instance:
            instanceDict = {
                "Id": instance.id,
                "Name": instance.name,
                "State": instance.state,
                "State": instance.state,
                "PublicIP": instance.public_ip,
                "PrivateIP": instance.private_ip,
                "RegionName": instance.region_name,
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
                    instanceList.append(instanceDict)
        return instanceList

    def get_user_instances(self, user_id):
        instance_detail = []
        instances = Instance.query.filter(Instance.user_ids.any(user_id)).all()
        
        for instance in instances:
            instanceDict = {
                "Id": instance.id,
                "Name": instance.name,
                "State": instance.state,
                "PublicIP": instance.public_ip,
                "PrivateIP": instance.private_ip,
                "KeyName": instance.key_name,
                "RegionName": instance.region_name,
            }
            instance_detail.append(instanceDict)
        return instance_detail

    def assign_instance_to_user(self, userId, ins_Id):
        row = Instance.query.filter_by(id=ins_Id).first()
        if row.user_ids is not None:
            if userId not in row.user_ids:
                row.user_ids.append(userId)
        else:
            row.user_ids = [userId]
        Instance.query.filter_by(id=ins_Id).update({Instance.user_ids: row.user_ids})
        db.session.commit()

    def un_assign_instance_from_user(self, userId, ins_Id):
        row = Instance.query.filter_by(id=ins_Id).first()
        print("method called ...")
        if not (not row.user_ids):
            userId = self.get_user_id_from_db(userId)
            if userId in row.user_ids:
                print("Removing user from list", userId)
                row.user_ids.remove(userId)
                Instance.query.filter_by(id=ins_Id).update({Instance.user_ids: row.user_ids})
                db.session.commit()
    
    def get_assigned_instances(self):
        assigned_instances_list = []
       
        all_instances = Instance.query.all()
       
        for row in all_instances:
            if not (not row.user_ids):
                owners = []
                for id in row.user_ids:
                    name = self.get_username(id)
                    if name is not None:
                        if name not in owners:
                            owners.append(name)
                instanceDict = {
                    "Id": row.id,
                    "Name": row.name,
                    "State": row.state,
                    "PublicIP": row.public_ip,
                    "PrivateIP": row.private_ip,
                    "RegionName": row.region_name,
                    "Owner": owners
                }
                assigned_instances_list.append(instanceDict)
        return assigned_instances_list
    
    def get_username(self, id):
        users = User.query.all()
        for user in users:
            if user.id == id:
                return user.name
        return None
    
    def get_user_id_from_db(self, username):
        userobj = db.session.query(User)
        for user in userobj:
            if user.name == username:
                return user.id


    def deleteUser(self, userId):
        all_instances = Instance.query.all()
        for row in all_instances:
            if row.user_ids is not None or len(row.user_ids) == 0:
                if int(userId) in row.user_ids:
                    row.user_ids.remove(int(userId))
                    Instance.query.filter_by(id=row.id).update({Instance.user_ids: row.user_ids})
                    db.session.commit()    
        db.session.query(User).filter(User.id == userId).delete()
        db.session.commit()

    def __repr__(self):
        return '<id {}>'.format(self.id)
