from django.shortcuts import render
from .models import CoreEngine as CEModel
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from components.core.coreEngine import CoreEngine
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


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
            data = CoreEngine.activate_core_engine(payload)
            if data:
                with transaction.atomic():
                    ce = CEModel()
                    o = CEModel.objects.create(
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

                    qs = CEModel.objects.order_by('last_updated_on')[0]
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



def get_ce_details(requests, ce):
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


