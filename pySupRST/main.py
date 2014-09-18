# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, DateTime, Float, Index, Integer, \
                       SmallInteger, String, Table, Text, text, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import db_class as db

# some consts
DB_STR = "mysql+mysqlconnector://sup_rst:sup_rst@localhost/sup_rst"

class sup_rst():
    """Fast access class to SUP_RST database"""

    def __init__(self):
        """Constructor"""
        # connect to DB
        self.engine = create_engine(DB_STR)
        # if tables not exist: create it
        db.Base.metadata.create_all(self.engine)
        # build a session instance for DB access
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_ts(self, tag_name):
        """Get a ts record for tag name"""
        return self.session.query(db.MbusTs).filter_by(tag=tag_name).first()

    def get_tm(self, tag_name):
        """Get a tm record for tag name"""
        return self.session.query(db.MbusTm).filter_by(tag=tag_name).first()

    def set_alarm(self, message, date_time = None, id_host=0, daemon=""):
        """Set an alarm message on the log"""
        try:
            _datetime = date_time if date_time else func.now()
            self.session.add(db.Alarm(message=message, date_time=_datetime,
                                      id_host=id_host, daemon=daemon))
            self.session.commit()
        except:
            return None
        else:
            return True
