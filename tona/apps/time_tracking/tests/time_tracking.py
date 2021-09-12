# -*- coding: utf-8 -*-
# Part of Sentilis. See LICENSE file for full copyright and licensing details.
from datetime import datetime
from fastapi.testclient import TestClient
from tona.server import app
from tona.utils.dt import format_datetime as fdt
from datetime import datetime
import os

client = TestClient(app)

ENDPOINTv1 = "/api/v1/time-tracking"

def xtest_post_entries_start():
    data = {
        "name": "Time Entry Start",
        "start": fdt(datetime.utcnow())
    }
    response = client.post(os.path.join(ENDPOINTv1, "entries/start"), json=data)
    assert response.status_code == 201, response.text

def xtest_get_entries_current():
    response = client.get(os.path.join(ENDPOINTv1, "entries/current"))
    assert response.status_code == 200

def xtest_post_entries_stop():
    data = {
        #"id": 1,
        "stop": fdt(datetime.now())
    }
    response = client.post(os.path.join(ENDPOINTv1, "entries/stop"), json=data)
    assert response.status_code == 202, response.text

def xtest_put_entries():
    data = {
        "id": 1,
        "stop": fdt(datetime.now())
    }
    response = client.put(os.path.join(ENDPOINTv1, f"entries/{data.get('id')}"), json=data)
    assert response.status_code == 202, response.text


def test_get_entries():
    response = client.get(os.path.join(ENDPOINTv1, "entries?sort_by=+created_at"))
    assert response.status_code == 200