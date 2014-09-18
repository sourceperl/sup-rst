# -*- coding: utf-8 -*-
from sqlalchemy import Column, DateTime, Float, Index, Integer, \
                       SmallInteger, String, Table, Text, text
from sqlalchemy.ext.declarative import declarative_base

# mother class of every map class (a class = SQL table row)
Base = declarative_base()

# SQL tables class maps (class name must be singular and CamelCase PEP8)
class Alarm(Base):
    __tablename__ = 'alarms'

    id = Column(Integer, primary_key=True)
    id_host = Column(Integer, nullable=False, server_default=text("'0'"))
    daemon = Column(String(6), nullable=False, server_default=text("''"))
    date_time = Column(DateTime, nullable=False, index=True,
                       server_default=text("'0000-00-00 00:00:00'"))
    ack = Column(String(1), nullable=False, server_default=text("'N'"))
    message = Column(String(80), nullable=False, server_default=text("''"))

    def __repr__(self):
        return u"<Alarm(id_host=%r, daemon=%r, date_time=%r, ack=%r, " \
                "message=%r)>" % (self.id_host, self.daemon, self.date_time,
                                  self.ack, self.message)


class Host(Base):
    __tablename__ = 'hosts'

    id = Column(Integer, primary_key=True)
    id_subnet = Column(Integer, nullable=False, server_default=text("'0'"))
    name = Column(String(30), nullable=False, server_default=text("''"))
    hostname = Column(String(30), nullable=False, server_default=text("''"))
    host_activity = Column(String(1), nullable=False,
                           server_default=text("'N'"))

    def __repr__(self):
        return u"<Host(id_subnet=%r, name=%r, hostname=%r, host_activity=%r>" \
               % (self.id_subnet, self.name, self.hostname, self.host_activity)


class Icmp(Base):
    __tablename__ = 'icmp'

    id_host = Column(Integer, primary_key=True, server_default=text("'0'"))
    icmp_inhibition = Column(String(1), nullable=False,
                             server_default=text("'N'"))
    icmp_timeout = Column(SmallInteger, nullable=False,
                          server_default=text("'4'"))
    icmp_good_threshold = Column(Integer, nullable=False,
                                 server_default=text("'2'"))
    icmp_good_count = Column(Integer, nullable=False,
                             server_default=text("'0'"))
    icmp_fail_threshold = Column(Integer, nullable=False,
                                 server_default=text("'2'"))
    icmp_fail_count = Column(Integer, nullable=False,
                             server_default=text("'0'"))
    icmp_log_rtt = Column(String(1), nullable=False, server_default=text("'N'"))
    icmp_state = Column(String(1), nullable=False, server_default=text("'D'"))
    icmp_chg_state = Column(DateTime, nullable=False,
                            server_default=text("'0000-00-00 00:00:00'"))
    icmp_rtt = Column(Integer, nullable=False, server_default=text("'0'"))
    icmp_up_index = Column(Integer, nullable=False, server_default=text("'0'"))
    icmp_down_index = Column(Integer, nullable=False,
                             server_default=text("'0'"))

    def __repr__(self):
        return u"<Icmp(id_host=%r, icmp_inhibition=%r, icmp_state=%r>" \
               % (self.id_host, self.icmp_inhibition, self.icmp_state)


class IcmpHistory(Base):
    __tablename__ = 'icmp_history'

    id = Column(Integer, primary_key=True)
    host_id = Column(Integer, nullable=False, index=True,
                     server_default=text("'0'"))
    event_type = Column(String(1), nullable=False, server_default=text("''"))
    event_date = Column(DateTime, nullable=False,
                        server_default=text("'0000-00-00 00:00:00'"))

    def __repr__(self):
        return u"<IcmpHistory(host_id=%r, event_type=%r, event_date=%r>" \
               % (self.host_id, self.event_type, self.event_date)


class IcmpIndex(Base):
    __tablename__ = 'icmp_index'

    id = Column(Integer, primary_key=True)
    id_host = Column(Integer, nullable=False, server_default=text("'0'"))
    date_time = Column(DateTime, nullable=False,
                       server_default=text("'0000-00-00 00:00:00'"))
    up_index = Column(Integer, nullable=False, server_default=text("'0'"))
    down_index = Column(Integer, nullable=False, server_default=text("'0'"))

    def __repr__(self):
        return u"<IcmpIndex(id_host=%r, date_time=%r, up_index=%r, " \
                "down_index=%r>" % (self.id_host, self.date_time,
                                    self.up_index, self.down_index)


class IcmpRttLog(Base):
    __tablename__ = 'icmp_rtt_log'

    id = Column(Integer, primary_key=True)
    id_host = Column(Integer, nullable=False, server_default=text("'0'"))
    rtt = Column(Integer, nullable=False, server_default=text("'0'"))
    rtt_datetime = Column(DateTime, nullable=False,
                          server_default=text("'0000-00-00 00:00:00'"))

    def __repr__(self):
        return u"<IcmpRTTLog(id_host=%r, rtt=%r, rtt_datetime=%r>" \
               % (self.id_host, self.rtt, self.rtt_datetime)


class Mbus(Base):
    __tablename__ = 'mbus'

    id_host = Column(Integer, primary_key=True, server_default=text("'0'"))
    mbus_inhibition = Column(String(1), nullable=False,
                             server_default=text("'N'"))
    mbus_timeout = Column(SmallInteger, nullable=False,
                             server_default=text("'4'"))
    mbus_port = Column(Integer, nullable=False, server_default=text("'502'"))

    def __repr__(self):
        return u"<Mbus(id_host=%r, mbus_inhibition=%r, mbus_timeout=%r, " \
                "mbus_port=%r>" % (self.id_host, self.mbus_inhibition,
                                   self.mbus_timeout, self.mbus_port)


class MbusTables(Base):
    __tablename__ = 'mbus_tables'

    id = Column(Integer, primary_key=True)
    id_host = Column(Integer, nullable=False, server_default=text("'0'"))
    unit_id = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    timeout = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    address = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    size = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    status = Column(String(1), nullable=False, server_default=text("'E'"))
    update = Column(DateTime, nullable=False,
                    server_default=text("'0000-00-00 00:00:00'"))

    def __repr__(self):
        return u"<Mbus(id_host=%r, unit_id=%r, timeout=%r, " \
                "address=%r, size=%r, status=%r>" \
                % (self.id_host, self.unit_id, self.timeout,
                   self.address, self.size, self.status)


class MbusTg(Base):
    __tablename__ = 'mbus_tg'

    id = Column(Integer, primary_key=True)
    id_table = Column(Integer, nullable=False, server_default=text("'0'"))
    use = Column(Integer, nullable=False, server_default=text("'1'"))
    error = Column(Integer, nullable=False, server_default=text("'1'"))
    index = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    tag = Column(String(15), nullable=False, unique=True,
                 server_default=text("''"))
    label = Column(String(25), nullable=False, server_default=text("''"))
    tg = Column(Integer, nullable=False, server_default=text("'0'"))
    last_tg = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    last_tg_h = Column(Integer, nullable=False, server_default=text("'0'"))
    unit = Column(String(8), nullable=False, server_default=text("''"))
    weight = Column(Integer, nullable=False, server_default=text("'0'"))
    info = Column(Text, nullable=False)

    def __repr__(self):
        return u"<MbusTg(tag=%r, label=%r, tg=%r, unit=%r)>" \
               % (self.tag, self.label, self.tg, self.unit)

class MbusTgLog(Base):
    __tablename__ = 'mbus_tg_log'

    id = Column(Integer, primary_key=True)
    id_tg = Column(Integer, nullable=False, index=True,
                   server_default=text("'0'"))
    type = Column(String(1), nullable=False, server_default=text("'H'"))
    tg = Column(Integer, nullable=False, server_default=text("'0'"))
    update = Column(DateTime, nullable=False,
                    server_default=text("'0000-00-00 00:00:00'"))

    def __repr__(self):
        return u"<MbusTgLog(id_tg=%r, type=%r, tg=%r, update=%r)>" \
               % (self.id_tg, self.type, self.tg, self.update)


class MbusTs(Base):
    __tablename__ = 'mbus_ts'

    id = Column(Integer, primary_key=True)
    id_table = Column(Integer, nullable=False, server_default=text("'0'"))
    use = Column(Integer, nullable=False, server_default=text("'1'"))
    error = Column(Integer, nullable=False, server_default=text("'1'"))
    index = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    bit = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    tag = Column(String(15), nullable=False, unique=True,
                 server_default=text("''"))
    label = Column(String(25), nullable=False, server_default=text("''"))
    ts = Column(Integer, nullable=False, server_default=text("'0'"))
    label_0 = Column(String(15), nullable=False, server_default=text("''"))
    label_1 = Column(String(15), nullable=False, server_default=text("''"))
    _not = Column('not', Integer, nullable=False, server_default=text("'0'"))
    info = Column(Text, nullable=False)
    al = Column(Integer, nullable=False, server_default=text("'1'"))

    def __repr__(self):
        return u"<MbusTs(tag=%r, label=%r, ts=%r, label_0=%r, label_1=%r)>" \
               % (self.tag, self.label, self.ts, self.label_0, self.label_1)

class MbusTsLog(Base):
    __tablename__ = 'mbus_ts_log'

    id = Column(Integer, primary_key=True)
    id_ts = Column(Integer, nullable=False, server_default=text("'0'"))
    ts = Column(Integer, nullable=False, server_default=text("'0'"))
    update = Column(DateTime, nullable=False,
                    server_default=text("'0000-00-00 00:00:00'"))

    def __repr__(self):
        return u"<MbusTsLog(id_ts=%r, ts=%r, update=%r)>" \
               % (self.id_ts, self.ts, self.update)


class MbusTm(Base):
    __tablename__ = 'mbus_tm'

    id = Column(Integer, primary_key=True)
    id_table = Column(Integer, nullable=False, server_default=text("'0'"))
    use = Column(Integer, nullable=False, server_default=text("'1'"))
    error = Column(Integer, nullable=False, server_default=text("'1'"))
    index = Column(SmallInteger, nullable=False, server_default=text("'0'"))
    tag = Column(String(15), nullable=False, unique=True,
                 server_default=text("''"))
    label = Column(String(25), nullable=False, server_default=text("''"))
    tm = Column(Float, nullable=False, server_default=text("'0'"))
    unit = Column(String(8), nullable=False, server_default=text("''"))
    info = Column(String(30), nullable=False, server_default=text("''"))
    can_min = Column(Integer, nullable=False, server_default=text("'0'"))
    can_max = Column(Integer, nullable=False, server_default=text("'0'"))
    gaz_min = Column(Integer, nullable=False, server_default=text("'0'"))
    gaz_max = Column(Integer, nullable=False, server_default=text("'0'"))
    signed = Column(Integer, nullable=False, server_default=text("'0'"))
    log = Column(Integer, nullable=False, server_default=text("'0'"))
    al = Column(Integer, nullable=False, server_default=text("'0'"))
    al_min = Column(Integer, nullable=False, server_default=text("'0'"))
    tm_min = Column(Float, nullable=False, server_default=text("'0'"))
    al_max = Column(Integer, nullable=False, server_default=text("'0'"))
    tm_max = Column(Float, nullable=False, server_default=text("'0'"))
    tm_hist = Column(Float, nullable=False, server_default=text("'0'"))

    def __repr__(self):
        return u"<MbusTm(tag=%r, label=%r, tm=%r)>" \
               % (self.tag, self.label, self.tm)


class MbusTmLog(Base):
    __tablename__ = 'mbus_tm_log'
    __table_args__ = (
        Index('graph', 'id_tm', 'update'),
    )

    id = Column(Integer, primary_key=True)
    id_tm = Column(Integer, nullable=False, index=True,
                   server_default=text("'0'"))
    tm = Column(Float, nullable=False, server_default=text("'0'"))
    update = Column(DateTime, nullable=False, index=True,
                    server_default=text("'0000-00-00 00:00:00'"))

    def __repr__(self):
        return u"<MbusTmLog(id_tm=%r, tm=%r, update=%r)>" \
               % (self.id_tm, self.tm, self.update)


class MbusVirtualTg(Base):
    __tablename__ = 'mbus_v_tg'

    id_tg = Column(Integer, primary_key=True, server_default=text("'0'"))
    id_host = Column(Integer, nullable=False, server_default=text("'0'"))
    script = Column(Text, nullable=False)
    i_time = Column(Integer, nullable=False, server_default=text("'3600'"))
    c_time = Column(Integer, nullable=False, server_default=text("'0'"))
    comment = Column(Text, nullable=False)

    def __repr__(self):
        return u"<MbusVirtualTg(id_host=%r, script=%r, i_time=%r, c_time=%r, " \
                "comment=%r)>" % (self.id_host, self.script, self.i_time,
                                  self.c_time, self.comment)


class MbusVirtualGradient(Base):
    __tablename__ = 'mbus_v_grad'

    id_tm = Column(Integer, primary_key=True, server_default=text("'0'"))
    use = Column(Integer, nullable=False, server_default=text("'1'"))
    last_tm = Column(Float, nullable=False, server_default=text("'0'"))
    max_grad = Column(Float, nullable=False, server_default=text("'0'"))
    comment = Column(Text, nullable=False)

    def __repr__(self):
        return u"<MbusVirtualGradient(id_tm = %r, use=%r, last_tm=%r, " \
                "max_grad=%r, comment=%r)>" \
               % (self.id_tm, self.use, self.last_tm,
                  self.max_grad, self.comment)


class MbusVirtualTm(Base):
    __tablename__ = 'mbus_v_tm'

    id_tm = Column(Integer, primary_key=True, server_default=text("'0'"))
    id_host = Column(Integer, nullable=False, server_default=text("'0'"))
    script = Column(Text, nullable=False)
    comment = Column(Text, nullable=False)

    def __repr__(self):
        return u"<MbusVirtualTm(id_tm = %r, id_host=%r, script=%r, " \
                "comment=%r)>" % (self.id_tm, self.id_host, self.script,
                                  self.comment)


class MbusVirtualTs(Base):
    __tablename__ = 'mbus_v_ts'

    id_ts = Column(Integer, primary_key=True, server_default=text("'0'"))
    id_host = Column(Integer, nullable=False, server_default=text("'0'"))
    script = Column(Text, nullable=False)

    def __repr__(self):
        return u"<MbusVirtualTs(id_ts=%r, id_host=%r, script=%r, comment=%r)>" \
               % (self.id_ts, self.id_host, self.script, self.comment)


class Subnet(Base):
    __tablename__ = 'subnets'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, server_default=text("''"))
    gateway_tag = Column(String(15), nullable=False, server_default=text("''"))
    gateway_code = Column(String(30), nullable=False, server_default=text("''"))
    link_type = Column(String(20), nullable=False, server_default=text("'P'"))
    link_backup = Column(String(1), nullable=False, server_default=text("'N'"))

    def __repr__(self):
        return u"<Subnet(name=%r, gateway_tag=%r, gateway_code=%r)>" \
               % (self.name, self.gateway_tag, self.gateway_code)

