$(document).ready(function() {
    var pie_chart = echarts.init(document.getElementById('pie_chart'));
    var option = {
        title: {
            text: 'Prediction Status',
            subtext: 'Correctness',
            x: 'center'
        },
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            x: 'left',
            data: ["Predict:Rise\nAcutal:Rise",
                   "Predict:Rise\nAcutal:Fall",
                   "Predict:Fall\nAcutal:Rise",
                   "Predict:Fall\nAcutal:Fall"]
        },
        toolbox: {
            show: true,
            feature: {
                mark: {show: true},
                dataView: {show: true, readOnly: false},
                magicType: {
                    show: true,
                    type: ['pie', 'funnel'],
                    option: {
                        funnel: {
                            x: '25%',
                            width: '50%',
                            funnelAlign: 'left',
                            max: '{{ ap00+ap11+ap01+ap10 }}'
                        }
                    }
                },
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        calculable: true,
        series: [
            {
                name: 'Number of the day',
                type: 'pie',
                radius: '55%',
                center: ['50%', '60%'],
                data: [
                    {value: '{{ ap11 }}', name: 'Predict:Rise\nAcutal:Rise'},
                    {value: '{{ ap01 }}', name: 'Predict:Rise\nAcutal:Fall'},
                    {value: '{{ ap10 }}', name: 'Predict:Fall\nAcutal:Rise'},
                    {value: '{{ ap00 }}', name: 'Predict:Fall\nAcutal:Fall'}
                ]
            }
        ]
    };
    pie_chart.setOption(option);
});