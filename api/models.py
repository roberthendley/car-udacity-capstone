from typing import Dict
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Column, String, Integer, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship, validates

DEFAULT_PAGE_SIZE = 20

db = SQLAlchemy()
migrate = Migrate()

'''
Contact
'''


class Contact(db.Model):
    __tablename__ = "Contacts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email_address = Column(String(255), nullable=False)
    mobile_phone = Column(String(20), nullable=False)
    position_title = Column(String(50), nullable=False)
    contact_type = (Column(String(20), nullable=False))
    status = (Column(String(1), nullable=False, default='A'))

    def from_dict(self, data: dict) -> None:
        for key in data.keys():
            if hasattr(self, key):
                setattr(self, key, data.get(key))

    @validates('contact_type')
    def validate_contact_type(self, key, contact_type: str):
        assert contact_type in ['consultant', 'clientmanager', 'other']
        return contact_type

    def __init__(self, name, position_title, email_address, mobile_phone, contact_type) -> None:
        self.name = name
        self.position_title = position_title
        self.email_address = email_address
        self.mobile_phone = mobile_phone
        self.contact_type = contact_type

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'position_title': self.position_title,
            'email_address': self.email_address,
            'mobile_phone': self.mobile_phone,
            'contact_type': self.contact_type
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Client(db.Model):
    __tablename__ = "Clients"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    bus_reg_nbr = Column(String(20), nullable=False)
    abbreviation = Column(String(10), nullable=False)
    contacts = relationship(
        'ClientContact',
        backref='client',
        lazy='noload')
    reports = relationship('Report', backref='client', lazy='noload')

    def __init__(self, name: str = None, bus_reg_nbr: str = None, abbreviation: str = None) -> None:
        self.name = name
        self.bus_reg_nbr = bus_reg_nbr
        self.abbreviation = abbreviation

    def from_dict(self, data: dict) -> None:
        for key in data.keys():
            if hasattr(self, key):
                setattr(self, key, data.get(key))

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'abbreviation': self.abbreviation,
            'bus_reg_nbr': self.bus_reg_nbr
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class ClientContact(db.Model):
    __tablename__ = "Client_Contacts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('Clients.id'), nullable=False)
    name = Column(String, nullable=False)
    email_address = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    position_title = Column(String(50), nullable=True)
    address_1 = Column(String(100), nullable=True)
    address_2 = Column(String(100), nullable=True)
    address_3 = Column(String(100), nullable=True)
    city = Column(String(50), nullable=True)
    state = Column(String(50), nullable=True)
    post_code = Column(String(10), nullable=True)

    def format(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'name': self.name,
            'email_address': self.email_address,
            'phone': self.phone,
            'position_title': self.position_title,
            'address_1': self.address_1,
            'address_2': self.address_2,
            'address_3': self.address_3,
            'city': self.city,
            'state': self.state,
            'post_code': self.post_code
        }

    def __init__(self, name: str = None) -> None:
        self.name = name

    def from_dict(self, data: dict) -> None:
        for key in data.keys():
            if hasattr(self, key):
                setattr(self, key, data.get(key))

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Report(db.Model):
    __tablename__ = "Reports"
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('Clients.id'), nullable=False)
    client_contact_id = Column(Integer, ForeignKey(
        'Client_Contacts.id'), nullable=False)
    consulant_id = Column(Integer, ForeignKey('Contacts.id'), nullable=False)
    client_manager_id = Column(
        Integer, ForeignKey('Contacts.id'), nullable=False)
    report_date = Column(Date, nullable=False)
    report_from_date = Column(Date, nullable=False)
    report_to_date = Column(Date, nullable=True)
    engagement_reference = Column(String(20), nullable=False)
    report_status = Column(String(10), nullable=False)

    def from_dict(self, data: dict):

        for key in data.keys():
            if hasattr(self, key):
                setattr(self, key, data.get(key))

    @validates('report_status')
    def validate_report_status(self, key, status):
        assert status in ['new', 'in-progess',
                          'complete', 'reviewed', 'issued']
        return status

    def format(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'client_contact_id': self.client_contact_id,
            'consulant_id': self.consulant_id,
            'client_manager_id': self.client_manager_id,
            'report_date': self.report_date.strftime('%Y-%m-%d'),
            'report_from_date': self.report_from_date.strftime('%Y-%m-%d'),
            'report_to_date': self.format_report_date(self.report_to_date),
            'engagement_reference': self.engagement_reference,
            'report_status': self.report_status
        }

    def format_report_date(self, date):
        if date is None:
            return None
        else:
            return date.strftime('%Y-%m-%d')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class ReportItem(db.Model):
    __tablename__ = "Report_Items"
    report_id = Column(Integer, ForeignKey('Reports.id'), primary_key=True)
    report_item_nbr = Column(Integer, nullable=False, primary_key=True)
    item_type = Column(String(20), nullable=False)
    item_sequence_nbr = Column(Integer, nullable=False)
    item_description = Column(String, nullable=False)
    item_complete = Column(Boolean, nullable=True, default=False)
    request_expected_outcome = Column(String, nullable=True)
    issue_status = Column(String(20), nullable=True)
    issue_action_description = Column(String, nullable=True)

    def from_dict(self, data: dict) -> None:
        for key in data.keys():
            if hasattr(self, key):
                setattr(self, key, data.get(key))

    @validates('issue_status')
    def validate_issue_status(self, key, issue_status):
        assert issue_status in ['open', 'on-hold', 'resolved', 'blocked']
        return issue_status

    @validates('item_type')
    def validate_item_type(self, key, item_type):
        assert item_type in ['requested_task', 'work_undertaken',
                             'follow_up_task', 'customer_task', 'issue_identified']
        return item_type

    def format(self):
        return {
            'report_id': self.report_id,
            'report_item_nbr': self.report_item_nbr,
            'item_type': self.item_type,
            'item_sequence_nbr': self.item_sequence_nbr,
            'item_description': self.item_description,
            'item_complete': self.item_complete,
            'request_expected_outcome': self.request_expected_outcome,
            'issue_status': self.issue_status,
            'issue_action_description': self.issue_action_description,
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
