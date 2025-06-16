#!/usr/bin/env python3

"""Ping a list of host (multi-threads for increase speed).
Design to use data from/to SQL database.
Use standard linux /bin/ping utility.
"""

# TODO FIX avoid except in thread : can cause infinite wait ?

import logging
import os
import re
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime
from queue import Empty, Queue
from threading import Thread
from typing import List, Optional, Tuple

from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from ..db.models import Host, Icmp, Variable

logger = logging.getLogger(__name__)


# some consts
PROCESS_NAME = 'icmp'


@dataclass
class HostStatus:
    id: int
    hostname: str
    timeout: int
    state: Optional[str] = None
    rtt: Optional[int] = None
    update: Optional[datetime] = None


class JobICMP:
    def __init__(self, engine: Engine, icmp_refresh: float = 30.0, n_threads: int = 40) -> None:
        # public
        self.engine = engine
        self.icmp_refresh = icmp_refresh
        # private
        self._queue_in: Queue[HostStatus] = Queue()
        self._queue_out: Queue[HostStatus] = Queue()
        # init and start the thread pool
        for _ in range(n_threads):
            Thread(target=self._worker_code, args=(), daemon=True).start()

    def run(self):
        # init a session
        session = sessionmaker(self.engine)()

        # insert data for test purpose
        if not session.query(Host).filter_by(name='localhost').first():
            session.add(Icmp(host=Host(id_subnet=0, name='localhost', hostname='127.0.0.1')))
        if not session.query(Host).filter_by(name='free').first():
            session.add(Icmp(host=Host(id_subnet=0, name='free', hostname='www.free.fr')))
        session.commit()

        # cycle loop
        while True:
            # save cycle start time
            cycle_start = time.monotonic()
            # populate input queue for workers
            for icmp in session.query(Icmp).filter(Icmp.icmp_inhibition == '0').all():
                # populate in queue
                host_status = HostStatus(id=icmp.id_host, hostname=icmp.host.hostname,
                                         timeout=icmp.icmp_timeout)
                self._queue_in.put(host_status)
                logger.warning(host_status)
            # wait until in queue empty (current cycle ending)
            self._queue_in.join()

            cycle_time = time.monotonic() - cycle_start

            # process results
            while True:
                try:
                    host_status = self._queue_out.get_nowait()
                    icmp = session.query(Icmp).filter_by(id_host=host_status.id).first()
                    if icmp and host_status.state:
                        # current state
                        icmp.icmp_state = host_status.state
                        # host is up
                        if icmp.icmp_state == 'U':
                            icmp.icmp_fail_count = 0
                            icmp.icmp_up_index += 1
                            icmp.icmp_rtt = host_status.rtt or 0
                        session.merge(icmp)
                        logger.warning(f'merge {icmp}')
                    session.commit()
                except Empty:
                    break

            # update variables at end of cycle
            session.merge(Variable(name='icmp_delay', value=0))
            session.merge(Variable(name='icmp_update', value=datetime.now()))
            session.commit()

            # wait before next cycle
            time.sleep(max(self.icmp_refresh - cycle_time, 0))

        return
        # main loop
        while True:
            # init connection to database
            try:
                with sup.db.cursor() as cursor:
                    # read nodes list on DB
                    sql = """\
                    SELECT
                        hosts.id AS host_id,
                        hosts.hostname AS host_hostname,
                        hosts.name AS host_name,
                        icmp.icmp_log_rtt AS icmp_log_rtt,
                        icmp.icmp_state AS icmp_state,
                        icmp.icmp_good_threshold AS icmp_good_threshold,
                        icmp.icmp_good_count AS icmp_good_count,
                        icmp.icmp_fail_threshold AS icmp_fail_threshold,
                        icmp.icmp_fail_count AS icmp_fail_count,
                        icmp.icmp_timeout AS icmp_timeout,
                        icmp.icmp_up_index AS icmp_up_index,
                        icmp.icmp_down_index AS icmp_down_index
                    FROM
                        `hosts`,
                        `icmp`
                    WHERE
                        hosts.id = icmp.id_host
                    AND
                        icmp.icmp_inhibition  = \'0\'"""
                    cursor.execute(sql)
                    nodes = cursor.fetchall()
                    # save cycle start time
                    cycle_start = time.time()
                    # fill in queue with nodes params
                    for host_status in nodes:
                        # format db value
                        host_status['icmp_timeout'] = max(host_status['icmp_timeout'], 4)
                        # populate in queue
                        self._queue_in.put(host_status)
                    # wait until in queue empty (current cycle ending)
                    self._queue_in.join()
                    # save cycle end time
                    end = time.time()
                    cycle_time = max(end - cycle_start, 0)
                    # update DB
                    while True:
                        try:
                            d_node_out = self._queue_out.get_nowait()
                            status_change = False
                            # if current node is "up"
                            if d_node_out['thread_state'] == u'U':
                                # process RTT log
                                if d_node_out['icmp_log_rtt'] == u'Y':
                                    # log RTT to DB
                                    sql = 'INSERT INTO `icmp_rtt_log` (`id_host`, `rtt`, `rtt_datetime`) ' \
                                        'VALUES (\'%i\', \'%i\', \'%s\')' \
                                        % (d_node_out['host_id'], d_node_out['thread_rtt'],
                                            d_node_out['thread_update'].strftime('%Y-%m-%d %H:%M:%S'))
                                    cursor.execute(sql)
                                # update icmp
                                d_node_out['icmp_fail_count'] = 0
                                d_node_out['icmp_up_index'] += 1
                                d_node_out['icmp_rtt'] = d_node_out['thread_rtt']
                                # if node is not already "up"
                                if d_node_out['icmp_state'] != u'U':
                                    # up count++
                                    d_node_out['icmp_good_count'] += 1
                                    # up counter > threshold -> host is set "up"
                                    if d_node_out['icmp_good_count'] >= d_node_out['icmp_good_threshold']:
                                        d_node_out['icmp_state'] = u'U'
                                        d_node_out['icmp_chg_state'] = d_node_out['thread_update'].strftime(
                                            '%Y-%m-%d %H:%M:%S')
                                        status_change = True
                            # if current host is "down"
                            elif d_node_out['thread_state'] == u'D':
                                d_node_out['icmp_down_index'] += 1
                                d_node_out['icmp_good_count'] = 0
                                # if node is not already "down"
                                if d_node_out['icmp_state'] != u'D':
                                    # down count++
                                    d_node_out['icmp_fail_count'] += 1
                                    # down counter > threshold -> host is set "down"
                                    if d_node_out['icmp_fail_count'] >= d_node_out['icmp_fail_threshold']:
                                        d_node_out['icmp_state'] = 'D'
                                        d_node_out['icmp_chg_state'] = d_node_out['thread_update'].strftime(
                                            '%Y-%m-%d %H:%M:%S')
                                        status_change = True
                            # if current host is in "error"
                            elif d_node_out['thread_state'] == 'E':
                                if d_node_out['icmp_state'] != 'E':
                                    d_node_out['icmp_state'] = 'E'
                                    d_node_out['icmp_chg_state'] = d_node_out['thread_update'].strftime(
                                        '%Y-%m-%d %H:%M:%S')
                                    status_change = True
                            # update icmp record
                            update_str = ''
                            for key_name in d_node_out:
                                if key_name.startswith(u'icmp_'):
                                    if update_str:
                                        update_str += u', '
                                    update_str += '`%s` = \'%s\'' % (key_name, d_node_out[key_name])
                            sql = 'UPDATE `icmp` SET %s WHERE `icmp`.`id_host` = %s' % (
                                update_str, d_node_out['host_id'])
                            cursor.execute(sql)
                            # on status change
                            if status_change:
                                # add icmp history
                                sql = 'INSERT INTO `icmp_history` (`id_host`, `event_type`, `event_date`) ' \
                                    'VALUES (\'%i\', \'%s\', \'%s\');' \
                                    % (d_node_out['host_id'], d_node_out['icmp_state'],
                                        d_node_out['thread_update'].strftime('%Y-%m-%d %H:%M:%S'))
                                cursor.execute(sql)
                                # add alarm message
                                state_word = "error"
                                if d_node_out['icmp_state'] == 'U':
                                    state_word = "up"
                                elif d_node_out['icmp_state'] == 'D':
                                    state_word = "down"
                                al_msg = 'host "%s" state: %s' % (d_node_out['host_name'], state_word)
                                sql = 'INSERT INTO `alarms` (`id_host`, `daemon`, `date_time`, `message`) ' \
                                    'VALUES (\'%i\', \'icmpd\', \'%s\', \'%s\')' \
                                    % (d_node_out['host_id'], d_node_out['thread_update'].strftime('%Y-%m-%d %H:%M:%S'),
                                        al_msg)
                                cursor.execute(sql)
                        except queue.Empty:
                            break
                    # update stats
                    cursor.execute('REPLACE INTO `sup_rst`.`variables` (`variables`.`name` , `variables`.`value` ) '
                                   'VALUES (\'icmp_delay\', \'%i\')' % cycle_time)
                    cursor.execute('REPLACE INTO `sup_rst`.`variables` (`variables`.`name` , `variables`.`value` ) '
                                   'VALUES (\'icmp_update\', NOW())')
            finally:
                sup.close()
            # wait before next cycle
            time.sleep(max(self.icmp_refresh - cycle_time, 0))

    def _worker_code(self):
        """wraps system ping command (use in and out queues to process request)"""
        while True:
            # get node dict from in queue (thread add new key with thread_ prefix to it)
            node = self._queue_in.get()
            try:
                # ping it
                args = f'/bin/ping -c 1 -W {node.timeout} {node.hostname}'.split()
                p_ping = subprocess.Popen(args,
                                          shell=False,
                                          stdout=subprocess.PIPE,
                                          stderr=open(os.devnull, 'w'))
                # save ping stdout
                p_ping_out = p_ping.communicate()[0].decode('utf-8')
                # ping return 0 if up
                node.update = datetime.now()
                # ping command return code
                ret_code = p_ping.wait()
                # ping command return 0: ping is ok
                if ret_code == 0:
                    # rtt min/avg/max/mdev = 22.293/22.293/22.293/0.000 ms
                    regex = 'rtt min/avg/max/mdev = (.*)/(.*)/(.*)/(.*) ms'
                    search = re.search(regex, p_ping_out, re.M | re.I)
                    node.state = 'U'
                    if search:
                        try:
                            node.rtt = int(round(float(search.group(2))))
                        except (AttributeError, ValueError):
                            node.rtt = None
                # ping command return 1: ping timeout
                elif ret_code == 1:
                    node.state = 'D'
                # ping command error for all others values
                else:
                    node.state = 'E'
                # update output queue
                self._queue_out.put(node)
            finally:
                # update queue : this node is processed by current thread
                self._queue_in.task_done()
