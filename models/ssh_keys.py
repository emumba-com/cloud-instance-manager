import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

from settings import db


class SSHKeys(db.Model):
    __tablename__ = 'ssh_keys'
    __table_args__ = {'extend_existing': True}

    # ssh_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ssh_key_name = db.Column(db.String(), primary_key=True)
    ssh_key_value = db.Column(db.String())
    ssh_key_format = db.Column(db.String())

    
    def add_ssh_key_name(self, key_name):
        self.ssh_key_name = key_name
        self.ssh_key_value = None
        self.ssh_key_format = None
        row = SSHKeys.query.filter_by(ssh_key_name=key_name).first()
        if not row:
            try:
                print("adding")
                db.session.add(self)
                db.session.commit()
            except Exception as db_exceptions:
                print(db_exceptions)


    def add_ssh_key_value(self, key_name, key_value, key_format):
        self.ssh_key_name = key_name
        self.ssh_key_value = key_value
        self.ssh_key_format = key_format
        row = db.session.merge(self)
        db.session.add(row)
        db.session.commit()
    
    
    def get_ssh_keys_from_db(self):
        all_keys_list = []
        key_list = []
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
                empty_key_dict = {
                    "KeyName": key.ssh_key_name,
                }
                key_list.append(empty_key_dict)
        return key_list, all_keys_list
    
    
    def get_key_by_name(key_name):
        row = SSHKeys.query.filter_by(ssh_key_name=key_name).first()
        key_dict = {
            "KeyName": row.ssh_key_name,
            "KeyValue": row.ssh_key_value,
            "keyFormat": row.ssh_key_format
        } 
        return key_dict