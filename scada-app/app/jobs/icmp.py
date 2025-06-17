#!/usr/bin/env python3

"""Ping a list of host (multi-threads for increase speed).
Design to use data from/to SQL database.
Use standard linux /bin/ping utility.
"""

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
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from ..db.models import Alarm, Host, Icmp, IcmpHistory, IcmpIndex, IcmpRttLog, Variable

logger = logging.getLogger(__name__)


# some consts
PROCESS_NAME = 'icmp'


@dataclass
class WorkerData:
    id_host: int
    hostname: str
    timeout: int
    state: Optional[str] = None
    rtt: Optional[int] = None
    update: Optional[datetime] = None


class JobICMP:
    def __init__(self, engine: Engine, refresh_s: float = 30.0, n_threads: int = 40) -> None:
        # public
        self.engine = engine
        self.refresh_s = refresh_s
        # private
        self._queue_in: Queue[WorkerData] = Queue()
        self._queue_out: Queue[WorkerData] = Queue()
        # init and start the thread pool
        for _ in range(n_threads):
            Thread(target=self._worker_code, args=(), daemon=True).start()

    def _insert_test_data(self):
        # insert data for test purpose
        with Session(self.engine) as session:
            if not session.query(Host).filter_by(name='localhost').first():
                session.add(Icmp(host=Host(id_subnet=0, name='localhost', hostname='127.0.0.1')))
            if not session.query(Host).filter_by(name='free').first():
                session.add(Icmp(host=Host(id_subnet=0, name='free', hostname='www.free.fr')))
            session.commit()

    def _populate_input_queue(self):
        with Session(self.engine) as session:
            for icmp in session.query(Icmp).filter(Icmp.icmp_inhibition == '0').all():
                # populate in queue
                worker_data = WorkerData(id_host=icmp.id_host, hostname=icmp.host.hostname,
                                         timeout=icmp.icmp_timeout)
                self._queue_in.put(worker_data)
                logger.debug(f'add to input queue: {worker_data}')

    def _process_worker_data(self, worker_data: WorkerData):
        with Session(self.engine) as session:
            icmp = session.query(Icmp).filter_by(id_host=worker_data.id_host).first()
            if icmp and worker_data.state:
                # new_state set on state change
                new_state: Optional[str] = None
                # host is up
                if worker_data.state == 'U':
                    icmp.icmp_up_index += 1
                    icmp.icmp_fail_count = 0
                    # process "Round Trip Time" info
                    if worker_data.rtt is not None:
                        icmp.icmp_rtt = worker_data.rtt
                        # log on need
                        if icmp.icmp_log_rtt == 'Y':
                            session.add(IcmpRttLog(id_host=worker_data.id_host,
                                                   rtt=worker_data.rtt,
                                                   rtt_datetime=worker_data.update or datetime.now()))
                    # if node is not already "up"
                    if icmp.icmp_state != 'U':
                        icmp.icmp_good_count += 1
                        # up counter > threshold -> host is set "up"
                        if icmp.icmp_good_count >= icmp.icmp_good_threshold:
                            new_state = 'U'
                # host is down
                elif worker_data.state == 'D':
                    icmp.icmp_down_index += 1
                    icmp.icmp_good_count = 0
                    # if node is not already "down"
                    if icmp.icmp_state != 'D':
                        # down count++
                        icmp.icmp_fail_count += 1
                        # down counter > threshold -> host is set "down"
                        if icmp.icmp_fail_count >= icmp.icmp_fail_threshold:
                            new_state = 'D'
                # host error
                elif worker_data.state == 'E':
                    if icmp.icmp_state != 'E':
                        new_state = 'E'
                # on status change
                if new_state:
                    # update state
                    icmp.icmp_state = new_state
                    icmp.icmp_chg_state = worker_data.update or datetime.now()
                    # add icmp history
                    session.add(IcmpHistory(id_host=worker_data.id_host, event_type=worker_data.state,
                                            event_date=worker_data.update or datetime.now()))
                    # add alarm message
                    status_str = dict(E='error', U='up', D='down').get(icmp.icmp_state, 'n/a')
                    msg = f'host "{icmp.host.name}" state: {status_str}'
                    session.add(Alarm(id_host=icmp.id_host, daemon=PROCESS_NAME, date_time=datetime.now(), message=msg))
                session.merge(icmp)
                logger.debug(f'session merge {icmp}')
            session.commit()

    def run(self):
        # add test data
        try:
            with Session(self.engine) as session:
                self._insert_test_data()
        except SQLAlchemyError as e:
            logger.error(f'unable to insert test data (DB error: {e})')

        # cycle loop
        while True:
            try:
                # save cycle start time
                cycle_start = time.monotonic()
                # populate input queue for workers
                self._populate_input_queue()
                # wait until in queue empty (current cycle ending)
                self._queue_in.join()
                # cycle start time
                cycle_duration_s = time.monotonic() - cycle_start

                # process results
                while True:
                    try:
                        worker_data = self._queue_out.get_nowait()
                        self._process_worker_data(worker_data)
                    except Empty:
                        break

                # update variables at end of cycle
                with Session(self.engine) as session:
                    session.merge(Variable(name='icmp_delay', value=cycle_duration_s))
                    session.merge(Variable(name='icmp_update', value=datetime.now()))
                    session.commit()

                # wait before next cycle
                time.sleep(max(self.refresh_s - cycle_duration_s, 0))
            except SQLAlchemyError as e:
                logger.error(f'abort cycle (DB error: {e})')
                time.sleep(5.0)

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
