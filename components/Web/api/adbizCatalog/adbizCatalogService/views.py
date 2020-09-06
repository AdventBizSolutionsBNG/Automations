from django.shortcuts import render
import json
from .models import *
from django.http import HttpResponse, JsonResponse
import logging


# Create your views here.

log = logging.getLogger("main")

# Gets all dashboards and its respective components
def get_all_dashboards(request):
    try:
        errmsg = {}
        errmsg["message"] = "Error validating the request"
        log.info("Request received for dashboards metadata...")
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

                            token = ""
                            datamodel_details = {}
                            catalog_details = {}
                            for k, v in data.items():

                                if k == "token":
                                    token = v       # need to validate the token
                                if k == "catalog_details":
                                    catalog_details = v
                                if k == "datamodel_details":
                                    datamodel_details = v

                            if validate_token(token):
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
                                                        dashboard_code = k.dashboard_code
                                                        dashboard_reference_class = k.dashboard_reference_class
                                                        dashboard_details = { "dashboard_id": dashboard_id, "dashboard_type": k.dashboard_type , "dashboard_code": k.dashboard_code,  "dashboard_name": k.dashboard_name , "dashboard_description": k.dashboard_description , "sequence": k.sequence , "dashboard_reference_class": k.dashboard_reference_class , "is_system_defined": k.is_system_defined, "is_incremental": k.is_incremental ,"dashboard_title":k.dashboard_title, "dashboard_sub_title":k.dashboard_sub_title}

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

                                                                if k1.component_query:
                                                                    kq =  k1.component_query
                                                                else:
                                                                    kq = "None"

                                                                component_details = {"component_code": k1.component_code, "component_title":k1.component_title, "component_id": k1.id, "component_category": k1.component_category, "component_type": k1.component_type, "component_sub_type": k1.component_sub_type, "component_name": k1.component_name, "component_reference_class": k1.component_reference_class, "sequence": k1.sequence, "display_properties":  dp , "data_filters": df, "data_source_methods": sm , "is_system_defined": is_sd, "is_auto_referesh": is_af, "refresh_interval": k1.refresh_interval, "component_query": kq , "component_tooltip":k1.component_tooltip, "aggregate_id": k1.aggregate_id, "container_id": k1.container_id}
                                                                component_list.append(component_details)

                                                        final_details = {"dashboard_id": dashboard_id, "dashboard_code": dashboard_code, "dashboard_reference_class": dashboard_reference_class, "dashboard_details": dashboard_details, "component_details": component_list}
                                                        final_list.append(final_details)
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
            log.info(errmsg, exc_info=True)
            return JsonResponse(errmsg, safe=False)
    except Exception as e:
        errmsg = {"error":"Critical", "error_description": "Catalog Engine: Error in retrieving Dashboard Metadata!!"}
        log.info(errmsg, exc_info=True)
        return JsonResponse(errmsg, safe=False)


def get_org_hierarchy(request):
    try:
        log.info("Request received for Org Hierarchy metadata...")
        errmsg = {}
        errmsg["message"] = "Error validating the request"
        log.info(request.headers)
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

                            token = ""
                            datamodel_details = {}
                            catalog_details = {}

                            for k, v in data.items():
                                if k == "token":
                                    token = v       # need to validate the token
                                if k == "catalog_details":
                                    catalog_details = v
                                if k == "datamodel_details":
                                    datamodel_details = v

                            if validate_token(token):
                                log.info("Reading Hierarchy Types defined")
                                org_hierarchy_type_qs = OrgHierarchyTypes.objects.filter(is_active = True, tenant_code = tenant_code, site_code = site_code, instance_code = instance_code)
                                if len(org_hierarchy_type_qs) > 0:
                                    my_org_entities = {}
                                    org_hierarchy_type_list = []
                                    for hierarchy_type in org_hierarchy_type_qs:
                                        my_org_entities[hierarchy_type.id] = {"id": hierarchy_type.id, "org_hierarchy_type": hierarchy_type.type, "org_hierarchy_description":hierarchy_type.description, "org_hierarchy_class_reference": hierarchy_type.hierarchy_class_reference }
                                        org_hierarchy_type_list.append(hierarchy_type.id)
                                    log.info(my_org_entities)

                                    if org_hierarchy_type_list:
                                        log.info("Reading Org Hierarchies")
                                        org_hierarchy_qs = OrgHierarchy.objects.filter(hierarchy_type__in =  org_hierarchy_type_list, is_active = True, tenant_code = tenant_code, site_code = site_code, instance_code = instance_code).order_by("hierarchy_type_id", "level")
                                        if len(org_hierarchy_qs) > 0:
                                            my_hierarchy_temp = {}

                                            # create a temp dict for mapping parent hierarchy
                                            log.info("Loading Org Hierarchy Types")
                                            for org_hierarchy_temp in org_hierarchy_qs:
                                                my_hierarchy_temp[org_hierarchy_temp.id] = {"parent_hierarchy_id": org_hierarchy_temp.parent_hierarchy_id, "hierarchy_type_id": org_hierarchy_temp.hierarchy_type_id}
                                            log.info(my_hierarchy_temp)

                                            my_org_hierarchy = {}
                                            for ht in org_hierarchy_type_list:
                                                hierarchy_list = []
                                                for h in org_hierarchy_qs:
                                                    if h.hierarchy_type_id == ht:
                                                        hierarchy_type_name = my_org_entities[ht].get("org_hierarchy_type")
                                                        hierarchy = {"hierarchy_id": h.id, "hierarchy_type": hierarchy_type_name, "hierarchy_type_id": ht, "hierarchy_name": h.hierarchy_name, "level": h.level, "parent_hierarchy_id": h.parent_hierarchy_id}
                                                        hierarchy_list.append(hierarchy)

                                                my_org_hierarchy[ht] = hierarchy_list
                                            log.info("Hierarchy generated successfully")
                                            log.info(my_org_hierarchy)
                                            return JsonResponse(my_org_hierarchy, safe=False)
                                        else:
                                            errmsg = {"error":"Critical", "error_description": "Error!! No Hierarchy defined for the Hierarchy type"}
                                            log.info(errmsg)
                                            return JsonResponse(errmsg, safe=False)
                                else:
                                    errmsg = {"error":"Critical", "error_description": "Error!! No Hierarchy Types defined in the system"}
                                    log.info(errmsg)
                                    return JsonResponse(errmsg, safe=False)
                            else:
                                errmsg = {"error":"Critical", "error_description": "Invalid Token!!!"}
                                log.info(errmsg)
                                return JsonResponse(errmsg, safe=False)
                        else:
                            errmsg = {"error":"Critical", "error_description": "No Instance specified in the Request Header!!!"}
                            log.info(errmsg)
                            return JsonResponse(errmsg, safe=False)
                    else:
                        errmsg = {"error":"Critical", "error_description": "No Site specified in the Request Header!!!"}
                        log.info(errmsg)
                        return JsonResponse(errmsg, safe=False)
                else:
                    errmsg = {"error":"Critical", "error_description": "No Tenant specified in the Request Header!!!"}
                    log.info(errmsg)
                    return JsonResponse(errmsg, safe=False)
            else:
                errmsg = {"error":"Critical", "error_description": "No Module specified in the Request Header!!!"}
                log.info(errmsg)
                return JsonResponse(errmsg, safe=False)
        else:
            errmsg = {"error":"Critical", "error_description": "Invalid Request method specified for this API!!!"}
            log.info(errmsg)
            return JsonResponse(errmsg, safe=False)

    except Exception as e:
        errmsg = {"error":"Critical", "error_description": "Catalog Engine: Error in retrieving Org Hierarchies."}
        log.info(errmsg, exc_info=True)
        return JsonResponse(errmsg, safe=False)

def get_org_entities(request):
    try:
        log.info("Request received for retrieving Org Entities...")
        errmsg = {}
        log.info(request.headers)
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

                            token = ""
                            datamodel_details = {}
                            catalog_details = {}

                            for k, v in data.items():
                                if k == "token":
                                    token = v       # need to validate the token
                                if k == "catalog_details":
                                    catalog_details = v
                                if k == "datamodel_details":
                                    datamodel_details = v
                                if k == "org_hierarchy_type_ids":
                                    hierarchy_type_ids = v

                            if validate_token(token):
                                log.info("Reading Org Entities for the Hierarchy Types")
                                org_entities_qs = Entities.objects.filter(hierarchy_type_id__in = hierarchy_type_ids, is_active = True, tenant_code = tenant_code, site_code = site_code, instance_code = instance_code)
                                if len(org_entities_qs) > 0:
                                    my_org_entities = []
                                    my_org_hierarchy = {}
                                    hierarchy_qs = OrgHierarchy.objects.filter(is_active=True, tenant_code=tenant_code, site_code=site_code, instance_code=instance_code)
                                    if len(hierarchy_qs) >0:
                                        for hierarchy in hierarchy_qs:
                                            my_org_hierarchy[hierarchy.id] = hierarchy.hierarchy_name

                                    for org_entity in org_entities_qs:
                                        h = org_entity.hierarchy_id
                                        hierarchy_name = my_org_hierarchy.get(h)
                                        entity = {"id": org_entity.id, "hierarchy": hierarchy_name, "entity_name": org_entity.entity_name, "entity_code":org_entity.entity_code, "entity_display_code": org_entity.entity_display_code}
                                        my_org_entities.append(entity)

                                    log.info(my_org_entities)
                                    return JsonResponse(my_org_entities, safe=False)

                                else:
                                    errmsg = {"error":"Critical", "error_description": "Error!! No Hierarchy Types defined in the system"}
                                    log.info(errmsg)
                                    return JsonResponse(errmsg, safe=False)
                            else:
                                errmsg = {"error":"Critical", "error_description": "Invalid Token!!!"}
                                log.info(errmsg)
                                return JsonResponse(errmsg, safe=False)
                        else:
                            errmsg = {"error":"Critical", "error_description": "No Instance specified in the Request Header!!!"}
                            log.info(errmsg)
                            return JsonResponse(errmsg, safe=False)
                    else:
                        errmsg = {"error":"Critical", "error_description": "No Site specified in the Request Header!!!"}
                        log.info(errmsg)
                        return JsonResponse(errmsg, safe=False)
                else:
                    errmsg = {"error":"Critical", "error_description": "No Tenant specified in the Request Header!!!"}
                    log.info(errmsg)
                    return JsonResponse(errmsg, safe=False)
            else:
                errmsg = {"error":"Critical", "error_description": "No Module specified in the Request Header!!!"}
                log.info(errmsg)
                return JsonResponse(errmsg, safe=False)
        else:
            errmsg = {"error":"Critical", "error_description": "Invalid Request method specified for this API!!!"}
            log.info(errmsg)
            return JsonResponse(errmsg, safe=False)

    except Exception as e:
        errmsg = {"error":"Critical", "error_description": "Catalog Engine: Error in retrieving Org Entities."}
        log.info(errmsg, exc_info=True)
        return JsonResponse(errmsg, safe=False)

def validate_token(token):
    try:
        return True
    except Exception as e:
        return False



