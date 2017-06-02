import contextlib
import json
import random
import time
import config
import MySQLdb


class MysqlStore(object):
    def __init__(self):
        store_mysql = json.loads(config.STORE_MYSQL)
        self.host = store_mysql['host']
        self.port = store_mysql['port']
        self.user = store_mysql['username']
        self.password = store_mysql['password']
        self.db = store_mysql['database']
        self.conn = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.password, db=self.db)

    def get_ip(self):
        sql = "SELECT DISTINCT ip FROM command_count"
        with contextlib.closing(self.conn.cursor()) as c:
            c.execute(sql)
            results = c.fetchall()
            return json.dumps(results)

    def set_command_count(self, optime, cmdcount, ip):
        sql = 'INSERT INTO command_count(optime, cmdcount, ip) VALUES (%s, %s, %s)'
        values = (optime, cmdcount, ip)
        return self.do_insert(sql, values)

    def set_memory_count(self, optime, used_memory, peak_memory, ip):
        sql = 'INSERT INTO memory_count(optime, used_memory, peak_memory, ip) VALUES (%s, %s, %s, %s)'
        values = (optime, used_memory, peak_memory, ip)
        return self.do_insert(sql, values)

    def set_info(self, optime, info_dict, ip):
        sql = '''INSERT INTO info(optime, info,ip) VALUES(%s,%s,%s)
              '''
        values = (optime, json.dumps(info_dict), ip)
        return self.do_insert(sql, values)

    def get_command_count(self, ip, start, end):
        sql = 'SELECT optime, cmdcount FROM command_count WHERE ip = %s AND optime >= %s AND optime <= %s ORDER BY optime ASC'
        values = (ip, start, end)
        with contextlib.closing(self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)) as c:
            c.execute(sql, values)
            self.conn.commit()
            results = c.fetchall()
            return json.dumps(results)

    def get_memory_count(self, ip, start, end):
        sql = 'SELECT optime, used_memory, peak_memory FROM memory_count WHERE ip = %s AND optime >= %s AND optime <= %s ORDER BY optime ASC'
        values = (ip, start, end)
        with contextlib.closing(self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)) as c:
            c.execute(sql, values)
            self.conn.commit()
            results = c.fetchall()
            return json.dumps(results)

    def get_info(self, ip):
        sql = 'SELECT info FROM info WHERE ip = %s ORDER BY optime DESC LIMIT 0,1;'
        values = (ip,)
        with contextlib.closing(self.conn.cursor()) as c:
            c.execute(sql, values)
            self.conn.commit()
            results = c.fetchone()
            if results:
                return results[0]
            else:
                return ''

    def do_insert(self, sql, values):
        with contextlib.closing(self.conn.cursor()) as c:
            result = c.execute(sql, values)
            self.conn.commit()
            return result

if __name__ == '__main__':
    mysql_store = MysqlStore()
    for i in range(1, 50):
        result = mysql_store.set_command_count(int(time.time())+i, random.randint(10, 100), "127.0.0.1:6379")
        print result
