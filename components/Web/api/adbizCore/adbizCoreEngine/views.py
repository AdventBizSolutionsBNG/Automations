from django.shortcuts import render
from .models import CoreEngine, Tenants, Sites, Instances, Modules, DataLakes
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from components.core.coreEngine import CoreEngine as CE
import json
from django.views.decorators.csrf import csrf_exempt
from components.core.modules.storageEngines import DataLakeStorage

# Create your views here.

from components.core.modules.settings import Settings
from components.core.coreEngine import CoreEngine

ce = CoreEngine()
display_metadata = ce.components

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
        payload = json.loads(request.body)
        if payload != None or payload != "":
            data = CE.activate_core_engine(payload)
            if data:
                with transaction.atomic():
                    ce = CoreEngine()
                    o = CoreEngine.objects.create(
                        core_engine_code = data["core_engine_code"],
                        customer_id = "",  #customer_id,
                        product_engine_code = data["product_engine_code"],
                        root_namespace = pe.get_root_namespace(),
                        registered_to = data["registered_to"],
                        activation_file_location = pe.get_activation_file_location(),
                        activation_key = data["activation_key"],
                        activation_dt = data["activation_dt"],
                        host_name = data["host_name"],
                        host_ip_address = data["host_ip_address"],
                        os_release = data["os_release"],
                        release_info = data["release_info"],
                        last_updated_by = "product_admin"
                    )
                    o.save()
                    output = "Activated Successfully!!"

                    qs = CoreEngine.objects.order_by('last_updated_on')[0]
                    output = output + " Engine Id:" + str(qs.engine_id)
                    return HttpResponse(output)
            else:
                output = "Error occurred during processing the payload for activation!!"
                return HttpResponse(output)
        else:
            output = "Error!! Incorrect Payload"
            return HttpResponse(output)

    except Exception as e:
        print(e)
        output = "Error in activating Product Engine using API. " + str(e)
        return HttpResponse(output)



def get_ce_details(request, ce):
    try:
        qs = CoreEngine.objects.filter(core_engine_code=ce, is_active=True)
        if len(qs) >0:
            data = {
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
            output="Error!! Incorrect Core Engine specified:" + ce
            return HttpResponse(output)

    except Exception as e:
        output = "Error in fetching details for the Core Engine"
        return HttpResponse(output)


def get_data_lake_storage_details(request):
    try:

        if request.method == "GET":
            body = request.body.decode('utf-8')
            data = {}
            data = json.loads(body)
            for k,v in data.items():
                if k == "tenant_code":
                    tenant = v
                if k == "core_engine_code":
                    ce = v
                if k == "site_code":
                    site = v
                if k == "instance_code":
                    instance = v
                if k == "module":
                    module = v

            if tenant is None or tenant == "" or ce is None or ce == "" or site is None or site == "" or instance is None or instance == "":

                output =  "Error!! Incorrect request body received!!!"
                return HttpResponse(output)
            else:
                qce = CoreEngine.objects.filter(core_engine_code= ce, is_active = True)
                if len(qce)>0:
                    for k in qce:
                        core_engine_id = k.id

                    qs1 = Tenants.objects.filter(tenant_code = tenant, is_active = True)
                    if len(qs1)>0:
                        for k in qs1:
                            tenant_id = k.id

                        qs2 = Sites.objects.filter(core_engine_id = core_engine_id, tenant_id=tenant_id, site_code=site, is_active=True)
                        if len(qs2)>0:
                            for k in qs2:
                                site_id = k.id
                            qs3 = Instances.objects.filter(core_engine_id = core_engine_id, tenant_id=tenant_id, site_id=site_id, is_active=True)
                            if len(qs3)>0:
                                for k in qs3:
                                    instance_id = k.id
                                qs4 = Modules.objects.filter(core_engine_id = core_engine_id, tenant_id=tenant_id, site_id=site_id, module=module, is_active=True)
                                if len(qs4)>0:
                                    for k in qs4:
                                        module_id = k.id
                                    qs = DataLakes.objects.filter(core_engine_id = core_engine_id,tenant_id=tenant_id, site_id=site_id, module=module, is_active=True)
                                    if len(qs)>0:
                                        for k in qs:
                                            dl_code = k.data_lake_code
                                            dl_class = k.storage_engine_class
                                            dl_primary = k.is_primary
                                            dl_type = k.data_lake_type
                                            dl_sub_type = k.data_lake_sub_type
                                            return JsonResponse({"data_lake_code":dl_code, "storage_engine_class":dl_class, "data_lake_type": dl_type, "data_lake_sub_type": dl_sub_type})
                                    else:
                                        output = "Error!! Data lake Storage doesnt exists in the system for the given parameters!!!"
                                        return HttpResponse(output)
                                else:
                                    output = "Error!! Specified Module doesnt exists in the system!!!"
                                    return HttpResponse(output)
                            else:
                                output = "Error!! Specified Instance doesnt exists in the system!!!"
                                return HttpResponse(output)
                        else:
                            output = "Error!! Specified Site doesnt exists in the system!!!"
                            return HttpResponse(output)
                    else:
                        output = "Error!! Specified Client doesnt exists in the system!!!"
                        return HttpResponse(output)
                else:
                    output = "Error!! Specified Core Engine doesnt exists in the system!!!"
                    return HttpResponse(output)

    except Exception as e:
        output = "Error in fetching details for the Data Lake Storage Engine"
        error = e
        print(e)
        return JsonResponse({"error":output, "error_details":e})


def get_display_component_metadata(request):
    try:
        if request.method == "GET":
            print("Request received for Display Components..")
            body = request.body.decode('utf-8')
            data = {}
            data = request.headers
            print("--->", request.headers)
            for k,v in data.items():
                if k == "Tenant":
                    tenant = v
                if k == "Site":
                    site = v
                if k == "Instance":
                    instance = v
                if k == "Module":
                    module = v

            if tenant is None or tenant == "" or site == "" or instance is None or instance == "":

                output =  "Error!! Incorrect request body received!!!"
                return JsonResponse(output)
            else:
                return JsonResponse(display_metadata)
    except Exception as e:
        output = "Error in fetching details for the Data Lake Storage Engine"
        error = e
        print(e)
        return JsonResponse({"error": output, "error_details": e})