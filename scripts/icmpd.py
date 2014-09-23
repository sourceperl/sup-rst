#!/usr/bin/env python
# ping a list of host with threads for increase speed
# design to use data from/to SQL database
# use standard linux /bin/ping utility

#FIX avoid except in thread : can cause infinite wait ?

from pySupRST.main import sup_rst
from pySupRST.db_class import *
from threading import Thread
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

# some global vars
num_threads = 40
ips_q = queue.Queue()
out_q = queue.Queue()

# thread code : wraps system ping command
def thread_pinger(i, q):
    """Pings hosts in queue"""
    while True:
        # get an IP item form queue
        item = q.get()
        try:
            # fix timeout max
            timeout = int(item['timeout'])
            timeout = timeout if (timeout <= 4) else 4
            # ping it
            args=['/bin/ping', '-c', '1', '-W', str(timeout), str(item['ip'])]
            p_ping = subprocess.Popen(args,
                                      shell=False,
                                      stdout=subprocess.PIPE)
            # save ping stdout
            p_ping_out = p_ping.communicate()[0]
            # ping return 0 if up
            item['update'] = datetime.datetime.utcnow()

            if (p_ping.wait() == 0):
                # rtt min/avg/max/mdev = 22.293/22.293/22.293/0.000 ms
                regex = 'rtt min/avg/max/mdev = (.*)/(.*)/(.*)/(.*) ms'
                search = re.search(regex,
                                   p_ping_out, re.M|re.I)
                item['new_state']  = u'U'
                try:
                    item['rtt'] = int(round(float(search.group(2))))
                except:
                    item['rtt'] = 0
            else:
                item['new_state']  = u'D'

            # update output queue
            out_q.put(item)
        finally:
            # update queue : this ip is processed 
            q.task_done()

# start the thread pool
for i in range(num_threads):
    worker = Thread(target=thread_pinger, args=(i, ips_q))
    worker.setDaemon(True)
    worker.start()

c = sup_rst()

# main loop
while True:
    # connect to DB
    session = c.Session()

    nodes = session.query(Icmp).join(Host).\
               filter(Host.host_activity == 'Y',
                      Icmp.icmp_inhibition == 'N').\
               limit(500).all()

    # loop start time
    start = time.time()
    # fill queue
    for node in nodes:
        ips_q.put({'id': node.id_host,
                   'name': node.host.name,
                   'ip': node.host.hostname,
                   'timeout': node.icmp_timeout,
                    'old_state': node.icmp_state,
                   'log_rtt': bool(node.icmp_log_rtt == 'Y')})
    # wait until worker threads are done to exit    
    ips_q.join()
    # loop end time
    end = time.time()
    loop_time = round(end - start, 2)
    # display result
    out_nodes = []
    while True:
        try:
            out_node = out_q.get_nowait()
        except queue.Empty:
            break
        out_nodes.append(out_node)

    # display loop time
    print("loop time: %s" % (loop_time))

    # update DB
    for out_node in out_nodes:
        pprint(out_node)
        # if current node is "up"
        if out_node['new_state'] == 'U':
            session.query(Icmp).\
                filter(Icmp.id_host == out_node['id']).\
                update({'icmp_state': out_node['new_state'],
                        'icmp_rtt':   out_node['rtt']})
            # RTT log facility
            if out_node['log_rtt']:
                print("log RTT")
                icmp_log_new = IcmpRttLog(id_host = out_node['id'],
                                          rtt     = out_node['rtt'],
                                          rtt_datetime = out_node['update'])
                session.add(icmp_log_new)
        # if current host is "down"
        elif out_node['new_state'] == 'D':
            session.query(Icmp).\
                filter(Icmp.id_host == out_node['id']).\
                update({'icmp_state': out_node['new_state']})

        # on status change
        if out_node['new_state'] != out_node['old_state']:
            event_new = IcmpHistory(host_id    = out_node['id'],
                                    event_type = out_node['new_state'],
                                    event_date = out_node['update'])
            session.add(event_new)
            # alarm message edit
            al_msg = "host '%s' state: %s" \
                   % (out_node['name'],
                      "up" if out_node['new_state'] == 'U' else "down")
            c.set_alarm(al_msg,
                        daemon = "icmpd",
                        date_time=out_node['update'],
                        id_host=out_node['id'])

    # commit all changes
    session.commit()
    #TODO update stats
    session.close()
    # wait before next cycle
    time.sleep(ICMP_REFRESH - loop_time)
