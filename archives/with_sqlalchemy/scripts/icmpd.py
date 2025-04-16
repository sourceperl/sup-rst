#!/usr/bin/env python
# ping a list of host with threads for increase speed
# design to use data from/to SQL database
# use standard linux /bin/ping utility

#FIX avoid except in thread : can cause infinite wait ?

from pySupRST.main import sup_rst
from pySupRST.db_class import *
from threading import Thread, current_thread
import subprocess
import datetime
from pprint import pprint
# Queue rename in Python3
try:
    import queue
except ImportError:
    import Queue as queue
import time
import re

## some consts
# polling delay in second
ICMP_REFRESH = 10

## some global vars
num_threads = 40
# thread in/out queue
th_in_q = queue.Queue()
th_out_q = queue.Queue()

# thread code : wraps system ping command
def thread_pinger(i, q):
    """Pings hosts in queue"""
    while True:
        # get thread in from in queue
        th_in  = q.get()
        # init thread out dict for out queue
        th_out = {}
        th_out['th_name'] = current_thread().name
        th_out['id']      = th_in['id']
        try:
            # fix timeout max
            timeout = int(th_in['timeout'])
            timeout = timeout if (timeout <= 4) else 4
            # ping it
            args=['/bin/ping', '-c', '1', '-W', str(timeout), str(th_in['ip'])]
            p_ping = subprocess.Popen(args,
                                      shell=False,
                                      stdout=subprocess.PIPE)
            # save ping stdout
            p_ping_out = p_ping.communicate()[0]
            # ping return 0 if up
            th_out['update'] = datetime.datetime.utcnow()
            # ping command return code
            ping_rcode = p_ping.wait()
            # ping command return 0: ping is ok
            if (ping_rcode == 0):
                # rtt min/avg/max/mdev = 22.293/22.293/22.293/0.000 ms
                regex = 'rtt min/avg/max/mdev = (.*)/(.*)/(.*)/(.*) ms'
                search = re.search(regex,
                                   p_ping_out, re.M|re.I)
                th_out['state']  = u'U'
                try:
                    th_out['rtt'] = int(round(float(search.group(2))))
                except:
                    th_out['rtt'] = 0
            # ping command return 1: ping timeout
            elif (ping_rcode == 1):
                th_out['state']  = u'D'
            # ping command error for all other values
            else:
                th_out['state']  = u'E'
            # update output queue
            th_out_q.put(th_out)
        finally:
            # update queue : this ip is processed 
            q.task_done()

# init and start the thread pool
for i in range(num_threads):
    worker = Thread(target=thread_pinger, args=(i, th_in_q))
    worker.setDaemon(True)
    worker.start()

# build DB object
c = sup_rst()

# main loop
while True:
    # begin a new DB session
    session = c.Session()
    # read nodes list
    nodes = session.query(Icmp).join(Host).\
               filter(Host.host_activity == 'Y',
                      Icmp.icmp_inhibition == 'N').\
               limit(500).all()
    # loop start time
    start = time.time()
    # fill queue
    for node in nodes:
        th_in_q.put({'id':      node.id_host,
                     'ip':      node.host.hostname,
                     'timeout': node.icmp_timeout})
    # wait until worker threads are done to exit
    th_in_q.join()
    # loop end time
    end = time.time()
    loop_time = round(end - start, 2)
    # display result
    th_outs = []
    while True:
        try:
            _th_out = th_out_q.get_nowait()
        except queue.Empty:
            break
        th_outs.append(_th_out)

    # display loop time
    print("################################")
    print("new loop (time: %s)" % (loop_time))
    print("################################")

    # update DB
    for th_out in th_outs:
        # DEBUG
        pprint(th_out)
        # init current node object
        c_node = session.query(Icmp). \
                 filter_by(id_host = th_out['id']).first()
        # copy last node state
        last_state = c_node.icmp_state

        # if current node is "up"
        if th_out['state'] == u'U':
            # process RTT log
            if c_node.icmp_log_rtt == u'Y':
                icmp_log_new = IcmpRttLog(id_host = th_out['id'],
                                          rtt     = th_out['rtt'],
                                          rtt_datetime = th_out['update'])
                session._add(icmp_log_new)
            # update icmp
            c_node.icmp_fail_count = 0
            c_node.icmp_up_index  += 1
            c_node.icmp_rtt        = th_out['rtt']
            # if node is not already "up"
            if c_node.icmp_state != u'U':
                # up count++
                c_node.icmp_good_count += 1
                # up counter > threshold -> host is set "up"
                if c_node.icmp_good_count >= c_node.icmp_good_threshold:
                    c_node.icmp_state = u'U'
        # if current host is "down"
        elif th_out['state'] == u'D':
            c_node.icmp_down_index += 1
            c_node.icmp_good_count  = 0
            # if node is not already "down"
            if c_node.icmp_state != u'D':
                # down count++
                c_node.icmp_fail_count += 1
                # down counter > threshold -> host is set "down"
                if c_node.icmp_fail_count >= c_node.icmp_fail_threshold:
                    c_node.icmp_state = u'D'
        # if current host is in "error"
        else:
            c_node.icmp_state = u'E'

        # on status change
        if c_node.icmp_state != last_state:
            event_new = IcmpHistory(host_id    = th_out['id'],
                                    event_type = c_node.icmp_state,
                                    event_date = th_out['update'])
            session._add(event_new)
            # alarm message edit
            state_word = "error"
            if c_node.icmp_state == u'U':
                state_word = "up"
            elif c_node.icmp_state == u'D':
                state_word = "down"
            al_msg = "host '%s' state: %s" \
                   % (c_node.host.name, state_word)
            c.set_alarm(al_msg,
                        daemon = "icmpd",
                        date_time=th_out['update'],
                        id_host=c_node.id_host)
    #update stats
    c.set_env_tag("ICMP_LOOP_TIME", loop_time)
    # commit all changes
    session.commit()
    session.close()
    # wait before next cycle
    time.sleep(ICMP_REFRESH - loop_time)
