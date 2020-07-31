from django.shortcuts import render
from django.http import request, response, JsonResponse, HttpResponse
from .models import DashboardQuery, DataLakes
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from django.db import connection
from decimal import Decimal
import pandas as pd
from itertools import *
# Create your views here.

def execute_sql_query(query, object_type):

    with connection.cursor() as cursor:
        try:
            print(query)
            cursor.execute(query)
            if object_type == "table":
                column_names = [col[0] for col in cursor.description]
                rows = dictfetchall(cursor)
                table_output = {"headers": column_names, "data": rows}
                output = json.dumps(table_output)
                return output
            else:
                rows = cursor.fetchall()
                df = pd.DataFrame(rows)
                return df

        except Exception as e:
            print("Error executing Query!!", e)
            return None


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    column_header = [col[0] for col in cursor.description]
    return [
        dict(zip(column_header, row))
        for row in cursor.fetchall()
    ]

    # data = [str(row) for row in cursor.fetchall()]
    # output = dict(zip(column_header, data))
    # return output

    # while True:
    #     row = cursor.fetchone()
    #     if row is None:
    #         break
    #     row_dict = dict(zip(columns, row))
    #     yield row_dict
    # return

def convert_df(df):
    data_labels = list(df[0])
    data_values = list(df[1])
    data_values_float = []
    for data in data_values:
        data_values_float.append(float(data))

    return data_labels,data_values_float

def validate_request_header(request):
    try:
        return True
    except Exception as e:
        print(e)

def execute_dashboard_query(request):
    try:
        print(request.headers)
        if request.method == "GET":
            if request.headers['module']:
                module = request.headers['module']
                if request.headers['tenant']:
                    tenant_code = request.headers['tenant']
                    if request.headers['site']:
                        site_code = request.headers['site']
                        if request.headers['instance']:
                            instance_code = request.headers['instance']
                            body = request.body.decode('utf-8')
                            data = {}
                            data = json.loads(body)
                            for k, v in data.items():
                                if k == "component_query":
                                    component_query = v
                                if k == "hierarchy":
                                    hierarchy = v

                            # datalake = DataLakes.objects.using('default').filter(is_active = True, tenant_code = tenant_code, site_code = site_code, instance_code = instance_code, module = module)
                            # if len(datalake) > 0:
                            #     for k in datalake:
                            #         data_lake_code = datalake.data_lake_code
                            #         data_lake_type = datalake.data_lake_type
                            #         data_lake_sub_type = datalake.data_lake_sub_type

                            data_lake_code = "9f2e0174d97d405eb83cbb779155ae30"
                            table_code = "9548f7ef20e04a4082fca7b75834b240"
                            start_Date = str(datetime.datetime.now()).split(" ")[0]


                            # Calculationg today() - 30 days
                            end_date = datetime.datetime.today() - datetime.timedelta(days=1000)
                            end_date = end_date.strftime("%Y-%m-%d")


                            final_query = component_query.replace("DB_NAME",data_lake_code).replace("TABLE_NAME", table_code).replace('adbiz.constants.startDate', "'"+start_Date+"'" ).replace('adbiz.constants.endDate', "'"+end_date+"'")
                            print(final_query)
                            data = execute_sql_query(final_query, "dashboard")
                            data_labels, data_values = convert_df(data)
                            context = {
                                "data_labels" : data_labels,
                                "data_values" : data_values
                            }

                            # print(list(data[0]))

                            return JsonResponse (context, safe=False)

    except Exception as e:
        print("Error in executing Query!!", e)
        return JsonResponse({"status": "Error!!"})


def execute_chart_query(request):
    try:
        print("Request received to execute a query for Chart")
        if request.method == "GET":

            if validate_request_header(request):
                body = request.body.decode('utf-8')
                data = {}
                # print(request.headers)
                # print(request.body)
                data = json.loads(body)

                for k, v in data.items():
                    if k == "chart_query":
                        chart_query = v
                    if k == "chart_category":
                        chart_category = v
                    if k == "hierarchy":
                        hierarchy = v

                # datalake = DataLakes.objects.using('default').filter(is_active = True, tenant_code = tenant_code, site_code = site_code, instance_code = instance_code, module = module)
                # if len(datalake) > 0:
                #     for k in datalake:
                #         data_lake_code = datalake.data_lake_code
                #         data_lake_type = datalake.data_lake_type
                #         data_lake_sub_type = datalake.data_lake_sub_type


                start_Date = str(datetime.datetime.now()).split(" ")[0]
                end_date = datetime.datetime.today() - datetime.timedelta(days=1000)
                end_date = end_date.strftime("%Y-%m-%d")

                final_query = chart_query.replace('adbiz.constants.startDate', "'" + start_Date + "'").replace(
                    'adbiz.constants.endDate', "'" + end_date + "'")
                datadf = execute_sql_query(final_query, "chart")

                value = datadf.iloc[0, 0]
                my_labels = datadf[0].to_list()
                my_data = datadf[1].to_list()

                labels = my_labels
                data = my_data
                print(data)
                output = {"labels":labels,"data":data}
                return JsonResponse(output)
    except Exception as e:
        print(e)

def execute_table_query(request):
    try:
        print("Request received to execute a query for Table")
        if request.method == "GET":

            if validate_request_header(request):
                body = request.body.decode('utf-8')
                data = {}
                # print(request.headers)
                # print(request.body)
                data = json.loads(body)

                for k, v in data.items():
                    if k == "table_query":
                        table_query = v
                    if k == "hierarchy":
                        hierarchy = v

                start_Date = str(datetime.datetime.now()).split(" ")[0]
                end_date = datetime.datetime.today() - datetime.timedelta(days=1000)
                end_date = end_date.strftime("%Y-%m-%d")

                final_query = table_query.replace('adbiz.constants.startDate', "'" + start_Date + "'").replace(
                    'adbiz.constants.endDate', "'" + end_date + "'")
                value = execute_sql_query(final_query, "table")
                print(value)
                #value = datadf.to_json()
                return HttpResponse(value)

    except Exception as e:
        print("IO Engine Error!! Error in executing Query!!", e)
        return JsonResponse({"status": "Error!!"})


def execute_value_query(request):
    try:
        print("Request received to execute a query for Widget Values")
        if request.method == "GET":

            if validate_request_header(request):
                body = request.body.decode('utf-8')
                data = {}
                # print(request.headers)
                # print(request.body)
                data = json.loads(body)

                for k, v in data.items():
                    if k == "component_query":
                        component_query = v
                    if k == "hierarchy":
                        hierarchy = v

                start_Date = str(datetime.datetime.now()).split(" ")[0]
                end_date = datetime.datetime.today() - datetime.timedelta(days=1000)
                end_date = end_date.strftime("%Y-%m-%d")

                final_query = component_query.replace('adbiz.constants.startDate', "'"+start_Date+"'" ).replace('adbiz.constants.endDate', "'"+end_date+"'")
                datadf = execute_sql_query(final_query, "value")
                print(datadf)
                value = datadf.iloc[0,0]        # for single value- first row + first column
                return HttpResponse (value)

    except Exception as e:
        print("IO Engine Error!! Error in executing Query!!", e)
        return JsonResponse({"status": "Error!!"})
