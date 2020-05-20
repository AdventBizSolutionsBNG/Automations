from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User

# Create your views here.

def activation(request):
    try:
        # Handles Activation of UI Engine.
        # Admin will trigger this API giving a payload that contains: Activation Key for UI Engine (as published by the Licensing Routine), Core Engine Id & URL (API end point)
        pass
        return HttpResponse("Successfully Activated UI Engine!!!")
    except Exception as e:
        print(e)


def login(request):
    try:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = User.objects.filter(username = username)
            if user:
                username = request.POST['username']
                request.session["username"] = username
                request.session["full_name"] = ""
                request.session["default_module"] = "ACTPBL"
                request.session["token"] = ""
                request.session["current_module"] = "ACTPBL"

            else:
                return render(request, 'app_foldername/login.html', {})

    except Exception as e:
        print(e)


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


# Load all menu items as per the role assigned to the user.
def load_menu(request):
    try:
        menu = {}
        request.session["menu"] = menu

        pass
    except Exception as e:
        print(e)

