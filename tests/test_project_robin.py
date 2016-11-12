import json
from flask import url_for
import sys

def test_get_data(client, app):
    resp = client.get(url_for('main.get_pr_data'))
    data = json.loads(resp.data.decode('utf-8'))
    print(sys.path)
    assert type(data['cms']) is list