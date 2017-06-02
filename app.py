import os

import pymongo
from flask import Flask, request, render_template, url_for, send_from_directory
from pymongo import MongoClient
from bson import json_util as jsonb
import config
import json

from datastore.storefactory import RedisDataStoreFactory

app = Flask(__name__)
data_sotre = RedisDataStoreFactory.get_store()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/api/ip", methods=['get', 'post'])
def ip():
    result = get_ip()
    return result


@app.route('/api/commandcount', methods=['post'])
def command_count():
    ip = request.form['ip']
    start = int(request.form['start'])
    end = int(request.form['end'])
    result = data_sotre.get_command_count(ip=ip, start=start, end=end)
    return result


@app.route('/api/memory', methods=['post'])
def memory_count():
    ip = request.form['ip']
    start = int(request.form['start'])
    end = int(request.form['end'])
    result = data_sotre.get_memory_count(ip=ip, start=start, end=end)
    return result


@app.route('/api/info', methods=['post'])
def info():
    ip = request.form['ip']
    result = data_sotre.get_info(ip=ip)
    return result


def get_ip():
    redis_servers = config.REDIS_SERVERS
    redis_servers = json.loads(redis_servers)
    results = []
    for server in redis_servers:
        results.append(server['host'] + ":" + str(server['port']))
    return json.dumps(results)


if __name__ == '__main__':
    app.run()
