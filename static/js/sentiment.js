/**
 * Created by hrwhisper on 2016/4/24.
 */

window.onload = function () {
    gauge = $("#gauge");
    gauge.height(gauge.width() / 1.5);

    myChart = echarts.init(document.getElementById('gauge'));
    myChart.setOption(option, true);

    $(window).resize(function () {
        gauge.height(gauge.width() / 1.5);
        myChart.resize();
    });
};


option = {
    tooltip: {
        formatter: "{c} {b}"
    },
    series: [
        {
            name: 'positive',
            type: 'gauge',
            z: 3,
            min: 0,
            max: 100,
            splitNumber: 10,
            radius: '70%',
            center: ['50%', '50%'],    // 默认全局居中
            axisLine: {            // 坐标轴线
                lineStyle: {       // 属性lineStyle控制线条样式
                    width: 10
                }
            },
            axisTick: {            // 坐标轴小标记
                length: 15,        // 属性length控制线长
                lineStyle: {       // 属性lineStyle控制线条样式
                    color: 'auto'
                }
            },
            splitLine: {           // 分隔线
                length: 10,         // 属性length控制线长
                lineStyle: {       // 属性lineStyle（详见lineStyle）控制线条样式
                    color: 'auto'
                }
            },
            title: {
                textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                    fontWeight: 'bolder',
                    fontSize: 20,
                    fontStyle: 'italic'
                }
            },
            detail: {
                textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                    fontWeight: 'bolder'
                }
            },
            data: [{value: 0, name: 'positive'}]
        },
        {
            name: 'negative',
            type: 'gauge',
            center: ['18%', '55%'],    // 默认全局居中
            radius: '40%',
            min: 0,
            max: 100,
            endAngle: 45,
            splitNumber: 10,
            axisLine: {            // 坐标轴线
                lineStyle: {       // 属性lineStyle控制线条样式
                    width: 8
                }
            },
            axisTick: {            // 坐标轴小标记
                length: 12,        // 属性length控制线长
                lineStyle: {       // 属性lineStyle控制线条样式
                    color: 'auto'
                }
            },
            splitLine: {           // 分隔线
                length: 20,         // 属性length控制线长
                lineStyle: {       // 属性lineStyle（详见lineStyle）控制线条样式
                    color: 'auto'
                }
            },
            pointer: {
                width: 5
            },
            title: {
                offsetCenter: [0, '-30%']       // x, y，单位px
            },
            detail: {
                textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                    fontWeight: 'bolder'
                }
            },
            data: [{value: 0, name: 'negative'}]
        },
        {
            name: 'neutral',
            type: 'gauge',
            center: ['78%', '50%'],    // 默认全局居中
            radius: '25%',
            min: 0,
            max: 100,
            startAngle: 135,
            endAngle: -50,
            splitNumber: 2,
            axisLine: {            // 坐标轴线
                lineStyle: {       // 属性lineStyle控制线条样式
                    width: 8
                }
            },
            axisTick: {            // 坐标轴小标记
                splitNumber: 5,
                length: 10,        // 属性length控制线长
                lineStyle: {       // 属性lineStyle控制线条样式
                    color: 'auto'
                }
            },
            splitLine: {           // 分隔线
                length: 15,         // 属性length控制线长
                lineStyle: {       // 属性lineStyle（详见lineStyle）控制线条样式
                    color: 'auto'
                }
            },
            pointer: {
                width: 2
            },
            detail: {
                textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                    fontSize: 20
                }
            },
            data: [{value: 0, name: 'neutral'}]
        }
    ]
};

function update_sentiment_result(res) {
    // update gauge charts
    var positive = res['positive'],
        negative = res['negative'],
        neutral = res['neutral'];

    option.series[0].data[0].value = (positive['percent'] * 100).toFixed(2) - 0;
    option.series[1].data[0].value = (negative['percent'] * 100).toFixed(2) - 0;
    option.series[2].data[0].value = (neutral['percent'] * 100).toFixed(2) - 0;
    myChart.setOption(option, true);

    //add text
    $("#positive_sample_result").empty();
    $("#negative_sample_result").empty();
    $("#neutral_sample_result").empty();

    var positive_text = positive['text'],
        negative_text = negative['text'],
        neutral_text = neutral['text'];

    for (var i = 0; i < positive_text.length; i++)
        update_sentiment_text_sample(positive_text[i], 'positive');

    for (i = 0; i < negative_text.length; i++)
        update_sentiment_text_sample(negative_text[i], 'negative');

    for (i = 0; i < neutral_text.length; i++)
        update_sentiment_text_sample(neutral_text[i], 'neutral');

    $("#sample_result").show(); //.css("display", "block");
}

// update_sentiment_text_sample('text' , false); //just text
function update_sentiment_text_sample(text, mode) {
    var tag_head = '<li class="list-group-item">', tag_end = '</li>';
    if (mode == 'positive')
        $("#positive_sample_result").append(tag_head + text + tag_end);
    else if (mode == 'negative')
        $("#negative_sample_result").append(tag_head + text + tag_end);
    else
        $("#neutral_sample_result").append(tag_head + text + tag_end);
}


function get_sentiment_result() {
    //TODO check data is empty
    var data = {
        'query_str': $('#name').val()
    };

    console.log(data);
    loading_control.start();

    $.ajax({
        url: 'sentiment_query',
        data: data,
        success: function (v) {
            console.log(v);
            update_sentiment_result(v);
            loading_control.stop();
        },
        error: function (v) {
            console.log('------error------' + v);
            loading_control.stop();
        },
        dataType: 'json'
    });
}