import re
from typing import Optional, TypeVar

from sqlalchemy import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from ..db.models import Alarm, MbusTm, MbusTs, MbusTsLog

T = TypeVar('T')


class Scada:
    def __init__(self, engine: Engine, process: str):
        self.engine = engine
        self.process = process[:6]

    def get_ts(self, tag: str, default: T = None) -> T:
        with Session(self.engine) as session:
            mbus_ts = session.query(MbusTs).filter(MbusTs.tag == tag).first()
            if mbus_ts:
                return bool(mbus_ts.ts)
            else:
                return default

    def get_tm(self, tag: str, default: T = None) -> T:
        with Session(self.engine) as session:
            if cursor.execute('SELECT `tm` FROM `mbus_tm` WHERE `tag` = %s', tag):
                return cursor.fetchone()['tm']
            else:
                return default

    def set_ts(self, tag: str, ts: bool, id_host: Optional[int] = None):
        with Session(self.engine) as session:
            # ts exist ?
            mbus_ts = session.query(MbusTs).filter_by(tag=tag).first()
            if mbus_ts:
                try:
                    if mbus_ts.use:
                        # ts must be a boolean
                        ts = bool(ts)
                        # "not" option
                        if mbus_ts._not:
                            ts = not ts
                        # on state change
                        if ts != mbus_ts.ts:
                            # add to log
                            session.add(MbusTsLog(id_ts=mbus_ts.id, ts=ts))
                            # edit alarm message ?
                            if mbus_ts.al:
                                # format message
                                if ts:
                                    msg = f'"{mbus_ts.label}" ({mbus_ts.label_0}) -> ({mbus_ts.label_1})'
                                else:
                                    msg = f'"{mbus_ts.label}" ({mbus_ts.label_1}) -> ({mbus_ts.label_0})'
                                # send it
                                self.add_alarm(msg=msg, id_host=id_host if id_host else mbus_ts.table.id_host)
                        # update ts record
                        cursor.execute('UPDATE `mbus_ts` SET `ts`=%s, `error`=\'0\' WHERE `id`=%s', (ts, mbus_ts['id']))
                except TypeError:
                    mbus_ts.error = 1
                    session.add(mbus_ts)
                    session.commit()

    def set_tm(self, tag: str, tm, id_host: int = 0):
        with self.db.cursor() as cursor:
            # tm exist ?
            if cursor.execute('SELECT * FROM `mbus_tm` WHERE `tag` = %s', tag):
                db_tm = cursor.fetchone()
                try:
                    # tm in use ?
                    if db_tm['use']:
                        # type error: None or float specials nan, -inf, +inf
                        if tm is None or not (float('-inf') < float(tm) < float('inf')):
                            raise TypeError
                        # search id_host if not define as param
                        if not id_host and db_tm['id_table']:
                            if cursor.execute('SELECT `id_host` FROM `mbus_tables` '
                                              'WHERE `id` = %s', db_tm['id_table']):
                                id_host = cursor.fetchone()['id_host']
                        # "signed" option (complement for 16 bits word)
                        if db_tm['signed'] and type(tm) is int:
                            # test MSB
                            if tm & (1 << (16 - 1)):
                                tm -= 1 << 16
                        # scale value
                        ratio = (db_tm['gaz_max'] - db_tm['gaz_min']) / (db_tm['can_max'] - db_tm['can_min'])
                        tm = (tm - db_tm['can_min']) * ratio + db_tm['gaz_min']
                        # TODO remove this after float web test
                        # force int
                        tm = int(round(tm))
                        # update tm record
                        cursor.execute('UPDATE `mbus_tm` SET `tm`=%s, `error`=\'0\' '
                                       'WHERE `id`=%s', (tm, db_tm['id']))
                        # add to log
                        if db_tm['log']:
                            cursor.execute('INSERT INTO `mbus_tm_log` (`id_tm`,`tm`,`update`) '
                                           'VALUES (%s, %s, NOW())', (db_tm['id'], tm))
                        # check alarm level
                        low_lvl = tm < db_tm['tm_min']
                        end_low_lvl = tm > (db_tm['tm_min'] + db_tm['tm_hist'])
                        high_lvl = tm > db_tm['tm_max']
                        end_high_lvl = tm < (db_tm['tm_max'] - db_tm['tm_hist'])
                        msg = ''
                        # start of low level
                        if low_lvl and not db_tm['al_min']:
                            cursor.execute('UPDATE `mbus_tm` SET `al_min`=\'1\' '
                                           'WHERE `id`=%s', db_tm['id'])
                            msg = '"%s" alarm () -> (LOW) %s %s' % (db_tm['label'], tm, db_tm['unit'])
                        # end of low level
                        if end_low_lvl and db_tm['al_min']:
                            cursor.execute('UPDATE `mbus_tm` SET `al_min`=\'0\' '
                                           'WHERE `id`=%s', db_tm['id'])
                            msg = '"%s" alarm (LOW) -> () %s %s' % (db_tm['label'], tm, db_tm['unit'])
                        # start of high level
                        if high_lvl and not db_tm['al_max']:
                            cursor.execute('UPDATE `mbus_tm` SET `al_max`=\'1\' '
                                           'WHERE `id`=%s', db_tm['id'])
                            msg = '"%s" alarm () -> (HIGH) %s %s' % (db_tm['label'], tm, db_tm['unit'])
                        # end of high level
                        if end_high_lvl and db_tm['al_max']:
                            cursor.execute('UPDATE `mbus_tm` SET `al_max`=\'0\' '
                                           'WHERE `id`=%s', db_tm['id'])
                            msg = '"%s" alarm (HIGH) -> () %s %s' % (db_tm['label'], tm, db_tm['unit'])
                        # add alarm message
                        if db_tm['al'] and msg:
                            self.add_alarm(msg, id_host=id_host)
                except TypeError:
                    # update tm record
                    cursor.execute('UPDATE `mbus_tm` SET `error`=\'1\' WHERE `id`=%s', db_tm['id'])

    def set_tg(self, tag: str, index: int):
        with self.db.cursor() as cursor:
            # ts exist ?
            if cursor.execute('SELECT * FROM `mbus_tg` WHERE `tag` = %s', tag):
                db_tg = cursor.fetchone()
                try:
                    # tg in use ?
                    if db_tg['use']:
                        # tg error ?
                        if index is None:
                            raise TypeError
                        # tg increment
                        diff = index - db_tg['last_tg']
                        # rollover ?
                        if diff < 0:
                            tg_inc = 65536 - db_tg['last_tg'] + index
                        else:
                            tg_inc = diff
                        # weight apply
                        tg_inc *= db_tg['weight']
                        # update tg record
                        cursor.execute('UPDATE `mbus_tg` SET `tg`=`tg`+%s, `last_tg`=%s, `error`=\'0\' '
                                       'WHERE `id`=%s', (tg_inc, index, db_tg['id']))
                except TypeError:
                    cursor.execute('UPDATE `mbus_tg` SET `error`=\'1\' WHERE `id`=%s', db_tg['id'])

    def add_alarm(self, msg: str, id_host: Optional[int] = None):
        with Session(self.engine) as session:
            session.add(Alarm(id_host=id_host, daemon=self.process, message=msg))
            session.commit()

    def strip_tags(self, tags_str: str) -> str:
        # "<TM@Q_GRO>" -> "956.0"
        token_d = dict()
        for (token, token_type, tag) in re.findall(r'(<([A-Z]+?)@([a-zA-Z0-9_]+?)>)', tags_str):
            if token_type == 'TS':
                token_d[token] = self.get_ts(tag, default=0)
            elif token_type == 'TM':
                token_d[token] = self.get_tm(tag, default=0)
        for token in token_d:
            tags_str = re.sub(token, str(token_d[token]), tags_str)
        return tags_str
