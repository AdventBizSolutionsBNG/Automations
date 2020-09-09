import json
import logging

# load tags for a component of type Widget
def generate_widget_tags(component, md_corelib_display_components, api_call_type):
    try:
        log = logging.getLogger("main")
        log.info("------------ Widget ------------")
        log.info("Core Library: Generating Widget Tags for Component: %s", component["component_code"])
        log.info("Core Library: Component Name: %s", component["component_name"])
        log.info("Core Library: Component Title: %s", component["component_title"])

        widget_code =  component["component_code"]
        widget_sequence = component["sequence"]
        widget_name = component["component_name"]
        widget_type = component["component_sub_type"]
        widget_reference_class = component["component_reference_class"]
        widget_category = component["component_category"]
        widget_tooltip = component["component_tooltip"]
        widget_title = component["component_title"]
        is_auto_refresh = component["is_auto_referesh"]
        refresh_interval_ms = component["refresh_interval"]
        component_queries = json.loads(component["component_query"])
        widget_queries = component_queries["widget"]
        md_widget_metadata = md_corelib_display_components["widgets"]
        md_extraction_metadata = md_corelib_display_components["data_extraction"]
        display_properties = component["display_properties"]
        widget_display_id = "W" +  str(widget_sequence)
        log.info("Core Library: Widget Display Id: %s", widget_display_id)

        log.info("Core Library: Retrieving Extraction methods metadata for the Widget")
        for methods in md_extraction_metadata:
            if methods["method"] == "api":
                method_details = methods["method_details"]
                md_api_method_details = method_details

        log.info("Core Library: Retrieving API Extraction methods metadata for the Widget-Value")
        md_api_method_value_tags = get_api_tags("values", api_call_type,  md_api_method_details)

        log.info("Core Library: Retrieving API Extraction methods metadata for the Widget-Indicators")
        md_api_method_indicators_tags = get_api_tags("indicators", api_call_type, md_api_method_details)

        log.info("Core Library: Retrieving API Payload metadata for the Widget Components")
        md_api_payload = get_api_payload(api_call_type, md_api_method_details)

        for md_widget in md_widget_metadata:
            if md_widget["component_sub_type"] == component["component_sub_type"]:
                md_widget_details = md_widget["widget_details"]
                if md_widget_details:
                    log.info("Core Library: Loading Widget Details: %s", widget_display_id)
                    max_values = md_widget_details["max_values"]
                    max_indicators = md_widget_details["max_indicators"]
                    default_status = md_widget_details["default_status"]
                    log.info("Core Library: Max Values: %s",max_values )
                    log.info("Core Library: Max Indicators: %s", max_indicators)

                    # load sections metadata for the widget
                    log.info("Core Library: Loading different Widget Metadata sections")
                    for sections in md_widget_details["sections"]:
                        md_main_section = sections["main_section"]
                        md_image_section = sections["image_section"]
                        md_indicator_section = sections["indicator_section"]
                        widget_display_properties = component["display_properties"].get("widget")

                        if md_main_section:
                            for k,v in md_main_section.items():
                                if k == "main_tag":
                                    widget_main_tag = md_main_section["main_tag"]
                                if k == "title_tag":
                                    widget_title_tag = md_main_section["title_tag"]

                            widget_main_tag = widget_main_tag.replace("{COMPONENT COLOR}", widget_display_properties["color"])

                            if widget_title:
                                widget_title_tag = widget_title_tag.replace("{COMPONENT_TITLE}", widget_title)
                                widget_main_tag = widget_main_tag.replace("{HEADING TAG}", widget_title_tag)\
                                                    .replace("{COMPONENT ID}",widget_display_id)


                            # load Values with metadata
                            md_widget_values = md_main_section["values"]
                            my_values = widget_display_properties["values"]
                            final_value_tags = ""
                            final_value_script_tags = ""
                            final_value_output = []
                            value_id_list = []
                            log.info("Core Library: Processing different Values for the current Widget")
                            if my_values:
                                for my_value in my_values:
                                    for md_widget_value in md_widget_values:
                                        if my_value["level"] == md_widget_value["level"]:
                                            my_value_level = md_widget_value["level"]
                                            log.info("Core Library: Loading Widget Value: %s", my_value_level)

                                            my_value_tooltip = my_value["tooltip"]
                                            md_value_tags = md_widget_value["value_tag"]
                                            value_condition = my_value["condition"]
                                            value_operator = my_value["condition"].get("operator")
                                            value_measure = my_value["condition"].get("measure")
                                            my_value_id = widget_display_id + "-" + "V" + str(my_value_level)
                                            log.info("Core Library: Loading Widget Id: %s", my_value_id)

                                            value_id_list.append(my_value_id)
                                            my_value_query = get_widget_query("values", my_value_level, widget_queries)

                                            if md_value_tags:
                                                my_value_tags = md_value_tags.replace("{W_V}", my_value_id)\
                                                                .replace("{VALUES}", default_status)\
                                                                .replace("{VALUE TOOLTIP}",my_value_tooltip)

                                                log.info("Core Library: Generating Widget API Scripts: %s", my_value_id)
                                                if my_value_query:
                                                    my_value_script_tags = generate_api_script_tags(my_value_id, md_api_payload, md_api_method_value_tags, component["data_source_methods"], my_value_query)
                                                else:
                                                    my_value_script_tags = ""
                                                    log.error("Core Library: Error Generating Widget API Scripts: %s", my_value_id)
                                            else:
                                                log.error("Core Library: Error Generating Widget Value Display Tags or Value Tags not defined: %s", my_value_id)
                                                my_value_tags = ""
                                                my_value_script_tags = ""


                                            final_value_tags = final_value_tags + my_value_tags
                                            final_value_script_tags = final_value_script_tags + my_value_script_tags

                                widget_main_tag = widget_main_tag.replace("{VALUE TAGS}", final_value_tags)
                                widget_main_tag = widget_main_tag.replace("{VALUE EXTRACTION SCRIPTS}", final_value_script_tags)

                            else:
                                widget_main_tag = widget_main_tag.replace("{VALUE TAGS}", "")
                                widget_main_tag = widget_main_tag.replace("{VALUE EXTRACTION SCRIPTS}", "")

                            # load images metadata. loop metadata image section and match the type
                            log.info("Core Library: Processing Image Tags for the current Widget")
                            images = widget_display_properties["image_type"]
                            if images:
                                for md_image in md_image_section:
                                    if md_image["type"] == widget_display_properties["image_type"]:
                                        log.info("Core Library: Loading Widget Image")
                                        image_source = md_image["source"]
                                        image_theme = md_image["theme"]
                                        image_tag = md_image["image_tag"]
                                        image_tag = image_tag.replace("{IMAGE SOURCE}", image_source)\
                                                        .replace("{DISPLAY THEME}", image_theme)\
                                                        .replace("{COMPONENT ID}", str(widget_sequence))

                                        widget_main_tag = widget_main_tag.replace("{IMAGE TAG}", image_tag)
                            else:
                                widget_main_tag = widget_main_tag.replace("{IMAGE TAG}", "")

                            # load indicators metadata
                            log.info("Core Library: Processing different Indicators for the current Widget")
                            if widget_display_properties["indicators"]:
                                final_indicator_script_tags = ""
                                final_indicator_tags = ""
                                for my_indicator in widget_display_properties["indicators"]:
                                    final_indicator_output = []
                                    indicator_id_list = []
                                    for md_indicator in md_indicator_section:
                                        if my_indicator["level"] == md_indicator["level"]:
                                            my_indicator_level = my_indicator["level"]
                                            my_indicator_id = widget_display_id + "-" + "I" + str(my_indicator_level)
                                            log.info( "Core Library: Loading Widget Indicator: %s", my_indicator_id)

                                            my_indicator_tooltip = my_indicator["tooltip"]
                                            indicator_condition = my_indicator["condition"]
                                            operator = my_indicator["condition"].get("operator")
                                            measure = my_indicator["condition"].get("measure")

                                            log.info("Core Library: Retrieving Indicator Query: %s", my_indicator_id )
                                            my_indicator_query = get_widget_query("indicators", my_indicator_level, widget_queries)
                                            for ind_type in md_indicator["types"]:
                                                if ind_type["status"] == "info":
                                                    md_indicator_tags = ind_type["indicator_tag"]


                                            indicator_id_list.append(my_indicator_id)
                                            if md_indicator_tags:
                                                log.info("Core Library: Retrieving Indicator API Script tags: %s", my_indicator_id)
                                                my_indicator_tags = md_indicator_tags.replace("{W_I}", my_indicator_id)\
                                                                        .replace("{INDICATOR_VALUE}", default_status)\
                                                                        .replace("{INDICATOR TOOLTIP}", my_indicator_tooltip)

                                                if my_indicator_query:
                                                    log.info("Core Library: Generating Indicator API Script Tags: %s", my_indicator_id)
                                                    my_indicator_script_tags = generate_api_script_tags(my_indicator_id, md_api_payload, md_api_method_indicators_tags, component["data_source_methods"],my_indicator_query)
                                                else:
                                                    log.error("Core Library: Retrieving Indicator API Script tags: %s", my_indicator_id)
                                                    my_indicator_script_tags = ""
                                            else:
                                                my_indicator_tags = ""
                                                my_indicator_script_tags = ""

                                            # indicator_output = {"indicator_level": indicator_level, "indicator_tooltip": indicator_tooltip,
                                            #                 "indicator_condition": indicator_condition,
                                            #                 "indicator_tags": indicator_tags, "data_source_script": indicator_script_tags}
                                            # final_indicator_output.append((indicator_output))
                                            final_indicator_tags = final_indicator_tags + my_indicator_tags
                                            final_indicator_script_tags = final_indicator_script_tags + my_indicator_script_tags
                                            #print(final_indicator_script_tags)
                                widget_main_tag = widget_main_tag.replace("{INDICATOR TAGS}", final_indicator_tags)
                                widget_main_tag = widget_main_tag.replace("{INDICATOR EXTRACTION SCRIPT}", final_indicator_script_tags)

                            else:
                                widget_main_tag = widget_main_tag.replace("{INDICATOR TAGS}", "")
                                widget_main_tag = widget_main_tag.replace("{INDICATOR EXTRACTION SCRIPT}", "")


        # widget_updated_tags["main"] = widget_main_tag

        widget_output = {"component_display_id": widget_display_id, "component_tags": widget_main_tag }
        return widget_output

    except Exception as e:
        log.error("CoreLibrary!! Error in generating Widget Tags!!", exc_info=True)
        return None


def get_widget_query(object_type, value_level, widget_queries ):
    try:
        log = logging.getLogger("main")
        for value in widget_queries.get(object_type):
            if value["level"] == value_level:
                return value["query"]
    except Exception as e:
        log.error("Error in extraction component Query!!!", exc_info=True)
        return None


# Generic function to retrieve the metadata for a particular object Type
def get_api_tags(object_type, call_type, md_api_method_details):
    try:
        log = logging.getLogger("main")

        for method_detail in md_api_method_details:
            if method_detail["call_type"] == call_type:
                for objects in method_detail["objects"]:
                    if objects["object_type"] == object_type:
                        return(objects["tags"])
        return None
    except Exception as e:
        log.error("Error in Extracting metadata for API", exc_info=True)
        return None


def get_api_payload(call_type, md_api_method_details):
    try:
        log = logging.getLogger("main")
        for method_detail in md_api_method_details:
            if method_detail["call_type"] == call_type:
                payload = method_detail["widget_payload"]
                return payload
        return None
    except Exception as e:
        log.error("Error in extracting payload metadata for API", exc_info=True)
        return None

def generate_api_script_tags(value_id, md_api_payload, md_api_metadata_value_tags, data_source_methods, component_query):
    try:
        log = logging.getLogger("main")
        method_type = data_source_methods["extractionType"]
        if method_type == "api":
            source_details = data_source_methods["source"]
            #url = source_details["url"]
            url = "io_execute_query"

            headers = source_details["headers"]
            data_lake = headers["data_lake"]

            payloads = source_details["headers"]
            ioEngineCode = source_details["headers"].get("io_engine_code")
            apiKey = source_details["headers"].get("api_key")
            token = source_details["headers"].get("token")

            headers = {"io_engine_code": ioEngineCode, "api_key": apiKey," token": token, "data_lake": data_lake}
            payload = md_api_payload
            data = {}
            my_payload = payload.replace("{COMPONENT QUERY}" , component_query).replace("{PERIOD START DATE}", 'periodStartDate').replace('{PERIOD END DATE}', 'periodEndDate')

            # for item in body:
            #     if item == "component_query":
            #         data["component_query"] = component_query
            #     if item == "period_start_date":
            #         data["period_start_date"] = "period_start_date"
            #     if item == "period_end_date":
            #         data["period_end_date"] = "period_end_date"


            if my_payload:
                tags = str(md_api_metadata_value_tags)
                final_extraction_tags = tags.replace("{ELEMENT_ID}", value_id).replace("{URL}", url).replace("{HEADERS}", str(headers)).replace("{PAYLOAD}", str(my_payload))
                log.info(final_extraction_tags)
                return final_extraction_tags
            else:
                log.error( "Core Library: Error generating API Script Tags.")
                return None

    except Exception as e:
        log.error("Core Library: Error in generating extraction method tags for API!!!", exc_info=True)
        return None

