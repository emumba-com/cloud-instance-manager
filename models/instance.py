import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

from settings import db
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

    def add_instance(self, instance_id, name, state, public_ip, private_ip, key_name, region_name):
        self.id = instance_id
        self.name = name
        self.state = state
        self.public_ip = public_ip
        self.private_ip = private_ip
        self.key_name = key_name
        self.region_name = region_name
        row = Instance.query.filter_by(id=instance_id).first()
        row = db.session.merge(self)
        db.session.add(row)
        db.session.commit()

    def get_all_instances_from_db(self):
        instances_list = []
        user_obj = User()

        all_instance = db.session.query(Instance)
        users_list = user_obj.get_all_users()

        for instance in all_instance:
            users = []
            ids = instance.user_ids
            if ids:
                for user in users_list:
                    if user['Id'] not in ids:
                        users.append(user)
            else:
                for user in users_list:
                    users.append(user)
            instance_dict = {
                "Id": instance.id,
                "Name": instance.name,
                "State": instance.state,
                "PublicIP": instance.public_ip,
                "PrivateIP": instance.private_ip,
                "RegionName": instance.region_name,
                "KeyName": instance.key_name,
                "Users": users
            }
            instances_list.append(instance_dict)
        return instances_list

    def get_user_instances(self, user_id):
        instance_detail = []
        instances = Instance.query.filter(Instance.user_ids.any(user_id)).all()

        for instance in instances:
            instance_dict = {
                "Id": instance.id,
                "Name": instance.name,
                "State": instance.state,
                "PublicIP": instance.public_ip,
                "PrivateIP": instance.private_ip,
                "KeyName": instance.key_name,
                "RegionName": instance.region_name,
            }
            instance_detail.append(instance_dict)
        return instance_detail

    def assign_instance_to_user(self, user_id, instance_id):
        row = Instance.query.filter_by(id=instance_id).first()
        if row.user_ids is not None:
            if user_id not in row.user_ids:
                row.user_ids.append(user_id)
        else:
            row.user_ids = [user_id]
        Instance.query.filter_by(id=instance_id).update({Instance.user_ids: row.user_ids})
        db.session.commit()

    def un_assign_instance_from_user(self, user_id, instance_id):
        row = Instance.query.filter_by(id=instance_id).first()
        if row.user_ids:
            user_id = self.get_user_id_from_db(user_id)
            if user_id in row.user_ids:
                row.user_ids.remove(user_id)
                Instance.query.filter_by(id=instance_id).update({Instance.user_ids: row.user_ids})
                db.session.commit()

    def get_assigned_instances(self):
        assigned_instances_list = []
        all_instances = Instance.query.all()
        for row in all_instances:
            if row.user_ids:
                owners = []
                for user_id in row.user_ids:
                    name = self.get_username(user_id)
                    if name is not None:
                        if name not in owners:
                            owners.append(name)
                instance_dict = {
                    "Id": row.id,
                    "Name": row.name,
                    "State": row.state,
                    "PublicIP": row.public_ip,
                    "PrivateIP": row.private_ip,
                    "RegionName": row.region_name,
                    "Owner": owners
                }
                assigned_instances_list.append(instance_dict)
        return assigned_instances_list

    def get_username(self, user_id):
        users = User.query.all()
        for user in users:
            if user.id == user_id:
                return user.name
        return None

    def get_user_id_from_db(self, username):
        userobj = db.session.query(User)
        for user in userobj:
            if user.name == username:
                return user.id
        return None

    def delete_user(self, user_id):
        all_instances = Instance.query.all()
        for row in all_instances:
            if row.user_ids:
                if int(user_id) in row.user_ids:
                    row.user_ids.remove(int(user_id))
                    Instance.query.filter_by(id=row.id).update({Instance.user_ids: row.user_ids})
                    db.session.commit()
        db.session.query(User).filter(User.id == user_id).delete()
        db.session.commit()

    def delete_instance_from_db(self, ins_list):
        for row in ins_list:
            db.session.query(Instance).filter(Instance.id == row).delete()
        db.session.commit()

    def __repr__(self):
        return '<id {}>'.format(self.id)
