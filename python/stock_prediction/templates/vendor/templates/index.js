$(document).ready(function(){
	var my_apikey = '596fe855925b9355e516ae327f4528ca';
	var apiurl = 'http://apis.baidu.com/apistore/stockservice/usastock?stockid=bidu&list=1';
     var djia_data_url = '/get_djia_data';

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

    $.get('/static/dataset/stock-DJI.json', function (rawData) {

        var data = splitData(rawData);
    
        myChart.setOption(option = {
            backgroundColor: '#eee',
            animation: false,
            legend: {
                bottom: 10,
                left: 'center',
                data: ['Dow-Jones index']
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'line'
                }
            },
            toolbox: {
                feature: {
                    dataZoom: {
                        yAxisIndex: false
                    },
                    brush: {
                        type: ['lineX', 'clear']
                    }
                }
            },
            brush: {
                xAxisIndex: 'all',
                brushLink: 'all',
                outOfBrush: {
                    colorAlpha: 0.1
                }
            },
            grid: [
                {
                    left: '10%',
                    right: '8%',
                    height: '50%'
                },
                {
                    left: '10%',
                    right: '8%',
                    top: '63%',
                    height: '16%'
                }
            ],
            xAxis: [
                {
                    type: 'category',
                    data: data.categoryData,
                    scale: true,
                    boundaryGap : false,
                    axisLine: {onZero: false},
                    splitLine: {show: false},
                    splitNumber: 20,
                    min: 'dataMin',
                    max: 'dataMax'
                },
                {
                    type: 'category',
                    gridIndex: 1,
                    data: data.categoryData,
                    scale: true,
                    boundaryGap : false,
                    axisLine: {onZero: false},
                    axisTick: {show: false},
                    splitLine: {show: false},
                    axisLabel: {show: false},
                    splitNumber: 20,
                    min: 'dataMin',
                    max: 'dataMax'
                }
            ],
            yAxis: [
                {
                    scale: true,
                    splitArea: {
                        show: true
                    }
                },
                {
                    scale: true,
                    gridIndex: 1,
                    splitNumber: 2,
                    axisLabel: {show: false},
                    axisLine: {show: false},
                    axisTick: {show: false},
                    splitLine: {show: false}
                }
            ],
            dataZoom: [
                {
                    type: 'inside',
                    xAxisIndex: [0, 1],
                    start: 98,
                    end: 100
                },
                {
                    show: true,
                    xAxisIndex: [0, 1],
                    type: 'slider',
                    top: '85%',
                    start: 98,
                    end: 100
                }
            ],
            series: [
                {
                    name: 'Dow-Jones index',
                    type: 'candlestick',
                    data: data.values,
                    itemStyle: {
                        normal: {
                            borderColor: null,
                            borderColor0: null
                        }
                    },
                    tooltip: {
                        formatter: function (param) {
                            var param = param[0];
                            return [
                                'Date: ' + param.name + '<hr size=1 style="margin: 3px 0">',
                                'Open: ' + param.data[0] + '<br/>',
                                'Close: ' + param.data[1] + '<br/>',
                                'Lowest: ' + param.data[2] + '<br/>',
                                'Highest: ' + param.data[3] + '<br/>'
                            ].join('');
                        }
                    }
                },
            ]
        }, true);

        myChart.dispatchAction({
            type: 'brush',
            areas: [
                {
                    brushType: 'lineX',
                    coordRange: ['2016-06-02', '2016-06-20'],
                    xAxisIndex: 0
                }
            ]
        });
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
