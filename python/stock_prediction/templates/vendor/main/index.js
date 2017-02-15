$(document).ready(function(){
	var my_apikey = '596fe855925b9355e516ae327f4528ca';
	var apiurl = 'http://apis.baidu.com/apistore/stockservice/usastock?stockid=bidu&list=1';
     
     //get djia now
	$.ajax({
		url: apiurl,
		method: 'POST',
		headers: {
			'apikey': my_apikey,
		},
		success: function(data){
			console.log(data);
			DJIA = data.retData.market.DJI;
			$("#djia").html(DJIA.startdot);
		}

	});
    
    //get previous djia
    $.get('/getfile/?filename=DowJones_Index.json', function (rawData) {
        
        //console.log(rawData) 
        var data = splitData(JSON.parse(rawData));

        var myChart = echarts.init(document.getElementById('djia-kline'));
    
        drawChart('DJIA Index', myChart, data);
    });
});

/*
"DJI": {
    "name": "道琼斯", 
    "date": "2015-07-29 05:28:06",
    "curdot": 17630.27, // 当前价格
    "rate": 1.09, //当前价格涨幅
    "growth": 189.68, //涨跌率,
    "startdot": 17561.78,//开盘价格
    "closedot": 17440.59,//前一天停盘价格
    "hdot": 17561.78,//今日最高价
    "ldot": 17399.17,//今日最低价
    "turnover":42460000//成交金额（万元）
},
*/
