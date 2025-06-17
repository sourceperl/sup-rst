from datetime import datetime

from sqlalchemy import (
    CHAR,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    SmallInteger,
    String,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.sql import func

# base class for declarative class definitions
Base = declarative_base()


# define the Alarm class that maps to the 'alarms' table in the database
class Alarm(Base):
    __tablename__ = 'alarms'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_host: Mapped[int] = mapped_column(ForeignKey('hosts.id'), nullable=False, default=0, server_default='0')
    daemon: Mapped[str] = mapped_column(String(6), nullable=False, default='')
    date_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    ack: Mapped[str] = mapped_column(CHAR(1), nullable=False, default='N', server_default='N')
    message: Mapped[str] = mapped_column(String(80), nullable=False, default='')

    # The index definition remains the same
    __table_args__ = (Index('alarms.date_time', 'date_time'),)

    def __repr__(self):
        return (f"<Alarm(id={self.id}, id_host={self.id_host}, daemon='{self.daemon}', "
                f"date_time={self.date_time}, ack='{self.ack}', message='{self.message}')>")


class Host(Base):
    __tablename__ = 'hosts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_subnet: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default='0')
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    hostname: Mapped[str] = mapped_column(String(30), nullable=False)

    icmp: Mapped['Icmp'] = relationship('Icmp', back_populates='host')
    mbus_l: Mapped[list['Mbus']] = relationship('Mbus', back_populates='host')

    def __repr__(self):
        return (f"<Host(id={self.id}, id_subnet={self.id_subnet}, name='{self.name}', "
                f"hostname='{self.hostname}')>")


class Subnet(Base):
    __tablename__ = 'subnets'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    gateway_tag: Mapped[str] = mapped_column(String(15), nullable=False)
    gateway_code: Mapped[str] = mapped_column(String(30), nullable=False)
    link_type: Mapped[str] = mapped_column(String(20), nullable=False)

    def __repr__(self):
        return (f"<Subnet(id={self.id}, name='{self.name}', gateway_tag='{self.gateway_tag}', "
                f"gateway_code='{self.gateway_code}', link_type='{self.link_type}')>")


class Variable(Base):
    __tablename__ = 'variables'

    name: Mapped[str] = mapped_column(String(30), primary_key=True, nullable=False)
    value: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self):
        return f"<Variable(name='{self.name}', value='{self.value}')>"


class Icmp(Base):
    __tablename__ = 'icmp'

    id_host: Mapped[int] = mapped_column(ForeignKey('hosts.id'), primary_key=True, nullable=False)
    icmp_inhibition: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, server_default='0')
    icmp_timeout: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=4, server_default='4')
    icmp_good_threshold: Mapped[int] = mapped_column(Integer, nullable=False, default=2, server_default='2')
    icmp_good_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default='0')
    icmp_fail_threshold: Mapped[int] = mapped_column(Integer, nullable=False, default=4, server_default='4')
    icmp_fail_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default='0')
    icmp_log_rtt: Mapped[str] = mapped_column(CHAR(1), nullable=False, default='N', server_default='N')
    icmp_state: Mapped[str] = mapped_column(CHAR(1), nullable=False, default='D', server_default='D')
    icmp_chg_state: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime(1970, 1, 1),
                                                     server_default=text("'1970-01-01 00:00:00'"))
    icmp_rtt: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default='0')
    icmp_up_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default='0')
    icmp_down_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default='0')

    host: Mapped['Host'] = relationship('Host', back_populates='icmp')

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

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_host: Mapped[int] = mapped_column(ForeignKey('hosts.id'), nullable=False, default=0)
    event_type: Mapped[str] = mapped_column(CHAR(1), nullable=False, default='')
    event_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime(1970, 1, 1))

    # The index definition remains the same
    __table_args__ = (Index('icmp_history.id_host', 'id_host'),)

    def __repr__(self):
        return (f"<IcmpHistory(id={self.id}, id_host={self.id_host}, event_type='{self.event_type}', "
                f"event_date={self.event_date})>")


class IcmpIndex(Base):
    __tablename__ = 'icmp_index'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_host: Mapped[int] = mapped_column(ForeignKey('hosts.id'), nullable=False, default=0)
    date_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime(1, 1, 1))
    up_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    down_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    def __repr__(self):
        return (f"<IcmpIndex(id={self.id}, id_host={self.id_host}, date_time={self.date_time}, "
                f"up_index={self.up_index}, down_index={self.down_index})>")


class IcmpRttLog(Base):
    __tablename__ = 'icmp_rtt_log'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_host: Mapped[int] = mapped_column(ForeignKey('hosts.id'), nullable=False, default=0)
    rtt: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rtt_datetime: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime(1970, 1, 1))

    def __repr__(self):
        return (f"<IcmpRttLog(id={self.id}, id_host={self.id_host}, rtt={self.rtt}, "
                f"rtt_datetime={self.rtt_datetime})>")


class Mbus(Base):
    __tablename__ = 'mbus'

    id_host: Mapped[int] = mapped_column(ForeignKey('hosts.id'), primary_key=True, nullable=False)
    mbus_inhibition: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, server_default='0')
    mbus_timeout: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=4, server_default='4')
    mbus_port: Mapped[int] = mapped_column(Integer, nullable=False, default=502, server_default='502')

    host: Mapped['Host'] = relationship('Host', back_populates='mbus_l')

    def __repr__(self):
        return (f"<Mbus(id_host={self.id_host}, mbus_inhibition={self.mbus_inhibition}, "
                f"mbus_timeout={self.mbus_timeout}, mbus_port={self.mbus_port})>")


class MbusTables(Base):
    __tablename__ = 'mbus_tables'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_host: Mapped[int] = mapped_column(ForeignKey('hosts.id'), nullable=False, default=0, server_default='0')
    unit_id: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1, server_default='1')
    type: Mapped[str] = mapped_column(String(16), nullable=False, default='words', server_default='words')
    address: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=23000, server_default='23000')
    size: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1, server_default='1')
    status: Mapped[str] = mapped_column(CHAR(1), nullable=False, default='E', server_default='E')
    update: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime(1970, 1, 1),
                                             server_default=text("'1970-01-01 00:00:00'"))
    comment: Mapped[str] = mapped_column(Text, nullable=False, default='')

    mbus_ts_l: Mapped[list['MbusTs']] = relationship('MbusTs', back_populates='mbus_table')

    def __repr__(self):
        return (f"<MbusTables(id={self.id}, id_host={self.id_host}, unit_id={self.unit_id}, "
                f"type='{self.type}', address={self.address}, size={self.size}, "
                f"status='{self.status}', update={self.update}, comment='{self.comment}')>")


class MbusTs(Base):
    __tablename__ = 'mbus_ts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_table: Mapped[int] = mapped_column(ForeignKey('mbus_tables.id'), nullable=False, default=0, server_default='0')
    use: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1, server_default='1')
    error: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1, server_default='1')
    index: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, server_default='0')
    bit: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, server_default='0')
    tag: Mapped[str] = mapped_column(String(15), nullable=False, default='')
    label: Mapped[str] = mapped_column(String(25), nullable=False, default='')
    ts: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, server_default='0')
    label_0: Mapped[str] = mapped_column(String(15), nullable=False, default='')
    label_1: Mapped[str] = mapped_column(String(15), nullable=False, default='')
    _not: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, server_default='0')
    info: Mapped[str] = mapped_column(Text, nullable=False, default='', server_default='1')
    al: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1, server_default='1')

    mbus_table: Mapped['MbusTables'] = relationship('MbusTables', back_populates='mbus_ts_l')

    __table_args__ = (Index('mbus_ts.tag', 'tag', unique=True),)

    def __repr__(self):
        return (f"<MbusTs(id={self.id}, id_table={self.id_table}, use={self.use}, "
                f"error={self.error}, index={self.index}, bit={self.bit}, "
                f"tag='{self.tag}', label='{self.label}', ts={self.ts}, "
                f"label_0='{self.label_0}', label_1='{self.label_1}', _not={self._not}, "
                f"info='{self.info}', al={self.al})>")


class MbusTsLog(Base):
    __tablename__ = 'mbus_ts_log'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_ts: Mapped[int] = mapped_column(ForeignKey('mbus_ts.id'), nullable=False, default=0)
    ts: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    update: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    __table_args__ = (Index('mbus_ts_log.id_ts', 'id_ts'),
                      Index('mbus_ts_log.update', 'update'))

    def __repr__(self):
        return (f"<MbusTsLog(id={self.id}, id_ts={self.id_ts}, ts={self.ts}, "
                f"update={self.update})>")


class MbusTm(Base):
    __tablename__ = 'mbus_tm'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_table: Mapped[int] = mapped_column(ForeignKey('mbus_tables.id'), nullable=False, default=0, server_default='0')
    use: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1, server_default='1')
    error: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1, server_default='1')
    index: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, server_default='0')
    tag: Mapped[str] = mapped_column(String(15), nullable=False, default='')
    label: Mapped[str] = mapped_column(String(25), nullable=False, default='')
    tm: Mapped[float] = mapped_column(Float, nullable=False, default=0.0, server_default='0')
    unit: Mapped[str] = mapped_column(String(8), nullable=False, default='')
    info: Mapped[str] = mapped_column(String(30), nullable=False, default='')
    can_min: Mapped[float] = mapped_column(Float, nullable=False, default=0.0, server_default='0')
    can_max: Mapped[float] = mapped_column(Float, nullable=False, default=1000.0, server_default='1000')
    gaz_min: Mapped[float] = mapped_column(Float, nullable=False, default=0.0, server_default='0')
    gaz_max: Mapped[float] = mapped_column(Float, nullable=False, default=1000.0, server_default='1000')
    signed: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1, server_default='1')
    log: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1, server_default='1')
    al: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, server_default='0')
    al_min: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, server_default='0')
    tm_min: Mapped[float] = mapped_column(Float, nullable=False, default=0.0, server_default='0')
    al_max: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0, server_default='0')
    tm_max: Mapped[float] = mapped_column(Float, nullable=False, default=1000.0, server_default='1000')
    tm_hist: Mapped[float] = mapped_column(Float, nullable=False, default=1.0, server_default='1')

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

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_tm: Mapped[int] = mapped_column(ForeignKey('mbus_tm.id'), nullable=False, default=0)
    tm: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    update: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime(1970, 1, 1))

    __table_args__ = (Index('mbus_tm_log.id_tm', 'id_tm'),
                      Index('mbus_tm_log.update', 'update'),
                      Index('mbus_tm_log.graph', 'id_tm', 'update'))

    def __repr__(self):
        return (f"<MbusTmLog(id={self.id}, id_tm={self.id_tm}, tm={self.tm}, "
                f"update={self.update})>")


class MbusTg(Base):
    __tablename__ = 'mbus_tg'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_table: Mapped[int] = mapped_column(ForeignKey('mbus_tables.id'), nullable=False, default=0)
    use: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)
    error: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)
    index: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    tag: Mapped[str] = mapped_column(String(15), nullable=False, default='')
    label: Mapped[str] = mapped_column(String(25), nullable=False, default='')
    tg: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_tg: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    last_tg_h: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    unit: Mapped[str] = mapped_column(String(8), nullable=False, default='')
    weight: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    info: Mapped[str] = mapped_column(Text, nullable=False)

    __table_args__ = (Index('mbus_tg.tag', 'tag', unique=True),)

    def __repr__(self):
        return (f"<MbusTg(id={self.id}, id_table={self.id_table}, use={self.use}, "
                f"error={self.error}, index={self.index}, tag='{self.tag}', "
                f"label='{self.label}', tg={self.tg}, last_tg={self.last_tg}, "
                f"last_tg_h={self.last_tg_h}, unit='{self.unit}', weight={self.weight}, "
                f"info='{self.info}')>")


class MbusTgLog(Base):
    __tablename__ = 'mbus_tg_log'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_tg: Mapped[int] = mapped_column(ForeignKey('mbus_tg.id'), nullable=False, default=0)
    type: Mapped[str] = mapped_column(CHAR(1), nullable=False, default='H')
    tg: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    update: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime(1, 1, 1))

    __table_args__ = (Index('mbus_tg_log.id_tg', 'id_tg'),)

    def __repr__(self):
        return (f"<MbusTgLog(id={self.id}, id_tg={self.id_tg}, type='{self.type}', "
                f"tg={self.tg}, update={self.update})>")


class MbusVGrad(Base):
    __tablename__ = 'mbus_v_grad'

    id_tm: Mapped[int] = mapped_column(ForeignKey('mbus_tm.id'), primary_key=True, nullable=False)
    use: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1, server_default='1')
    last_tm: Mapped[float] = mapped_column(Float, nullable=False, default=0, server_default='0')
    max_grad: Mapped[float] = mapped_column(Float, nullable=False, default=0, server_default='0')
    comment: Mapped[str] = mapped_column(Text, nullable=False, default='')

    def __repr__(self):
        return (f"<MbusVGrad(id_tm={self.id_tm}, use={self.use}, last_tm={self.last_tm}, "
                f"max_grad={self.max_grad}, comment='{self.comment}')>")


class MbusVTg(Base):
    __tablename__ = 'mbus_v_tg'

    id_tg: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, default=0)
    id_host: Mapped[int] = mapped_column(ForeignKey('hosts.id'), nullable=False, default=0, server_default='0')
    script: Mapped[str] = mapped_column(Text, nullable=False, default='')
    i_time: Mapped[int] = mapped_column(Integer, nullable=False, default=3600, server_default='3600')
    c_time: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default='0')
    comment: Mapped[str] = mapped_column(Text, nullable=False, default='')

    def __repr__(self):
        return (f"<MbusVTg(id_tg={self.id_tg}, id_host={self.id_host}, script='{self.script}', "
                f"i_time={self.i_time}, c_time={self.c_time}, comment='{self.comment}')>")


class MbusVTm(Base):
    __tablename__ = 'mbus_v_tm'

    id_tm: Mapped[int] = mapped_column(ForeignKey('mbus_tm.id'), primary_key=True, nullable=False, default=0)
    id_host: Mapped[int] = mapped_column(ForeignKey('hosts.id'), nullable=False, default=0)
    script: Mapped[str] = mapped_column(Text, nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False, default='')

    def __repr__(self):
        return (f"<MbusVTm(id_tm={self.id_tm}, id_host={self.id_host}, script='{self.script}', "
                f"comment='{self.comment}')>")


class MbusVTs(Base):
    __tablename__ = 'mbus_v_ts'

    id_ts: Mapped[int] = mapped_column(ForeignKey('mbus_ts.id'), primary_key=True, nullable=False)
    id_host: Mapped[int] = mapped_column(ForeignKey('hosts.id'), nullable=False, default=0, server_default='0')
    script: Mapped[str] = mapped_column(Text, nullable=False, default='')
    comment: Mapped[str] = mapped_column(Text, nullable=False, default='')

    def __repr__(self):
        return (f"<MbusVTs(id_ts={self.id_ts}, id_host={self.id_host}, script='{self.script}', "
                f"comment='{self.comment}')>")
