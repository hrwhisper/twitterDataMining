/**
 * Created by hrwhisper on 2016/4/24.
 */


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
            center: ['62%', '50%'],    // 默认全局居中
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
            center: ['30%', '55%'],    // 默认全局居中
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
        }
    ]
};


var gauge = $("#gauge");
gauge.height(gauge.width() / 1.5);

var myChart = echarts.init(document.getElementById('gauge'));
myChart.setOption(option, true);


$(window).resize(function() {
    gauge.height(gauge.width() / 1.5);
    myChart.resize();
});



function update_sentiment_result(res) {
    // update gauge charts
    var total_positive = res['total_positive'],
        total_tweets = res['total_tweets'],
        positive_percentage = res['positive_percentage'];

    var total_negative = total_tweets - total_positive;
    var negative_percentage = total_negative / total_tweets;
    option.series[0].data[0].value = (positive_percentage * 100).toFixed(2) - 0;
    option.series[1].data[0].value = (negative_percentage * 100).toFixed(2) - 0;
    myChart.setOption(option, true);


    //add text
    $("#positive_sample_result").empty();
    $("#negative_sample_result").empty();
    $("#sample_result").show(); //.css("display", "block");

    var positive_text = res['positive_text'],
        negative_text = res['negative_text'];

    for (var i = 0; i < positive_text.length; i++)
        update_sentiment_text_sample(positive_text[i], true);

    for (i = 0; i < negative_text.length; i++)
        update_sentiment_text_sample(negative_text[i], false);
}

// update_sentiment_text_sample('text' , false); //just text
function update_sentiment_text_sample(text, is_positive) {
    var tag_head = '<li class="list-group-item">', tag_end = '</li>';
    if (is_positive)
        $("#positive_sample_result").append(tag_head + text + tag_end);
    else
        $("#negative_sample_result").append(tag_head + text + tag_end);
}


function get_sentiment_result() {
    //TODO check data is empty
    var data = {
        'query_str': $('#name').val()
    };

    console.log(data);

    $.ajax({
        url: 'sentiment_query',
        data: data,
        success: function (v) {
            console.log(v);
            update_sentiment_result(v);
        },
        error: function (v) {
            console.log('------error------' + v);
        },
        dataType: 'json'
    });
}