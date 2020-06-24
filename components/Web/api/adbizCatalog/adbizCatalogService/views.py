from django.shortcuts import render
import json
from .models import *
from django.http import HttpResponse, JsonResponse

# Create your views here.

# Gets all dashboards and its respective components
def get_all_dashboards(request):
    try:
        errmsg = {}
        errmsg["message"] = "Error validating the request"
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
                            print(data)
                            token = ""
                            datamodel_details = {}
                            catalog_details = {}
                            for k, v in data.items():
                                print(k, "--->",v)
                                if k == "token":
                                    token = v       # need to validate the token
                                if k == "catalog_details":
                                    catalog_details = v
                                if k == "datamodel_details":
                                    datamodel_details = v

                            if validate_token(token):
                                print(datamodel_details)
                                print(catalog_details)
                                catalog_qs = Catalogs.objects.filter(catalog_code = catalog_details["catalog_code"], is_active = True, tenant_code = tenant_code, site_code = site_code, instance_code = instance_code)
                                if len(catalog_qs) > 0:
                                    for k in catalog_qs:
                                        catalog_id= k.id

                                    if catalog_id:
                                        datamodel_qs = DataModels.objects.filter(catalog_id = catalog_id, datamodel_code = datamodel_details["datamodel_code"], is_active = True, tenant_code = tenant_code, site_code = site_code, instance_code = instance_code)
                                        if len(datamodel_qs):
                                            for k in datamodel_qs:
                                                datamodel_id = k.id
                                            if datamodel_id:
                                                dashboard_qs = Dashboards.objects.filter(datamodel_id = datamodel_id, catalog_id = catalog_id, module = module, is_active = True, tenant_code = tenant_code, site_code = site_code, instance_code = instance_code )
                                                if len(dashboard_qs) > 0:
                                                    final_list = []
                                                    for k in dashboard_qs:
                                                        component_list = []
                                                        dashboard_id = k.id
                                                        dashboard_details = { "dashboard_id": dashboard_id, "dashboard_type": k.dashboard_type , "dashboard_code": k.dashboard_code,  "dashboard_name": k.dashboard_name , "dashboard_description": k.dashboard_description , "sequence": k.sequence , "dashboard_reference_class": k.dashboard_reference_class , "is_system_defined": k.is_system_defined, "is_incremental": k.is_incremental }

                                                        component_qs = DashboardComponents.objects.filter(dashboard_id = dashboard_id, is_active = True)
                                                        if len(component_qs) > 0:
                                                            for k1 in component_qs:

                                                                dp = json.loads(k1.display_properties) #.replace('/\r?\n|\r/g', '')
                                                                df = json.loads(k1.data_filters) #.replace('/\r?\n|\r/g', '')
                                                                sm = json.loads(k1.data_source_methods) #.replace('/\r?\n|\r/g', '')
                                                                if k1.is_system_defined:
                                                                    is_sd = "True"
                                                                else:
                                                                    is_sd = "False"

                                                                if k1.is_auto_referesh:
                                                                    is_af = "True"
                                                                else:
                                                                    is_af = "False"


                                                                component_details = {"component_code": k1.component_code, "component_id": k1.id, "component_category": k1.component_category, "component_type": k1.component_type, "component_name": k1.component_name, "component_reference_class": k1.component_reference_class, "sequence": k1.sequence, "display_properties":  dp , "data_filters": df, "data_source_methods": sm , "is_system_defined": is_sd, "is_auto_referesh": is_af, "refresh_interval": k1.refresh_interval }
                                                                component_list.append(component_details)

                                                        final_details = {"dashboard_id": dashboard_id, "dashboard_details": dashboard_details, "component_details": component_list}
                                                        final_list.append(final_details)
                                                    print(final_list)
                                                    return JsonResponse(final_list, safe=False)
                                                else:
                                                    errmsg["description"] = "Dashboards not found!!"
                                                    return JsonResponse(errmsg, safe=False)
                                        else:
                                            errmsg["description"] = "Datamodel not found!!"
                                            return JsonResponse(errmsg, safe=False)
                                else:
                                    errmsg["description"] = "Catalog not found!!"
                                    return JsonResponse(errmsg, safe=False)
                            else:
                                errmsg["description"] = "Invalid Token!!!"
                                return JsonResponse(errmsg, safe=False)
                        else:
                            errmsg["description"] = "No Instance specified in the Request Header!!!"
                            return JsonResponse(errmsg, safe=False)
                    else:
                        errmsg["description"] = "No Site specified in the Request Header!!!"
                        return JsonResponse(errmsg, safe=False)
                else:
                    errmsg["description"] = "No Tenant specified in the Request Header!!!"
                    return JsonResponse(errmsg, safe=False)
            else:
                errmsg["description"] = "No Module specified in the Request Header!!!"
                return JsonResponse(errmsg, safe=False)
        else:
            errmsg["description"] = "Invalid Request method specified for this API!!!"
            print(errmsg)
            return JsonResponse(errmsg, safe=False)
    except Exception as e:
        print("Error!!!!!", e)
        errmsg["description"] = e
        return JsonResponse(errmsg, safe=False)


def validate_token(token):
    try:
        return True
    except Exception as e:
        return False

