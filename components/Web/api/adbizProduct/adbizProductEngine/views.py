from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core import validators
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.db import transaction
import datetime
import uuid
import json
import random
from .models import ProductEngine as PEModel
from .models import Customers as CustModel
from django.views.generic import TemplateView
from components.product.productEngine import ProductEngine
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def activate(request):
    try:
        payload = json.loads(request.body)
        if payload != None or payload != "":
            pe = ProductEngine()
            data = pe.activate_product_engine(payload)
            if data:
                with transaction.atomic():
                    o = PEModel.objects.create(
                        product_engine_code = data['engine_id'],
                        root_namespace = pe.get_root_namespace(),
                        registered_to = data["registered_to"],
                        activation_file_location = pe.get_activation_file_location(),
                        activation_key = data["activation_key"],
                        activation_dt = data["activation_dt"],
                        host_name = data["host_name"],
                        host_ip_address = data["host_ip_address"],
                        os_release = data["os_release"],
                        release_info = data["release_info"],
                        last_updated_by = "product_admin",
                        is_activated = True
                    )
                    o.save()
                    output = "Activated Successfully!!"

                    qs = PEModel.objects.order_by('last_updated_on')[0]
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

@csrf_exempt
def add_customer(request, pe):
    try:
        payload = json.loads(request.body)
        if payload != None or payload != "":
            qs = PEModel.objects.filter(engine_id=pe)
            print(qs)
            if len(qs)>0:
                engine_id = pe
                customer = CustModel()
                uq = random.randrange(10 ** 11, 10 ** 12)
                ns = payload["customer_namespace"]
                customer_code = str(uq) + "@" + str(ns)
                print(customer_code)
                o = CustModel.objects.create(
                    engine_id = engine_id,
                    customer_name = payload["customer_name"],
                    customer_namespace = payload["customer_namespace"],
                    customer_code = customer_code,
                    registration_number=payload["registration_number"],
                    registration_dt = payload["registration_dt"],
                    city = payload["city"],
                    country = payload["country"],
                    state = payload["state"],
                    company_category = payload["company_category"],
                    company_sub_category=payload["company_sub_category"],
                    company_type = payload["company_type"],
                    company_class=payload["company_class"],
                    website_url = payload["website_url"],
                    last_updated_by = "product_admin"
                )
                o.save()
                output = "Customer added Successfully!!"
                output = output + " Customer Id:" + str(customer_code)
                return HttpResponse(output)
            else:
                output = "Error occurred during processing the payload for adding customer!! Product Engine doesnt exists!!"
                return HttpResponse(output)
        else:
            output = "Error!! Incorrect Payload"
            return HttpResponse(output)
    except Exception as e:
        print("Error!!! Error in creating new customer. ", e)

@csrf_exempt
def sync_hub(request, pe):
    try:
        payload = json.loads(request.body)
        if payload != None or payload != "":
            qs = PEModel.objects.filter(engine_id=pe, is_active=True, is_activated=True)
            print(qs)
            if len(qs)>0:
                output = {
                    "product_engine_code": pe,
                    "activation_key": qs.activation_key
                }
            else:
                output = "Error occurred during processing the request for Product Engine details!! Product Engine doesnt exists!!"
                return HttpResponse(output)
        else:
            output = "Error!! Incorrect Payload"
            return HttpResponse(output)

    except Exception as e:
        print("Error!!! Error in creating new customer. ", e)

#
# def contact_us(request):
#     try:
#         if request.method == 'POST':
#             print('POST')
#             f = ContactUsForm(request.POST)
#             if f.is_valid():
#                 print("Valid")
#                 f.save()
#                 output = "Successfull!!"
#                 return HttpResponse(output)
#             else:
#                 print("InValid")
#                 output = "Invalid"
#                 print (f.errors)
#                 return HttpResponse(output)
#         elif request.method=='GET':
#             f = ContactUsForm()
#
#         return render(request, "contact_us.html", {'form': f})
#     except Exception as e:
#         print(e)

#
# def login(TemplateView):
#     try:
#         print('registration')
#         template_name = "pages_login.html"
#
#     except Exception as e:
#         print(e)
#
# # # Create your views here.
# def index(request):
#     output = "Welcome to Adbiz"
#     return render(request, 'index.html',{})

# def product_engine_index(request):
#     try:
#         product_engine = ProductEngine.objects.all()
#         template = loader.get_template('product_engines.html')
#         context = {
#             'product_engine': product_engine,
#             'time': datetime.datetime.now(),
#         }
#         return HttpResponse(template.render(context, request))
#
#         #output = ', '.join([p for p in product_engine])
#         # for product_engine in pe :
#         #     print(product_engine.registered_to)
#         #     return HttpResponse(product_engine)
#
#         # rows = {
#         #     'product_engine': product_engine,
#         #     #'test': 'test1',
#         # }
#         # print(rows)
#         # return render(request, 'product_engines.html', rows)  #{'rows':rows}
#     except Exception as e:
#         print(e)
#
# def viewProductEngine(request):
#     try:
#         pass
#     except Exception as e:
#         print(e)