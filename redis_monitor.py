#!/usr/bin/env python
#-*- coding:utf-8 -*-
import argparse
import json
import threading
import time
import datetime
import traceback
import redis
import config
from threading import Timer
from datastore.storefactory import RedisDataStoreFactory


class Monitor(object):
    def __init__(self, connection_pool):
        self.connection_pool = connection_pool
        self.connection = None

    def __del__(self):
        try:
            self.reset()
        except:
            pass

    def reset(self):
        if self.connection:
            self.connection_pool.release(self.connection)
            self.connection = None

    def monitor(self):
        if self.connection is None:
            self.connection = self.connection_pool.get_connection('monitor', None)
        self.connection.send_command("monitor")
        return self.listen()

    def parse_response(self):
        return self.connection.read_response()

    def listen(self):
        while True:
            yield self.parse_response()


class InfoThread(threading.Thread):
    def __init__(self, host, port, password=None):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.password = password
        self.server = self.host + ":" + str(self.port)
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.is_set()

    def run(self):
        data_store = RedisDataStoreFactory.get_store()
        redis_client = redis.StrictRedis(host=self.host, port=self.port, db=0, password=self.password)
        # process the results from redis
        while not self.stopped():
            try:
                redis_info = redis_client.info()
                optime = int(time.time())
                used_memory = int(redis_info['used_memory'])
                total_commands_processed = int(redis_info['total_commands_processed'])

                # used_memory_peak not available in older versions of redis
                try:
                    peak_memory = int(redis_info['used_memory_peak'])
		    max_memory = str(redis_info['maxmemory_human'])
                except:
                    peak_memory = used_memory
                    max_memory = 'xxx'
                
                data_store.set_command_count(optime=optime,cmdcount=total_commands_processed,ip=self.server)
                data_store.set_memory_count(optime=optime, used_memory=used_memory, peak_memory=peak_memory, ip=self.server)

                info_dict = {'uptime': int(redis_info['uptime_in_seconds']),
                             'max_memory': max_memory,
                             'connnected_clients': str(redis_info['connected_clients']),
                             'used_cpu_sys': str(redis_info['used_cpu_sys']),
                             'used_cpu_user': str(redis_info['used_cpu_user']),
                             'used_memory': str(redis_info['used_memory']),
                             'used_memory_rss': str(redis_info['used_memory_rss']),
                             'used_memory_peak': str(redis_info['used_memory_peak']),
                             'mem_fragmentation_ratio': str(redis_info['mem_fragmentation_ratio']),
                             'total_connection_recevied': str(redis_info['total_connections_received']),
                             'total_commands_processed': str(redis_info['total_commands_processed']),
                             'expired_keys': str(redis_info['expired_keys']), 'ip': self.server}
                data_store.set_info(optime=optime, info_dict=info_dict, ip=self.server)
                #  sleep xs
                print 'Collecting redis data.......'
                time.sleep(args.interval)

            except Exception, e:
                tb = traceback.format_exc()
                print "==============================\n"
                print datetime.datetime.now()
                print tb
                print "==============================\n"


class RedisMonitor(object):
    def __init__(self):
        self.threads = []
        self.active = True

    def run(self):
        redis_servers = config.REDIS_SERVERS
        redis_servers = json.loads(redis_servers)
        for redis_server in redis_servers:
            print redis_server
            password = redis_server.get('password')
            info = InfoThread(redis_server['host'], redis_server['port'], password)
            self.threads.append(info)
            info.setDaemon(True)
            info.start()
        t = Timer(args.duration, self.stop)
        t.start()

        try:
            while self.active:
                pass
        except (KeyboardInterrupt, SystemExit):
            self.stop()
            t.cancel()

    def stop(self):
        """Stops the monitor and all associated threads.
        """
        if not args.quiet:
            print "shutting down..."
        for t in self.threads:
            t.stop()
        self.active = False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Monitor redis.')
    parser.add_argument('--duration',
                        type=int,
                        help="duration to run the info command (in seconds)",
                        required=True)
    parser.add_argument('--interval',
                        type=int,
                        help="interval to run the info command (in seconds)",
                        required=True)
    parser.add_argument('--quiet',
                        help="do  not write anything to standard output",
                        required=False,
                        action='store_true')
    args = parser.parse_args()
    monitor = RedisMonitor()
    monitor.run()
