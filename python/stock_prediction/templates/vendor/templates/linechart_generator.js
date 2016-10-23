function convertDJIACSVToArray(data){
	var djia_array = [];
	for(var daily_data in data){
		var daily_djia = [];
		var timestamp = Date.parse(daily_data.date);
		daily_djia.append(timestamp);
		daily_djia.append(daily_data.dji_close);
		djia_array.append(daily_djia);
	}
	return djia_array;
}

function plotLineChart(item, arraydata){
	var line = [{
        data: arraydata,
        label: "DJIA"
    }];
    var plotdata = {
        xaxes: [{
            mode: 'time'
        }],
        yaxes: [{
            min: 0
        }, {
            // align if we are to the right
            alignTicksWithAxis: position == "right" ? 1 : null,
            position: position,
            tickFormatter: euroFormatter
        }],
        legend: {
            position: 'sw'
        },
        grid: {
            hoverable: true //IMPORTANT! this is needed for tooltip to work
        },
        tooltip: true,
        tooltipOpts: {
            content: "%s for %x was %y",
            xDateFormat: "%y-%0m-%0d",

            onHover: function(flotItem, $tooltipEl) {
                // console.log(flotItem, $tooltipEl);
            }
        }
    };
	$.plot(item, line, data);
}