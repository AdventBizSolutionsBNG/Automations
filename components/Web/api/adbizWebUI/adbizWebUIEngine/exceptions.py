from django.contrib.auth.forms import AuthenticationForm
import logging, sys
from django.shortcuts import render, HttpResponse, HttpResponseRedirect

log = logging.getLogger("main")

class InvalidLogin(Exception):
    def __init__(self, request):
        errmsg = "Error in validating the user!!"
        log.error(errmsg)
        relogin(request, errmsg)

class InactiveUser(Exception):
    def __init__(self, request):
        errmsg = "User is currently marked as inactive!!"
        log.error(errmsg)
        relogin(request, errmsg)

class LockedUser(Exception):
    def __init__(self, request):
        errmsg = "User is currently locked!! Please contact your administrator"
        log.error(errmsg)
        relogin(request, errmsg)

class NoRoleAccess(Exception):
    def __init__(self, request):
        errmsg = "User not granted access to any Role yet. Please contact your Administrator!!"
        log.error(errmsg)
        relogin(request, errmsg)

class NoModuleAccess(Exception):
    def __init__(self, request):
        errmsg = "User not granted access to any Role yet. Please contact your Administrator!!"
        log.error(errmsg)
        relogin(request, errmsg)

class NoSystemDefaultModule(Exception):
    def __init__(self, request):
        errmsg = "No System default module set for the user!!"
        log.error(errmsg)
        relogin(request, errmsg)

class NoUserDefaultModule(Exception):
    def __init__(self, request):
        errmsg = "No default module set for the user as  preferences!!"
        log.error(errmsg)
        relogin(request, errmsg)

class NoDashboards(Exception):
    def __init__(self, request):
        errmsg = "No Dashboards defined current user/roles!!"
        log.error(errmsg)
        relogin(request, errmsg)

class CoreEngineConnection(Exception):
    def __init__(self, request):
        errmsg = "Error in connecting to Core Engine for metadata!!"
        log.error(errmsg)
        relogin(request, errmsg)

class MenuRender(Exception):
    def __init__(self, request):
        errmsg = "Error in rendering Menu from the Metadata!!"
        log.error(errmsg)
        relogin(request, errmsg)

class NoUserPreferences(Exception):
    def __init__(self, request):
        errmsg = "No User Preferences set for the current user!!"
        log.error(errmsg)
        relogin(request, errmsg)

class NoOrgHierarchies(Exception):
    def __init__(self, request):
        errmsg = "Error in retrieving Org Hierarchies from the Catalog Engine!!"
        log.error(errmsg)
        relogin(request, errmsg)

class NoActiveModules(Exception):
    def __init__(self, request):
        errmsg = "Error in retrieving Active Modules from Core Engine!!"
        log.error(errmsg)
        relogin(request, errmsg)

class NoRuntimeDetails(Exception):
    def __init__(self, request):
        errmsg = "No Run Time Details set for the current user"
        log.error(errmsg)
        relogin(request, errmsg)

class NoUserDetails(Exception):
    def __init__(self, request):
        errmsg = "No User details set for the current user"
        log.error(errmsg)
        relogin(request, errmsg)

def relogin(request, errmsg):
    try:
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'errors': errmsg, 'form': form})
    except Exception as e:
        log.error("Error in routing the request to the login page", exc_info = True)

