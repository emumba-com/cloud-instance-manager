import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
from models.instance import Instance
from settings import db
from sqlalchemy import func
from datetime import datetime, timedelta
from sqlalchemy.schema import PrimaryKeyConstraint


ins_obj = Instance()


class CostExplorer(db.Model):
    __tablename__ = 'cost_explorer'

    ce_instance_id = db.Column(db.String())
    ce_date = db.Column(db.String(), nullable=True)
    ce_instance_name = db.Column(db.String(), nullable=True)
    ce_month = db.Column(db.String())
    ce_instance_daily_bill = db.Column(db.Float())
    __table_args__ = (
        PrimaryKeyConstraint('ce_instance_id', 'ce_date'),
        {},
    )

    def add_daily_bill(self, instance_id, current_month, today_date, daily_bill):
        ids = ins_obj.get_instances_ids()
        if instance_id in ids:
            print(instance_id)
            self.ce_instance_id = instance_id
            self.ce_month = current_month
            self.ce_date = today_date
            self.ce_instance_daily_bill = daily_bill
            instance_name = ins_obj.get_instance_name_by_id(instance_id)
            self.ce_instance_name = instance_name
            row = db.session.merge(self)
            db.session.add(row)
            db.session.commit()

    def get_complete_bill_from_db(self):
        c_month = datetime.utcnow().month
        c_date = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')
        instances_bill_list = []
        complete_bill_list = CostExplorer.query.filter_by(ce_month=str(c_month)).\
            with_entities(CostExplorer.ce_instance_id, func.sum(CostExplorer.ce_instance_daily_bill)).\
                group_by(CostExplorer.ce_instance_id).all()
        for row in complete_bill_list:
            instance_name = ins_obj.get_instance_name_by_id(row[0])
            result = CostExplorer.query.filter_by(ce_instance_id=row[0]).filter_by(ce_date=str(c_date)).first()
            if row[1] is None:
                row[1] = 0.0
            if result is None:
                daily_bill = 0.0
            else:
                daily_bill = result.ce_instance_daily_bill
<<<<<<< HEAD
            d_bill_roundoff = round(float(daily_bill), 2)
            m_bill_roundoff = round(float(row[1]), 2)
=======
>>>>>>> 6a13ae50b7ade24b90cf427446761f20862bd610
            bill_dict = {
                "Id": row[0],
                "Name": instance_name,
                "DailyBill": d_bill_roundoff,
                "MonthlyBill": m_bill_roundoff
            }
            instances_bill_list.append(bill_dict)
        return instances_bill_list

    def delete_instance_cost_from_db(self, ins_cost_list):
        for row in ins_cost_list:
            db.session.query(CostExplorer).filter(CostExplorer.ce_instance_id == row).delete()
        db.session.commit()
