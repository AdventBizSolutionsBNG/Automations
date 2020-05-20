from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Country
from django.db import transaction
from .forms import CountryForm
from django.core import serializers


# Create your views here.

from .models import Country,State

def country_index(request):
    try:
        print("--------->", request.method)
        if request.method == 'GET':
            country_list = Country.objects.filter(is_active=True)
            template = loader.get_template('country/country.html')
            f = CountryForm()
            context = {'country_list': country_list, 'form':f}
            return HttpResponse(template.render(context, request))

        elif request.method == "POST":
            f = CountryForm(request.POST)

            if f.is_valid():
                try:
                    model = f.save()
                    country_list = Country.objects.filter(is_active=True)
                    template = loader.get_template('country/country.html')
                    f = CountryForm()
                    context = {'country_list': country_list, 'form': f}
                    return HttpResponse(template.render(context, request))
                except Exception as e:
                    output = "Error!!" + str(e)
                    return HttpResponse(output)

            #return HttpResponse(template.render(context, request))
        #return render(request, 'country/country.html', context)


    except Exception as e:
        print(e)
        output = "Error!!" + str(e)
        return HttpResponse(output)

def get_country(request, cc):
    try:
        if request.method == 'GET':
            if cc == "ALL":
                qs = Country.objects.filter(is_active=True).values('country_code', 'country_name')
            elif cc != "" or cc is not None:
                qs = Country.objects.filter(is_active=True, country_code=cc).values('country_code', 'country_name')
            print(qs)
            if len(qs) >0:
                qs_list = list(qs)
                return JsonResponse(qs_list, safe=False)
                #qs_json = serializers.serialize('json', qs, fields=('country_code', 'country_name'))
                #return HttpResponse(qs) #, content_type='application/json')
                #print(qs)
                #return HttpResponse(qs)  #, content_type='application/json')
            else:
                output = "Error!!! No Country found with the code:" + cc
                return HttpResponse(output)

    except Exception as e:
        output = "Error!!!" + str(e)
        return HttpResponse(output)

# This method will accept payload as a file using the curl command (below). Single record addition:
# curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "Accept: text/html,application/json" -X POST -d @add_country.json http://127.0.0.1:8000/test/country/ops/add/
# sample payload:
# {
#     "country_code": "SA",
#     "country_name": "South America"
# }

method_decorator(csrf_exempt)
def add_country(request):
    try:
        data = json.loads(request.body)
        if data != None or data != "":
            cc = data['country_code']
            cn = data['country_name']
            cb = "Admin"
            o = Country.objects.create(country_code=cc, country_name=cn, create_by="Admin")
            o.save()
            output = "Added Successfully!!"
            return HttpResponse(output)
        else:
            output = "Error!! Incorrect Payload"
            return HttpResponse(output)
    except Exception as e:
        print(e)
        output = "Error in adding new data." + str(e)
        return HttpResponse(output)

# This method will accept payload as a file using the curl command (below). Multiple records addition:
# curl -i -H "Accept: application/json" -H "Content-Type: application/json" -H "Accept: text/html,application/json" -X POST -d @add_country_2.json http://127.0.0.1:8000/test/country/ops/add/
# sample payload: [
# {
#  "country_code": "SF",
#     "country_name": "South Africa"
# },
# {
#  "country_code": "GBR",
#     "country_name": " Great Britain"
# }]

method_decorator(csrf_exempt)
def upload_country(request):
    try:
        data = json.loads(request.body)
        if data != None or data != "":
            with transaction.atomic():
                for k in data:
                    cc = k['country_code']
                    cn = k['country_name']
                    cb = "Admin"
                    o = Country.objects.create(country_code=cc, country_name=cn, create_by="Admin")
                    o.save()
                output = "Uploaded Successfully!!"
                return HttpResponse(output)
        else:
            output = "Error!! Incorrect Payload"
            return HttpResponse(output)
    except Exception as e:
        print(e)
        output = "Error in uploading data." + str(e)
        return HttpResponse(output)

# Returns JSON object
def get_state(request, cc, sc):
    try:
        if request.method == 'GET':
            country_id = Country.objects.filter(is_active=True, country_code=cc)
            if country_id is not None:
                if sc == "ALL":
                    qs = State.objects.filter(country__in = country_id, is_active=True)
                elif sc != "" or sc is not None:
                    qs = State.objects.filter(country__in = country_id, is_active=True, state_code=sc )

                if len(qs)>0:
                    qs_json = serializers.serialize('json', qs)
                    return HttpResponse(qs_json, content_type='application/json')
                else:
                    output = "Error!!! No State found with the code:" + sc
                    return HttpResponse(output)
            else:
                output = "Error!!! No Country found with the code:" + cc
                return HttpResponse(output)

    except Exception as e:
        print(e)
        output = "Error!!!" + str(e)
        return HttpResponse(output)