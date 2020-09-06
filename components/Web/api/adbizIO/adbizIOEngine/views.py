from django.shortcuts import render
from django.http import request, response, JsonResponse, HttpResponse
from .models import DashboardQuery, DataLakes
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from django.db import connection
from decimal import Decimal
import pandas as pd
import logging


# Create your views here.
mylog = logging.getLogger("main")

# Executes a SQL Query
def execute_sql_query(query, object_type):
    with connection.cursor() as cursor:
        try:
            mylog.info("Executing SQL Query.. ")
            mylog.info(query)

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
            mylog.info("Error executing Query!!", exc_info=True)
            return None


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    column_header = [col[0] for col in cursor.description]
    return [
        dict(zip(column_header, row))
        for row in cursor.fetchall()
    ]

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
                            # start_Date = str(datetime.datetime.now()).split(" ")[0]


                            # # Calculationg today() - 30 days
                            # end_date = datetime.datetime.today() - datetime.timedelta(days=1000)
                            # end_date = end_date.strftime("%Y-%m-%d")

                            # start_Date = request.session.get("run_time_details")["period_start_date"]
                            # end_Date = request.session.get("run_time_details")["period_end_date"]
                            #
                            # print("------request details-------")
                            # print(request.session.get("run_time_details"))

                            final_query = component_query.replace("DB_NAME",data_lake_code).replace("TABLE_NAME", table_code).replace('adbiz.constants.startDate', "'"+start_Date+"'" ).replace('adbiz.constants.endDate', "'"+end_Date+"'")
                            print(final_query)
                            data = execute_sql_query(final_query, "dashboard")
                            data_labels, data_values = convert_df(data)
                            context = {
                                "data_labels" : data_labels,
                                "data_values" : data_values
                            }

                            return JsonResponse (context, safe=False)

    except Exception as e:
        mylog.error("Error in executing Dashboard/Widget Query!!", exc_info=True)
        return JsonResponse({"status": "Error!!"})


def execute_chart_query(request):
    try:
        mylog.info("-----------------------------------------------------")
        mylog.info("Request received to execute a query for Chart")
        if request.method == "GET":
            if validate_request_header(request):
                body = request.body.decode('utf-8')
                data = {}
                data = json.loads(body)

                for k, v in data.items():
                    if k == "chart_query":
                        chart_query = v
                    if k == "chart_category":
                        chart_category = v
                    if k == "hierarchy":
                        hierarchy = v
                    if k == "period_start_date":
                        period_start_date = v
                    if k == "period_end_date":
                        period_end_date = v

                # datalake = DataLakes.objects.using('default').filter(is_active = True, tenant_code = tenant_code, site_code = site_code, instance_code = instance_code, module = module)
                # if len(datalake) > 0:
                #     for k in datalake:
                #         data_lake_code = datalake.data_lake_code
                #         data_lake_type = datalake.data_lake_type
                #         data_lake_sub_type = datalake.data_lake_sub_type


                # start_Date = str(datetime.datetime.now()).split(" ")[0]
                # end_date = datetime.datetime.today() - datetime.timedelta(days=1000)
                # end_date = end_date.strftime("%Y-%m-%d")
                # start_Date = request.session["period_start_date"]
                # end_Date = request.session["period_end_date"]

                final_query = chart_query.replace('adbiz.constants.startDate', "'" + period_start_date + "'").replace('adbiz.constants.endDate', "'" + period_end_date + "'")

                mylog.info(final_query)
                datadf = execute_sql_query(final_query, "chart")
                my_labels = datadf[0].to_list()
                # if len(datadf.columns) > 2:
                row_list = []
                i = 1
                while i < len(datadf.columns):
                    #row_list.append(datadf[i].to_list())
                    row_list.append(list(datadf[i]))
                    i = i+1
                output = {"labels": my_labels, "data": row_list}
                mylog.info(output)

                # else:
                #     my_data = datadf[1].to_list()
                #     output = {"labels": my_labels,"data": my_data}
                return JsonResponse(output)

    except Exception as e:
        mylog.error("Error occurred in executing Chart Query!!", exc_info=True)
        return JsonResponse({"status": "Error!!"})

def execute_table_query(request):
    try:
        mylog.info("-----------------------------------------------------")
        mylog.info("Request received to execute a query for Table")

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
                    if k == "period_start_date":
                        period_start_date = v
                    if k == "period_end_date":
                        period_end_date = v

                # start_Date = request.session["period_start_date"]
                # end_Date = request.session["period_end_date"]

                # start_Date = str(datetime.datetime.now()).split(" ")[0]
                # end_date = datetime.datetime.today() - datetime.timedelta(days=1000)
                # end_date = end_date.strftime("%Y-%m-%d")

                final_query = table_query.replace('adbiz.constants.startDate', "'" + period_start_date + "'").replace(
                    'adbiz.constants.endDate', "'" + period_end_date + "'")

                mylog.info(final_query)
                value = execute_sql_query(final_query, "table")
                #print(value)
                #value = datadf.to_json()
                return HttpResponse(value)

    except Exception as e:
        mylog.error("Error occurred in executing Table Query!!", exc_info=True)
        return JsonResponse({"status": "Error!!"})


def execute_value_query(request):
    try:
        mylog.info("-----------------------------------------------------")
        mylog.info("Request received to execute a query for Value/Indicator")
        if request.method == "GET":
            if validate_request_header(request):
                body = request.body.decode('utf-8')
                data = {}
                # print(request.headers)
                # print(request.body)
                data = json.loads(body)

                mylog.info(data)

                for k, v in data.items():
                    if k == "component_query":
                        component_query = v
                    if k == "hierarchy":
                        hierarchy = v
                    if k == "period_start_date":
                        period_start_date = v
                    if k == "period_end_date":
                        period_end_date = v


                # start_Date = request.session.get("run_time_details")["period_start_date"]
                # end_Date = request.session.get("run_time_details")["period_end_date"]

                # start_Date = str(datetime.datetime.now()).split(" ")[0]
                # end_date = datetime.datetime.today() - datetime.timedelta(days=1000)
                # end_date = end_date.strftime("%Y-%m-%d")

                final_query = component_query.replace('adbiz.constants.startDate', "'"+period_start_date+"'" ).replace('adbiz.constants.endDate', "'"+period_end_date+"'")
                datadf = execute_sql_query(final_query, "value")
                mylog.info(final_query)
                mylog.info(datadf)
                value = datadf.iloc[0,0]        # for single value- first row + first column
                return HttpResponse (value)

    except Exception as e:
        mylog.error("Error occurred in executing Value/Indicator Query!!", exc_info=True)
        return JsonResponse({"status": "Error!!"})
