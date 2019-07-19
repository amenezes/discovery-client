import json
import threading

from discovery.client import Consul
from discovery.check import Check, http
from discovery.service import Service

from flask import Flask


app = Flask(__name__)
dc = Consul(
    host='discovery',
    port=8500,
    service=Service(
        'standard-client',
        5000,
        check=Check(
            'standard-client-check',
            http('http://standard-client:5000/manage/health')
        )
    )
)
dc.register()


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
