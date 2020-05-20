from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import ProductEngine
import datetime

# Create your views here.
def index(request):
    # output = "Welcome to Adbiz"
    return render(request, 'index.html',{})

def product_engine_index(request):
    try:
        product_engine = ProductEngine.objects.all()
        template = loader.get_template('product_engines.html')
        context = {
            'product_engine': product_engine,
            'time': datetime.datetime.now(),
        }
        return HttpResponse(template.render(context, request))

        #output = ', '.join([p for p in product_engine])
        # for product_engine in pe :
        #     print(product_engine.registered_to)
        #     return HttpResponse(product_engine)

        # rows = {
        #     'product_engine': product_engine,
        #     #'test': 'test1',
        # }
        # print(rows)
        # return render(request, 'product_engines.html', rows)  #{'rows':rows}
    except Exception as e:
        print(e)

def viewProductEngine(request):
    try:
        pass
    except Exception as e:
        print(e)