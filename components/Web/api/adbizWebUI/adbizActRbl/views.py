from django.views.generic import TemplateView
from django.shortcuts import render
#from chartjs.views.lines import BaseLineChartView
from django.template.response import TemplateResponse
import logging
from .models import ModuleSettings

log = logging.getLogger("actrbl")

def get_actrbl_main(request, dashboard_code):
    try:
        log.info("Loading Account Receivables")

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
            user_details = request.session.get("user_details")
            run_time_details = request.session.get("run_time_details")

            context = {
                "component_tags": component_tags,
                "chart_api_tags": chart_api_tags,
                "dashboard_title": dashboard_title,
                "dashboard_sub_title": dashboard_sub_title,
                "table_api_tags": table_api_tags,
                "table_container_tags": table_container_tags,
                "chart_container_tags": chart_container_tags,
                "common_scripts": common_scripts,
                "user_details": user_details,
                "run_time_details": run_time_details
            }
        else:
            user_details = request.session.get("user_details")
            run_time_details = request.session.get("run_time_details")
            context = {
                "component_tags": "",
                "chart_api_tags": "",
                "dashboard_title": "No Dashboards defined for this KPI!!!!",
                "dashboard_sub_title": "Please contact your Product Team/Admin",
                "table_api_tags": "",
                "table_container_tags": "",
                "chart_container_tags": "",
                "common_scripts": "",
                "user_details": user_details,
                "run_time_details": ""
            }
        log.info(context)

        if dashboard_code == "836469cb-e5e2-4151-b285-784623615458@dtl.site.env.catalog.datamodel.dashboard":
            return TemplateResponse(request, 'actrbl_sales_summary.html', context)
        elif dashboard_code == "93f1ee8b-cae2-47aa-8fb1-95ded769a513@dtl.site.env.catalog.datamodel.dashboard":
            return TemplateResponse(request, 'actrbl_sales_forecast.html', context)
        elif dashboard_code == "54416a91-9d43-4f98-a69f-a1aa357a2fe6@dtl.site.env.catalog.datamodel.dashboard":
            return TemplateResponse(request, 'actrbl_sales_exception.html', context)
        elif dashboard_code == "4781f53b-e967-4eb8-bd06-b5c377d7645e@dtl.site.env.catalog.datamodel.dashboard":
            return TemplateResponse(request, 'actrbl_sales_trends.html', context)
        elif dashboard_code == "4c9fca79-1fad-4585-9c5c-36ec77327174@dtl.site.env.catalog.datamodel.dashboard":
            return TemplateResponse(request, 'actrbl_discounted_invoices.html', context)
        elif dashboard_code == "4625c091-47e0-4721-880e-d41228f43ff8@dtl.site.env.catalog.datamodel.dashboard":
            return TemplateResponse(request, 'actrbl_goods_invoiced_dispatch_comparision.html', context)
        elif dashboard_code == "c9145c2b-8ad2-4d3b-99e8-23dc4c93352d@dtl.site.env.catalog.datamodel.dashboard":
            return TemplateResponse(request, 'actrbl_ageing_report.html', context)
        elif dashboard_code == "8f5cb197-e3ed-4e59-9008-47c53a87b156@dtl.site.env.catalog.datamodel.dashboard":
            return TemplateResponse(request, 'actrbl_customer_planned_vs_actuals.html', context)
        elif dashboard_code == "e56aa9e6-aa9a-4109-96a5-e5492ef3fd8a@dtl.site.env.catalog.datamodel.dashboard":
            return TemplateResponse(request, 'actrbl_customer_collections.html', context)
        elif dashboard_code == "4ae1ca70-ee60-4f24-a2b1-f0d423fe24fd@dtl.site.env.catalog.datamodel.dashboard":
            return TemplateResponse(request, 'actrbl_customer_sales_vs_collections.html', context)
        elif dashboard_code == "f5eb26ab-7b49-46d1-a51c-492be476237b@dtl.site.env.catalog.datamodel.dashboard":
            return TemplateResponse(request, 'actrbl_blocked_customers.html', context)
        elif dashboard_code == "3b8e2566-4850-41e5-8bd2-aafcc38fe087@dtl.site.env.catalog.datamodel.dashboard":
            return TemplateResponse(request, 'actrbl_customer_sales_vs_credit_loss.html', context)



       #return TemplateResponse(request, 'actrbl_discounted_invoices.html', {"output": None})
    except Exception as e:
        err_msg = "Error occurred in rendering the dashboard!!"
        err_description = str(e)

        errors = {"errors": {"level": "critical", "error_msg": err_msg, "error_description": err_description}}
        log.error(errors, exc_info=True)
        return TemplateResponse(request, 'actrbl_sales_summary.html',
                                {"dashboard_output": None, "widget_output": None,
                                 "chart_output": None, "table_output": None, "errors": errors})

def get_actrbl_custom(request, dashboard_code, period_start_date, period_end_date):
    try:
        log = logging.getLogger("actrbl")
        log.info("Loading Account Receivables Sales Summary Page - Custom")

        request.session.get("run_time_details")["period_start_date"] = period_end_date
        request.session.get("run_time_details")["period_end_date"] = period_start_date

        if dashboard_code:
            return get_actrbl_main(request, dashboard_code)

    except Exception as e:
        err_msg = "Error occurred in rendering the dashboard!!"
        err_description = str(e)

        errors = {"errors": {"level": "critical", "error_msg": err_msg, "error_description": err_description}}
        log.error(errors, exc_info=True)
        return TemplateResponse(request, 'actrbl_sales_summary.html',
                                {"dashboard_output": None, "widget_output": None,
                                 "chart_output": None, "table_output": None, "errors": errors})



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

# def get_actrbl_sales_summary(request, dashboard_code):
#     try:
#         log = logging.getLogger("actrbl")
#         log.info("Loading Account Receivables Sales Summary Page")
#
#         log.info("Loading Session Data for the current signed in User")
#         dash_details_key = "dashboard" + "$" + dashboard_code
#         dashboard_details = request.session.get(dash_details_key)
#
#         dash_tag_key = "dashboardComponentTags$" + dashboard_code
#         log.info(dash_tag_key)
#         component_tags = request.session.get(dash_tag_key)
#
#         if component_tags:
#
#             dashboard_title = dashboard_details["dashboard_title"]
#             dashboard_sub_title = dashboard_details["dashboard_sub_title"]
#
#             dash_chart_key = "dashboardChartTags" + "$" + dashboard_code
#             chart_api_tags = request.session.get(dash_chart_key)
#
#             dash_table_key = "dashboardTableTags" + "$" + dashboard_code
#             table_api_tags = request.session.get(dash_table_key)
#
#             dash_table_containers_key = "dashboardTableContainerTags" + "$" + dashboard_code
#             table_container_tags = request.session.get(dash_table_containers_key)
#
#             dash_chart_containers_key = "dashboardChartContainerTags" + "$" + dashboard_code
#             chart_container_tags = request.session.get(dash_chart_containers_key)
#
#             common_scripts= request.session.get("common_scripts")
#
#             user_details = request.session.get("user_details")
#
#             run_time_details = request.session.get("run_time_details")
#
#             context = {
#                 "component_tags": component_tags,
#                 "chart_api_tags": chart_api_tags,
#                 "dashboard_title": dashboard_title,
#                 "dashboard_sub_title": dashboard_sub_title,
#                 "table_api_tags": table_api_tags,
#                 "table_container_tags": table_container_tags,
#                 "chart_container_tags": chart_container_tags,
#                 "common_scripts": common_scripts,
#                 "user_details": user_details,
#                 "run_time_details": run_time_details
#             }
#         else:
#             user_details = request.session.get("user_details")
#
#             run_time_details = request.session.get("run_time_details")
#             context = {
#                 "component_tags": "",
#                 "chart_api_tags": "",
#                 "dashboard_title": "No Dashboards defined for this KPI!!!!",
#                 "dashboard_sub_title": "Please contact your Product Team/Admin",
#                 "table_api_tags": "",
#                 "table_container_tags": "",
#                 "chart_container_tags": "",
#                 "common_scripts": "",
#                 "user_details": user_details,
#                 "run_time_details": run_time_details
#             }
#             log.info(context)
#
#         return TemplateResponse(request, 'actrbl_sales_summary.html', context)
#
#        #return TemplateResponse(request, 'actrbl_discounted_invoices.html', {"output": None})
#     except Exception as e:
#         err_msg = "Error occurred in rendering the dashboard!!"
#         err_description = str(e)
#
#         errors = {"errors": {"level": "critical", "error_msg": err_msg, "error_description": err_description}}
#         log.error(errors, exc_info=True)
#         return TemplateResponse(request, 'actrbl_sales_summary.html',
#                                 {"dashboard_output": None, "widget_output": None,
#                                  "chart_output": None, "table_output": None, "errors": errors})
#
# def get_actrbl_sales_summary_custom(request, dashboard_code, period_start_date, period_end_date):
#     try:
#         log = logging.getLogger("actrbl")
#         log.info("Loading Account Receivables Sales Summary Page - Custom")
#
#         request.session.get("run_time_details")["period_start_date"] = period_end_date
#         request.session.get("run_time_details")["period_end_date"] = period_start_date
#
#         log.info("Run Time Details")
#         log.info(request.session.get("run_time_details"))
#
#         log.info("Loading Session Data for the current signed in User")
#         dash_details_key = "dashboard" + "$" + dashboard_code
#         dashboard_details = request.session.get(dash_details_key)
#
#         dash_tag_key = "dashboardComponentTags$" + dashboard_code
#         component_tags = request.session.get(dash_tag_key)
#
#         if component_tags:
#
#             dashboard_title = dashboard_details["dashboard_title"]
#             dashboard_sub_title = dashboard_details["dashboard_sub_title"]
#
#             dash_chart_key = "dashboardChartTags" + "$" + dashboard_code
#             chart_api_tags = request.session.get(dash_chart_key)
#
#             dash_table_key = "dashboardTableTags" + "$" + dashboard_code
#             table_api_tags = request.session.get(dash_table_key)
#
#             dash_table_containers_key = "dashboardTableContainerTags" + "$" + dashboard_code
#             table_container_tags = request.session.get(dash_table_containers_key)
#
#             dash_chart_containers_key = "dashboardChartContainerTags" + "$" + dashboard_code
#             chart_container_tags = request.session.get(dash_chart_containers_key)
#
#             common_scripts= request.session.get("common_scripts")
#
#             user_details = request.session.get("user_details")
#
#             run_time_details = request.session.get("run_time_details")
#
#             context = {
#                 "component_tags": component_tags,
#                 "chart_api_tags": chart_api_tags,
#                 "dashboard_title": dashboard_title,
#                 "dashboard_sub_title": dashboard_sub_title,
#                 "table_api_tags": table_api_tags,
#                 "table_container_tags": table_container_tags,
#                 "chart_container_tags": chart_container_tags,
#                 "common_scripts": common_scripts,
#                 "user_details": user_details,
#                 "run_time_details": run_time_details
#             }
#         else:
#             request.session.get("run_time_details")["period_start_date"] = period_end_date
#             request.session.get("run_time_details")["period_end_date"] = period_start_date
#
#             user_details = request.session.get("user_details")
#
#             run_time_details = request.session.get("run_time_details")
#
#             context = {
#                 "component_tags": "",
#                 "chart_api_tags": "",
#                 "dashboard_title": "No Dashboards defined for this KPI!!!!",
#                 "dashboard_sub_title": "Please contact your Product Team/Admin",
#                 "table_api_tags": "",
#                 "table_container_tags": "",
#                 "chart_container_tags": "",
#                 "common_scripts": "",
#                 "user_details": user_details,
#                 "run_time_details": run_time_details
#             }
#             log.info(context)
#
#         return TemplateResponse(request, 'actrbl_sales_summary.html', context)
#
#     except Exception as e:
#         err_msg = "Error occurred in rendering the dashboard!!"
#         err_description = str(e)
#
#         errors = {"errors": {"level": "critical", "error_msg": err_msg, "error_description": err_description}}
#         log.error(errors, exc_info=True)
#         return TemplateResponse(request, 'actrbl_sales_summary.html',
#                                 {"dashboard_output": None, "widget_output": None,
#                                  "chart_output": None, "table_output": None, "errors": errors})
#
#
# def get_actrbl_sales_exceptions(request, dashboard_code, start_date, end_date):
#     try:
#         log = logging.getLogger("actrbl")
#         log.info("Loading Account Receivables Sales Exception Page")
#
#         log.info("Loading Session Data for the current signed in User")
#         dash_details_key = "dashboard" + "$" + dashboard_code
#         dashboard_details = request.session.get(dash_details_key)
#
#         dash_tag_key = "dashboardComponentTags$" + dashboard_code
#         component_tags = request.session.get(dash_tag_key)
#
#         if component_tags:
#
#             dashboard_title = dashboard_details["dashboard_title"]
#             dashboard_sub_title = dashboard_details["dashboard_sub_title"]
#
#             dash_chart_key = "dashboardChartTags" + "$" + dashboard_code
#             chart_api_tags = request.session.get(dash_chart_key)
#
#             dash_table_key = "dashboardTableTags" + "$" + dashboard_code
#             table_api_tags = request.session.get(dash_table_key)
#
#             dash_table_containers_key = "dashboardTableContainerTags" + "$" + dashboard_code
#             table_container_tags = request.session.get(dash_table_containers_key)
#
#             dash_chart_containers_key = "dashboardChartContainerTags" + "$" + dashboard_code
#             chart_container_tags = request.session.get(dash_chart_containers_key)
#
#             common_scripts= request.session.get("common_scripts")
#
#             # user_session_tags = request.session.get("user_session")  {"user_session_id": ', "user_full_name": , "period_start_date": "" }
#             context = {
#                 "component_tags": component_tags,
#                 "chart_api_tags": chart_api_tags,
#                 "dashboard_title": dashboard_title,
#                 "dashboard_sub_title": dashboard_sub_title,
#                 "table_api_tags": table_api_tags,
#                 "table_container_tags": table_container_tags,
#                 "chart_container_tags": chart_container_tags,
#                 "common_scripts": common_scripts
#                 # "user_session_tags": user_session_tags
#             }
#         else:
#             context = {
#                 "component_tags": "",
#                 "chart_api_tags": "",
#                 "dashboard_title": "No Dashboards defined for this KPI!!!!",
#                 "dashboard_sub_title": "Please contact your Product Team/Admin",
#                 "table_api_tags": "",
#                 "table_container_tags": "",
#                 "chart_container_tags": "",
#                 "common_scripts": ""
#             }
#             log.info(context)
#
#         return TemplateResponse(request, 'actrbl_sales_exception.html', context)
#
#        #return TemplateResponse(request, 'actrbl_discounted_invoices.html', {"output": None})
#     except Exception as e:
#         err_msg = "Error occurred in rendering the dashboard!!"
#         err_description = str(e)
#
#         errors = {"errors": {"level": "critical", "error_msg": err_msg, "error_description": err_description}}
#         log.error(errors, exc_info=True)
#         return TemplateResponse(request, 'actrbl_sales_exception.html',
#                                 {"dashboard_output": None, "widget_output": None,
#                                  "chart_output": None, "table_output": None, "errors": errors})
#
#
# def get_actrbl_sales_forecasts(request, dashboard_code):
#     try:
#         log = logging.getLogger("actrbl")
#         log.info("Loading Account Receivables Sales forecast Page")
#
#         log.info("Loading Session Data for the current signed in User")
#         dash_details_key = "dashboard" + "$" + dashboard_code
#         dashboard_details = request.session.get(dash_details_key)
#
#         dash_tag_key = "dashboardComponentTags$" + dashboard_code
#         component_tags = request.session.get(dash_tag_key)
#
#         if component_tags:
#
#             dashboard_title = dashboard_details["dashboard_title"]
#             dashboard_sub_title = dashboard_details["dashboard_sub_title"]
#
#             dash_chart_key = "dashboardChartTags" + "$" + dashboard_code
#             chart_api_tags = request.session.get(dash_chart_key)
#
#             dash_table_key = "dashboardTableTags" + "$" + dashboard_code
#             table_api_tags = request.session.get(dash_table_key)
#
#             dash_table_containers_key = "dashboardTableContainerTags" + "$" + dashboard_code
#             table_container_tags = request.session.get(dash_table_containers_key)
#
#             dash_chart_containers_key = "dashboardChartContainerTags" + "$" + dashboard_code
#             chart_container_tags = request.session.get(dash_chart_containers_key)
#
#             common_scripts = request.session.get("common_scripts")
#
#             context = {
#                 "component_tags": component_tags,
#                 "chart_api_tags": chart_api_tags,
#                 "dashboard_title": dashboard_title,
#                 "dashboard_sub_title": dashboard_sub_title,
#                 "table_api_tags": table_api_tags,
#                 "table_container_tags": table_container_tags,
#                 "chart_container_tags": chart_container_tags,
#                 "common_scripts": common_scripts
#             }
#         else:
#             context = {
#                 "component_tags": "",
#                 "chart_api_tags": "",
#                 "dashboard_title": "No Dashboards defined for this KPI!!!!",
#                 "dashboard_sub_title": "Please contact your Product Team/Admin",
#                 "table_api_tags": "",
#                 "table_container_tags": "",
#                 "chart_container_tags": "",
#                 "common_scripts": ""
#             }
#             log.info(context)
#
#         return TemplateResponse(request, 'actrbl_sales_forecast.html', context)
#
#         # return TemplateResponse(request, 'actrbl_discounted_invoices.html', {"output": None})
#     except Exception as e:
#         err_msg = "Error occurred in rendering the dashboard!!"
#         err_description = str(e)
#
#         errors = {"errors": {"level": "critical", "error_msg": err_msg, "error_description": err_description}}
#         log.error(errors, exc_info=True)
#         return TemplateResponse(request, 'actrbl_sales_forecast.html',
#                                 {"dashboard_output": None, "widget_output": None,
#                                  "chart_output": None, "table_output": None, "errors": errors})
#
#
# def get_actrbl_discounted_invoices(request, dashboard_code):
#     try:
#         log = logging.getLogger("actrbl")
#         log.info("Loading Account Receivables Discounted Invoices Page")
#
#         log.info("Loading Session Data for the current signed in User")
#         dash_details_key = "dashboard" + "$" + dashboard_code
#         dashboard_details = request.session.get(dash_details_key)
#
#         dash_tag_key = "dashboardComponentTags$" + dashboard_code
#         component_tags = request.session.get(dash_tag_key)
#
#         if component_tags:
#
#             dashboard_title = dashboard_details["dashboard_title"]
#             dashboard_sub_title = dashboard_details["dashboard_sub_title"]
#
#             dash_chart_key = "dashboardChartTags" + "$" + dashboard_code
#             chart_api_tags = request.session.get(dash_chart_key)
#
#             dash_table_key = "dashboardTableTags" + "$" + dashboard_code
#             table_api_tags = request.session.get(dash_table_key)
#
#             dash_table_containers_key = "dashboardTableContainerTags" + "$" + dashboard_code
#             table_container_tags = request.session.get(dash_table_containers_key)
#
#             dash_chart_containers_key = "dashboardChartContainerTags" + "$" + dashboard_code
#             chart_container_tags = request.session.get(dash_chart_containers_key)
#
#             common_scripts = request.session.get("common_scripts")
#
#             context = {
#                 "component_tags": component_tags,
#                 "chart_api_tags": chart_api_tags,
#                 "dashboard_title": dashboard_title,
#                 "dashboard_sub_title": dashboard_sub_title,
#                 "table_api_tags": table_api_tags,
#                 "table_container_tags": table_container_tags,
#                 "chart_container_tags": chart_container_tags,
#                 "common_scripts": common_scripts
#             }
#         else:
#             context = {
#                 "component_tags": "",
#                 "chart_api_tags": "",
#                 "dashboard_title": "No Dashboards defined for this KPI!!!!",
#                 "dashboard_sub_title": "Please contact your Product Team/Admin",
#                 "table_api_tags": "",
#                 "table_container_tags": "",
#                 "chart_container_tags": "",
#                 "common_scripts": ""
#             }
#             log.info(context)
#
#         return TemplateResponse(request, 'actrbl_discounted_invoices.html', context)
#
#         # return TemplateResponse(request, 'actrbl_discounted_invoices.html', {"output": None})
#     except Exception as e:
#         err_msg = "Error occurred in rendering the dashboard!!"
#         err_description = str(e)
#
#         errors = {"errors": {"level": "critical", "error_msg": err_msg, "error_description": err_description}}
#         log.error(errors, exc_info=True)
#         return TemplateResponse(request, 'actrbl_discounted_invoices.html',
#                                 {"dashboard_output": None, "widget_output": None,
#                                  "chart_output": None, "table_output": None, "errors": errors})
#
#
#
# def get_actrbl_sales_trends(request, dashboard_code):
#     try:
#         log = logging.getLogger("actrbl")
#         log.info("Loading Account Receivables Home Page")
#
#         log.info("Loading Session Data for the current signed in User")
#         dash_details_key = "dashboard" + "$" + dashboard_code
#         dashboard_details = request.session.get(dash_details_key)
#
#         dash_tag_key = "dashboardComponentTags$" + dashboard_code
#         component_tags = request.session.get(dash_tag_key)
#
#         if component_tags:
#
#             dashboard_title = dashboard_details["dashboard_title"]
#             dashboard_sub_title = dashboard_details["dashboard_sub_title"]
#
#             dash_chart_key = "dashboardChartTags" + "$" + dashboard_code
#             chart_api_tags = request.session.get(dash_chart_key)
#
#             dash_table_key = "dashboardTableTags" + "$" + dashboard_code
#             table_api_tags = request.session.get(dash_table_key)
#
#             dash_table_containers_key = "dashboardTableContainerTags" + "$" + dashboard_code
#             table_container_tags = request.session.get(dash_table_containers_key)
#
#             dash_chart_containers_key = "dashboardChartContainerTags" + "$" + dashboard_code
#             chart_container_tags = request.session.get(dash_chart_containers_key)
#
#             common_scripts= request.session.get("common_scripts")
#
#             context = {
#                 "component_tags": component_tags,
#                 "chart_api_tags": chart_api_tags,
#                 "dashboard_title": dashboard_title,
#                 "dashboard_sub_title": dashboard_sub_title,
#                 "table_api_tags": table_api_tags,
#                 "table_container_tags": table_container_tags,
#                 "chart_container_tags": chart_container_tags,
#                 "common_scripts": common_scripts
#             }
#         else:
#             context = {
#                 "component_tags": "",
#                 "chart_api_tags": "",
#                 "dashboard_title": "No Dashboards defined for this KPI!!!!",
#                 "dashboard_sub_title": "Please contact your Product Team/Admin",
#                 "table_api_tags": "",
#                 "table_container_tags": "",
#                 "chart_container_tags": "",
#                 "common_scripts": ""
#             }
#             log.info(context)
#
#         return TemplateResponse(request, 'actrbl_sales_trends.html', context)
#
#        #return TemplateResponse(request, 'actrbl_discounted_invoices.html', {"output": None})
#     except Exception as e:
#         err_msg = "Error occurred in rendering the dashboard!!"
#         err_description = str(e)
#
#         errors = {"errors": {"level": "critical", "error_msg": err_msg, "error_description": err_description}}
#         log.error(errors, exc_info=True)
#         return TemplateResponse(request, 'actrbl_sales_trends.html',
#                                 {"dashboard_output": None, "widget_output": None,
#                                  "chart_output": None, "table_output": None, "errors": errors})
#
#
#
# def get_actrbl_customer_collections(request, dashboard_code):
#     try:
#         log = logging.getLogger("actrbl")
#         log.info("Loading Account Receivables - Customer Collections Home Page")
#
#         log.info("Loading Session Data for the current signed in User")
#         dash_details_key = "dashboard" + "$" + dashboard_code
#         dashboard_details = request.session.get(dash_details_key)
#
#         dash_tag_key = "dashboardComponentTags$" + dashboard_code
#         component_tags = request.session.get(dash_tag_key)
#
#         if component_tags:
#
#             dashboard_title = dashboard_details["dashboard_title"]
#             dashboard_sub_title = dashboard_details["dashboard_sub_title"]
#
#             dash_chart_key = "dashboardChartTags" + "$" + dashboard_code
#             chart_api_tags = request.session.get(dash_chart_key)
#
#             dash_table_key = "dashboardTableTags" + "$" + dashboard_code
#             table_api_tags = request.session.get(dash_table_key)
#
#             dash_table_containers_key = "dashboardTableContainerTags" + "$" + dashboard_code
#             table_container_tags = request.session.get(dash_table_containers_key)
#
#             dash_chart_containers_key = "dashboardChartContainerTags" + "$" + dashboard_code
#             chart_container_tags = request.session.get(dash_chart_containers_key)
#
#             common_scripts= request.session.get("common_scripts")
#
#             context = {
#                 "component_tags": component_tags,
#                 "chart_api_tags": chart_api_tags,
#                 "dashboard_title": dashboard_title,
#                 "dashboard_sub_title": dashboard_sub_title,
#                 "table_api_tags": table_api_tags,
#                 "table_container_tags": table_container_tags,
#                 "chart_container_tags": chart_container_tags,
#                 "common_scripts": common_scripts
#             }
#         else:
#             context = {
#                 "component_tags": "",
#                 "chart_api_tags": "",
#                 "dashboard_title": "No Dashboards defined for this KPI!!!!",
#                 "dashboard_sub_title": "Please contact your Product Team/Admin",
#                 "table_api_tags": "",
#                 "table_container_tags": "",
#                 "chart_container_tags": "",
#                 "common_scripts": ""
#             }
#             log.info(context)
#
#         return TemplateResponse(request, 'actrbl_customer_collections.html', context)
#
#        #return TemplateResponse(request, 'actrbl_discounted_invoices.html', {"output": None})
#     except Exception as e:
#         err_msg = "Error occurred in rendering the dashboard!!"
#         err_description = str(e)
#
#         errors = {"errors": {"level": "critical", "error_msg": err_msg, "error_description": err_description}}
#         log.error(errors, exc_info=True)
#         return TemplateResponse(request, 'actrbl_customer_collections.html',
#                                 {"dashboard_output": None, "widget_output": None,
#                                  "chart_output": None, "table_output": None, "errors": errors})
#
# def get_actrbl_ageing_report(request, dashboard_code):
#     try:
#         log = logging.getLogger("actrbl")
#         log.info("Loading Account Receivables - Ageing Report Home Page")
#
#         user_details = request.session.get("user_details")
#         run_time_details = request.session.get("run_time_details")
#
#
#         log.info("Loading Session Data for the current signed in User")
#         dash_details_key = "dashboard" + "$" + dashboard_code
#         dashboard_details = request.session.get(dash_details_key)
#
#         dash_tag_key = "dashboardComponentTags$" + dashboard_code
#         component_tags = request.session.get(dash_tag_key)
#
#         if component_tags:
#
#             dashboard_title = dashboard_details["dashboard_title"]
#             dashboard_sub_title = dashboard_details["dashboard_sub_title"]
#
#             dash_chart_key = "dashboardChartTags" + "$" + dashboard_code
#             chart_api_tags = request.session.get(dash_chart_key)
#
#             dash_table_key = "dashboardTableTags" + "$" + dashboard_code
#             table_api_tags = request.session.get(dash_table_key)
#
#             dash_table_containers_key = "dashboardTableContainerTags" + "$" + dashboard_code
#             table_container_tags = request.session.get(dash_table_containers_key)
#
#             dash_chart_containers_key = "dashboardChartContainerTags" + "$" + dashboard_code
#             chart_container_tags = request.session.get(dash_chart_containers_key)
#
#             common_scripts= request.session.get("common_scripts")
#
#
#             context = {
#                 "component_tags": component_tags,
#                 "chart_api_tags": chart_api_tags,
#                 "dashboard_title": dashboard_title,
#                 "dashboard_sub_title": dashboard_sub_title,
#                 "table_api_tags": table_api_tags,
#                 "table_container_tags": table_container_tags,
#                 "chart_container_tags": chart_container_tags,
#                 "common_scripts": common_scripts,
#                 "user_details": user_details,
#                 "run_time_details": run_time_details
#             }
#
#         else:
#
#             context = {
#                 "component_tags": "",
#                 "chart_api_tags": "",
#                 "dashboard_title": "No Dashboards defined for this KPI!!!!",
#                 "dashboard_sub_title": "Please contact your Product Team/Admin",
#                 "table_api_tags": "",
#                 "table_container_tags": "",
#                 "chart_container_tags": "",
#                 "common_scripts": "",
#                 "user_details": user_details,
#                 "run_time_details": ""
#             }
#             log.info(context)
#             print(context)
#
#         return TemplateResponse(request, 'actrbl_ageing_report.html', context)
#
#        #return TemplateResponse(request, 'actrbl_discounted_invoices.html', {"output": None})
#     except Exception as e:
#         err_msg = "Error occurred in rendering the dashboard!!"
#         err_description = str(e)
#
#         errors = {"errors": {"level": "critical", "error_msg": err_msg, "error_description": err_description}}
#         log.error(errors, exc_info=True)
#         return TemplateResponse(request, 'actrbl_ageing_report.html',
#                                 {"dashboard_output": None, "widget_output": None,
#                                  "chart_output": None, "table_output": None, "errors": errors})
#
# def get_actrbl_ageing_report_custom(request, dashboard_code, period_start_date, period_end_date):
#     try:
#         log = logging.getLogger("actrbl")
#         log.info("Loading Account Receivables - Ageing Report Home Page Custom")
#
#         request.session.get("run_time_details")["period_start_date"] = period_end_date
#         request.session.get("run_time_details")["period_end_date"] = period_start_date
#
#         log.info("Run Time Details")
#         log.info(request.session.get("run_time_details"))
#
#         return get_actrbl_ageing_report(request, dashboard_code)
#
#
#     except Exception as e:
#         err_msg = "Error occurred in rendering the dashboard!!"
#         err_description = str(e)
#
#         errors = {"errors": {"level": "critical", "error_msg": err_msg, "error_description": err_description}}
#         log.error(errors, exc_info=True)
#         return TemplateResponse(request, 'actrbl_ageing_report.html',
#                                 {"dashboard_output": None, "widget_output": None,
#                                  "chart_output": None, "table_output": None, "errors": errors})
#
# def get_actrbl_goods_invoiced_dispatch_comparision(request, dashboard_code):
#     try:
#         log = logging.getLogger("actrbl")
#         log.info("Loading Account Receivables - Goods Invoiced Vs Dispatched Comparision Home Page")
#
#         log.info("Loading Session Data for the current signed in User")
#         dash_details_key = "dashboard" + "$" + dashboard_code
#         dashboard_details = request.session.get(dash_details_key)
#
#         dash_tag_key = "dashboardComponentTags$" + dashboard_code
#         component_tags = request.session.get(dash_tag_key)
#
#         if component_tags:
#
#             dashboard_title = dashboard_details["dashboard_title"]
#             dashboard_sub_title = dashboard_details["dashboard_sub_title"]
#
#             dash_chart_key = "dashboardChartTags" + "$" + dashboard_code
#             chart_api_tags = request.session.get(dash_chart_key)
#
#             dash_table_key = "dashboardTableTags" + "$" + dashboard_code
#             table_api_tags = request.session.get(dash_table_key)
#
#             dash_table_containers_key = "dashboardTableContainerTags" + "$" + dashboard_code
#             table_container_tags = request.session.get(dash_table_containers_key)
#
#             dash_chart_containers_key = "dashboardChartContainerTags" + "$" + dashboard_code
#             chart_container_tags = request.session.get(dash_chart_containers_key)
#
#             common_scripts= request.session.get("common_scripts")
#
#             context = {
#                 "component_tags": component_tags,
#                 "chart_api_tags": chart_api_tags,
#                 "dashboard_title": dashboard_title,
#                 "dashboard_sub_title": dashboard_sub_title,
#                 "table_api_tags": table_api_tags,
#                 "table_container_tags": table_container_tags,
#                 "chart_container_tags": chart_container_tags,
#                 "common_scripts": common_scripts
#             }
#         else:
#             context = {
#                 "component_tags": "",
#                 "chart_api_tags": "",
#                 "dashboard_title": "No Dashboards defined for this KPI!!!!",
#                 "dashboard_sub_title": "Please contact your Product Team/Admin",
#                 "table_api_tags": "",
#                 "table_container_tags": "",
#                 "chart_container_tags": "",
#                 "common_scripts": ""
#             }
#             log.info(context)
#
#         return TemplateResponse(request, 'actrbl_goods_invoiced_dispatch_comparision.html', context)
#
#        #return TemplateResponse(request, 'actrbl_discounted_invoices.html', {"output": None})
#     except Exception as e:
#         err_msg = "Error occurred in rendering the dashboard!!"
#         err_description = str(e)
#
#         errors = {"errors": {"level": "critical", "error_msg": err_msg, "error_description": err_description}}
#         log.error(errors, exc_info=True)
#         return TemplateResponse(request, 'actrbl_goods_invoiced_dispatch_comparision.html',
#                                 {"dashboard_output": None, "widget_output": None,
#                                  "chart_output": None, "table_output": None, "errors": errors})
#
# def get_actrbl_customer_sales_vs_collections(request, dashboard_code):
#     try:
#         log = logging.getLogger("actrbl")
#         log.info("Loading Account Receivables - Customer Sales Vs Collection Home Page")
#
#         log.info("Loading Session Data for the current signed in User")
#         dash_details_key = "dashboard" + "$" + dashboard_code
#         dashboard_details = request.session.get(dash_details_key)
#
#         dash_tag_key = "dashboardComponentTags$" + dashboard_code
#         component_tags = request.session.get(dash_tag_key)
#
#         if component_tags:
#
#             dashboard_title = dashboard_details["dashboard_title"]
#             dashboard_sub_title = dashboard_details["dashboard_sub_title"]
#
#             dash_chart_key = "dashboardChartTags" + "$" + dashboard_code
#             chart_api_tags = request.session.get(dash_chart_key)
#
#             dash_table_key = "dashboardTableTags" + "$" + dashboard_code
#             table_api_tags = request.session.get(dash_table_key)
#
#             dash_table_containers_key = "dashboardTableContainerTags" + "$" + dashboard_code
#             table_container_tags = request.session.get(dash_table_containers_key)
#
#             dash_chart_containers_key = "dashboardChartContainerTags" + "$" + dashboard_code
#             chart_container_tags = request.session.get(dash_chart_containers_key)
#
#             common_scripts= request.session.get("common_scripts")
#
#             context = {
#                 "component_tags": component_tags,
#                 "chart_api_tags": chart_api_tags,
#                 "dashboard_title": dashboard_title,
#                 "dashboard_sub_title": dashboard_sub_title,
#                 "table_api_tags": table_api_tags,
#                 "table_container_tags": table_container_tags,
#                 "chart_container_tags": chart_container_tags,
#                 "common_scripts": common_scripts
#             }
#         else:
#             context = {
#                 "component_tags": "",
#                 "chart_api_tags": "",
#                 "dashboard_title": "No Dashboards defined for this KPI!!!!",
#                 "dashboard_sub_title": "Please contact your Product Team/Admin",
#                 "table_api_tags": "",
#                 "table_container_tags": "",
#                 "chart_container_tags": "",
#                 "common_scripts": ""
#             }
#             log.info(context)
#
#         return TemplateResponse(request, 'actrbl_customer_sales_vs_collections.html', context)
#
#        #return TemplateResponse(request, 'actrbl_discounted_invoices.html', {"output": None})
#     except Exception as e:
#         err_msg = "Error occurred in rendering the dashboard!!"
#         err_description = str(e)
#
#         errors = {"errors": {"level": "critical", "error_msg": err_msg, "error_description": err_description}}
#         log.error(errors, exc_info=True)
#         return TemplateResponse(request, 'actrbl_customer_sales_vs_collections.html',
#                                 {"dashboard_output": None, "widget_output": None,
#                                  "chart_output": None, "table_output": None, "errors": errors})
#
#
# def get_actrbl_customer_planned_vs_actuals(request, dashboard_code):
#     try:
#         log = logging.getLogger("actrbl")
#         log.info("Loading Account Receivables - Collections Planed Vs Actuals Home Page")
#
#         log.info("Loading Session Data for the current signed in User")
#         dash_details_key = "dashboard" + "$" + dashboard_code
#         dashboard_details = request.session.get(dash_details_key)
#
#         dash_tag_key = "dashboardComponentTags$" + dashboard_code
#         component_tags = request.session.get(dash_tag_key)
#
#         if component_tags:
#
#             dashboard_title = dashboard_details["dashboard_title"]
#             dashboard_sub_title = dashboard_details["dashboard_sub_title"]
#
#             dash_chart_key = "dashboardChartTags" + "$" + dashboard_code
#             chart_api_tags = request.session.get(dash_chart_key)
#
#             dash_table_key = "dashboardTableTags" + "$" + dashboard_code
#             table_api_tags = request.session.get(dash_table_key)
#
#             dash_table_containers_key = "dashboardTableContainerTags" + "$" + dashboard_code
#             table_container_tags = request.session.get(dash_table_containers_key)
#
#             dash_chart_containers_key = "dashboardChartContainerTags" + "$" + dashboard_code
#             chart_container_tags = request.session.get(dash_chart_containers_key)
#
#             common_scripts= request.session.get("common_scripts")
#
#             context = {
#                 "component_tags": component_tags,
#                 "chart_api_tags": chart_api_tags,
#                 "dashboard_title": dashboard_title,
#                 "dashboard_sub_title": dashboard_sub_title,
#                 "table_api_tags": table_api_tags,
#                 "table_container_tags": table_container_tags,
#                 "chart_container_tags": chart_container_tags,
#                 "common_scripts": common_scripts
#             }
#         else:
#             context = {
#                 "component_tags": "",
#                 "chart_api_tags": "",
#                 "dashboard_title": "No Dashboards defined for this KPI!!!!",
#                 "dashboard_sub_title": "Please contact your Product Team/Admin",
#                 "table_api_tags": "",
#                 "table_container_tags": "",
#                 "chart_container_tags": "",
#                 "common_scripts": ""
#             }
#             log.info(context)
#
#         return TemplateResponse(request, 'actrbl_customer_planned_vs_actuals.html', context)
#
#        #return TemplateResponse(request, 'actrbl_discounted_invoices.html', {"output": None})
#     except Exception as e:
#         err_msg = "Error occurred in rendering the dashboard!!"
#         err_description = str(e)
#
#         errors = {"errors": {"level": "critical", "error_msg": err_msg, "error_description": err_description}}
#         log.error(errors, exc_info=True)
#         return TemplateResponse(request, 'actrbl_customer_planned_vs_actuals.html',
#                                 {"dashboard_output": None, "widget_output": None,
#                                  "chart_output": None, "table_output": None, "errors": errors})