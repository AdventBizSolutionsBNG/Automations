from django.views.generic import TemplateView
from django.shortcuts import render
#from chartjs.views.lines import BaseLineChartView
from django.template.response import TemplateResponse
import logging
from .models import ModuleSettings


def get_actrbl_home(request, dashboard_code):
    try:
        log = logging.getLogger("actrbl")
        log.info("Loading Account Receivables Home Page")

        log.info("Loading Session Data for the current signed in User")
        dash_details_key = "dashboard" + "$" + dashboard_code
        dashboard_details = request.session.get(dash_details_key)

        dash_tag_key = "dashboardComponentTags$" + dashboard_code
        component_tags = request.session.get(dash_tag_key)

        if component_tags:

            dashboard_title = dashboard_details["dashboard_title"]
            dashboard_sub_title = dashboard_details["dashboard_sub_title"]

            dash_chart_key = "dashboardChartTags" + "$" + dashboard_code
            chart_api_tags = request.session.get(dash_chart_key)

            dash_table_key = "dashboardTableTags" + "$" + dashboard_code
            table_api_tags = request.session.get(dash_table_key)

            dash_table_containers_key = "dashboardTableContainerTags" + "$" + dashboard_code
            table_container_tags = request.session.get(dash_table_containers_key)

            dash_chart_containers_key = "dashboardChartContainerTags" + "$" + dashboard_code
            chart_container_tags = request.session.get(dash_chart_containers_key)

            common_scripts= request.session.get("common_scripts")

            context = {
                "component_tags": component_tags,
                "chart_api_tags": chart_api_tags,
                "dashboard_title": dashboard_title,
                "dashboard_sub_title": dashboard_sub_title,
                "table_api_tags": table_api_tags,
                "table_container_tags": table_container_tags,
                "chart_container_tags": chart_container_tags,
                "common_scripts": common_scripts
            }
        else:
            context = {
                "component_tags": "",
                "chart_api_tags": "",
                "dashboard_title": "No Dashboards defined for this KPI!!!!",
                "dashboard_sub_title": "Please contact your Product Team/Admin",
                "table_api_tags": "",
                "table_container_tags": "",
                "chart_container_tags": "",
                "common_scripts": ""
            }
            log.info(context)

        return TemplateResponse(request, 'actrbl_index.html', context)

       #return TemplateResponse(request, 'actrbl_discounted_invoices.html', {"output": None})
    except Exception as e:
        err_msg = "Error occurred in rendering the dashboard!!"
        err_description = str(e)

        errors = {"errors": {"level": "critical", "error_msg": err_msg, "error_description": err_description}}
        log.error(errors, exc_info=True)
        return TemplateResponse(request, 'actrbl_index.html',
                                {"dashboard_output": None, "widget_output": None,
                                 "chart_output": None, "table_output": None, "errors": errors})

def get_actrbl_sales_summary(request, dashboard_code):
    try:
        log = logging.getLogger("actrbl")
        log.info("Loading Account Receivables Sales Summary Page")

        log.info("Loading Session Data for the current signed in User")
        dash_details_key = "dashboard" + "$" + dashboard_code
        dashboard_details = request.session.get(dash_details_key)

        dash_tag_key = "dashboardComponentTags$" + dashboard_code
        component_tags = request.session.get(dash_tag_key)

        if component_tags:

            dashboard_title = dashboard_details["dashboard_title"]
            dashboard_sub_title = dashboard_details["dashboard_sub_title"]

            dash_chart_key = "dashboardChartTags" + "$" + dashboard_code
            chart_api_tags = request.session.get(dash_chart_key)

            dash_table_key = "dashboardTableTags" + "$" + dashboard_code
            table_api_tags = request.session.get(dash_table_key)

            dash_table_containers_key = "dashboardTableContainerTags" + "$" + dashboard_code
            table_container_tags = request.session.get(dash_table_containers_key)

            dash_chart_containers_key = "dashboardChartContainerTags" + "$" + dashboard_code
            chart_container_tags = request.session.get(dash_chart_containers_key)

            common_scripts= request.session.get("common_scripts")

            context = {
                "component_tags": component_tags,
                "chart_api_tags": chart_api_tags,
                "dashboard_title": dashboard_title,
                "dashboard_sub_title": dashboard_sub_title,
                "table_api_tags": table_api_tags,
                "table_container_tags": table_container_tags,
                "chart_container_tags": chart_container_tags,
                "common_scripts": common_scripts
            }
        else:
            context = {
                "component_tags": "",
                "chart_api_tags": "",
                "dashboard_title": "No Dashboards defined for this KPI!!!!",
                "dashboard_sub_title": "Please contact your Product Team/Admin",
                "table_api_tags": "",
                "table_container_tags": "",
                "chart_container_tags": "",
                "common_scripts": ""
            }
            log.info(context)

        return TemplateResponse(request, 'actrbl_sales_summary.html', context)

       #return TemplateResponse(request, 'actrbl_discounted_invoices.html', {"output": None})
    except Exception as e:
        err_msg = "Error occurred in rendering the dashboard!!"
        err_description = str(e)

        errors = {"errors": {"level": "critical", "error_msg": err_msg, "error_description": err_description}}
        log.error(errors, exc_info=True)
        return TemplateResponse(request, 'actrbl_sales_summary.html',
                                {"dashboard_output": None, "widget_output": None,
                                 "chart_output": None, "table_output": None, "errors": errors})

def get_actrbl_sales_exceptions(request, dashboard_code):
    try:
        log = logging.getLogger("actrbl")
        log.info("Loading Account Receivables Sales Exception Page")

        log.info("Loading Session Data for the current signed in User")
        dash_details_key = "dashboard" + "$" + dashboard_code
        dashboard_details = request.session.get(dash_details_key)

        dash_tag_key = "dashboardComponentTags$" + dashboard_code
        component_tags = request.session.get(dash_tag_key)

        if component_tags:

            dashboard_title = dashboard_details["dashboard_title"]
            dashboard_sub_title = dashboard_details["dashboard_sub_title"]

            dash_chart_key = "dashboardChartTags" + "$" + dashboard_code
            chart_api_tags = request.session.get(dash_chart_key)

            dash_table_key = "dashboardTableTags" + "$" + dashboard_code
            table_api_tags = request.session.get(dash_table_key)

            dash_table_containers_key = "dashboardTableContainerTags" + "$" + dashboard_code
            table_container_tags = request.session.get(dash_table_containers_key)

            dash_chart_containers_key = "dashboardChartContainerTags" + "$" + dashboard_code
            chart_container_tags = request.session.get(dash_chart_containers_key)

            common_scripts= request.session.get("common_scripts")

            context = {
                "component_tags": component_tags,
                "chart_api_tags": chart_api_tags,
                "dashboard_title": dashboard_title,
                "dashboard_sub_title": dashboard_sub_title,
                "table_api_tags": table_api_tags,
                "table_container_tags": table_container_tags,
                "chart_container_tags": chart_container_tags,
                "common_scripts": common_scripts
            }
        else:
            context = {
                "component_tags": "",
                "chart_api_tags": "",
                "dashboard_title": "No Dashboards defined for this KPI!!!!",
                "dashboard_sub_title": "Please contact your Product Team/Admin",
                "table_api_tags": "",
                "table_container_tags": "",
                "chart_container_tags": "",
                "common_scripts": ""
            }
            log.info(context)

        return TemplateResponse(request, 'actrbl_sales_exception.html', context)

       #return TemplateResponse(request, 'actrbl_discounted_invoices.html', {"output": None})
    except Exception as e:
        err_msg = "Error occurred in rendering the dashboard!!"
        err_description = str(e)

        errors = {"errors": {"level": "critical", "error_msg": err_msg, "error_description": err_description}}
        log.error(errors, exc_info=True)
        return TemplateResponse(request, 'actrbl_sales_exception.html',
                                {"dashboard_output": None, "widget_output": None,
                                 "chart_output": None, "table_output": None, "errors": errors})


def get_actrbl_sales_forecasts(request, dashboard_code):
    try:
        log = logging.getLogger("actrbl")
        log.info("Loading Account Receivables Sales forecast Page")

        log.info("Loading Session Data for the current signed in User")
        dash_details_key = "dashboard" + "$" + dashboard_code
        dashboard_details = request.session.get(dash_details_key)

        dash_tag_key = "dashboardComponentTags$" + dashboard_code
        component_tags = request.session.get(dash_tag_key)

        if component_tags:

            dashboard_title = dashboard_details["dashboard_title"]
            dashboard_sub_title = dashboard_details["dashboard_sub_title"]

            dash_chart_key = "dashboardChartTags" + "$" + dashboard_code
            chart_api_tags = request.session.get(dash_chart_key)

            dash_table_key = "dashboardTableTags" + "$" + dashboard_code
            table_api_tags = request.session.get(dash_table_key)

            dash_table_containers_key = "dashboardTableContainerTags" + "$" + dashboard_code
            table_container_tags = request.session.get(dash_table_containers_key)

            dash_chart_containers_key = "dashboardChartContainerTags" + "$" + dashboard_code
            chart_container_tags = request.session.get(dash_chart_containers_key)

            common_scripts = request.session.get("common_scripts")

            context = {
                "component_tags": component_tags,
                "chart_api_tags": chart_api_tags,
                "dashboard_title": dashboard_title,
                "dashboard_sub_title": dashboard_sub_title,
                "table_api_tags": table_api_tags,
                "table_container_tags": table_container_tags,
                "chart_container_tags": chart_container_tags,
                "common_scripts": common_scripts
            }
        else:
            context = {
                "component_tags": "",
                "chart_api_tags": "",
                "dashboard_title": "No Dashboards defined for this KPI!!!!",
                "dashboard_sub_title": "Please contact your Product Team/Admin",
                "table_api_tags": "",
                "table_container_tags": "",
                "chart_container_tags": "",
                "common_scripts": ""
            }
            log.info(context)

        return TemplateResponse(request, 'actrbl_sales_forecast.html', context)

        # return TemplateResponse(request, 'actrbl_discounted_invoices.html', {"output": None})
    except Exception as e:
        err_msg = "Error occurred in rendering the dashboard!!"
        err_description = str(e)

        errors = {"errors": {"level": "critical", "error_msg": err_msg, "error_description": err_description}}
        log.error(errors, exc_info=True)
        return TemplateResponse(request, 'actrbl_sales_forecast.html',
                                {"dashboard_output": None, "widget_output": None,
                                 "chart_output": None, "table_output": None, "errors": errors})


def get_actrbl_discounted_invoices(request, dashboard_code):
    try:
        log = logging.getLogger("actrbl")
        log.info("Loading Account Receivables Discounted Invoices Page")

        log.info("Loading Session Data for the current signed in User")
        dash_details_key = "dashboard" + "$" + dashboard_code
        dashboard_details = request.session.get(dash_details_key)

        dash_tag_key = "dashboardComponentTags$" + dashboard_code
        component_tags = request.session.get(dash_tag_key)

        if component_tags:

            dashboard_title = dashboard_details["dashboard_title"]
            dashboard_sub_title = dashboard_details["dashboard_sub_title"]

            dash_chart_key = "dashboardChartTags" + "$" + dashboard_code
            chart_api_tags = request.session.get(dash_chart_key)

            dash_table_key = "dashboardTableTags" + "$" + dashboard_code
            table_api_tags = request.session.get(dash_table_key)

            dash_table_containers_key = "dashboardTableContainerTags" + "$" + dashboard_code
            table_container_tags = request.session.get(dash_table_containers_key)

            dash_chart_containers_key = "dashboardChartContainerTags" + "$" + dashboard_code
            chart_container_tags = request.session.get(dash_chart_containers_key)

            common_scripts = request.session.get("common_scripts")

            context = {
                "component_tags": component_tags,
                "chart_api_tags": chart_api_tags,
                "dashboard_title": dashboard_title,
                "dashboard_sub_title": dashboard_sub_title,
                "table_api_tags": table_api_tags,
                "table_container_tags": table_container_tags,
                "chart_container_tags": chart_container_tags,
                "common_scripts": common_scripts
            }
        else:
            context = {
                "component_tags": "",
                "chart_api_tags": "",
                "dashboard_title": "No Dashboards defined for this KPI!!!!",
                "dashboard_sub_title": "Please contact your Product Team/Admin",
                "table_api_tags": "",
                "table_container_tags": "",
                "chart_container_tags": "",
                "common_scripts": ""
            }
            log.info(context)

        return TemplateResponse(request, 'actrbl_discounted_invoices.html', context)

        # return TemplateResponse(request, 'actrbl_discounted_invoices.html', {"output": None})
    except Exception as e:
        err_msg = "Error occurred in rendering the dashboard!!"
        err_description = str(e)

        errors = {"errors": {"level": "critical", "error_msg": err_msg, "error_description": err_description}}
        log.error(errors, exc_info=True)
        return TemplateResponse(request, 'actrbl_discounted_invoices.html',
                                {"dashboard_output": None, "widget_output": None,
                                 "chart_output": None, "table_output": None, "errors": errors})



def get_actrbl_sales_trends(request, dashboard_code):
    try:
        log = logging.getLogger("actrbl")
        log.info("Loading Account Receivables Home Page")

        log.info("Loading Session Data for the current signed in User")
        dash_details_key = "dashboard" + "$" + dashboard_code
        dashboard_details = request.session.get(dash_details_key)

        dash_tag_key = "dashboardComponentTags$" + dashboard_code
        component_tags = request.session.get(dash_tag_key)

        if component_tags:

            dashboard_title = dashboard_details["dashboard_title"]
            dashboard_sub_title = dashboard_details["dashboard_sub_title"]

            dash_chart_key = "dashboardChartTags" + "$" + dashboard_code
            chart_api_tags = request.session.get(dash_chart_key)

            dash_table_key = "dashboardTableTags" + "$" + dashboard_code
            table_api_tags = request.session.get(dash_table_key)

            dash_table_containers_key = "dashboardTableContainerTags" + "$" + dashboard_code
            table_container_tags = request.session.get(dash_table_containers_key)

            dash_chart_containers_key = "dashboardChartContainerTags" + "$" + dashboard_code
            chart_container_tags = request.session.get(dash_chart_containers_key)

            common_scripts= request.session.get("common_scripts")

            context = {
                "component_tags": component_tags,
                "chart_api_tags": chart_api_tags,
                "dashboard_title": dashboard_title,
                "dashboard_sub_title": dashboard_sub_title,
                "table_api_tags": table_api_tags,
                "table_container_tags": table_container_tags,
                "chart_container_tags": chart_container_tags,
                "common_scripts": common_scripts
            }
        else:
            context = {
                "component_tags": "",
                "chart_api_tags": "",
                "dashboard_title": "No Dashboards defined for this KPI!!!!",
                "dashboard_sub_title": "Please contact your Product Team/Admin",
                "table_api_tags": "",
                "table_container_tags": "",
                "chart_container_tags": "",
                "common_scripts": ""
            }
            log.info(context)

        return TemplateResponse(request, 'actrbl_sales_trends.html', context)

       #return TemplateResponse(request, 'actrbl_discounted_invoices.html', {"output": None})
    except Exception as e:
        err_msg = "Error occurred in rendering the dashboard!!"
        err_description = str(e)

        errors = {"errors": {"level": "critical", "error_msg": err_msg, "error_description": err_description}}
        log.error(errors, exc_info=True)
        return TemplateResponse(request, 'actrbl_sales_trends.html',
                                {"dashboard_output": None, "widget_output": None,
                                 "chart_output": None, "table_output": None, "errors": errors})



def get_actrbl_customer_collections(request, dashboard_code):
    try:
        log = logging.getLogger("actrbl")
        log.info("Loading Account Receivables - Customer Collections Home Page")

        log.info("Loading Session Data for the current signed in User")
        dash_details_key = "dashboard" + "$" + dashboard_code
        dashboard_details = request.session.get(dash_details_key)

        dash_tag_key = "dashboardComponentTags$" + dashboard_code
        component_tags = request.session.get(dash_tag_key)

        if component_tags:

            dashboard_title = dashboard_details["dashboard_title"]
            dashboard_sub_title = dashboard_details["dashboard_sub_title"]

            dash_chart_key = "dashboardChartTags" + "$" + dashboard_code
            chart_api_tags = request.session.get(dash_chart_key)

            dash_table_key = "dashboardTableTags" + "$" + dashboard_code
            table_api_tags = request.session.get(dash_table_key)

            dash_table_containers_key = "dashboardTableContainerTags" + "$" + dashboard_code
            table_container_tags = request.session.get(dash_table_containers_key)

            dash_chart_containers_key = "dashboardChartContainerTags" + "$" + dashboard_code
            chart_container_tags = request.session.get(dash_chart_containers_key)

            common_scripts= request.session.get("common_scripts")

            context = {
                "component_tags": component_tags,
                "chart_api_tags": chart_api_tags,
                "dashboard_title": dashboard_title,
                "dashboard_sub_title": dashboard_sub_title,
                "table_api_tags": table_api_tags,
                "table_container_tags": table_container_tags,
                "chart_container_tags": chart_container_tags,
                "common_scripts": common_scripts
            }
        else:
            context = {
                "component_tags": "",
                "chart_api_tags": "",
                "dashboard_title": "No Dashboards defined for this KPI!!!!",
                "dashboard_sub_title": "Please contact your Product Team/Admin",
                "table_api_tags": "",
                "table_container_tags": "",
                "chart_container_tags": "",
                "common_scripts": ""
            }
            log.info(context)

        return TemplateResponse(request, 'actrbl_customer_collections.html', context)

       #return TemplateResponse(request, 'actrbl_discounted_invoices.html', {"output": None})
    except Exception as e:
        err_msg = "Error occurred in rendering the dashboard!!"
        err_description = str(e)

        errors = {"errors": {"level": "critical", "error_msg": err_msg, "error_description": err_description}}
        log.error(errors, exc_info=True)
        return TemplateResponse(request, 'actrbl_customer_collections.html',
                                {"dashboard_output": None, "widget_output": None,
                                 "chart_output": None, "table_output": None, "errors": errors})

def get_actrbl_ageing_report(request, dashboard_code):
    try:
        log = logging.getLogger("actrbl")
        log.info("Loading Account Receivables - Ageing Report Home Page")

        log.info("Loading Session Data for the current signed in User")
        dash_details_key = "dashboard" + "$" + dashboard_code
        dashboard_details = request.session.get(dash_details_key)

        dash_tag_key = "dashboardComponentTags$" + dashboard_code
        component_tags = request.session.get(dash_tag_key)

        if component_tags:

            dashboard_title = dashboard_details["dashboard_title"]
            dashboard_sub_title = dashboard_details["dashboard_sub_title"]

            dash_chart_key = "dashboardChartTags" + "$" + dashboard_code
            chart_api_tags = request.session.get(dash_chart_key)

            dash_table_key = "dashboardTableTags" + "$" + dashboard_code
            table_api_tags = request.session.get(dash_table_key)

            dash_table_containers_key = "dashboardTableContainerTags" + "$" + dashboard_code
            table_container_tags = request.session.get(dash_table_containers_key)

            dash_chart_containers_key = "dashboardChartContainerTags" + "$" + dashboard_code
            chart_container_tags = request.session.get(dash_chart_containers_key)

            common_scripts= request.session.get("common_scripts")

            context = {
                "component_tags": component_tags,
                "chart_api_tags": chart_api_tags,
                "dashboard_title": dashboard_title,
                "dashboard_sub_title": dashboard_sub_title,
                "table_api_tags": table_api_tags,
                "table_container_tags": table_container_tags,
                "chart_container_tags": chart_container_tags,
                "common_scripts": common_scripts
            }
        else:
            context = {
                "component_tags": "",
                "chart_api_tags": "",
                "dashboard_title": "No Dashboards defined for this KPI!!!!",
                "dashboard_sub_title": "Please contact your Product Team/Admin",
                "table_api_tags": "",
                "table_container_tags": "",
                "chart_container_tags": "",
                "common_scripts": ""
            }
            log.info(context)

        return TemplateResponse(request, 'actrbl_ageing_report.html', context)

       #return TemplateResponse(request, 'actrbl_discounted_invoices.html', {"output": None})
    except Exception as e:
        err_msg = "Error occurred in rendering the dashboard!!"
        err_description = str(e)

        errors = {"errors": {"level": "critical", "error_msg": err_msg, "error_description": err_description}}
        log.error(errors, exc_info=True)
        return TemplateResponse(request, 'actrbl_ageing_report.html',
                                {"dashboard_output": None, "widget_output": None,
                                 "chart_output": None, "table_output": None, "errors": errors})

def get_actrbl_goods_invoiced_dispatch_comparision(request, dashboard_code):
    try:
        log = logging.getLogger("actrbl")
        log.info("Loading Account Receivables - Goods Invoiced Vs Dispatched Comparision Home Page")

        log.info("Loading Session Data for the current signed in User")
        dash_details_key = "dashboard" + "$" + dashboard_code
        dashboard_details = request.session.get(dash_details_key)

        dash_tag_key = "dashboardComponentTags$" + dashboard_code
        component_tags = request.session.get(dash_tag_key)

        if component_tags:

            dashboard_title = dashboard_details["dashboard_title"]
            dashboard_sub_title = dashboard_details["dashboard_sub_title"]

            dash_chart_key = "dashboardChartTags" + "$" + dashboard_code
            chart_api_tags = request.session.get(dash_chart_key)

            dash_table_key = "dashboardTableTags" + "$" + dashboard_code
            table_api_tags = request.session.get(dash_table_key)

            dash_table_containers_key = "dashboardTableContainerTags" + "$" + dashboard_code
            table_container_tags = request.session.get(dash_table_containers_key)

            dash_chart_containers_key = "dashboardChartContainerTags" + "$" + dashboard_code
            chart_container_tags = request.session.get(dash_chart_containers_key)

            common_scripts= request.session.get("common_scripts")

            context = {
                "component_tags": component_tags,
                "chart_api_tags": chart_api_tags,
                "dashboard_title": dashboard_title,
                "dashboard_sub_title": dashboard_sub_title,
                "table_api_tags": table_api_tags,
                "table_container_tags": table_container_tags,
                "chart_container_tags": chart_container_tags,
                "common_scripts": common_scripts
            }
        else:
            context = {
                "component_tags": "",
                "chart_api_tags": "",
                "dashboard_title": "No Dashboards defined for this KPI!!!!",
                "dashboard_sub_title": "Please contact your Product Team/Admin",
                "table_api_tags": "",
                "table_container_tags": "",
                "chart_container_tags": "",
                "common_scripts": ""
            }
            log.info(context)

        return TemplateResponse(request, 'actrbl_goods_invoiced_dispatch_comparision.html', context)

       #return TemplateResponse(request, 'actrbl_discounted_invoices.html', {"output": None})
    except Exception as e:
        err_msg = "Error occurred in rendering the dashboard!!"
        err_description = str(e)

        errors = {"errors": {"level": "critical", "error_msg": err_msg, "error_description": err_description}}
        log.error(errors, exc_info=True)
        return TemplateResponse(request, 'actrbl_goods_invoiced_dispatch_comparision.html',
                                {"dashboard_output": None, "widget_output": None,
                                 "chart_output": None, "table_output": None, "errors": errors})

def get_actrbl_customer_sales_vs_collections(request, dashboard_code):
    try:
        log = logging.getLogger("actrbl")
        log.info("Loading Account Receivables - Customer Sales Vs Collection Home Page")

        log.info("Loading Session Data for the current signed in User")
        dash_details_key = "dashboard" + "$" + dashboard_code
        dashboard_details = request.session.get(dash_details_key)

        dash_tag_key = "dashboardComponentTags$" + dashboard_code
        component_tags = request.session.get(dash_tag_key)

        if component_tags:

            dashboard_title = dashboard_details["dashboard_title"]
            dashboard_sub_title = dashboard_details["dashboard_sub_title"]

            dash_chart_key = "dashboardChartTags" + "$" + dashboard_code
            chart_api_tags = request.session.get(dash_chart_key)

            dash_table_key = "dashboardTableTags" + "$" + dashboard_code
            table_api_tags = request.session.get(dash_table_key)

            dash_table_containers_key = "dashboardTableContainerTags" + "$" + dashboard_code
            table_container_tags = request.session.get(dash_table_containers_key)

            dash_chart_containers_key = "dashboardChartContainerTags" + "$" + dashboard_code
            chart_container_tags = request.session.get(dash_chart_containers_key)

            common_scripts= request.session.get("common_scripts")

            context = {
                "component_tags": component_tags,
                "chart_api_tags": chart_api_tags,
                "dashboard_title": dashboard_title,
                "dashboard_sub_title": dashboard_sub_title,
                "table_api_tags": table_api_tags,
                "table_container_tags": table_container_tags,
                "chart_container_tags": chart_container_tags,
                "common_scripts": common_scripts
            }
        else:
            context = {
                "component_tags": "",
                "chart_api_tags": "",
                "dashboard_title": "No Dashboards defined for this KPI!!!!",
                "dashboard_sub_title": "Please contact your Product Team/Admin",
                "table_api_tags": "",
                "table_container_tags": "",
                "chart_container_tags": "",
                "common_scripts": ""
            }
            log.info(context)

        return TemplateResponse(request, 'actrbl_customer_sales_vs_collections.html', context)

       #return TemplateResponse(request, 'actrbl_discounted_invoices.html', {"output": None})
    except Exception as e:
        err_msg = "Error occurred in rendering the dashboard!!"
        err_description = str(e)

        errors = {"errors": {"level": "critical", "error_msg": err_msg, "error_description": err_description}}
        log.error(errors, exc_info=True)
        return TemplateResponse(request, 'actrbl_customer_sales_vs_collections.html',
                                {"dashboard_output": None, "widget_output": None,
                                 "chart_output": None, "table_output": None, "errors": errors})


def get_actrbl_customer_planned_vs_actuals(request, dashboard_code):
    try:
        log = logging.getLogger("actrbl")
        log.info("Loading Account Receivables - Collections Planed Vs Actuals Home Page")

        log.info("Loading Session Data for the current signed in User")
        dash_details_key = "dashboard" + "$" + dashboard_code
        dashboard_details = request.session.get(dash_details_key)

        dash_tag_key = "dashboardComponentTags$" + dashboard_code
        component_tags = request.session.get(dash_tag_key)

        if component_tags:

            dashboard_title = dashboard_details["dashboard_title"]
            dashboard_sub_title = dashboard_details["dashboard_sub_title"]

            dash_chart_key = "dashboardChartTags" + "$" + dashboard_code
            chart_api_tags = request.session.get(dash_chart_key)

            dash_table_key = "dashboardTableTags" + "$" + dashboard_code
            table_api_tags = request.session.get(dash_table_key)

            dash_table_containers_key = "dashboardTableContainerTags" + "$" + dashboard_code
            table_container_tags = request.session.get(dash_table_containers_key)

            dash_chart_containers_key = "dashboardChartContainerTags" + "$" + dashboard_code
            chart_container_tags = request.session.get(dash_chart_containers_key)

            common_scripts= request.session.get("common_scripts")

            context = {
                "component_tags": component_tags,
                "chart_api_tags": chart_api_tags,
                "dashboard_title": dashboard_title,
                "dashboard_sub_title": dashboard_sub_title,
                "table_api_tags": table_api_tags,
                "table_container_tags": table_container_tags,
                "chart_container_tags": chart_container_tags,
                "common_scripts": common_scripts
            }
        else:
            context = {
                "component_tags": "",
                "chart_api_tags": "",
                "dashboard_title": "No Dashboards defined for this KPI!!!!",
                "dashboard_sub_title": "Please contact your Product Team/Admin",
                "table_api_tags": "",
                "table_container_tags": "",
                "chart_container_tags": "",
                "common_scripts": ""
            }
            log.info(context)

        return TemplateResponse(request, 'actrbl_customer_planned_vs_actuals.html', context)

       #return TemplateResponse(request, 'actrbl_discounted_invoices.html', {"output": None})
    except Exception as e:
        err_msg = "Error occurred in rendering the dashboard!!"
        err_description = str(e)

        errors = {"errors": {"level": "critical", "error_msg": err_msg, "error_description": err_description}}
        log.error(errors, exc_info=True)
        return TemplateResponse(request, 'actrbl_customer_planned_vs_actuals.html',
                                {"dashboard_output": None, "widget_output": None,
                                 "chart_output": None, "table_output": None, "errors": errors})