function splitData(rawData) { // process .json rawdata
    var categoryData = [];
    var values = [];
    var volumes = [];
    for (var i = 0; i < rawData.length; i++) {
        var line = rawData[i]; // line: ["2004-01-02",10452.74,10409.85,10367.41,10554.96,168890000]
        //console.log(line);
        var date = line.splice(0, 1); // delete the first element then return it as an array
        categoryData.push(date[0]);
        values.push(line);
        volumes.push(line[4]);
    }
    return {
        categoryData: categoryData, // Date
        values: values, // The first element is deleted. [10452.74,10409.85,10367.41,10554.96,168890000]
        volumes: volumes // 168890000
    };
}


function drawChart(dataname, myChart, data){ // The data is what splitdata() returned
    console.log('dataname ------' + dataname);
    myChart.setOption(option = {
            backgroundColor: '#eee',
            animation: false,
            legend: {
                bottom: 10,
                left: 'center',
                data: [dataname] // The name in the bottom, matching the data series
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
                    data: data.categoryData, // Date
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
                    name: dataname,
                    type: 'candlestick',
                    data: data.values, // The first element is deleted. [10452.74,10409.85,10367.41,10554.96,168890000]
                    itemStyle: {
                        normal: {
                            borderColor: null,
                            borderColor0: null
                        }
                    },
                    tooltip: {
                        formatter: function (param) { // param指某一条纵向线中点的数据 derived from series
                            console.log('param ------' + param);
                            var param = param[0];
                            return [
                                'Date: ' + param.name + '<hr size=1 style="margin: 3px 0">', // Dow-Jones index
                                'Open: ' + param.data[0] + '<br/>',
                                'Close: ' + param.data[1] + '<br/>',
                                'Lowest: ' + param.data[2] + '<br/>',
                                'Highest: ' + param.data[3] + '<br/>',
                            ].join('');
                        }
                    }
                }
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
}