from django.shortcuts import render
from .models import CoreEngine as CoreMainEngine, Tenants, Sites, Instances, Modules, DataLakes, ModuleActivations,CoreEngineActivations
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from components.core.coreEngine import CoreEngine as CE
import json
from django.views.decorators.csrf import csrf_exempt
import logging

from components.core.modules.storageEngines import DataLakeStorage

# Create your views here.

from components.core.modules.settings import Settings
from components.core.coreEngine import CoreEngine as CoreLib

coreLib=CoreLib()
display_metadata=coreLib.components
log=logging.getLogger("main")

def add_site(requests):
    try:
        pass

    except Exception as e:
        print(e)


def sync_hub(requests, pe):
    try:
        pass

    except Exception as e:
        print(e)


@csrf_exempt
def activate(request, pe):
    try:
        payload=json.loads(request.body)
        if payload != None or payload != "":
            data=coreLib.activate_core_engine(payload)
            if data:
                with transaction.atomic():
                    o=CoreEngine.objects.create(
                        core_engine_code=data["core_engine_code"],
                        customer_id="",  #customer_id,
                        product_engine_code=data["product_engine_code"],
                        root_namespace=pe.get_root_namespace(),
                        registered_to=data["registered_to"],
                        activation_file_location=pe.get_activation_file_location(),
                        activation_key=data["activation_key"],
                        activation_dt=data["activation_dt"],
                        host_name=data["host_name"],
                        host_ip_address=data["host_ip_address"],
                        os_release=data["os_release"],
                        release_info=data["release_info"],
                        last_updated_by="product_admin"
                    )
                    o.save()
                    errmsg = {"error":"Critical", "error_description": "Activated Successfully!!"}

                    qs=CoreEngine.objects.order_by('last_updated_on')[0]

                    return JsonResponse(errmsg, safe=False)
            else:
                errmsg = {"error":"Critical", "error_description": "Error occurred during processing the payload for activation!!"}
                return JsonResponse(errmsg, safe=False)
        else:
            errmsg = {"error":"Critical", "error_description": "Error!! Incorrect Payload"}
            return JsonResponse(errmsg, safe=False)

    except Exception as e:
        errmsg = {"error":"Critical", "error_description": "Error in activating Core Engine using API."}
        log.info(errmsg, exc_info=True)
        return JsonResponse(errmsg, safe=False)


def get_ce_details(request, ce):
    try:
        qs=CoreEngine.objects.filter(core_engine_code=ce, is_active=True)
        if len(qs) >0:
            data={
                "core_engine_code": qs.core_engine_code,
                "product_engine_code": qs.product_engine_code,
                "activation_key": qs.activation_key,
                "activation_dt": qs.activation_dt,
                "host_name": qs.host_name,
                "host_ip_address": qs.host_ip_address,
                "os_release": qs.os_release,
                "release_info": qs.release_info,
                "validity_start_date": qs.validity_start_date,
                "validity_end_date": qs.validity_end_date,
                "is_activated": qs.is_activated
            }
        else:
            errmsg = {"error":"Critical", "error_description": "Error!! Incorrect Core Engine specified:" }
            return JsonResponse(errmsg, safe=False)

    except Exception as e:
        errmsg = {"error":"Critical", "error_description": "Error in fetching details for the Core Engine"}
        return JsonResponse(errmsg, safe=False)


def get_data_lake_storage_details(request):
    try:
        log.info("Request received for Datalake storage details")
        if request.method == "GET":
            body=request.body.decode('utf-8')
            data={}
            data=json.loads(body)
            for k,v in data.items():
                if k == "tenant_code":
                    tenant=v
                if k == "core_engine_code":
                    ce=v
                if k == "site_code":
                    site=v
                if k == "instance_code":
                    instance=v
                if k == "module":
                    module=v

            if tenant is None or tenant == "" or ce is None or ce == "" or site is None or site == "" or instance is None or instance == "":
                errmsg = {"error":"Critical", "error_description":  "Error!! Incorrect request body received!!!"}
                return JsonResponse(errmsg, safe=False)
            else:
                core_qs=CoreEngine.objects.filter(core_engine_code=ce, is_active=True)
                if len(core_qs)>0:
                    for k in core_qs:
                        core_engine_id=k.id
                    log.info("$$$$")
                    tenant_qs=Tenants.objects.filter(tenant_code=tenant, is_active=True)
                    if len(tenant_qs)>0:
                        for k in tenant_qs:
                            tenant_id=k.id
                        log.info("$$$$$")
                        site_qs=Sites.objects.filter(core_engine_id=core_engine_id, tenant=tenant_id, site_code=site, is_active=True)
                        if len(site_qs)>0:
                            for k in site_qs:
                                site_id=k.id
                                
                            instance_qs=Instances.objects.filter(core_engine_id=core_engine_id, tenant=tenant_id, site_id=site_id, is_active=True)
                            if len(instance_qs)>0:
                                for instance in instance_qs:
                                    instance_id=instance.id
                                    
                                modules_qs=Modules.objects.filter(core_engine_id=core_engine_id, tenant=tenant_id, site_id=site_id, module=module, is_active=True)
                                if len(modules_qs)>0:
                                    for module in modules_qs:
                                        module_id=module.id
                                    qs=DataLakes.objects.filter(core_engine_id=core_engine_id,tenant=tenant_id, site_id=site_id, module=module, is_active=True)
                                    if len(qs)>0:
                                        for k in qs:
                                            dl_code=k.data_lake_code
                                            dl_class=k.storage_engine_class
                                            dl_primary=k.is_primary
                                            dl_type=k.data_lake_type
                                            dl_sub_type=k.data_lake_sub_type
                                            return JsonResponse({"data_lake_code":dl_code, "storage_engine_class":dl_class, "data_lake_type": dl_type, "data_lake_sub_type": dl_sub_type})
                                    else:
                                        errmsg = {"error":"Critical", "error_description": "Error!! Data lake Storage doesnt exists in the system for the given parameters!!!"}
                                        log.info(errmsg, exc_info=True)
                                        return JsonResponse(errmsg, safe=False)
                                else:
                                    errmsg = {"error":"Critical", "error_description": "Error!! Specified Module doesnt exists in the system!!!"}
                                    log.info(errmsg, exc_info=True)
                                    return JsonResponse(errmsg, safe=False)
                            else:
                                errmsg = {"error":"Critical", "error_description": "Error!! Specified Instance doesnt exists in the system!!!"}
                                log.info(errmsg, exc_info=True)
                                return JsonResponse(errmsg, safe=False)
                        else:
                            errmsg = {"error":"Critical", "error_description": "Error!! Specified Site doesnt exists in the system!!!"}
                            log.info(errmsg, exc_info=True)
                            return JsonResponse(errmsg, safe=False)
                    else:
                        errmsg = {"error":"Critical", "error_description": "Error!! Specified Client doesnt exists in the system!!!"}
                        log.info(errmsg, exc_info=True)
                        return JsonResponse(errmsg, safe=False)
                else:
                    errmsg = {"error":"Critical", "error_description": "Error!! Specified Core Engine doesnt exists in the system!!!"}
                    log.info(errmsg, exc_info=True)
                    return JsonResponse(errmsg, safe=False)

    except Exception as e:
        errmsg = {"error":"Critical", "error_description": "Error in fetching details for the Data Lake Storage Engine"}
        log.info(errmsg, exc_info=True)
        return JsonResponse(errmsg, safe=False)


def get_display_component_metadata(request):
    try:
        log.info("Request received for Display Component Metadata")
        if request.method == "GET":
            body=request.body.decode('utf-8')
            data={}
            data=request.headers
            for k,v in data.items():
                if k == "Tenant":
                    tenant=v
                if k == "Site":
                    site=v
                if k == "Instance":
                    instance=v
                if k == "Module":
                    module=v

            if tenant is None or tenant == "" or site == "" or instance is None or instance == "":
                errmsg = {"error":"Critical", "error_description":  "Error!! Incorrect request body received!!!"}
                return JsonResponse(errmsg, safe=False)
            else:
                return JsonResponse(display_metadata, safe=False)
    except Exception as e:
        errmsg = {"error":"Critical", "error_description": "Error in fetching details for the Data Lake Storage Engine"}
        log.info(errmsg, exc_info=True)
        return JsonResponse(errmsg, safe=False)

def get_active_modules(request):
    try:
        log.info("Request received for Active modules")
        if request.method == "GET":
            body=request.body.decode('utf-8')
            data={}
            data=request.headers
            tenant=""
            ce=""
            site=""
            instance=""

            log.info(data)
            log.info(body)

            for k,v in data.items():
                if k == "Tenant":
                    tenant=v
                if k == "Core":
                    core_engine_code=v
                if k == "Site":
                    site=v
                if k == "Instance":
                    instance=v

            if tenant is None or tenant == "" or core_engine_code is None or core_engine_code == "" or site is None or site == "" or instance is None or instance == "":
                errmsg = {"error":"Critical", "error_description":  "Error!! Incorrect request body received!!!"}
                log.error(errmsg)
                return JsonResponse(errmsg, safe=False)
            else:
                print(tenant, "/",ce,"/", site,"/", instance)
                core_qs=CoreMainEngine.objects.filter(core_engine_code=core_engine_code, is_active=True)

                if len(core_qs)>0:

                    for core_engine in core_qs:
                        core_engine_id=core_engine.id
                        log.info(core_engine_id)

                    tenant_qs=Tenants.objects.filter(tenant_code=tenant, is_active=True)
                    if len(tenant_qs)>0:
                        log.info("1")
                        for tenants in tenant_qs:
                            tenant_id=tenants.id

                        site_qs=Sites.objects.filter(core_engine_id=core_engine_id, tenant_id=tenant_id, site_code=site, is_active=True)
                        if len(site_qs)>0:
                            for sites in site_qs:
                                site_id=sites.id

                            instance_qs=Instances.objects.filter(core_engine_id=core_engine_id, tenant_id=tenant_id, site_id=site_id, is_active=True)
                            if len(instance_qs)>0:
                                for instances in instance_qs:
                                    instance_id=instances.id

                                module_activation_qs=Modules.objects.filter(core_engine_id=core_engine_id, tenant_id=tenant_id, site_id=site_id, is_active=True, is_activated=True)
                                if len(module_activation_qs)>0:
                                    my_active_modules=[]
                                    for active_modules in module_activation_qs:
                                        activations= {"module": active_modules.module, "activation_dt": active_modules.activation_dt, "validity_start_date": active_modules.validity_start_date, "validity_end_date":active_modules.validity_end_date , "activation_key": active_modules.activation_key}
                                        my_active_modules.append(activations)

                                    log.info(my_active_modules)
                                    return JsonResponse(my_active_modules, safe=False)
                                else:
                                    errmsg = {"error":"Critical", "error_description": "Error!! No modules activated in the system yet!!!"}
                                    log.info(errmsg)
                                    return JsonResponse(errmsg, safe=False)
                            else:
                                errmsg = {"error":"Critical", "error_description": "Error!! Specified Instance doesnt exists in the system!!!"}
                                log.info(errmsg)
                                return JsonResponse(errmsg, safe=False)
                        else:
                            errmsg = {"error":"Critical", "error_description": "Error!! Specified Site doesnt exists in the system!!!"}
                            log.info(errmsg)
                            return JsonResponse(errmsg, safe=False)
                    else:
                        errmsg = {"error":"Critical", "error_description": "Error!! Specified Client doesnt exists in the system!!!"}
                        log.info(errmsg)
                        return JsonResponse(errmsg, safe=False)
                else:
                    errmsg = {"error":"Critical", "error_description": "Error!! Specified Core Engine doesnt exists in the system!!!"}
                    log.info(errmsg)
                    return JsonResponse(errmsg, safe=False)

    except Exception as e:
        errmsg = {"error":"Critical", "error_description": "Error in fetching active modules"}
        log.error(errmsg, exc_info=True)
        return JsonResponse(errmsg, safe=False)
