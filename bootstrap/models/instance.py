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

            except Exception as e:
                pass
        return instance_detail

    def assign_instance_to_user(self, userId, ins_Id):
        # instance = db.session.query(Instance).filter(Instance.id == ins_Id)
        # db.session.query(Instance).filter(Instance.id == ins_Id).update(Instance.user_ids.insert(0, userId))
        row = Instance.query.filter_by(id=ins_Id).first()
        if row.user_ids is not None:
            row.user_ids.append(userId)
        else:
            row.user_ids = [userId]
        Instance.query.filter_by(id=ins_Id).update({Instance.user_ids: row.user_ids})
        db.session.commit()
    def __repr__(self):
        return '<id {}>'.format(self.id)
