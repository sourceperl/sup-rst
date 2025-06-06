from datetime import datetime

from sqlalchemy import (
    CHAR,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    SmallInteger,
    String,
    Text,
)
from sqlalchemy.orm import declarative_base

# base class for declarative class definitions
Base = declarative_base()


# define the Alarm class that maps to the 'alarms' table in the database
class Alarm(Base):
    __tablename__ = 'alarms'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_host = Column(Integer, nullable=False, default=0)
    daemon = Column(String(6), nullable=False, default='')
    date_time = Column(DateTime, nullable=False, default=datetime(1, 1, 1))
    ack = Column(CHAR(1), nullable=False, default='N')
    message = Column(String(80), nullable=False, default='')

    # define the index on the date_time column
    __table_args__ = (Index('alarms.date_time', 'date_time'),)

    def __repr__(self):
        return (f"<Alarm(id={self.id}, id_host={self.id_host}, daemon='{self.daemon}', "
                f"date_time={self.date_time}, ack='{self.ack}', message='{self.message}')>")


class Host(Base):
    __tablename__ = 'hosts'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_subnet = Column(Integer, nullable=False, default=0)
    name = Column(String(30), nullable=False, default='')
    hostname = Column(String(30), nullable=False, default='')

    def __repr__(self):
        return (f"<Host(id={self.id}, id_subnet={self.id_subnet}, name='{self.name}', "
                f"hostname='{self.hostname}')>")


class Icmp(Base):
    __tablename__ = 'icmp'

    id_host = Column(Integer, ForeignKey('hosts.id'), primary_key=True, nullable=False, default=0)
    icmp_inhibition = Column(SmallInteger, nullable=False, default=0)
    icmp_timeout = Column(SmallInteger, nullable=False, default=4)
    icmp_good_threshold = Column(Integer, nullable=False, default=2)
    icmp_good_count = Column(Integer, nullable=False, default=0)
    icmp_fail_threshold = Column(Integer, nullable=False, default=4)
    icmp_fail_count = Column(Integer, nullable=False, default=0)
    icmp_log_rtt = Column(CHAR(1), nullable=False, default='N')
    icmp_state = Column(CHAR(1), nullable=False, default='D')
    icmp_chg_state = Column(DateTime, nullable=False, default=datetime(1, 1, 1))
    icmp_rtt = Column(Integer, nullable=False, default=0)
    icmp_up_index = Column(Integer, nullable=False, default=0)
    icmp_down_index = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return (f"<Icmp(id_host={self.id_host}, icmp_inhibition={self.icmp_inhibition}, "
                f"icmp_timeout={self.icmp_timeout}, icmp_good_threshold={self.icmp_good_threshold}, "
                f"icmp_good_count={self.icmp_good_count}, icmp_fail_threshold={self.icmp_fail_threshold}, "
                f"icmp_fail_count={self.icmp_fail_count}, icmp_log_rtt='{self.icmp_log_rtt}', "
                f"icmp_state='{self.icmp_state}', icmp_chg_state={self.icmp_chg_state}, "
                f"icmp_rtt={self.icmp_rtt}, icmp_up_index={self.icmp_up_index}, "
                f"icmp_down_index={self.icmp_down_index})>")


class IcmpHistory(Base):
    __tablename__ = 'icmp_history'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_host = Column(Integer, nullable=False, default=0)
    event_type = Column(CHAR(1), nullable=False, default='')
    event_date = Column(DateTime, nullable=False, default=datetime(1, 1, 1))

    __table_args__ = (Index('icmp_history.id_host', 'id_host'),)

    def __repr__(self):
        return (f"<IcmpHistory(id={self.id}, id_host={self.id_host}, event_type='{self.event_type}', "
                f"event_date={self.event_date})>")


class IcmpIndex(Base):
    __tablename__ = 'icmp_index'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_host = Column(Integer, nullable=False, default=0)
    date_time = Column(DateTime, nullable=False, default=datetime(1, 1, 1))
    up_index = Column(Integer, nullable=False, default=0)
    down_index = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return (f"<IcmpIndex(id={self.id}, id_host={self.id_host}, date_time={self.date_time}, "
                f"up_index={self.up_index}, down_index={self.down_index})>")


class IcmpRttLog(Base):
    __tablename__ = 'icmp_rtt_log'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_host = Column(Integer, nullable=False, default=0)
    rtt = Column(Integer, nullable=False, default=0)
    rtt_datetime = Column(DateTime, nullable=False, default=datetime(1, 1, 1))

    def __repr__(self):
        return (f"<IcmpRttLog(id={self.id}, id_host={self.id_host}, rtt={self.rtt}, "
                f"rtt_datetime={self.rtt_datetime})>")


class Mbus(Base):
    __tablename__ = 'mbus'

    id_host = Column(Integer, primary_key=True, nullable=False, default=0)
    mbus_inhibition = Column(SmallInteger, nullable=False, default=0)
    mbus_timeout = Column(SmallInteger, nullable=False, default=4)
    mbus_port = Column(Integer, nullable=False, default=502)

    def __repr__(self):
        return (f"<Mbus(id_host={self.id_host}, mbus_inhibition={self.mbus_inhibition}, "
                f"mbus_timeout={self.mbus_timeout}, mbus_port={self.mbus_port})>")


class MbusTables(Base):
    __tablename__ = 'mbus_tables'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_host = Column(Integer, nullable=False, default=0)
    unit_id = Column(SmallInteger, nullable=False, default=1)
    type = Column(String(16), nullable=False, default='words')
    address = Column(SmallInteger, nullable=False, default=23000)
    size = Column(SmallInteger, nullable=False, default=1)
    status = Column(CHAR(1), nullable=False, default='E')
    update = Column(DateTime, nullable=False, default=datetime(1, 1, 1))
    comment = Column(Text, nullable=False)

    def __repr__(self):
        return (f"<MbusTables(id={self.id}, id_host={self.id_host}, unit_id={self.unit_id}, "
                f"type='{self.type}', address={self.address}, size={self.size}, "
                f"status='{self.status}', update={self.update}, comment='{self.comment}')>")


class MbusTg(Base):
    __tablename__ = 'mbus_tg'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_table = Column(Integer, nullable=False, default=0)
    use = Column(SmallInteger, nullable=False, default=1)
    error = Column(SmallInteger, nullable=False, default=1)
    index = Column(SmallInteger, nullable=False, default=0)
    tag = Column(String(15), nullable=False, default='')
    label = Column(String(25), nullable=False, default='')
    tg = Column(Integer, nullable=False, default=0)
    last_tg = Column(SmallInteger, nullable=False, default=0)
    last_tg_h = Column(Integer, nullable=False, default=0)
    unit = Column(String(8), nullable=False, default='')
    weight = Column(Integer, nullable=False, default=0)
    info = Column(Text, nullable=False)

    __table_args__ = (Index('mbus_tg.tag', 'tag', unique=True),)

    def __repr__(self):
        return (f"<MbusTg(id={self.id}, id_table={self.id_table}, use={self.use}, "
                f"error={self.error}, index={self.index}, tag='{self.tag}', "
                f"label='{self.label}', tg={self.tg}, last_tg={self.last_tg}, "
                f"last_tg_h={self.last_tg_h}, unit='{self.unit}', weight={self.weight}, "
                f"info='{self.info}')>")


class MbusTgLog(Base):
    __tablename__ = 'mbus_tg_log'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_tg = Column(Integer, nullable=False, default=0)
    type = Column(CHAR(1), nullable=False, default='H')
    tg = Column(Integer, nullable=False, default=0)
    update = Column(DateTime, nullable=False, default=datetime(1, 1, 1))

    __table_args__ = (Index('mbus_tg_log.id_tg', 'id_tg'),)

    def __repr__(self):
        return (f"<MbusTgLog(id={self.id}, id_tg={self.id_tg}, type='{self.type}', "
                f"tg={self.tg}, update={self.update})>")


class MbusTm(Base):
    __tablename__ = 'mbus_tm'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_table = Column(Integer, nullable=False, default=0)
    use = Column(SmallInteger, nullable=False, default=1)
    error = Column(SmallInteger, nullable=False, default=1)
    index = Column(SmallInteger, nullable=False, default=0)
    tag = Column(String(15), nullable=False, default='')
    label = Column(String(25), nullable=False, default='')
    tm = Column(Float, nullable=False, default=0.0)
    unit = Column(String(8), nullable=False, default='')
    info = Column(String(30), nullable=False, default='')
    can_min = Column(Float, nullable=False, default=0.0)
    can_max = Column(Float, nullable=False, default=1000.0)
    gaz_min = Column(Float, nullable=False, default=0.0)
    gaz_max = Column(Float, nullable=False, default=1000.0)
    signed = Column(SmallInteger, nullable=False, default=1)
    log = Column(SmallInteger, nullable=False, default=1)
    al = Column(SmallInteger, nullable=False, default=0)
    al_min = Column(SmallInteger, nullable=False, default=0)
    tm_min = Column(Float, nullable=False, default=0.0)
    al_max = Column(SmallInteger, nullable=False, default=0)
    tm_max = Column(Float, nullable=False, default=1000.0)
    tm_hist = Column(Float, nullable=False, default=1.0)

    __table_args__ = (Index('mbus_tm.tag', 'tag', unique=True),)

    def __repr__(self):
        return (f"<MbusTm(id={self.id}, id_table={self.id_table}, use={self.use}, "
                f"error={self.error}, index={self.index}, tag='{self.tag}', "
                f"label='{self.label}', tm={self.tm}, unit='{self.unit}', "
                f"info='{self.info}', can_min={self.can_min}, can_max={self.can_max}, "
                f"gaz_min={self.gaz_min}, gaz_max={self.gaz_max}, signed={self.signed}, "
                f"log={self.log}, al={self.al}, al_min={self.al_min}, tm_min={self.tm_min}, "
                f"al_max={self.al_max}, tm_max={self.tm_max}, tm_hist={self.tm_hist})>")


class MbusTmLog(Base):
    __tablename__ = 'mbus_tm_log'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_tm = Column(Integer, nullable=False, default=0)
    tm = Column(Float, nullable=False, default=0.0)
    update = Column(DateTime, nullable=False, default=datetime(1, 1, 1))

    __table_args__ = (Index('mbus_tm_log.id_tm', 'id_tm'), 
                      Index('mbus_tm_log.update', 'update'), 
                      Index('mbus_tm_log.graph', 'id_tm', 'update'))

    def __repr__(self):
        return (f"<MbusTmLog(id={self.id}, id_tm={self.id_tm}, tm={self.tm}, "
                f"update={self.update})>")


class MbusTs(Base):
    __tablename__ = 'mbus_ts'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_table = Column(Integer, nullable=False, default=0)
    use = Column(SmallInteger, nullable=False, default=1)
    error = Column(SmallInteger, nullable=False, default=1)
    index = Column(SmallInteger, nullable=False, default=0)
    bit = Column(SmallInteger, nullable=False, default=0)
    tag = Column(String(15), nullable=False, default='')
    label = Column(String(25), nullable=False, default='')
    ts = Column(SmallInteger, nullable=False, default=0)
    label_0 = Column(String(15), nullable=False, default='')
    label_1 = Column(String(15), nullable=False, default='')
    _not = Column(SmallInteger, nullable=False, default=0)
    info = Column(Text, nullable=False)
    al = Column(SmallInteger, nullable=False, default=1)

    __table_args__ = (Index('mbus_ts.tag', 'tag', unique=True),)

    def __repr__(self):
        return (f"<MbusTs(id={self.id}, id_table={self.id_table}, use={self.use}, "
                f"error={self.error}, index={self.index}, bit={self.bit}, "
                f"tag='{self.tag}', label='{self.label}', ts={self.ts}, "
                f"label_0='{self.label_0}', label_1='{self.label_1}', _not={self._not}, "
                f"info='{self.info}', al={self.al})>")


class MbusTsLog(Base):
    __tablename__ = 'mbus_ts_log'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_ts = Column(Integer, nullable=False, default=0)
    ts = Column(SmallInteger, nullable=False, default=0)
    update = Column(DateTime, nullable=False, default=datetime(1, 1, 1))

    __table_args__ = (Index('mbus_ts_log.id_ts', 'id_ts'), 
                      Index('mbus_ts_log.update', 'update'))

    def __repr__(self):
        return (f"<MbusTsLog(id={self.id}, id_ts={self.id_ts}, ts={self.ts}, "
                f"update={self.update})>")


class MbusVGrad(Base):
    __tablename__ = 'mbus_v_grad'

    id_tm = Column(Integer, primary_key=True, nullable=False, default=0)
    use = Column(SmallInteger, nullable=False, default=1)
    last_tm = Column(Float, nullable=False, default=0.0)
    max_grad = Column(Float, nullable=False, default=0.0)
    comment = Column(Text, nullable=False)

    def __repr__(self):
        return (f"<MbusVGrad(id_tm={self.id_tm}, use={self.use}, last_tm={self.last_tm}, "
                f"max_grad={self.max_grad}, comment='{self.comment}')>")


class MbusVTg(Base):
    __tablename__ = 'mbus_v_tg'

    id_tg = Column(Integer, primary_key=True, nullable=False, default=0)
    id_host = Column(Integer, nullable=False, default=0)
    script = Column(Text, nullable=False)
    i_time = Column(Integer, nullable=False, default=3600)
    c_time = Column(Integer, nullable=False, default=0)
    comment = Column(Text, nullable=False)

    def __repr__(self):
        return (f"<MbusVTg(id_tg={self.id_tg}, id_host={self.id_host}, script='{self.script}', "
                f"i_time={self.i_time}, c_time={self.c_time}, comment='{self.comment}')>")


class MbusVTm(Base):
    __tablename__ = 'mbus_v_tm'

    id_tm = Column(Integer, primary_key=True, nullable=False, default=0)
    id_host = Column(Integer, nullable=False, default=0)
    script = Column(Text, nullable=False)
    comment = Column(Text, nullable=False)

    def __repr__(self):
        return (f"<MbusVTm(id_tm={self.id_tm}, id_host={self.id_host}, script='{self.script}', "
                f"comment='{self.comment}')>")


class MbusVTs(Base):
    __tablename__ = 'mbus_v_ts'

    id_ts = Column(Integer, primary_key=True, nullable=False, default=0)
    id_host = Column(Integer, nullable=False, default=0)
    script = Column(Text, nullable=False)
    comment = Column(Text, nullable=False)

    def __repr__(self):
        return (f"<MbusVTs(id_ts={self.id_ts}, id_host={self.id_host}, script='{self.script}', "
                f"comment='{self.comment}')>")


class Subnet(Base):
    __tablename__ = 'subnets'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(30), nullable=False, default='')
    gateway_tag = Column(String(15), nullable=False, default='')
    gateway_code = Column(String(30), nullable=False, default='')
    link_type = Column(String(20), nullable=False, default='')

    def __repr__(self):
        return (f"<Subnet(id={self.id}, name='{self.name}', gateway_tag='{self.gateway_tag}', "
                f"gateway_code='{self.gateway_code}', link_type='{self.link_type}')>")


class Variable(Base):
    __tablename__ = 'variables'

    name = Column(String(30), primary_key=True, nullable=False)
    value = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<Variable(name='{self.name}', value='{self.value}')>"
