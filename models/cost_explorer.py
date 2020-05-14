import os
import sys
import pprint

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
from models.instance import Instance
from settings import db

ins_obj = Instance()

class CostExplorer(db.Model):
    __tablename__ = 'cost_explorer'
    __table_args__ = {'extend_existing': True}

    ce_instance_id = db.Column(db.String(), primary_key=True)
    ce_instance_name = db.Column(db.String())
    ce_instance_monthly_bill = db.Column(db.Float())
    ce_instance_daily_bill = db.Column(db.Float())
    
    def add_monthly_bill(self, instance_id, monthly_bill):
        self.ce_instance_id = instance_id
        self.ce_instance_monthly_bill = monthly_bill
        instance_name = ins_obj.get_instance_name_by_id(instance_id)
        self.ce_instance_name = instance_name
        row = CostExplorer.query.filter_by(ce_instance_id=instance_id).first()
        row = db.session.merge(self)
        db.session.add(row)
        db.session.commit()
        # if row:
        #     CostExplorer.query.filter_by(ce_instance_id=instance_id).update({CostExplorer.ce_instance_monthly_bill: monthly_bill})
        # else:
        #     db.session.add(self)
        # db.session.commit()

    def add_daily_bill(self, instance_id, daily_bill):
        self.ce_instance_id = instance_id
        self.ce_instance_daily_bill = daily_bill
        instance_name = ins_obj.get_instance_name_by_id(instance_id)
        self.ce_instance_name = instance_name
        row = CostExplorer.query.filter_by(ce_instance_id=instance_id).first()
        row = db.session.merge(self)
        db.session.add(row)
        db.session.commit()
        # if row:
        #     CostExplorer.query.filter_by(ce_instance_id=instance_id).update({CostExplorer.ce_instance_daily_bill: daily_bill})
        # else:
        #     db.session.add(self)
        # db.session.commit()
        
    def get_complete_bill_from_db(self):
        instances_bill_list = []
        complete_bill_list = CostExplorer.query.all()
        # pprint(complete_bill_list, '\n\n')
        for row in complete_bill_list:
            instance_name = ins_obj.get_instance_name_by_id(row.ce_instance_id)
            bill_dict = {
                "Id": row.ce_instance_id,
                "Name": instance_name,
                "DailyBill": row.ce_instance_daily_bill,
                "MonthlyBill": row.ce_instance_monthly_bill
            }
            instances_bill_list.append(bill_dict)
        return instances_bill_list
