$(document).ready(function(){
    //get previous djia
    $(".flot-chart-content").each(function(){
        var elem = $(this);
        var elem_id = $(this).attr('id');
        var company_name = $(this).parent().parent().prev().html().trim();
        var json_filename = elem_id + '.json';
        // get the history stock data
        $.get('/getfile/?filename=' + json_filename, function(json){
            var data = splitData(JSON.parse(json));
            var chart = echarts.init(document.getElementById(elem_id));
            drawChart(company_name, chart, data);
        });
        // get the current status of the stock
        /*
        $.get(juhe_stock_api_addr+elem_id, function(data){
            var stock_data = data.result.data;
            var latest_price = stock_data.latestpri;
            var open_price = stock_data.openpri;
            // Create the current status of the stock
            var current_status = document.createElement('span');
            current_status.innerHTML = latest_price;
            current_status.style.color =latest_price >= open_price? 'red':'green';
            elem.parent().parent().prev().append(current_status);
        });
        */
    });
});
