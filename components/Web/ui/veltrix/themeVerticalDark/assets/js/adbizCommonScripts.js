function select_widget(widget_id){
    console.log("selecting widget", widget_id);
    var elements = document.getElementsByClassName("selectedWidget");
    while(elements.length){
        console.log("Element Class:");
        console.log(elements[0]);
        elements[0].classList.remove("selectedWidget")
    }
    document.getElementById(widget_id).className += " selectedWidget";
}

function select_chart(chart_id){
    console.log("selecting Chart", chart_id);
    var elements = document.getElementsByClassName("selectedChart");
    while(elements.length){
        console.log("Element Class:");
        console.log(elements[0]);
        elements[0].classList.remove("selectedChart")
    }
    document.getElementById(chart_id).className += " selectedChart";
}

function add_spinner_table(table_container_id){
    console.log('adding spinner');
    document.getElementById(table_container_id).className += " spinner";
}

function remove_spinner_table(table_container_id){
    element = document.getElementById(table_container_id);
    if (element){
        console.log('removing spinner');
        element.classList.remove("spinner");
    }
}

function hide_all_charts(){
    document.getElementById('div_chart_container_1').style.visibility='hidden';
    document.getElementById('div_chart_container_2').style.visibility='hidden';
    var elements = document.getElementsByClassName("selectedChart");
    while(elements.length){
        console.log("Element Class:");
        console.log(elements[0]);
        elements[0].classList.remove("selectedChart")
    }
}

function hide_all_tables(){
    document.getElementById('div_table_container_1').style.visibility='hidden';
    document.getElementById('table_title_1').innerHTML = '';
    document.getElementById('table_sub_title_1').innerHTML = '';
    console.log('checking datatables-1...');
    tableElement = document.getElementById('adbizTable_1');
    if($.fn.DataTable.fnIsDataTable(tableElement)) {
        $('#adbizTable_1').DataTable().clear().destroy();
        $("#adbizTable_1").html("");
        console.log('datatable 1 destroyed...');
        console.log('checking datatables-2...');
     };
    tableElement = document.getElementById('adbizTable_2');
    if($.fn.DataTable.fnIsDataTable(tableElement)) {
        $('#adbizTable_2').DataTable().clear().destroy();
        $("#adbizTable_2").html("");
        console.log('datatable 2 destroyed...');
    };
    document.getElementById('div_table_container_2').style.visibility='hidden';
    document.getElementById('table_title_2').innerHTML = '';
    document.getElementById('table_sub_title_2').innerHTML = '';
}

          

