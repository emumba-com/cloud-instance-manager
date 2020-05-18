import os
import sys
import pprint

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

from settings import db
from models.instance import Instance

instance_obj = Instance()


class SSHKeys(db.Model):
    __tablename__ = 'ssh_keys'
    __table_args__ = {'extend_existing': True}

    # ssh_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ssh_key_name = db.Column(db.String(), primary_key=True)
    ssh_key_value = db.Column(db.String())
    ssh_key_format = db.Column(db.String())

    def add_ssh_key_value(self, key_name, key_value, key_format):
        self.ssh_key_name = key_name
        self.ssh_key_value = key_value
        self.ssh_key_format = key_format
        row = db.session.merge(self)
        db.session.add(row)
        db.session.commit()

    def get_ssh_key_names(self):
        ssh_keys = set({})
        instances_list = instance_obj.get_all_instances_from_db()
        for instance in instances_list:
            ssh_keys.add(instance['KeyName'])
        return list(ssh_keys)

    def get_ssh_keys_from_db(self):
        all_keys_list = []
        remaining_keys_list = []
        key_names = self.get_ssh_key_names()
        all_ssh_keys = db.session.query(SSHKeys)
        for key in all_ssh_keys:
            keys_dict = {
                # "KeyId": key.ssh_id,
                "KeyName": key.ssh_key_name,
                "KeyValue": key.ssh_key_value,
                "KeyFormat": key.ssh_key_format
            }
            all_keys_list.append(keys_dict)
            if not key.ssh_key_value:
                if key in key_names:
                    key_names.remove(key)
        remaining_keys_list = [{"KeyName": key} for key in key_names]
        return remaining_keys_list, all_keys_list

    def get_key_by_name(self, key_name):
        row = SSHKeys.query.filter_by(ssh_key_name=key_name).first()
        key_dict = {
            "KeyName": row.ssh_key_name,
            "KeyValue": row.ssh_key_value,
            "keyFormat": row.ssh_key_format
        }
        return key_dict

    def delete_key(self, key_id):
        db.session.query(SSHKeys).filter(SSHKeys.ssh_key_name == key_id).delete()
        db.session.commit()
