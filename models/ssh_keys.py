import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

from settings import db


class SSHKeys(db.Model):
    __tablename__ = 'ssh_keys'
    __table_args__ = {'extend_existing': True}

    ssh_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ssh_key_name = db.Column(db.String(), unique=True)
    ssh_key_value = db.Column(db.String())
    ssh_key_format = db.Column(db.String())
    
    def add_key_name(self, key_name):
        self.ssh_key_name = key_name
        row = SSHKeys.query.filter_by(ssh_key_name=key_name).first()
        if row:
            try:
                db.session.merge(self)
                db.session.commit()
            except Exception as db_exceptions:
                print(db_exceptions)
        else:
            try:
                db.session.add(self)
                db.session.commit()
            except Exception as db_exceptions:
                print(db_exceptions)
        
    
    def add_key_with_value(self, ssh_key_name, ssh_key_value, ssh_key_format):
        self.ssh_key_name = ssh_key_name
        self.ssh_key_value = ssh_key_value
        self.ssh_key_format = ssh_key_formate
        row = SSHKeys.query.filter_by(ssh_key_name=ssh_key_name).first()
        if row:
            try:
                db.session.merge(self)
                db.session.commit()
            except Exception as db_exceptions:
                print(db_exceptions)
        else:
            try:
                db.session.add(self)
                db.session.commit()
            except Exception as db_exceptions:
                print(db_exceptions)
                
    def get_ssh_keys_from_db(self):
        keys_list = []
        all_ssh_keys = db.session.query(SSHKeys)
        for key in all_ssh_keys:
            keys_dict = {
                "KeyId": key.ssh_id,
                "KeyName": key.ssh_key_name,
                "KeyValue": key.ssh_key_value,
                "KeyFormat": key.ssh_key_format
            }
            keys_list.append(keys_dict)
        return keys_list