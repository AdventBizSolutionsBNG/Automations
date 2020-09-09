from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.auth import logout, authenticate
from django.contrib.auth.views import LoginView
from .models import *
from django.contrib.auth.forms import AuthenticationForm
import json
import sys
from datetime import datetime
import requests
import logging
from django.core.serializers import serialize
from django.http import JsonResponse
import components.core.library.display.coreUIDisplayEngine as CoreLibDisplayEngine
import components.core.library.query.coreQueryEngine as CoreLibQueryEngine
from .exceptions import *

# Create your views here.

log = logging.getLogger("main")

class CustomLogin(LoginView):

    def post(self, request):
        try:


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

                        # todo: Update User table with the login details: example - last login

                        engine = AdbizUIEngine.objects.filter(is_active = True, is_activated = True)
                        if len(engine) >0:
                            # loading other dependent Engine details that UI Engine interacts
                            for k in engine:
                                request.session['tenant_code'] = k.tenant_code
                                request.session['site_code'] = k.site_code
                                request.session['instance_code'] = k.instance_code
                                request.session['ui_engine_code'] = k.ui_engine_code
                                request.session['core_engine_code'] = k.core_engine_code

                                core_engine_details = json.loads(k.core_engine_details)
                                io_engine_details = json.loads(k.io_engine_details)
                                catalog_engine_details = json.loads(k.catalog_engine_details)
                                catalog_details = json.loads(k.catalog_details)
                                datamodel_details = json.loads(k.datamodel_details)

                            log.info("Loading Core Engine details into Session...")
                            request.session['core_engine_url'] = core_engine_details['core_engine_url']
                            #request.session['core_engine_code'] = core_engine_details['core_engine_code']
                            request.session['core_engine_api_key'] = core_engine_details['api_key']

                            log.info("Loading Catalog Engine details into Session...")
                            request.session['catalog_engine_url'] = catalog_engine_details['catalog_engine_url']
                            request.session['catalog_engine_code'] = catalog_engine_details['catalog_engine_code']
                            request.session['catalog_engine_api_key'] = catalog_engine_details['api_key']

                            log.info("Loading IO Engine details into Session...")
                            request.session['io_engine_url'] = io_engine_details['io_engine_url']
                            request.session['io_engine_headers'] = io_engine_details['headers']
                            request.session["data_lake"] = io_engine_details["properties"].get("data_lake")

                            log.info("Loading Catalog & DataModel Details for the User details into Session...")
                            request.session['catalog_code'] = catalog_details['catalog_code']
                            request.session['catalog_name'] = catalog_details['catalog_name']
                            request.session['date_hierarchy'] = catalog_details['date_hierarchy']
                            request.session['calendar_type'] = catalog_details['calendar_type']

                            request.session['datamodel_code'] = datamodel_details['datamodel_code']
                            request.session['datamodel_name'] = datamodel_details['datamodel_name']


                        request.session["username"] = username

                        log.info("Loading User Details")
                        myUsers = AdbizUser.objects.filter(email = username, is_active = True)
                        if len(myUsers) > 0:
                            for myUser in myUsers:
                                if not myUser.is_locked:
                                    my_user_profile = {}
                                    my_user_id = str(myUser.id)
                                    my_user_email = myUser.email

                                    my_user_profile["user_id"] = my_user_id
                                    my_user_profile["user_email"] = my_user_email
                                    my_user_profile["user_account"] = myUser.user_account
                                    my_user_profile["is_super_user"] = myUser.is_super_user
                                    my_user_profile["is_system_user"] = myUser.is_system_user
                                    my_user_profile["user_since"] = myUser.joined_dt.strftime("%Y/%m/%d")
                                    my_user_profile["login_dt"] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

                                    request.session["user_id"] = my_user_id

                                    # request.session['is_super_user'] = myUser.is_super_user
                                    # request.session['is_system_user'] = myUser.is_system_user
                                    #
                                    # request.session['user_since'] = myUser.joined_dt.strftime("%Y/%m/%d")
                                    # request.session['login_dt'] = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

                                    f_name = myUser.first_name
                                    l_name = myUser.last_name

                                    request.session["first_name"] = f_name
                                    request.session["last_name"] = l_name

                                    if l_name:
                                        my_user_full_name = f_name + " " + l_name
                                    else:
                                        my_user_full_name = f_name
                                    my_user_profile["user_full_name"] = my_user_full_name
                                    log.info("User Profile: %s", my_user_full_name)

                                    #request.session["full_name"] = my_user_full_name

                                    # Get list of all roles assigned to the user (for all modules)
                                    log.info("Loading User Access Details (Roles & Modules) %s", my_user_email)
                                    roles = AdbizUserAccess.objects.filter(user_id = my_user_id)
                                    if len(roles) >0:
                                        my_user_roles = {}
                                        modules_list = []
                                        for role in roles:
                                            role_details = AdbizRoles.objects.filter(id = role.role_id, is_active = True)
                                            if len(role_details) >0:
                                                for my_role_detail in role_details:
                                                    # print(m.is_module_admin, m.is_service_account)
                                                    my_user_roles = {"module": my_role_detail.module, "is_module_admin":my_role_detail.is_module_admin, "is_service_account":my_role_detail.is_service_account, "role_name": my_role_detail.role_name, "role_class": my_role_detail.system_role_reference}
                                                    modules_list.append(my_role_detail.module)

                                                my_user_profile["roles_access"] = my_user_roles
                                                my_user_profile["modules_access"] = modules_list
                                                    

                                        # log.info("Loading User Access Details (Modules) %s", my_user_email)
                                        # myModules = AdbizUserAccess.objects.filter(user_id = my_user_id)
                                        # if len(myModules) > 0:
                                        #     modules_list = []
                                        #     for myModule in myModules:
                                        #         modules_list.append(myModule.module)

                                            my_user_profile["modules_access"]= modules_list
                                            request.session["module_access"] = modules_list
                                            log.info("User granted access to Modules: %s", modules_list)

                                            # Check for Default module. First load the system preference and then user preference value for default module
                                            # log.info("Load System Preferences & set default module")
                                            # my_sys_preferences = {}
                                            # sys_preferences = AdbizPreferences.objects.filter()     # for default module access
                                            # if len(sys_preferences) > 0:
                                            #     for sys_preference in sys_preferences:
                                            #         my_sys_preferences[sys_preference.id] = { "preference_name": sys_preference.preference_name, "module": sys_preference.module, "default_value": sys_preference.default_value, "id":sys_preference.id, "preference_code": sys_preference.preference_code}
                                            #         if sys_preference.preference_code == "P0001":
                                            #             if len(sys_preference.default_value) > 0:
                                            #                 my_sys_default_module = sys_preference.default_value
                                            #                 log.info("System Default Module: %s", my_sys_default_module)
                                            #             else:
                                            #                 log.error("System default module not set in the System Preferences")

                                            # Load Active Modules:
                                            log.info("Load Active Modules")
                                            active_modules = get_active_modules(request)
                                            if active_modules:
                                                log.info(active_modules)
                                                request.session["active_modules"] = active_modules

                                                # Load System Preferences
                                                log.info("Load Sytem Preferences")
                                                system_preferences_qs = AdbizUserPreferences.objects.filter(user_id__isnull = True)
                                                if len(system_preferences_qs) > 0:
                                                    my_system_preferences_qs = {}
                                                    my_system_preferences = {}
                                                    for system_preference in system_preferences_qs:
                                                        my_system_preferences[system_preference.preference_code] = {"preference_code": system_preference.preference_code, "preference_value": system_preference.preference_value, "module": system_preference.module}

                                                        if system_preference.preference_code == "P0001":
                                                            request.session["system_default_module"] = system_preference.preference_value
                                                            request.session["default_module"] = system_preference.preference_value

                                                        if system_preference.preference_code == "P0102":

                                                            system_period_preference = my_system_preferences["P0102"]["preference_value"]
                                                            date_range = CoreLibQueryEngine.decode_date_range(system_period_preference)

                                                            request.session["period_start_date"] = date_range["start_date"]
                                                            request.session["period_end_date"] = date_range["end_date"]

                                                        if system_preference.preference_code == "P0103":

                                                            system_hist_preference = my_system_preferences["P0103"]["preference_value"]
                                                            date_range = CoreLibQueryEngine.decode_date_range(system_hist_preference)

                                                            request.session["hist_start_date"] = date_range["start_date"]
                                                            request.session["hist_end_date"] = date_range["end_date"]

                                                # Load Default Module
                                                log.info("Load Default Module set for user login")
                                                user_preferences_qs = AdbizUserPreferences.objects.filter(user_id = my_user_id, preference_code = 'P0001')
                                                if len(user_preferences_qs) > 0:
                                                    my_user_preferences_qs = {}
                                                    my_user_preferences = {}
                                                    for user_preference in user_preferences_qs:
                                                        if user_preference.preference_code == "P0001":
                                                            if user_preference.preference_value:
                                                                request.session["default_module"] = user_preference.preference_value
                                                                request.session["current_module"] = user_preference.preference_value
                                                                current_module = user_preference.preference_value

                                                # Load User Preferences
                                                log.info("Load User Preferences")
                                                user_preferences_qs = AdbizUserPreferences.objects.filter(user_id=my_user_id, module = current_module)
                                                if len(user_preferences_qs) > 0:
                                                    my_user_preferences = {}

                                                    for user_preference in user_preferences_qs:

                                                        my_user_preferences[user_preference.preference_code] = {
                                                                "preference_code": user_preference.preference_code,
                                                                "module": user_preference.module,
                                                                "preference_value": user_preference.preference_value}

                                                        if user_preference.preference_code == "P0102":
                                                            print('P0102')
                                                            user_period_preference = user_preference.preference_value
                                                            print(type(user_period_preference))
                                                            date_range = CoreLibQueryEngine.decode_date_range(user_period_preference)

                                                            request.session["period_start_date"] = date_range["start_date"]
                                                            request.session["period_end_date"] = date_range["end_date"]

                                                        if user_preference.preference_code == "P0103":
                                                            print('P0103')
                                                            user_hist_preference = user_preference.preference_value
                                                            date_range = CoreLibQueryEngine.decode_date_range(user_hist_preference)

                                                            request.session["hist_start_date"] = date_range["start_date"]
                                                            request.session["hist_end_date"] = date_range["end_date"]

                                                    if request.session["default_module"]:
                                                        log.info("User Default Module: %s", request.session["default_module"])

                                                        # Load Role Privileges - TODO

                                                        # Load Hierarchy
                                                        log.info("Loading Org Hierarchy")
                                                        my_org_hierarchy = get_org_hierarchy(request)
                                                        if check_response(my_org_hierarchy):
                                                            request.session["org_hierarchies"] = my_org_hierarchy

                                                            # load default hierarchy

                                                            # load the entities for the defined hierarchy
                                                            my_org_entities = {}
                                                            for hierarchy_type_id, hierarchy in my_org_hierarchy.items():
                                                                log.info("Loading Org Entities")
                                                                entities = get_org_entities(request, hierarchy_type_id)
                                                                if entities:
                                                                    my_org_entities[hierarchy_type_id] = entities

                                                            request.session["org_entities"] = my_org_entities

                                                            # Load metadata from Core Engine (API call)
                                                            log.info("Load Display Library from Core")
                                                            disp_metadata = load_coreLib_display_components(request)
                                                            if disp_metadata:
                                                                md_corelib_display_components = json.loads(disp_metadata)
                                                                log.info("Loading all dashboards")
                                                                all_dashboards = load_all_dashboards(request, md_corelib_display_components)
                                                                if all_dashboards:
                                                                    log.info("Loading Menu items")
                                                                    menu = get_menu_items(request, request.session["default_module"], my_user_id)
                                                                    log.info("Loading User Session details")
                                                                    if load_user_details(request):
                                                                        log.info("Loading User Run Time details")
                                                                        if load_run_time_details((request)):
                                                                            # for key, value in request.session.items():
                                                                            #     print('{} => {}'.format(key, value))
                                                                            if len(menu)>0:
                                                                                request.session["menu_items"] = menu
                                                                                if current_module == "ACTRBL":
                                                                                    return TemplateResponse(request, 'actrbl_index.html')
                                                                                elif current_module == "ACTPBL":
                                                                                    return TemplateResponse(request, 'actpbl_index.html')
                                                                            else:
                                                                                raise MenuRender(request)
                                                                        else:
                                                                            raise NoRuntimeDetails(request)
                                                                    else:
                                                                        raise NoUserDetails(request)
                                                                else:
                                                                    raise NoDashboards(request)
                                                            else:
                                                                raise CoreEngineConnection(request)
                                                        else:
                                                            raise NoOrgHierarchies(request)
                                                    else:
                                                        raise NoUserDefaultModule(request)
                                                else:
                                                    raise NoUserPreferences(request)
                                            
                                            else:
                                                raise NoActiveModules(request)
                                        else:
                                            raise NoModuleAccess(request)
                                    else:
                                       raise NoRoleAccess(request)
                else:
                    raise InvalidLogin(request)
            else:
                raise InvalidLogin(request)


        except Exception as e:
            msg = "Error in authentication user and loading the session!!!"
            log.error(errmsg, exc_info=True)
            form = AuthenticationForm()
            return render(request, 'registration/login.html', {'errors': errmsg, 'form': form})

def load_user_details(request):
    try:
        user_id = request.session["user_id"]
        user_name = request.session["username"]
        first_name = request.session["first_name"]
        last_name = request.session["last_name"]
        user_details = {"user_id": user_id, "user_name": user_name, "first_name": first_name, "last_name": last_name}
        request.session["user_details"] = user_details
        return True
    except Exception as e:
        log.info("Error loading User Details", exc_info=True)
        return False


def load_run_time_details(request):
    try:
        period_start_date = request.session["period_start_date"]
        period_end_date = request.session["period_end_date"]
        hist_start_date = request.session["hist_start_date"]
        hist_end_date = request.session["hist_end_date"]
        run_time_details = {"period_start_date": period_start_date, "period_end_date": period_end_date, "hist_start_date": hist_start_date, "hist_end_date": hist_end_date}
        request.session["run_time_details"] = run_time_details
        return True
    except Exception as e:
        log.info("Error loading User Run Time Details", exc_info=True)
        return False


def custom_Logout(request):
    try:
        # log = logging.getLogger("main")
        log.info("Logging out user")
        logout(request)
        return HttpResponseRedirect('/adbizUI/')
    except Exception as e:
        log.error("Error in logging out the current user", exc_info=True)



def activation(request):
    try:
        # Handles Activation of UI Engine.
        # Admin will trigger this API giving a payload that contains: Activation Key for UI Engine (as published by the Licensing Routine), Core Engine Id & URL (API end point)
        # log = logging.getLogger("main")
        return HttpResponse("Successfully Activated UI Engine!!!")
    except Exception as e:
        #log.error("Error in Activating UI Web Engine!!!", exc_info=True)
        pass


def load_home_page(request):
    try:
        # log = logging.getLogger("main")
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
def get_user_preferences_qs(request, module):
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
        # log = logging.getLogger("main")
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
        # log = logging.getLogger("main")
        log.info("Loading all dashboards for the current Module + Role")
        dashboard_catalog = get_all_dashboards(request)
        if dashboard_catalog:
            log.info("Generating Chart Container tags...")
            chart_container_tags = generate_chart_container_tags(md_corelib_display_components)

            log.info("Generating Table Container tags...")
            table_container_tags = generate_table_container_tags(md_corelib_display_components)

            for dashboard in dashboard_catalog:
                dashboard_code = dashboard["dashboard_code"]
                dashboard_details = dashboard["dashboard_details"]
                log.info("<<<<<<<<<<<<<<<<< ----------------------- >>>>>>>>>>>>>>>>>>>>")
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

                    # user_details = {"session_id" : , "first_name":  ... ...... }
                    # request.session["user_session"] = user_details

                    log.info("Done generating Dashboards....")
                else:
                    log.info("No components defined for this dashboard")
            return True
        else:
            log.error("Error in connecting to Catalog Engine!!")
            return False


    except Exception as e:
        log.error("UI Engine. Error in generating Dashboards for the Module!!", exc_info=True)
        return False


# Load Core Library for Components
def load_coreLib_display_components(request):
    try:
        # log = logging.getLogger("main")
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
        # log = logging.getLogger("main")
        log.info("--------------- Loading Component/Widget Tags ---------------")
        component_tags = CoreLibDisplayEngine.generate_component_tags(my_component, md_corelib_display_components)
        return component_tags
    except Exception as e:
        log.error("Error in generating Component/Widget Tags!!", exc_info=True)
        return None


# generate Tags for Chart
def generate_chart_tags(my_component, component_display_id, md_corelib_display_components):
    try:
        # log = logging.getLogger("main")
        log.info("--------------- Loading Chart Tags ---------------")
        chart_tags = CoreLibDisplayEngine.generate_chart_tags(my_component, component_display_id ,md_corelib_display_components)
        return chart_tags
    except Exception as e:
        log.error("Error in generating Chart Tags!!", exc_info=True)
        return None


# generate Tags for Table
def generate_table_tags(my_component, component_display_id, chart_id,  md_corelib_display_components):
    try:
        # log = logging.getLogger("main")
        log.info("--------------- Loading Table Tags ---------------")
        table_tags = CoreLibDisplayEngine.generate_table_tags(my_component, component_display_id, chart_id, md_corelib_display_components)
        return table_tags
    except Exception as e:
        log.error("Error in generating Table Tags!!", exc_info=True)
        return None


# generate Container Tags for Table
def generate_table_container_tags(md_corelib_display_components):
    try:
        # log = logging.getLogger("main")
        log.info("--------------- Loading Table Container Tags ---------------")
        table_container_tags = CoreLibDisplayEngine.generate_table_container_tags(md_corelib_display_components)
        return table_container_tags
    except Exception as e:
        log.error("Error in generating Table Container Tags!!", exc_info=True)
        return None

# generate Container Tags for charts
def generate_chart_container_tags(md_corelib_display_components):
    try:
        # log = logging.getLogger("main")
        log.info("--------------- Loading Chart Container Tags ---------------")
        chart_container_tags = CoreLibDisplayEngine.generate_chart_container_tags(md_corelib_display_components)
        return chart_container_tags
    except Exception as e:
        log.error("Error in generating Chart Container Tags!!", exc_info=True)
        return None

# Get data for the Component like Values/Indicators using the Component Query from IO Engine
def get_component_data(request):
    try:
        # log = logging.getLogger("main")
        log.info("--------------- Get Component Data (API) ---------------")

        errmsg = {}
        errmsg["message"] = "Error validating the request"
        log.info(request)

        component_query = request.GET['component_query']

        period_start_date = request.GET['period_start_date']
        period_end_date = request.GET['period_end_date']

        post_url = 'http://127.0.0.1:10002/adbiz/IOEngine/executeValueQuery/'
        log.info(post_url)

        headers = {"module": request.session["current_module"], "tenant": request.session["tenant_code"],
                   "site": request.session["site_code"], "instance": request.session["instance_code"],"data_lake": request.session["data_lake"],
                   "Content-Type": "application/json"}

        payload = json.dumps({"component_query": component_query,
                              "period_start_date":period_start_date,
                              "period_end_date": period_end_date,
                              "user_id": request.session["user_id"],
                              "hierarchy": {"H1": "419258870883@dtl.entity", "H2": ["ALL"]}})

        log.info(payload)
        response = requests.get(post_url, data=payload, headers=headers)
        return HttpResponse(response.content)

    except Exception as e:
        log.error("Error in creating payload for IO Engine!!", exc_info=True)
        return JsonResponse({"status": "Error!!"})


def get_chart_data(request):
    try:
        # log = logging.getLogger("main")
        log.info("--------------- Get Chart Data (API) ---------------")

        errmsg = {}
        errmsg["message"] = "Error validating the request"

        chart_query = request.GET['chart_query']
        period_start_date = request.GET['period_start_date']
        period_end_date = request.GET['period_end_date']

        post_url = 'http://127.0.0.1:10002/adbiz/IOEngine/executeChartQuery/'
        log.info(post_url)

        headers = {"module": request.session["current_module"], "tenant": request.session["tenant_code"],
                   "site": request.session["site_code"], "instance": request.session["instance_code"],"data_lake": request.session["data_lake"],
                   "Content-Type": "application/json"}

        payload = json.dumps({"chart_query": chart_query, "user_id": request.session["user_id"],
                              "period_start_date": period_start_date,
                              "period_end_date": period_end_date,
                              "hierarchy": {"H1": "419258870883@dtl.entity", "H2": ["ALL"]}})

        response = requests.get(post_url, data=payload, headers=headers)
        return HttpResponse(response.content)

    except Exception as e:
        log.error("Error in creating payload for IO Engine!!", exc_info=True)
        return JsonResponse({"status": "Error!!"})


def get_table_data(request):
    try:
        # log = logging.getLogger("main")
        log.info("--------------- Get Table Data (API) ---------------")

        errmsg = {}
        errmsg["message"] = "Error validating the request"

        table_query = request.GET['table_query']
        period_start_date = request.GET['period_start_date']
        period_end_date = request.GET['period_end_date']

        if table_query:
            post_url = 'http://127.0.0.1:10002/adbiz/IOEngine/executeTableQuery/'
            log.info(post_url)
            headers = {"module": request.session["current_module"], "tenant": request.session["tenant_code"],
                       "site": request.session["site_code"], "instance": request.session["instance_code"],"data_lake": request.session["data_lake"],
                       "Content-Type": "application/json"}

            payload = json.dumps({"table_query": table_query, "user_id": request.session["user_id"],
                                  "period_start_date": period_start_date,
                                  "period_end_date": period_end_date,
                                  "hierarchy": {"H1": "419258870883@dtl.entity", "H2": ["ALL"]}})

            response = requests.get(post_url, data=payload, headers=headers)
            return HttpResponse(response.content)
        else:
            errmsg["description"] = "Table Query not correct or not provided in the metadata!!!"
            log.error(errmsg)
            return HttpResponse({"error": errmsg})

    except Exception as e:
        errmsg["description"] = "Error in creating payload for IO Engine Table Query execution!!" + str(e)
        log.error(errmsg, exc_info=True)
        return HttpResponse({"error": errmsg})


# Get list of all dashboards for the current module from Catalog Engine
def get_all_dashboards(request):
    try:
        post_url = request.session['catalog_engine_url'] + "getAllDashboards/"
        log.info("Connecting to Catalog Engine to retrieve the latest Catalogs & Data Models for the current user...")
        log.info(post_url)
        headers = {"module": request.session["current_module"],
                   "tenant": request.session["tenant_code"],
                   "site": request.session["site_code"],
                   "instance": request.session["instance_code"],
                   "Content-Type": "application/json"}

        payload = json.dumps({"catalog_details": {"catalog_code": request.session["catalog_code"]},
                              "datamodel_details": {"datamodel_code": request.session["datamodel_code"]},
                              "token": "112233445566778899"})

        response = requests.get(post_url, data=payload, headers=headers)
        if response.content:
            content_data = json.loads(response.content)
            return content_data
        else:
            errmsg = "Error retrieving Dashboards metadata from Catalog Engine!!!"
            log.error(errmsg)
            return False

    except Exception as e:
        errmsg = "Error in retrieving Dashboards metadata from the Catalog Engine!!"
        log.error(errmsg, exc_info=True)
        return False

def get_org_hierarchy(request):
    try:
        # log = logging.getLogger("main")
        post_url = request.session['catalog_engine_url'] + "getOrgHierarchy/"
        log.info("Connecting to Catalog Engine to retrieve the Org Hierachies...")
        log.info(post_url)
        headers = {"module": request.session["current_module"], "tenant": request.session["tenant_code"],
                   "site": request.session["site_code"], "instance": request.session["instance_code"],
                   "Content-Type": "application/json"}
        payload = json.dumps({"catalog_details": {"catalog_code": request.session["catalog_code"]},
                              "datamodel_details": {"datamodel_code": request.session["datamodel_code"]},
                              "token": "112233445566778899"})

        response = requests.get(post_url, data=payload, headers=headers)
        if response.content:
            content_data = json.loads(response.content)
            return content_data
        else:
            errmsg = "Error retrieving Org Hierarchies from Metadata!!!"
            log.error(errmsg)
            return False

    except Exception as e:
        errmsg = "Error in retrieving Org Hierarchy from the Catalog Engine!!"
        log.error(errmsg, exc_info=True)
        return False

def get_active_modules(request):
    try:
        # log = logging.getLogger("main")
        post_url = request.session['core_engine_url'] + "getActiveModules/"
        log.info("Connecting to Core Engine to retrieve active modules...")
        log.info(post_url)
        headers = {"Tenant": request.session["tenant_code"],
                   "Site": request.session["site_code"],
                   "Instance": request.session["instance_code"],
                   "Core": request.session["core_engine_code"],
                   "Content-Type": "application/json"}

        payload = json.dumps({"core_engine_api_key": request.session["core_engine_api_key"], "token": "112233445566778899"})

        response = requests.get(post_url, data=payload, headers=headers)
        if response.content:
            content_data = json.loads(response.content)
            return content_data
        else:
            errmsg = "Error retrieving active modules from Core Engine!!!"
            log.error(errmsg)
            return False

    except Exception as e:
        errmsg = "Error in retrieving active modules from Core Engin!!"
        log.error(errmsg, exc_info=True)
        return False

def check_response(content_data):
    try:
        if content_data:
            log.info("Verifying API Response... ")
            is_err = content_data.get("error")
            if is_err:
                err_msg = content_data.get("error_description")
                log.error(content_data)
                return False
            else:
                return True
        else:
            return False
    except Exception as e:
        log.error("Error in verifying the response content!!", exc_info=True)
        return False

def get_org_entities(request, org_hierarchy_type_ids):
    try:
        # log = logging.getLogger("main")
        post_url = request.session['catalog_engine_url'] + "getOrgEntities/"
        log.info("Connecting to Catalog Engine to retrieve the Org Entities...")
        log.info(post_url)
        # post_url = "http://127.0.0.1:10001/adbiz/CatalogService/getAllDashboards/"
        headers = {"module": request.session["current_module"], "tenant": request.session["tenant_code"],
                   "site": request.session["site_code"], "instance": request.session["instance_code"],
                   "Content-Type": "application/json"}
        payload = json.dumps({"catalog_details": {"catalog_code": request.session["catalog_code"]},
                              "datamodel_details": {"datamodel_code": request.session["datamodel_code"]},
                              "token": "112233445566778899", "org_hierarchy_type_ids": org_hierarchy_type_ids})

        response = requests.get(post_url, data=payload, headers=headers)
        if response.content:
            content_data = json.loads(response.content)
            return content_data
        else:
            errmsg = "Error retrieving Org Entities from the Catalog Engine!!!"
            log.error(errmsg, exc_info=True)
            return False

    except Exception as e:
        errmsg = "Error in retrieving Org Entities from the Catalog Engine!!"
        log.error(errmsg, exc_info=True)
        return False