from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

from django.views.decorators.csrf import csrf_exempt

from datetime import datetime, timedelta
import json

from rest_framework.exceptions import PermissionDenied
import jwt
from django.conf import settings

@csrf_exempt
def login(request):
    try:
        u = User.objects.all()
        print(request.user)

        if len(u) >0:
            data = json.loads(request.body)
            if data != None or data != "":
                username = data['username']
                password = data['password']
                engine_id = data['engine_id']
                user = authenticate(username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    if request.user.is_authenticated:
                        print(request.user)
                        dt = datetime.utcnow() + timedelta(days=1)
                        token = jwt.encode({
                            'username': username,
                            'engine_id': engine_id,
                            'exp': int(dt.strftime('%s'))
                        },settings.SECRET_KEY, algorithm='HS256')

                        print(token)
                        request.session['engine_id'] = engine_id
                        request.session['token'] = str(token)
                        request.session['token_expiry'] = str(int(dt.strftime('%s')))
                        request.session.modified = True
                        return HttpResponse(True)
                    else:
                        raise PermissionDenied()
                        return HttpResponse(False)
                else:
                    print('---- no user -------')
        else:
            print('Setting up ETL Engine First Time..')
            su = User.objects.create_superuser('etladmin','etladmin@adventbizsolutions.com','etladmin@adbiz.com')
            eu = User.objects.create_user('etluser', 'etluser@adventbizsolutions.com', 'etluser@adbiz.com')

    except Exception as e:
        print("Error!!!")
        print(e)