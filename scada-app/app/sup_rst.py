import re
import pymysql.cursors

# some consts
# DB
DB_HOST = 'localhost'
DB_NAME = 'sup_rst'
DB_USER = 'sup_rst'
DB_PWD = 'sup_rst'


class SupRstDB:
    def __init__(self, db_user: str = DB_USER, db_pwd: str = DB_PWD, process: str = ''):
        # init connection to database
        self.db = pymysql.connect(host=DB_HOST, user=db_user, password=db_pwd, db=DB_NAME,
                                  charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, autocommit=True)
        # process name (max 6 chars)
        self.process = process[:6]

    def __del__(self):
        self.close()

    def close(self):
        try:
            self.db.close()
        except pymysql.err.Error:
            pass

    def alarm(self, msg: str, id_host: int = 0):
        with self.db.cursor() as cursor:
            cursor.execute('INSERT INTO `alarms` (`date_time`, `id_host`, `daemon`, `message`) '
                           'VALUES (NOW(), %s, %s, %s)', (id_host, self.process, msg))

    def set_ts(self, tag_name: str, ts: bool, id_host: int = 0):
        with self.db.cursor() as cursor:
            # ts exist ?
            cursor.execute('SELECT * FROM `mbus_ts` WHERE `tag` = %s', tag_name)
            mbus_ts = cursor.fetchone()
            if mbus_ts:
                try:
                    # ts in use ?
                    if mbus_ts['use']:
                        # ts error ?
                        if ts is None:
                            raise TypeError
                        # ts must be a boolean
                        ts = bool(ts)
                        # search id_host if not define as param
                        if not id_host and mbus_ts['id_table']:
                            cursor.execute('SELECT `id_host` FROM `mbus_tables` WHERE `id` = %s', mbus_ts['id_table'])
                            mbus_tables = cursor.fetchone()
                            if mbus_tables:
                                id_host = mbus_tables['id_host']
                        # "not" option
                        if mbus_ts['not']:
                            ts = not ts
                        # on state change
                        if ts != mbus_ts['ts']:
                            # add to log
                            cursor.execute('INSERT INTO `mbus_ts_log` (`id_ts`,`ts`,`update`) '
                                           'VALUES (%s, %s, NOW())', (mbus_ts['id'], ts))
                            # edit alarm message ?
                            if mbus_ts['al']:
                                # format message
                                msg = '"%s" ' % mbus_ts['label']
                                if ts:
                                    msg += '(%s) -> (%s)' % (mbus_ts['label_0'], mbus_ts['label_1'])
                                else:
                                    msg += '(%s) -> (%s)' % (mbus_ts['label_1'], mbus_ts['label_0'])
                                # send it
                                self.alarm(msg, id_host=id_host)
                        # update ts record
                        cursor.execute('UPDATE `mbus_ts` SET `ts`=%s, `error`=\'0\' '
                                       'WHERE `id`=%s', (ts, mbus_ts['id']))
                except TypeError:
                    cursor.execute('UPDATE `mbus_ts` SET `error`=\'1\' WHERE `id`=%s', mbus_ts['id'])

    def set_tm(self, tag_name: str, tm, id_host: int = 0):
        with self.db.cursor() as cursor:
            # tm exist ?
            if cursor.execute('SELECT * FROM `mbus_tm` WHERE `tag` = %s', tag_name):
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
                            self.alarm(msg, id_host=id_host)
                except TypeError:
                    # update tm record
                    cursor.execute('UPDATE `mbus_tm` SET `error`=\'1\' WHERE `id`=%s', db_tm['id'])

    def set_tg(self, tag_name: str, index: int):
        with self.db.cursor() as cursor:
            # ts exist ?
            if cursor.execute('SELECT * FROM `mbus_tg` WHERE `tag` = %s', tag_name):
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

    def ts(self, tag_name: str, default=None):
        with self.db.cursor() as cursor:
            if cursor.execute('SELECT `ts` FROM `mbus_ts` WHERE `tag` = %s', tag_name):
                return cursor.fetchone()['ts']
            else:
                return default

    def tm(self, tag_name: str, default=None):
        with self.db.cursor() as cursor:
            if cursor.execute('SELECT `tm` FROM `mbus_tm` WHERE `tag` = %s', tag_name):
                return cursor.fetchone()['tm']
            else:
                return default

    def strip_tags(self, tags_str: str) -> str:
        # "<TM@Q_GRO>" -> "956.0"
        t = dict()
        for (token, token_type, tag) in re.findall(r'(<([A-Z]+?)@([a-zA-Z0-9_]+?)>)', tags_str):
            if token_type == 'TS':
                t[token] = self.ts(tag, 0)
            elif token_type == 'TM':
                t[token] = self.tm(tag, 0)
        for token in t:
            tags_str = re.sub(token, str(t[token]), tags_str)
        return tags_str
