from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
import json
import requests
from django.core.serializers import serialize
from django.http import JsonResponse

# Create your views here.


class CustomLogin(LoginView):

    def post(self, request):
        try:
            #login(request, form.get_user())
            errmsg = []
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password') #request.POST['password']
                print("--> Authenticating User")
                user = authenticate(
                    request,
                    username=username,
                    password=password
                )
                if user:
                    if user.is_active:
                        login(request, user)
                        print("--> Loading Session")

                        engine = AdbizUIEngine.objects.filter(is_active = True, is_activated = True)
                        if len(engine):
                            # loading other dependent Engine details that UI Engine interacts
                            for k in engine:
                                request.session['tenant_code'] = k.tenant_code
                                request.session['site_code'] = k.site_code
                                request.session['instance_code'] = k.instance_code
                                request.session['ui_engine_code'] = k.ui_engine_code
                                #request.session['core_engine_code'] = k.core_engine_code
                                core_engine_details = json.loads(k.core_engine_details)
                                io_engine_details = json.loads(k.io_engine_details)
                                catalog_engine_details = json.loads(k.catalog_engine_details)
                                catalog_details = json.loads(k.catalog_details)
                                datamodel_details = json.loads(k.datamodel_details)


                            request.session['core_engine_url'] = core_engine_details['core_engine_url']
                            request.session['core_engine_code'] = core_engine_details['core_engine_code']
                            request.session['core_engine_api_key'] = core_engine_details['api_key']

                            request.session['catalog_engine_url'] = catalog_engine_details['catalog_engine_url']
                            request.session['catalog_engine_code'] = catalog_engine_details['catalog_engine_code']
                            request.session['catalog_engine_api_key'] = catalog_engine_details['api_key']

                            request.session['io_engine_url'] = io_engine_details['io_engine_url']
                            request.session['io_engine_code'] = io_engine_details['io_engine_code']
                            request.session['io_engine_api_key'] = io_engine_details['api_key']

                            request.session['catalog_code'] = catalog_details['catalog_code']
                            request.session['catalog_name'] = catalog_details['catalog_name']
                            request.session['date_hierarchy'] = catalog_details['date_hierarchy']
                            request.session['calendar_type'] = catalog_details['calendar_type']

                            request.session['datamodel_code'] = datamodel_details['datamodel_code']
                            request.session['datamodel_name'] = datamodel_details['datamodel_name']


                        request.session['username'] = username
                        print("Loading User Details")
                        user_details = AdbizUser.objects.filter(email = username, is_active = True)
                        if len(user_details) > 0:
                            for k in user_details:
                                user_account = k.user_account
                                request.session['user_id'] = k.id
                                request.session['user_account'] = k.user_account
                                request.session['is_super_user'] = k.is_super_user
                                request.session['is_locked'] = k.is_locked
                                request.session['is_system_user'] = k.is_system_user
                                f_name = k.first_name
                                l_name = k.last_name
                                if l_name:
                                    full_name = f_name + " " + l_name
                                else:
                                    full_name = f_name
                                request.session['full_name'] = full_name

                            if request.session['is_locked']:
                                errmsg.append("User is currently locked!! Please contact your administrator")
                                return render(request, 'registration/login.html', {'errors': errmsg})
                            else:
                                print("Loading User Access Details", request.session['user_id'])
                                modules = AdbizUserAccess.objects.filter(user_id = request.session['user_id'])
                                modules_list  =[]
                                if len(modules) > 0:
                                    for k in modules:
                                        modules_list.append(k.module)

                                    request.session["module_access"] = modules_list
                                    print("User granted access to Module:", request.session["module_access"])

                                    # Check for Default module. First load the system preference and then user preference value for default module
                                    print("Finding default module as per the System Preferences")
                                    preferences = AdbizPreferences.objects.filter(preference_code = 'P0001', module__isnull = True)      # for default module access
                                    if len(preferences) > 0:
                                        for k in preferences:
                                            preference_id = k.id
                                            system_default_module = k.default_value

                                        print("System Default Module:", system_default_module)
                                        print("Finding default module as per the User Preferences")
                                        default_module = AdbizUserPreferences.objects.filter(preference_id = preference_id , user_id = request.session['user_id'], module__isnull = True)
                                        if len(default_module) > 0:
                                            for k in default_module:
                                                request.session["default_module"] = k.preference_value
                                                request.session["current_module"] = k.preference_value
                                                current_module = k.preference_value
                                            print("User Default Module:", request.session["default_module"])

                                            # if system_default_module:
                                            #     request.session["default_module"] = system_default_module

                                            print("Loading all User Preferences")
                                            user_preferences = AdbizUserPreferences.objects.filter(user_id=request.session['user_id'], module__isnull=False)
                                            if len(user_preferences) > 0:
                                                user_preferences_serialized = json.loads(
                                                    serialize('json', user_preferences))
                                                request.session["user_preferences"] = user_preferences_serialized

                                            print("Loading all dashboards")
                                            all_dashboards = get_all_dashboards(request)
                                            #print(all_dashboards)
                                            if all_dashboards:
                                                request.session["dashboards"] = json.loads(all_dashboards)
                                                print("Loading Menu items")
                                                menu = get_menu_items(request, request.session["default_module"], request.session['user_id'])
                                                if menu:
                                                    request.session["menu_items"] = menu
                                                    if current_module == "ACTRBL":
                                                        return TemplateResponse(request, 'actrbl_index.html')
                                                    elif current_module == "ACTPBL":
                                                        return TemplateResponse(request, 'actpbl_index.html')
                                                else:
                                                    errmsg.append("No menu items defined for the current user!!")
                                                    form = AuthenticationForm()
                                                    return render(request, 'registration/login.html', {'errors': errmsg, 'form': form})
                                            else:
                                                errmsg.append("No Dashboards defined current user/roles!!")
                                                form = AuthenticationForm()
                                                return render(request, 'registration/login.html', {'errors': errmsg, 'form': form})
                                        else:
                                            errmsg.append("No default module set for the user!!")
                                            form = AuthenticationForm()
                                            return render(request, 'registration/login.html', {'errors': errmsg, 'form': form})
                                    else:
                                        errmsg.append("No System default module set for the user!!")
                                        form = AuthenticationForm()
                                        return render(request, 'registration/login.html', {'errors': errmsg, 'form': form})
                                else:
                                    msg = ("User not granted access to any Module!!")
                                    errmsg.append(msg)
                                    print(msg)
                                    form = AuthenticationForm()
                                    return render(request, 'registration/login.html', {'errors': errmsg, 'form': form})
                    else:
                        msg = "User is currently marked as inactive. Cannot login!!"
                        errmsg.append(msg)
                        form = AuthenticationForm()
                        return render(request, 'registration/login.html', {'errors': errmsg, 'form': form})
            else:
                errmsg.append( "Invalid login!!")
                print("Error!!!!", errmsg)
                form = AuthenticationForm()
                return render(request, 'registration/login.html', {'errors': errmsg, 'form': form})

        except Exception as e:
            print("Error in authentication user and loading the session!!!", e)
            form = AuthenticationForm()
            return render(request, 'registration/login.html', {'errors': errmsg, 'form': form})


def custom_Logout(request):
    logout(request)
    return HttpResponseRedirect('/adbizUI/login/')


def activation(request):
    try:
        # Handles Activation of UI Engine.
        # Admin will trigger this API giving a payload that contains: Activation Key for UI Engine (as published by the Licensing Routine), Core Engine Id & URL (API end point)
        pass
        return HttpResponse("Successfully Activated UI Engine!!!")
    except Exception as e:
        print(e)


def load_home_page(request):
    try:
        if request.user.is_authenticated:
            if request.session["current_module"] == "ACTRBL":
                return TemplateResponse(request, 'actrbl_index.html')
            elif request.session["current_module"] == "ACTPBL":
                return TemplateResponse(request, 'actpbl_index.html')
        else:
            form = AuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})

    except Exception as e:
        print(e)

#
# def login(request):
#     try:
#         if request.method == 'POST':
#             username = request.POST['username']
#             password = request.POST['password']
#             user = User.objects.filter(username =

#             if user:
#                 username = request.POST['username']
#                 request.session["username"] = username
#                 request.session["full_name"] = ""
#                 request.session["default_module"] = "ACTPBL"
#                 request.session["token"] = ""
#                 request.session["current_module"] = "ACTPBL"
#
#             else:
#                 return render(request, 'registration/login.html', {})
#
#         if request.method == "GET":
#             return
#     except Exception as e:
#         print(e)


# Get all the user preferences for the signed in user. Update the current session parameters using the preferences.
# Preferences are set for each module and are applied during active session only
def get_user_preferences(request, module):
    try:
        request.session["max_rows_per_page"] = ""
        request.session["home_page"] = ""
        request.session["home_page_max_widgets"] = ""
        request.session["default_kpi"] = ""
        pass
    except Exception as e:
        print(e)


# Load all the user privileges for the signed in user.
def load_user_privileges(request):
    try:
        privileges = {}
        request.session["privileges"] = privileges
        pass
    except Exception as e:
        print(e)


def get_engine_details(request):
    try:
        pass
    except Exception as e:
        print(e)



# Load all menu items as per the role assigned to the user.
def get_menu_items(request, module, user_id ):
    try:
        # load menu items for the module, role & user combination
        # find the role for the user

        user_role = AdbizUserAccess.objects.filter(user_id=user_id, module=module)
        if len(user_role) > 0:
            for k in user_role:
                request.session["user_role_id"] = k.role_id

            role = AdbizRoles.objects.filter(id = request.session["user_role_id"], module = module, is_active=True)
            if len(role) > 0:
                for k in role:
                    request.session["role"] = k.role_name
                    request.session["role_code"] = k.role_code
                    request.session["is_module_admin"] = k.is_module_admin
                    request.session["is_service_account"] = k.is_service_account
                    request.session["system_role_reference"] = k.system_role_reference
                    if k.system_role_reference == "adbiz.roles.manager":
                        request.session["is_manager"] = True
                    else:
                        request.session["is_manager"] = False

                menu = AdbizMenuRoles.objects.filter(role_id = request.session["user_role_id"])
                if len(menu) > 0:
                    menu_id = []
                    for k in menu:
                        menu_id.append(k.menu_items_id)

                    menu_items = AdbizMenuItems.objects.filter(id__in = menu_id, module = module, is_active = True).order_by("display_seq", "level")
                    if len(menu_items) > 0:
                        menu_items_list = []
                        for k in menu_items:
                            menu_details = { "menu_id": k.id , "level": k.level,  "menu_name": k.menu_name , "menu_tooltip": k.menu_tooltip , "menu_url": k.menu_url , "display_seq": k.display_seq , "menu_code": k.menu_code, "menu_properties": k.menu_properties }
                            menu_items_list.append(menu_details)
                        print("----menu items ---#")
                        return menu_items_list
                else:
                    return None
            else:
                return None
        else:
            return None


    except Exception as e:
        print("Error in loading menu items!!", e)
        return None

def get_all_dashboards(request):
    try:
        #post_url = request.session['catalog_engine_url'] + "/getAllDashboards/"
        post_url= 'http://127.0.0.1:10001/adbiz/CatalogService/getAllDashboards/'
        headers = {"module": request.session["current_module"],  "tenant": request.session["tenant_code"], "site": request.session["site_code"], "instance": request.session["instance_code"], "Content-Type": "application/json"}
        payload = json.dumps({"catalog_details": {"catalog_code": request.session["catalog_code"]}, "datamodel_details":{"datamodel_code": request.session["datamodel_code"]}, "token":"112233445566778899"})
        # print(post_url)
        # print(headers)
        # print(payload)
        response = requests.get(post_url, data=payload, headers=headers)
        return response.content


    except Exception as e:
        print("Error in loading Dashboards!!", e)
        return None

# find all components for sales forecast dashbooard
def get_actrbl_sales_forecast(request):
    try:
        dashboards = request.session["dashboards"]
        for k in dashboards:
            if (k["dashboard_details"].get("dashboard_reference_class") == "adbiz.actrbl.salesForecastDashboard") :
                component_details = k["component_details"]

        if component_details is not None:
            output = {"components": component_details, "count": len(component_details)  }

            return TemplateResponse(request, 'actrbl_sales_forecast.html', {"output":output})
        else:
            return TemplateResponse(request, 'actrbl_sales_forecast.html', {"output": None})

    except Exception as e :
        print(e)

# sends request to IO engine for execution and getting the table data
def get_output_data(request, *args, **kwargs):
    try:
        errmsg = {}
        errmsg["message"] = "Error validating the request"
        component_query = request.GET['component_query']
        # print("--->")
        # for key, value in request.session.items():
        #     print('{} => {}'.format(key, value))

        post_url = 'http://127.0.0.1:10002/adbiz/IOEngine/executeDashboardQuery/'
        headers = {"module": request.session["current_module"], "tenant": request.session["tenant_code"],
                   "site": request.session["site_code"], "instance": request.session["instance_code"],
                   "Content-Type": "application/json"}
        payload = json.dumps({"component_query": component_query, "user_id": request.session["user_id"], "hierarchy":{ "H1":"419258870883@dtl.entity", "H2":["ALL"]}})
        print("-->", headers)
        print(payload)
        response = requests.get(post_url, data=payload, headers=headers)
        print(response.content)
        return HttpResponse(response.content)

    except Exception as e:
        print("Error in creating payload for IO Engine!!", e)
        return JsonResponse({"status": "Error!!"})


