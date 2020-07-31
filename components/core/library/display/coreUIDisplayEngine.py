import components.core.library.display.coreUIDisplayWidgets as CoreLibWidgets
import components.core.library.display.coreUIDisplayCharts as CoreLibCharts
import components.core.library.display.coreUIDisplayTables as CoreLibTables
import logging

def generate_component_tags(my_component, md_corelib_display_components):
    try:
        log = logging.getLogger("main")
        log.info("Core Library: Generating Component Tags")

        default_call_type = "ajax"
        log.info("Core Library: Using Default call Type: %s",default_call_type )

        if my_component["component_type"] == "W":      # of type Widget

            # Generate the tags for widget based on the metadata (passed as parameter)
            widget_output = CoreLibWidgets.generate_widget_tags(my_component, md_corelib_display_components, default_call_type)
            return widget_output
        else:
            log.error("Core Library: Received incorrect Component Type: %s", my_component["component_type"] )
            return None

    except Exception as e:
        log.error("Core Library Error!! Error generating Component Tags!!", exc_info=True)
        return None


def generate_chart_tags(my_component, component_display_id, md_corelib_display_components):
    try:
        log = logging.getLogger("main")
        log.info("Core Library: Generating Chart Tags for Component: %s", component_display_id)

        default_call_type = "ajax"
        log.info("Core Library: Using Default call Type: %s", default_call_type)

        chart_output = CoreLibCharts.generate_chart_tags(my_component, component_display_id, md_corelib_display_components)
        if chart_output:
            return chart_output
        else:
            log.error("Core Library: Error generating Chart Tags for Component:", component_display_id)
            return None

    except Exception as e:
        log.error("Core Library Error!! Error generating Chart Tags!!", exc_info=True)
        return None


def generate_table_tags(my_component, component_display_id, chart_display_id, md_corelib_display_components):
    try:
        log = logging.getLogger("main")
        log.info("Core Library: Generating Chart Tags for Component: %s  And for Chart: %s", component_display_id, chart_display_id)

        default_call_type = "ajax"
        log.info("Core Library: Using Default call Type: %s", default_call_type)

        table_output = CoreLibTables.generate_table_tags(my_component, component_display_id, chart_display_id,
                                                                     md_corelib_display_components)
        if table_output:
            return table_output
        else:
            log.error("Core Library: Error generating Table Tags for Chart:", chart_display_id)
            return None

    except Exception as e:
        log.error("Core Library Error!! Error generating Table Tags!!", exc_info=True)
        return None


def generate_chart_container_tags(md_corelib_display_components):
    try:
        log = logging.getLogger("main")
        log.info("Core Library: Generating Chart Container Tags")

        default_call_type = "ajax"
        chart_container_output = CoreLibCharts.generate_chart_container_tags(md_corelib_display_components)
        if chart_container_output:
            return chart_container_output
        else:
            log.error("Core Library: Error generating Chart Container Tags.")
            return None

    except Exception as e:
        log.error("Core Library Error!! Error generating Chart Container Tags!!", exc_info=True)
        return None


def generate_table_container_tags(md_corelib_display_components):
    try:
        log = logging.getLogger("main")
        log.info("Core Library: Generating Table Container Tags")

        default_call_type = "ajax"
        table_container_output = CoreLibTables.generate_table_container_tags(md_corelib_display_components)
        if table_container_output:
            return table_container_output
        else:
            log.error("Core Library: Error generating Table Container Tags.")
            return None

    except Exception as e:
        log.error("Core Library Error!! Error generating Table Container Tags!!", exc_info=True)
        return None


def generate_data_filter_tag(component_details):
    try:
        data_filters = component_details["data_filters"]
        aggregate_id = component_details["aggregate_id"]
        container_id = component_details["container_id"]

    except Exception as e:
        print(e)

