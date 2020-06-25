from django.shortcuts import render
from django.http import request, response, JsonResponse, HttpResponse
from .models import DashboardQuery, DataLakes
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
from django.db import connection
import pandas as pd
# Create your views here.

def execute_sql_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        row = cursor.fetchall()
        df = pd.DataFrame(row)
    return df

def convert_df(df):
    data_labels = list(df[0])
    data_values = list(df[1])

    data_values_float = []

    for data in data_values:
        data_values_float.append(float(data))

    return data_labels,data_values_float


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


                            data = execute_sql_query(final_query)

                            data_labels, data_values = convert_df(data)

                            # print(data)
                            # print()
                            # print(data_lables)
                            # print(data_values)

                            context = {
                                "data_labels" : data_labels,
                                "data_values" : data_values
                            }

                            # print(list(data[0]))

                            return JsonResponse (context, safe=False)

    except Exception as e:
        print("Error in executing Query!!", e)
        return JsonResponse({"status": "Error!!"})