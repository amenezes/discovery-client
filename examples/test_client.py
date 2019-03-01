import json
import threading

from discovery.client import Consul

from flask import Flask


app = Flask(__name__)
dc = Consul('discovery', 8500)
dc.register('standard-client', 5000)


@app.route('/manage/health')
def health():
    return json.dumps({'status': 'UP'})


@app.route('/manage/info')
def info():
    return json.dumps({'app': 'standard-client'})


@app.before_first_request
def enable_service_registry():
    def probe_discovery_connection():
        dc.consul_is_healthy()
    thread = threading.Thread(target=probe_discovery_connection)
    thread.start()
