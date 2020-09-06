import json
import logging

def generate_chart_container_tags(md_corelib_display_components):
    try:
        log = logging.getLogger("main")
        log.info( "Core Library: Processing Chart Metadata")

        md_charts = md_corelib_display_components["charts"]
        for md_chart in md_charts:
            if md_chart["chart_library"] == "chart.js":  # todo from settings module. currently only set for table
                log.info( "Core Library: Using Chart Library for generating Chart Container Tags: %s", md_chart["chart_library"] )

                # Start creating Chart tags for each chart (use max_chart value)
                md_chart_container_tags = md_chart["chart_details"].get("chart_container_tags")
                md_canvas_tags = md_chart["chart_details"].get("canvas_tags")

                my_final_chart_container_tags = ""

                i = 1
                max_charts = md_chart["max_charts"]
                log.info( "Core Library: Max Charts %s", max_charts)
                my_chart_container_tags = ""
                if max_charts:
                    while i <= max_charts:
                        my_canvas_id = md_chart["chart_details"].get("canvas_container") + "_" + str(i)
                        log.info( "Core Library: Processing Tags for Chart Canvas #: %s", my_canvas_id)
                        my_canvas_tags = md_canvas_tags.replace("{CHART CANVAS ID}", my_canvas_id)

                        my_chart_container_id = md_chart["chart_details"].get("chart_container") + "_" + str(i)
                        log.info( "Core Library: Processing Tags for Chart Container #: %s", my_chart_container_id)

                        my_chart_container_tags = md_chart_container_tags.replace("{CHART CONTAINER ID}", my_chart_container_id) \
                                            .replace("{CHART TITLE}", "CHART #" + str(i) ) \
                                            .replace("{CANVAS TAGS}", my_canvas_tags)\
                                            .replace("{CHART ID}", "chart_" + str(i))
                                            # .replace("{CHART DISPLAY SCRIPTS}","{CHART DISPLAY SCRIPTS " + str(i) + "}") \
                                            # .replace("{CHART API SCRIPTS}", "{CHART API SCRIPTS " + str(i) + "}") \

                        if my_chart_container_tags:
                            my_final_chart_container_tags = my_final_chart_container_tags + my_chart_container_tags

                        i = i + 1
            else:
                log.error( "Core Library: Incorrect Chart Library specified: %s", md_chart["chart_library"] )
                return None

        return my_final_chart_container_tags

    except Exception as e:
        log.error( "Core Library: Error in generating Chart Container tags", exc_info=True)
        return None



def generate_chart_tags(my_component, component_display_id, md_corelib_display_components):
    try:
        log = logging.getLogger("main")

        # loading chart queries as list
        log.info( "Core Library: Loading Chart Queries from Display Properties for Widget: %s" , component_display_id)
        my_charts = my_component["display_properties"].get("chart")
        all_queries = json.loads(my_component["component_query"])
        component_queries = all_queries["chart"]
        my_chart_queries = {}
        for q in component_queries:
            my_chart_queries[q["id"]] = q["query"]


        # loading Chart API metadata
        log.info( "Core Library: Loading Chart API metadata tags from Core Lib..")
        for methods in md_corelib_display_components["data_extraction"]:
            if methods["method"] == "api":  # todo from settings module. currently only set for table
                for method_types in methods["method_details"]:
                    if method_types["call_type"] == "ajax":
                        for objects in method_types["objects"]:
                            if objects["object_type"] == "chart":
                                md_chart_extraction_method = objects
                                md_chart_url = objects["url"]
                                md_chart_api_tags = objects["tags"]

        # loading Chart Script metadata
        log.info( "Core Library: Loading Chart Display metadata tags from Core Lib..")
        md_charts = md_corelib_display_components["charts"]
        for md_chart in md_charts:
            # compare the chart library and then load the tags
            if md_chart["chart_library"] == "chart.js":  # todo from settings module. currently only set for chart.js
                max_charts = int(md_chart["max_charts"])
                my_chart_container = md_chart["chart_details"].get("chart_container")
                my_canvas_container = md_chart["chart_details"].get("canvas_container")
                my_chart_var = md_chart["chart_details"].get("chart_var")
                md_display_tags = md_chart["chart_details"].get("chart_display_script")
                md_chart_dataset_tags = md_chart["chart_details"].get("chart_dataset_tags")
                cdns_tags = ""
                cdns = md_chart["lib_cdn"]  # libraries for the chart
                for k, v in cdns.items():
                    cdns_tags = cdns_tags + v

        final_chart_tags = ""

        final_api_tags = ""
        chart_output = {}
        chart_display_ids = []
        chart_ids = []
        chart_container_ids = []
        my_chart_titles = {}
        my_chart_var_id = ""

        i = 1
        for my_chart in my_charts:
            log.info( "Core Library: Processing Chart: %s ", my_chart["chart_id"])
            log.info( "Core Library: Loading Chart Display Properties..")

            my_dataset_tags = ""
            my_chart_id = int(my_chart["chart_id"])
            my_chart_type = my_chart["chart_type"]
            if my_chart_type == "bar":
                my_chart_bar_options = my_chart.get("chart_bar_options")
                if my_chart.get("chart_sub_type") == "multi_bar":
                    my_chart_items = int(my_chart.get("chart_bar_items"))
                else:
                    my_chart_items = 1

                j = 1
                if my_chart_bar_options:
                    dataset_tags = ""
                    while j <= my_chart_items:
                        for bar_option in my_chart_bar_options:
                            if bar_option["id"] == j:
                                log.info("Updating Dataset tags for Chart: %s", str(j))
                                my_chart_bar_option = bar_option
                                temp_var = md_chart_dataset_tags.replace("%i",str(j-1)) \
                                                    .replace("{CHART LABEL}", my_chart_bar_option["label"]) \
                                                    .replace("{CHART COLOR}",my_chart_bar_option["backgroundColor"]) \
                                                    .replace("{CHART BORDER COLOR}", my_chart_bar_option["borderColor"]) \
                                                    .replace("{CHART HOVER COLOR}",my_chart_bar_option["hoverBackgroundColor"] ) \
                                                    .replace("{CHART BORDER WIDTH}", my_chart_bar_option["borderWidth"])
                                dataset_tags = "{" + temp_var + "}"
                                if len(my_dataset_tags) == 0:
                                    my_dataset_tags = dataset_tags
                                else:
                                    my_dataset_tags = my_dataset_tags + "," + dataset_tags

                        j = j +1
            my_dataset_tags = "[" + my_dataset_tags + "]"
            # log.info("Chart Datasets: %s", my_dataset_tags)

            my_chart_library = my_chart["chart_library"]
            my_chart_title = my_chart["chart_title"]
            my_chart_sub_title = my_chart["chart_sub_title"]
            my_chart_label = my_chart["chart_label"]
            my_chart_color = my_chart["chart_color"]
            my_chart_var_id = my_chart_var + "_" + str(my_chart_id)
            my_chart_x_axis = my_chart.get("chart_x_axis")
            if my_chart_x_axis:
                my_chart_x_axis_display = my_chart_x_axis["display_flag"]
                my_chart_x_axis_name = my_chart_x_axis["axis_name"]
                my_chart_x_axis_font_color = my_chart_x_axis["font_color"]
                my_chart_x_axis_font_size = my_chart_x_axis["font_size"]
                my_chart_x_axis_display_grid = my_chart_x_axis["display_grid_flag"]
                my_chart_x_axis_display_grid_color = my_chart_x_axis["grid_lines_color"]

            my_chart_y_axis = my_chart.get("chart_y_axis")
            if my_chart_y_axis:
                my_chart_y_axis_display = my_chart_y_axis["display_flag"]
                my_chart_y_axis_name = my_chart_y_axis["axis_name"]
                my_chart_y_axis_font_color = my_chart_y_axis["font_color"]
                my_chart_y_axis_font_size = my_chart_y_axis["font_size"]
                my_chart_y_axis_display_grid = my_chart_y_axis["display_grid_flag"]
                my_chart_y_axis_display_grid_color = my_chart_y_axis["grid_lines_color"]

            my_chart_display_tags = None
            my_chart_api_tags = None

            if my_chart["chart_title_font_color"]:
                my_chart_title_font_color = my_chart["chart_title_font_color"]
            else:
                my_chart_title_font_color = "rgb(255, 255, 255)"

            if my_chart["chart_title_font_size"]:
                my_chart_title_font_size = my_chart["chart_title_font_size"]
            else:
                my_chart_title_font_size = 14

            if my_chart["options"].get("legend_display"):
                my_chart_legend_display = my_chart["options"].get("legend_display")
            else:
                my_chart_legend_display = 'true'

            if my_chart["options"].get("legend_position"):
                my_chart_legend_position = my_chart["options"].get("legend_position")
            else:
                my_chart_legend_position = "bottom"

            if my_chart["options"].get("legend_color"):
                my_chart_legend_color = my_chart["options"].get("legend_color")
            else:
                my_chart_legend_color = "rgb(255, 255, 255)"

            my_chart_tooltip = my_chart["chart_tooltip"]
            my_chart_display_id = component_display_id + "_" + "C" + str(my_chart_id)
            log.info("Chart Display Id: %s", my_chart_display_id)

            my_chart_query = my_chart_queries[my_chart_id]

            chart_display_ids.append(my_chart_display_id)
            chart_ids.append(my_chart_id)

            my_chart_object = component_display_id + "_" + "C" + str(my_chart_id)
            my_chart_container_id = my_chart_container + "_" + str(my_chart_id)
            chart_container_ids.append(my_chart_container_id)

            my_canvas_container_id = my_canvas_container + "_" + str(my_chart_id)

            if my_chart_library == "chart.js":
                if i <= max_charts:
                    if md_display_tags:
                        log.info("Processing Display Tags for the Chart")
                        log.info( "Core Library: Updating Display Tags: %s", my_chart_display_id)

                        my_chart_display_tags = md_display_tags.replace("{CHART OBJECT}", my_chart_display_id) \
                                                    .replace("{CHART CONTAINER}", my_chart_container_id) \
                                                    .replace("{CHART TYPE}", my_chart_type) \
                                                    .replace("{CHART LABEL}", my_chart_label) \
                                                    .replace("{CHART COLOR}", my_chart_color) \
                                                    .replace("{CHART SUB TITLE}", my_chart_sub_title) \
                                                    .replace("{CHART TITLE FONT COLOR}", my_chart_title_font_color) \
                                                    .replace("{CHART TITLE FONT SIZE}", my_chart_title_font_size) \
                                                    .replace("{LEGEND POSITION}", my_chart_legend_position) \
                                                    .replace("{LEGEND COLOR}", my_chart_legend_color) \
                                                    .replace("{CANVAS CONTAINER}", my_canvas_container_id)\
                                                    .replace("{CHART ONCLICK CALLS}", "{CHART ONCLICK CALLS " + str(my_chart_id) + "}")\
                                                    .replace("{CHART TITLE " + str(my_chart_id) + "}", my_chart_title) \
                                                    .replace("{CHART ID}", "chart_" + str(my_chart_id)) \
                                                    .replace("{CHART DATASET}", my_dataset_tags)\
                                                    .replace("{CHART VAR ID}", my_chart_var_id)\
                                                    .replace("{CHART X AXIS DISPLAY}", my_chart_x_axis_display) \
                                                    .replace("{CHART X AXIS FONT COLOR}", my_chart_x_axis_font_color) \
                                                    .replace("{CHART X AXIS NAME}", my_chart_x_axis_name) \
                                                    .replace("{CHART X AXIS FONT SIZE}", my_chart_x_axis_font_size) \
                                                    .replace("{CHART X GRID LINES DISPLAY}", my_chart_x_axis_display_grid) \
                                                    .replace("{CHART X GRID LINES COLOR}", my_chart_x_axis_display_grid_color) \
                                                    .replace("{CHART Y AXIS DISPLAY}", my_chart_y_axis_display) \
                                                    .replace("{CHART Y AXIS FONT COLOR}", my_chart_y_axis_font_color) \
                                                    .replace("{CHART Y AXIS NAME}", my_chart_y_axis_name) \
                                                    .replace("{CHART Y AXIS FONT SIZE}", my_chart_y_axis_font_size) \
                                                    .replace("{CHART Y GRID LINES DISPLAY}", my_chart_y_axis_display_grid) \
                                                    .replace("{CHART Y GRID LINES COLOR}", my_chart_y_axis_display_grid_color)

                        # log.info("Display tags: %s", my_chart_display_tags)

                        my_chart_titles[my_chart_id] = my_chart_title
                        log.info( "Core Library: Updating API Tags: %s", my_chart_display_id)
                        if md_chart_api_tags:
                            my_chart_api_tags = md_chart_api_tags.replace("{CHART OBJECT}", my_chart_display_id) \
                                                    .replace("{CHART QUERY}", my_chart_query )

                            log.info( "Core Library: Creating Chart output: %s", my_chart_display_id)
                            if my_chart_display_tags is not None and my_chart_api_tags is not None:
                                my_chart_script_tags = my_chart_api_tags + my_chart_display_tags
                                final_chart_tags = final_chart_tags + my_chart_script_tags

                        else:
                            log.error( "Core Library: Error!! No Metadata found for Chart API tags..")
                    else:
                        log.error( "Core Library: Error!! No Metadata found for Chart Display..")


                    i = i +1

            log.info( "Core Library: Generating consolidated Chart Tags Output..")
            # log.info(final_chart_tags)

            if len(final_chart_tags) > 0:
                chart_output = {"chart_tags": final_chart_tags, "chart_display_ids": chart_display_ids,
                                "chart_ids": chart_ids, "chart_container_ids":chart_container_ids, "chart_titles":my_chart_titles, "errors": ""}
            else:
                chart_output = {"chart_tags": "", "chart_display_ids": "", "chart_ids": "", "chart_container_ids": "", "chart_titles":"", "errors": "Error"}

        return chart_output

    except Exception as e:
        log.error("Core Library Error!! Error in generating chart tags", exc_info=True)
        return None


# def generate_chart_tags(my_component, component_display_id, md_corelib_display_components):
#     try:
#         # loading chart details for the component
#         my_charts = my_component["display_properties"].get("chart")
#         all_queries = json.loads(my_component["component_query"])
#         component_queries = all_queries["chart"]
#         my_chart_queries = {}
#         for q in component_queries:
#             my_chart_queries[q["id"]] = q["query"]
#
#         # loading metadata for the chart
#         md_charts = md_corelib_display_components["charts"]
#         for md_chart in md_charts:
#             # compare the chart library and then load the tags
#             if md_chart["chart_library"] == "chart.js":         # todo from settings module. currently only set for chart.js
#                 cdns_tags = ""
#                 cdns = md_chart["lib_cdn"]  # libraries for the chart
#                 for k, v in cdns.items():
#                     cdns_tags = cdns_tags + v
#
#                 # loading chart tags from the metadata
#                 md_chart_details = md_chart["chart_details"]
#                 if md_chart_details["main_tags"]:
#                     md_chart_main_tags = md_chart_details["main_tags"]
#                     md_display_tags = md_chart_details["chart_display_tags"]
#
#         final_chart_tags = ""
#         final_api_tags = ""
#         chart_output = {}
#         chart_display_ids = []
#         chart_ids = []
#
#         if md_chart_main_tags:
#             for my_chart in my_charts:
#                 my_chart_id = my_chart["chart_id"]
#                 my_chart_type = my_chart["chart_type"]
#                 my_chart_library = my_chart["chart_library"]
#                 my_chart_title = my_chart["chart_title"]
#                 my_chart_label = my_chart["chart_label"]
#                 my_chart_tooltip = my_chart["chart_tooltip"]
#                 my_chart_display_id = component_display_id + "_" + "C" + str(my_chart_id)
#                 my_chart_query = my_chart_queries[my_chart_id]
#                 chart_display_ids.append(my_chart_display_id)
#                 chart_ids.append(my_chart_id)
#
#                 for md_chart in md_charts:
#                     chart_tags = ""
#                     api_tags = ""
#
#                     # load the canvas tags
#                     md_canvas_tags = md_chart_details["canvas_tags"]
#                     if md_canvas_tags:
#                         md_canvas_tags = md_canvas_tags.replace("{CHART OBJECT}", my_chart_display_id) + cdns_tags
#
#                         # load chart display tags
#                         md_chart_tags = md_chart_details["chart_tags"]
#                         if len(md_chart_tags)>0:
#                             chart_tags = md_chart_tags.replace("{CHART OBJECT}", my_chart_display_id)\
#                                 .replace("{CHART TYPE}", my_chart_type)\
#                                 .replace("{CHART LABEL}", my_chart_label)\
#                                 .replace("{CHART TITLE}", my_chart_title)\
#                                 .replace("{CHART ONCLICK CALLS}", "{CHART ONCLICK CALLS " + str(my_chart_id) + "}")  # placeholder for functions to be called when this particular chart id is clicked
#
#                             # load chart api tags
#                             md_api_tags = md_chart_details["api_tags"]
#                             if md_api_tags:
#                                 api_tags = md_api_tags.replace("{CHART OBJECT}", my_chart_display_id).replace(
#                                     "{CHART QUERY}", my_chart_query)
#
#                             chart_tags = md_canvas_tags + chart_tags
#                             final_chart_tags = final_chart_tags + chart_tags
#                             final_api_tags = final_api_tags + api_tags
#                         else:
#                             print("error")
#                     else:
#                         print("error")
#
#             if len(final_chart_tags)>0 and len(final_api_tags)>0:
#                 final_main_tags = md_chart_main_tags.replace("{CHART API TAGS}", final_api_tags).replace("{CHART DISPLAY TAGS}", final_chart_tags)
#                 chart_output= {"chart_tags":final_main_tags, "chart_display_ids":chart_display_ids, "chart_ids":  chart_ids}
#
#             else:
#                 chart_output= {"chart_tags":"", "chart_display_ids": "", "chart_ids": "", "errors":"Error"}
#
#             return chart_output
#         else:
#             print("error")
#
#     except Exception as e:
#             print("Core Library Error!! Errror in generating chart tags")
#             print(e)
#
