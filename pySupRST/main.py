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
        self.Session = sessionmaker(bind=self.engine)

    def get_ts(self, tag_name):
        """Get a ts record for tag name"""
        session = self.Session()
        try:
            ts = session.query(db.MbusTs).filter_by(tag=tag_name).first()
        except:
            return None
        finally:
            session.close()
        return ts

    def get_tm(self, tag_name):
        """Get a tm record for tag name"""
        session = self.Session()
        try:
            tm = session.query(db.MbusTm).filter_by(tag=tag_name).first()
        except:
            return None
        finally:
            session.close()
        return tm

    def set_alarm(self, message, date_time = None, id_host=0, daemon=""):
        """Set an alarm message on the log"""
        _datetime = date_time if date_time else func.now()
        session = self.Session()
        try:
            session.add(db.Alarm(message=message, date_time=_datetime,
                                 id_host=id_host, daemon=daemon))
            session.commit()
        except:
            return None
        finally:
            session.close()
        return True

    def get_env_tag(self, tag):
        """Get supervisor environment tag"""
        session = self.Session()
        try:
            env = session.query(db.SupEnv).filter_by(tag=tag).first()
        except:
            return None
        finally:
            session.close()
        return env.tag_value if env else None

    def set_env_tag(self, tag, tag_value):
        """Set supervisor environment tag"""
        session = self.Session()
        try:
            env = session.query(db.SupEnv).filter_by(tag=tag).first()
            if t:
                # update tag
                env.tag_value = tag_value
            else:
                # create tag
                session.add(db.SupEnv(tag=tag, tag_value=tag_value))
            session.commit()
        except:
            return None
        finally:
            session.close()
        return True

