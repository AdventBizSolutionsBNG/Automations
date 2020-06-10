from django.shortcuts import render
from django.http import request, response
from .models import DashboardQuery
import json
# Create your views here.


def execute_dashboard_query(requests):
    try:
        if requests.method == "GET":
            body = request.body.decode('utf-8')
            data = {}
            dq = DashboardQuery()
            data = json.loads(body)
            for k, v in data.items():
                if k == "io_engine_code":
                    dq.io_engine_code = v
                if k == "api_key":
                    dq.api_key = v
                if k == "token":
                    dq.token = v
                if k == "date_filter":
                    instance = v
                if k == "module":
                    module = v

    except Exception as e:
        print(e)