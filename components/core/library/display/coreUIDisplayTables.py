
import json
import logging


def generate_table_container_tags(md_corelib_display_components):
    try:
        log = logging.getLogger("main")
        md_tables = md_corelib_display_components["tables"]

        for md_table in md_tables:
            if md_table["table_library"] == "dataTable":  # todo from settings module. currently only set for table
                md_table_tags = md_table["table_details"].get("main_table_tags")

                # Load Table header tags
                log.info("Core Library: Loading Table Header Tags")
                md_table_header_style = md_table["table_details"].get("header_style")
                md_table_header_tags = md_table["table_details"].get("header_tags")
                my_header_style = ""
                for header_style in md_table_header_style:
                    my_header_style = my_header_style + header_style + ";"

                if my_header_style:
                    my_table_header_tags = md_table_header_tags.replace("{HEADER STYLE}", my_header_style)
                else:
                    my_table_header_tags = md_table_header_tags.replace("{HEADER STYLE}", "")


                # load Table Classes if any specified
                log.info("Core Library: Loading Table Class Tags")
                md_table_class = md_table["table_details"].get("table_class")
                my_table_class = ""
                for item in md_table_class:
                    my_table_class = my_table_class + " " + item
                if my_table_class:
                    md_table_tags = md_table_tags.replace("{TABLE CLASS}", my_table_class)
                else:
                    md_table_tags = md_table_tags.replace("{TABLE CLASS}", "")


                # load Table styles if any specified
                log.info("Core Library: Loading Table Style Tags")
                md_table_style = md_table["table_details"].get("table_style")
                my_table_style = None
                for k, v in md_table_style.items():
                    if my_table_style:
                        my_table_style = my_table_style + k + ":" + v + "; "
                    else:
                        my_table_style =  k + ":" + v + "; "
                if my_table_style:
                    md_table_tags = md_table_tags.replace("{TABLE STYLE}", my_table_style)
                else:
                    md_table_tags = md_table_tags.replace("{TABLE STYLE}", "")


                # Generate create datatable script
                log.info("Core Library: Loading Table Main/Config Tags")
                md_datatable_configs = md_table["table_details"].get("datatable_configs")
                md_datatable_main_tags = md_datatable_configs["datatable_main_tags"]

                # Start creating table tags for each table (use max_table value)
                log.info("Core Library: Loading Table Container Tags")
                md_table_container_tags = md_table["table_details"].get("table_container_tags")
                md_table_create_script_tags = md_table["table_details"].get("script_create_load_table_tags")
                my_final_html_table_tags = None

                i = 1
                max_tables = md_table["max_tables"]
                log.info("Core Library: Max Tables: %s", max_tables)
                my_final_table_container_tags = ""
                table_containers = []
                if max_tables:
                    while i <= max_tables:
                        log.info("Core Library: Processing Tags for Table Container: %s", str(i))
                        my_table_script_tags = md_table_create_script_tags
                        my_datatable_main_tags = md_datatable_main_tags
                        my_table_container_tags = md_table_container_tags
                        my_table_object_id = md_table["table_object"]  + "_" + str(i)
                        my_datatable_object_id = md_table["datatable_object"] + "_" + str(i)
                        my_table_container_id = md_table["table_container"] + "_" + str(i)

                        log.info("Core Library: Table Container Id: %s", my_table_container_id)
                        log.info("Core Library: Table DataTable Id: %s", my_datatable_object_id)
                        log.info("Core Library: Table Id: %s", my_table_object_id)


                        my_table_tags = md_table_tags.replace("{TABLE OBJECT ID}", my_table_object_id )
                        # table_containers[i] = my_table_container_id

                        # generate create table script to be replaced in the main tags
                        log.info("Core Library: Generating Table Scripts")
                        my_table_script_tags = md_table_create_script_tags.replace("{TABLE OBJECT ID}", my_table_object_id )\
                                                    .replace("{HEADER TAGS}", my_table_header_tags )\
                                                    .replace("{HEADER STYLE}", my_header_style)\
                                                    .replace("{TABLE DATATABLE ID}", my_datatable_object_id) \
                                                    .replace("{TABLE CONTAINER ID}", my_table_container_id) \
                                                    .replace("{MAIN TABLE TAGS}", my_table_tags)

                        log.info("Core Library: Generating Datatable Scripts")
                        my_datatable_script_tags = md_datatable_main_tags.replace("{TABLE OBJECT ID}", my_table_object_id)\
                                                    .replace("{TABLE DATATABLE ID}", my_datatable_object_id)

                        log.info("Core Library: Generating Table Container Scripts")
                        my_table_container_tags = md_table_container_tags.replace("{TABLE CONTAINER ID}", my_table_container_id )\
                                                    .replace("{TABLE OBJECT ID}", my_table_object_id)\
                                                    .replace("{TABLE CREATE AND LOAD DATA SCRIPTS}", my_table_script_tags)\
                                                    .replace("{DATATABLE SCRIPTS}", my_datatable_script_tags)\
                                                    .replace("{table_title_$i}", "table_title_" + str(i))\
                                                    .replace("{table_sub_title_$i}", "table_sub_title_" + str(i)) \
                                                    .replace("{TABLE DATATABLE ID}", my_datatable_object_id)

                        if my_table_container_tags:
                            if my_final_table_container_tags:
                                my_final_table_container_tags = my_final_table_container_tags + my_table_container_tags
                            else:
                                my_final_table_container_tags = my_table_container_tags

                        i = i + 1

        return my_final_table_container_tags

    except Exception as e:
        log.error("Core Library Error!! Error in generating Table Container tags", exc_info=True)
        return None


def generate_table_tags(my_component,  component_display_id, my_chart_id, md_corelib_display_components):
    try:
        log = logging.getLogger("main")
        # loading table queries for the current chart
        log.info("Core Library: Loading Table Queries from Display Properties..")
        my_tables = my_component["display_properties"].get("tables")
        all_queries = json.loads(my_component["component_query"])
        component_queries = all_queries["table"]

        my_table_queries = {}
        for q in component_queries:
            if q["chart_id"] == my_chart_id:
                my_table_queries[q["seq"]] = q["query"]      # get table query for the current chart id. display multiple tables for a chart.

        # loading metadata for the Table API
        log.info("Core Library:Loading Table metadata tags from Core Lib..")
        md_tables = md_corelib_display_components["tables"]
        for md_table in md_tables:
            if md_table["table_library"] == "dataTable":
                my_datatable_object = md_table["datatable_object"]
                my_table_object = md_table["table_object"]
                my_table_container = md_table["table_container"]
                md_onclick_tags = md_table["table_details"].get("onclick_tags")

        log.info("Core Library: Loading Table API metadata tags from Core Lib..")
        for methods in md_corelib_display_components["data_extraction"]:
            if methods["method"] == "api":  # todo from settings module. currently only set for table
                for method_types in methods["method_details"]:
                    if method_types["call_type"] == "ajax":
                        for objects in method_types["objects"]:
                            if objects["object_type"] == "table":
                                md_table_extraction_method = objects
                                md_url = objects["url"]
                                md_api_tags = objects["tags"]

        # Generate table script tags from metadata to extract data for the current chart
        my_tables = my_component["display_properties"].get("table")
        final_table_api_tags = ""
        chart_onclick_calls = ""
        my_table_display_ids = []
        my_table_container_ids = []
        my_table_display_tags = {}
        table_display_tags = []
        final_table_calls = ""
        for my_table in my_tables:
            log.info("Core Library: Processing Table: %s", my_table["seq"])
            if my_table["table_library"] == "dataTable":
                if my_table["chart_id"] == my_chart_id:

                    my_table_api_tags = ""
                    my_table_id = my_table["seq"]
                    my_table_container_id = my_table_container + "_" + str(my_table_id)
                    my_table_container_ids.append(my_table_container_id)

                    my_table_title = my_table["table_title"]
                    my_table_sub_title = my_table["table_sub_title"]
                    my_table_query = my_table_queries[my_table_id]

                    my_table_display_id = component_display_id + "_C" + str(my_chart_id) + "_T" + str(my_table_id)
                    my_table_display_ids.append(my_table_display_id)
                    log.info("Core Library:Table Display Id: %s", my_table_display_ids)

                    my_table_object_id = my_table_object + "_" + str(my_table_id)
                    log.info("Core Library:Table Object Id: %s", my_table_object_id)

                    my_datatable_object_id = my_datatable_object + "_" + str(my_table_id)
                    log.info("Core Library:Table DataTable Object Id: %s", my_table_object_id)

                    my_table_title_element_id = "{table_title_" + str(my_table_id) + "}"
                    my_table_sub_title_element_id = "{table_sub_title_" + str(my_table_id) + "}"

                    log.info("Core Library: Processing Table API Tags : %s", my_table_display_id)
                    my_table_api_tags = md_api_tags.replace("{URL}", md_url) \
                        .replace("{TABLE QUERY}", my_table_query) \
                        .replace("{TABLE DISPLAY ID}", my_table_display_id)\
                        .replace("{TABLE OBJECT ID}",my_table_object_id)
                        # .replace("{TABLE TITLE ELEMENT ID}", my_table_title_element_id)\
                        # .replace("{TABLE TITLE}",my_table_title)\
                        # .replace("{TABLE SUB TITLE ELEMENT ID}", my_table_sub_title_element_id)\
                        # .replace("{TABLE SUB_TITLE}", my_table_sub_title)

                    log.info("Core Library: Updating Table Display Tags :%s", my_table_display_id)
                    my_table_display_tags = {
                                                "table_id": my_table_id,
                                                "table_container_id": my_table_container_id ,
                                                "table_display_id": my_table_display_id,
                                                "table_object_id": my_table_object_id,
                                                "table_title": my_table_title,
                                                "table_sub_title": my_table_sub_title,
                                                "table_script_tags": my_table_api_tags
                                              }
                    table_display_tags.append(my_table_display_tags)

                    log.info("Core Library: Updating Table OnClick Tags : %s", my_table_display_id)
                    my_onclick_tags = md_onclick_tags.replace("{TABLE CONTAINER ID}", my_table_container_id) \
                                        .replace("{TABLE TITLE ID}", "table_title_" + str(my_table_id) )\
                                        .replace("{TABLE SUB TITLE ID}", "table_sub_title_" + str(my_table_id))\
                                        .replace("{TABLE TITLE}", my_table_title) \
                                        .replace("{TABLE SUB TITLE}", my_table_sub_title)\
                                        .replace("{TABLE OBJECT ID}", my_table_object_id)\
                                        .replace("{TABLE DATATABLE ID}", my_datatable_object_id)

                    my_table_calls = my_table_display_id + "_getTableData();"
                    final_table_calls = final_table_calls + "\n												" + my_table_calls

                    chart_onclick_calls = chart_onclick_calls + my_onclick_tags
                    final_table_api_tags = final_table_api_tags + my_table_api_tags


        chart_onclick_calls = chart_onclick_calls + final_table_calls

        log.info("Core Library: Generating Chart Onclick Calls")
        log.info("Core Library: Generating Table Output..")
        if len(final_table_api_tags) > 0:
            table_output= {"chart_id": my_chart_id, "table_api_tags": final_table_api_tags, "table_display_ids": my_table_display_ids, "table_details":  table_display_tags , "chart_onclick_tags": chart_onclick_calls, "errors": ""}
        else:
            table_output= {"chart_id": my_chart_id, "table_tags":"", "table_display_ids": "", "table_containers":"", "errors": "Error in generating Table Script Tags!!!"}


        return table_output

    except Exception as e:
            errmsg = "Error in generating Table Script Tags!!!"
            log.error("Core Engine: Error in generating Table Script Tags!!!", exc_info=True)
            table_output = {"table_tags": "", "table_display_ids": "", "errors": errmsg}
            return table_output

