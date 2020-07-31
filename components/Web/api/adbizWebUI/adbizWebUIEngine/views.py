from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.auth import logout, authenticate
from django.contrib.auth.views import LoginView
from .models import *
from django.contrib.auth.forms import AuthenticationForm
import json
import sys
import requests
import logging
from django.core.serializers import serialize
from django.http import JsonResponse
import components.core.library.display.coreUIDisplayEngine as CoreLibDisplayEngine
# Create your views here.


class CustomLogin(LoginView):

    def post(self, request):
        try:
            log = logging.getLogger("main")

            #login(request, form.get_user())
            errmsg = []
            form = AuthenticationForm(request, data=request.POST)


            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password') #request.POST['password']
                log.info("Login request received for user: %s..", username)
                log.info("Authenticating User now..")
                user = authenticate(
                    request,
                    username=username,
                    password=password
                )
                if user:
                    if user.is_active:
                        login(request, user)
                        log.info("Loading Session for the user")

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

                            log.info("Loading Core Engine Session...")
                            request.session['core_engine_url'] = core_engine_details['core_engine_url']
                            request.session['core_engine_code'] = core_engine_details['core_engine_code']
                            request.session['core_engine_api_key'] = core_engine_details['api_key']

                            log.info("Loading Catalog Engine Session...")
                            request.session['catalog_engine_url'] = catalog_engine_details['catalog_engine_url']
                            request.session['catalog_engine_code'] = catalog_engine_details['catalog_engine_code']
                            request.session['catalog_engine_api_key'] = catalog_engine_details['api_key']

                            log.info("Loading IO Engine Session...")
                            request.session['io_engine_url'] = io_engine_details['io_engine_url']
                            request.session['io_engine_headers'] = io_engine_details['headers']
                            request.session["data_lake"] = io_engine_details["properties"].get("data_lake")

                            log.info("Loading Catalog & DataModel Details for the User...")
                            request.session['catalog_code'] = catalog_details['catalog_code']
                            request.session['catalog_name'] = catalog_details['catalog_name']
                            request.session['date_hierarchy'] = catalog_details['date_hierarchy']
                            request.session['calendar_type'] = catalog_details['calendar_type']

                            request.session['datamodel_code'] = datamodel_details['datamodel_code']
                            request.session['datamodel_name'] = datamodel_details['datamodel_name']


                        request.session['username'] = username

                        log.info("Loading User Details")
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
                                log.error(errmsg)
                                return render(request, 'registration/login.html', {'errors': errmsg})
                            else:
                                log.info("Loading User Access Details %s", request.session['user_id'])
                                modules = AdbizUserAccess.objects.filter(user_id = request.session['user_id'])
                                modules_list  =[]
                                if len(modules) > 0:
                                    for k in modules:
                                        modules_list.append(k.module)

                                    request.session["module_access"] = modules_list
                                    log.info("User granted access to Module: %s", request.session["module_access"])

                                    # Check for Default module. First load the system preference and then user preference value for default module
                                    log.info("Finding default module as per the System Preferences")
                                    preferences = AdbizPreferences.objects.filter(preference_code = 'P0001', module__isnull = True)      # for default module access
                                    if len(preferences) > 0:
                                        for k in preferences:
                                            preference_id = k.id
                                            system_default_module = k.default_value

                                        log.info("System Default Module: %s", system_default_module)
                                        log.info("Finding default module as per the User Preferences")
                                        default_module = AdbizUserPreferences.objects.filter(preference_id = preference_id , user_id = request.session['user_id'], module__isnull = True)
                                        if len(default_module) > 0:
                                            for k in default_module:
                                                request.session["default_module"] = k.preference_value
                                                request.session["current_module"] = k.preference_value
                                                current_module = k.preference_value
                                            log.info("User Default Module: %s", request.session["default_module"])

                                            # if system_default_module:
                                            #     request.session["default_module"] = system_default_module

                                            log.info("Loading all User Preferences")
                                            user_preferences = AdbizUserPreferences.objects.filter(user_id=request.session['user_id'], module__isnull=False)
                                            if len(user_preferences) > 0:
                                                user_preferences_serialized = json.loads(
                                                    serialize('json', user_preferences))
                                                request.session["user_preferences"] = user_preferences_serialized

                                            # Load metadata from Core Engine (API call)
                                            log.info("Load Display Library from Core")
                                            disp_metadata = load_coreLib_display_components(request)
                                            if disp_metadata:
                                                md_corelib_display_components = json.loads(disp_metadata)

                                                log.info("Loading all dashboards")
                                                all_dashboards = load_all_dashboards(request, md_corelib_display_components)

                                                # for key, value in request.session.items():
                                                #     log.info('{} => {}'.format(key, value))

                                                if all_dashboards:
                                                    log.info("Loading Menu items")
                                                    menu = get_menu_items(request, request.session["default_module"], request.session['user_id'])
                                                    if menu:
                                                        request.session["menu_items"] = menu
                                                        # load_home_page(request)

                                                        if current_module == "ACTRBL":
                                                            return TemplateResponse(request, 'actrbl_index.html')
                                                        elif current_module == "ACTPBL":
                                                            return TemplateResponse(request, 'actpbl_index.html')
                                                    else:
                                                        errmsg.append("No menu items defined for the current user!!")
                                                        log.error(errmsg)
                                                        form = AuthenticationForm()
                                                        return render(request, 'registration/login.html', {'errors': errmsg, 'form': form})
                                                else:
                                                    errmsg.append("No Dashboards defined current user/roles!!")
                                                    log.error(errmsg)
                                                    form = AuthenticationForm()
                                                    return render(request, 'registration/login.html', {'errors': errmsg, 'form': form})
                                            else:
                                                errmsg.append("Not able to connect to Core Engine for the Metadata!!")
                                                log.error(errmsg)
                                                form = AuthenticationForm()
                                                return render(request, 'registration/login.html',
                                                              {'errors': errmsg, 'form': form})
                                        else:
                                            errmsg.append("No default module set for the user!!")
                                            log.error(errmsg)
                                            form = AuthenticationForm()
                                            return render(request, 'registration/login.html', {'errors': errmsg, 'form': form})
                                    else:
                                        errmsg.append("No System default module set for the user!!")
                                        log.error(errmsg)
                                        form = AuthenticationForm()
                                        return render(request, 'registration/login.html', {'errors': errmsg, 'form': form})
                                else:
                                    msg = ("User not granted access to any Module!!")
                                    errmsg.append(msg)
                                    log.error(msg)
                                    form = AuthenticationForm()
                                    return render(request, 'registration/login.html', {'errors': errmsg, 'form': form})
                    else:
                        msg = "User is currently marked as inactive. Cannot login!!"
                        errmsg.append(msg)
                        log.error(errmsg)
                        form = AuthenticationForm()
                        return render(request, 'registration/login.html', {'errors': errmsg, 'form': form})
            else:
                errmsg.append( "Invalid login!!")
                log.error("Error in validating the user!!!! %s", errmsg)
                form = AuthenticationForm()
                return render(request, 'registration/login.html', {'errors': errmsg, 'form': form})

        except Exception as e:
            msg = "Error in authentication user and loading the session!!!"
            errmsg.append(msg)
            errmsg.append(e)
            log.error(errmsg, exc_info=True)
            form = AuthenticationForm()
            return render(request, 'registration/login.html', {'errors': errmsg, 'form': form})


def custom_Logout(request):
    try:
        log = logging.getLogger("main")
        log.info("Logging out user")
        logout(request)
        return HttpResponseRedirect('/adbizUI/')
    except Exception as e:
        log.error("Error in logging out the current user", exc_info=True)



def activation(request):
    try:
        # Handles Activation of UI Engine.
        # Admin will trigger this API giving a payload that contains: Activation Key for UI Engine (as published by the Licensing Routine), Core Engine Id & URL (API end point)
        log = logging.getLogger("main")
        return HttpResponse("Successfully Activated UI Engine!!!")
    except Exception as e:
        #log.error("Error in Activating UI Web Engine!!!", exc_info=True)
        pass


def load_home_page(request):
    try:
        log = logging.getLogger("main")
        if request.user.is_authenticated:
            if request.session["current_module"] == "ACTRBL":
                log.info("Loading ACTRBL Home Page...")
                return TemplateResponse(request, 'actrbl_index.html')
            elif request.session["current_module"] == "ACTPBL":
                return TemplateResponse(request, 'actpbl_index.html')
        else:
            form = AuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})

    except Exception as e:
        #log.error("Error in loading home page post login process", exc_info=True)
        pass




# Get all the user preferences for the signed in user. Update the current session parameters using the preferences.
# Preferences are set for each module and are applied during active session only
def get_user_preferences(request, module):
    try:
        request.session["max_rows_per_page"] = ""
        request.session["home_page"] = ""
        request.session["home_page_max_widgets"] = ""
        request.session["default_kpi"] = ""
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
        log = logging.getLogger("main")
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
                        return menu_items_list
                else:
                    return None
            else:
                return None
        else:
            return None


    except Exception as e:
        #log.error("Error in loading menu items!!", exc_info=True)
        return None


# Load all dashboard and its components (widgets/graph/table) to Session as a part of the login process.
# Catalog service provides the metadata (data model/dashboard) via API Call.
# Uses the Core Library to generate the required tags for Widget/Chart/Table based on the libraries configured.
# Session variables are later used by different views (html pages) to display individual components

def load_all_dashboards(request, md_corelib_display_components):
    try:
        log = logging.getLogger("main")
        log.info("--------------- Loading Dashboards for the logged in User ---------------")
        post_url = request.session['catalog_engine_url'] + "getAllDashboards/"
        log.info("Connecting to Catalog Engine to retrieve the latest Catalogs & Data Models for the current user...")
        log.info(post_url)
        #post_url = "http://127.0.0.1:10001/adbiz/CatalogService/getAllDashboards/"
        headers = {"module": request.session["current_module"],  "tenant": request.session["tenant_code"], "site": request.session["site_code"], "instance": request.session["instance_code"], "Content-Type": "application/json"}
        payload = json.dumps({"catalog_details": {"catalog_code": request.session["catalog_code"]}, "datamodel_details":{"datamodel_code": request.session["datamodel_code"]}, "token":"112233445566778899"})

        response = requests.get(post_url, data=payload, headers=headers)
        if response.text:
            dashboard_catalog = json.loads(response.content)

            log.info("Generating Chart Container tags...")
            chart_container_tags = generate_chart_container_tags(md_corelib_display_components)

            log.info("Generating Table Container tags...")
            table_container_tags = generate_table_container_tags(md_corelib_display_components)

            for dashboard in dashboard_catalog:
                dashboard_code = dashboard["dashboard_code"]
                dashboard_details = dashboard["dashboard_details"]
                log.info("Loading dashboard: %s", dashboard_details["dashboard_name"])
                dash_key = "dashboard" + "$" + dashboard_code       # create a unique key for each dashboard in the request object
                request.session[dash_key] = dashboard_details

                all_dashboard_components = dashboard["component_details"]
                if all_dashboard_components:
                    final_component_tags = ""
                    final_chart_tags = ""
                    final_table_api_tags = ""
                    for component in all_dashboard_components:
                        if component:
                            component_code = component["component_code"]
                            log.info("Loading Components: %s", component["component_title"])
                            log.info("Generating Component tags...")
                            component_tags_output = generate_component_tags(component, md_corelib_display_components)
                            if component_tags_output:
                                component_tags = component_tags_output["component_tags"]
                                component_display_id = component_tags_output["component_display_id"]
                                log.info("Widget Display Id: %s", component_display_id)

                                # Generate Charts tags for the component. One component can have many charts.
                                log.info("Generating Chart tags for Component: %s", component_display_id)
                                chart_tags_output = generate_chart_tags(component, component_display_id, md_corelib_display_components)
                                if chart_tags_output:
                                    log.info("Chart Display Id's: %s", chart_tags_output["chart_display_ids"])
                                    component_click_functions = None
                                    for item in chart_tags_output["chart_display_ids"]:
                                        if component_click_functions:
                                            component_click_functions = component_click_functions + item + "_getChartData();"
                                        else:
                                            component_click_functions = item + "_getChartData();"
                                    log.info("Component On Click Calls: %s", component_click_functions)
                                    chart_tags = chart_tags_output["chart_tags"]
                                    component_tags = component_tags.replace("{COMPONENT ONCLICK CALLS}", component_click_functions )

                                    # Generate Table tags for each chart. One chart can have many tables.
                                    chart_titles = chart_tags_output["chart_titles"]
                                    for chart_id in chart_tags_output["chart_ids"]:
                                        log.info("Generating Table tags for chart: %s", str(chart_id))

                                        if chart_titles:
                                            chart_title = chart_titles[chart_id]
                                            if chart_title:
                                                chart_container_tags = chart_container_tags.replace("{CHART TITLE " + str(chart_id) + "}", chart_title)

                                        table_tags_output = generate_table_tags(component, component_display_id, chart_id, md_corelib_display_components)
                                        if table_tags_output:
                                            if table_tags_output["chart_id"] == chart_id:
                                                log.info("Table Display Id's: %s", table_tags_output["table_display_ids"])
                                                table_api_tags = table_tags_output["table_api_tags"]
                                                chart_onclick_tags = table_tags_output["chart_onclick_tags"]
                                                log.info("Generating Chart Onclick Calls")
                                                final_table_api_tags = final_table_api_tags + table_api_tags
                                                chart_tags = chart_tags.replace("{CHART ONCLICK CALLS " + str(chart_id) + "}", chart_onclick_tags)

                                    final_chart_tags = final_chart_tags + chart_tags

                                final_component_tags = final_component_tags + component_tags

                    log.info("Generating Common Scripts..")
                    md_common_scripts = md_corelib_display_components["common_scripts"]
                    my_common_scripts = ""
                    for script in md_common_scripts:
                        for k,v in script.items():
                            my_common_scripts = my_common_scripts + v
                    request.session["common_scripts"] = my_common_scripts

                    log.info("Generating Session Data for the dashboard..")
                    dash_table_containers_key = "dashboardTableContainerTags" + "$" + dashboard_code
                    request.session[dash_table_containers_key] = table_container_tags

                    dash_comp_key = "dashboardComponentTags" + "$" + dashboard_code
                    request.session[dash_comp_key] = final_component_tags

                    dash_chart_containers_key = "dashboardChartContainerTags" + "$" + dashboard_code
                    request.session[dash_chart_containers_key] = chart_container_tags

                    dash_chart_key = "dashboardChartTags" + "$" + dashboard_code
                    request.session[dash_chart_key] = final_chart_tags

                    dash_table_key = "dashboardTableTags" + "$" + dashboard_code
                    request.session[dash_table_key] = final_table_api_tags

                    return True

                else:
                    log.info("No components defined for this dashboard")

        else:
            log.error("Error in connecting to Catalog Engine!!")
            return False


    except Exception as e:
        log.error("Error in UI Engine!! Error in generating Dashboards for the Module!!", exc_info=True)
        return False


# Load Core Library for Components
def load_coreLib_display_components(request):
    try:
        log = logging.getLogger("main")
        log.info("--------------- Loading Core Display Component Metadata ---------------")
        post_url = request.session['core_engine_url']  + "DisplayComponents/"
        log.info(post_url)

        headers = {"module": request.session["current_module"],  "tenant": request.session["tenant_code"], "site": request.session["site_code"], "instance": request.session["instance_code"], "Content-Type": "application/json"}
        payload = json.dumps({"token":"112233445566778899"})
        log.info(headers)
        response = requests.get(post_url, data=payload, headers=headers)

        if response.text:
            log.info("Response received from Core Engine..")
            return response.text
        else:
            log.error("Error in connecting to Core Engine to retrieve the Display Component Metadata!!")
            return None

    except Exception as e:
        log.error("Error in retrieving Display Component Metadata!!", exc_info=True)
        return None


# load components metadata along with tags
def generate_component_tags(my_component, md_corelib_display_components):
    try:
        log = logging.getLogger("main")
        log.info("--------------- Loading Component/Widget Tags ---------------")
        component_tags = CoreLibDisplayEngine.generate_component_tags(my_component, md_corelib_display_components)
        return component_tags
    except Exception as e:
        log.error("Error in generating Component/Widget Tags!!", exc_info=True)
        return None


# generate Tags for Chart
def generate_chart_tags(my_component, component_display_id, md_corelib_display_components):
    try:
        log = logging.getLogger("main")
        log.info("--------------- Loading Chart Tags ---------------")
        chart_tags = CoreLibDisplayEngine.generate_chart_tags(my_component, component_display_id ,md_corelib_display_components)
        return chart_tags
    except Exception as e:
        log.error("Error in generating Chart Tags!!", exc_info=True)
        return None


# generate Tags for Table
def generate_table_tags(my_component, component_display_id, chart_id,  md_corelib_display_components):
    try:
        log = logging.getLogger("main")
        log.info("--------------- Loading Table Tags ---------------")
        table_tags = CoreLibDisplayEngine.generate_table_tags(my_component, component_display_id, chart_id, md_corelib_display_components)
        return table_tags
    except Exception as e:
        log.error("Error in generating Table Tags!!", exc_info=True)
        return None


# generate Container Tags for Table
def generate_table_container_tags(md_corelib_display_components):
    try:
        log = logging.getLogger("main")
        log.info("--------------- Loading Table Container Tags ---------------")
        table_container_tags = CoreLibDisplayEngine.generate_table_container_tags(md_corelib_display_components)
        return table_container_tags
    except Exception as e:
        log.error("Error in generating Table Container Tags!!", exc_info=True)
        return None

# generate Container Tags for charts
def generate_chart_container_tags(md_corelib_display_components):
    try:
        log = logging.getLogger("main")
        log.info("--------------- Loading Chart Container Tags ---------------")
        chart_container_tags = CoreLibDisplayEngine.generate_chart_container_tags(md_corelib_display_components)
        return chart_container_tags
    except Exception as e:
        log.error("Error in generating Chart Container Tags!!", exc_info=True)
        return None

# Get data for the Component like Values/Indicators using the Component Query
# def get_component_data(request):
#     try:
#         log = logging.getLogger("main")
#         log.info("--------------- Get Component Data (API) ---------------")
#
#         errmsg = {}
#         errmsg["message"] = "Error validating the request"
#
#         component_query = request.GET['component_query']
#         post_url = 'http://127.0.0.1:10002/adbiz/IOEngine/executeValueQuery/'
#
#         headers = {"module": request.session["current_module"], "tenant": request.session["tenant_code"],
#                    "site": request.session["site_code"], "instance": request.session["instance_code"],"data_lake": request.session["data_lake"],
#                    "Content-Type": "application/json"}
#
#         payload = json.dumps({"component_query": component_query, "user_id": request.session["user_id"],
#                               "hierarchy": {"H1": "419258870883@dtl.entity", "H2": ["ALL"]}})
#
#         response = requests.get(post_url, data=payload, headers=headers)
#         return HttpResponse(response.content)
#
#     except Exception as e:
#         print("Error in creating payload for IO Engine!!", e)
#         return JsonResponse({"status": "Error!!"})
#
#
# def get_chart_data(request):
#     try:
#         errmsg = {}
#         errmsg["message"] = "Error validating the request"
#
#         chart_query = request.GET['chart_query']
#         post_url = 'http://127.0.0.1:10002/adbiz/IOEngine/executeChartQuery/'
#
#         headers = {"module": request.session["current_module"], "tenant": request.session["tenant_code"],
#                    "site": request.session["site_code"], "instance": request.session["instance_code"],"data_lake": request.session["data_lake"],
#                    "Content-Type": "application/json"}
#
#         payload = json.dumps({"chart_query": chart_query, "user_id": request.session["user_id"],
#                               "hierarchy": {"H1": "419258870883@dtl.entity", "H2": ["ALL"]}})
#
#         response = requests.get(post_url, data=payload, headers=headers)
#         return HttpResponse(response.content)
#
#     except Exception as e:
#         print("Error in creating payload for IO Engine!!", e)
#         return JsonResponse({"status": "Error!!"})
#
#
# def get_table_data(request):
#     try:
#         errmsg = {}
#         errmsg["message"] = "Error validating the request"
#
#         table_query = request.GET['table_query']
#         print(table_query)
#         if table_query:
#             post_url = 'http://127.0.0.1:10002/adbiz/IOEngine/executeTableQuery/'
#
#             headers = {"module": request.session["current_module"], "tenant": request.session["tenant_code"],
#                        "site": request.session["site_code"], "instance": request.session["instance_code"],"data_lake": request.session["data_lake"],
#                        "Content-Type": "application/json"}
#
#             payload = json.dumps({"table_query": table_query, "user_id": request.session["user_id"],
#                                   "hierarchy": {"H1": "419258870883@dtl.entity", "H2": ["ALL"]}})
#
#             response = requests.get(post_url, data=payload, headers=headers)
#             return HttpResponse(response.content)
#         else:
#             errmsg["description"] = "Table Query not correct or not provided in the metadata!!!"
#             return HttpResponse({"error": errmsg})
#
#     except Exception as e:
#         errmsg["description"] = "Error in creating payload for IO Engine Table Query execution!!" + str(e)
#         print(errmsg)
#         return HttpResponse({"error": errmsg})



#
# # find all components for sales forecast dashbooard
# def get_actrbl_sales_forecast(request):
#     try:
#         dashboards = request.session["dashboards"]
#         for k in dashboards:
#             if (k["dashboard_details"].get("dashboard_reference_class") == "adbiz.actrbl.salesForecastDashboard") :
#                 component_details = k["component_details"]
#
#         if component_details is not None:
#             output = {"components": component_details, "count": len(component_details)  }
#
#             return TemplateResponse(request, 'actrbl_sales_forecast.html', {"output":output})
#         else:
#             return TemplateResponse(request, 'actrbl_sales_forecast.html', {"output": None})
#
#     except Exception as e :
#         print(e)
#
#
#
# # find all components for sales forecast dashbooard
# def get_actrbl_sales_exception(request):
#     try:
#         return TemplateResponse(request, 'actrbl_sales_exception.html', {})
#
#
#         # dashboards = request.session["dashboards"]
#         # for k in dashboards:
#         #     if (k["dashboard_details"].get("dashboard_reference_class") == "adbiz.actrbl.salesForecastDashboard") :
#         #         component_details = k["component_details"]
#         #
#         # if component_details is not None:
#         #     # output = {"components": component_details, "count": len(component_details)  }
#         #
#         #     return TemplateResponse(request, 'actrbl_sales_exception.html', {"output":output})
#         # else:
#         #     return TemplateResponse(request, 'actrbl_sales_exception.html', {"output": None})
#
#     except Exception as e :
#         print(e)
#
# #
# # # find all components for sales forecast dashbooard
# # def get_actrbl_sales_summary(request):
# #     try:
# #         dashboards = request.session["dashboards"]
# #         for k in dashboards:
# #             if (k["dashboard_details"].get("dashboard_reference_class") == "adbiz.actrbl.salesForecastDashboard") :
# #                 component_details = k["component_details"]
# #
# #         if component_details is not None:
# #             output = {"components": component_details, "count": len(component_details)  }
# #
# #             return TemplateResponse(request, 'actrbl_sales_summary.html', {"output":output})
# #         else:
# #             return TemplateResponse(request, 'actrbl_sales_summary.html', {"output": None})
# #
# #     except Exception as e :
# #         print(e)
#
#
# # sends request to IO engine for execution and getting the table data
# def get_output_data(request, *args, **kwargs):
#     try:
#         errmsg = {}
#         errmsg["message"] = "Error validating the request"
#         component_query = request.GET['component_query']
#
#         post_url = 'http://127.0.0.1:10002/adbiz/IOEngine/executeDashboardQuery/'
#         headers = {"module": request.session["current_module"], "tenant": request.session["tenant_code"],
#                    "site": request.session["site_code"], "instance": request.session["instance_code"],
#                    "Content-Type": "application/json"}
#         payload = json.dumps({"component_query": component_query, "user_id": request.session["user_id"], "hierarchy":{ "H1":"419258870883@dtl.entity", "H2":["ALL"]}})
#         print("-->", headers)
#         print(payload)
#         response = requests.get(post_url, data=payload, headers=headers)
#         print(response.content)
#         return HttpResponse(response.content)
#
#     except Exception as e:
#         print("Error in creating payload for IO Engine!!", e)
#         return JsonResponse({"status": "Error!!"})
#
#