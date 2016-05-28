/**
 * Created by hrwhisper on 2016/4/16.
 */

var userTopicParam = {
    // mode 1
    track: null,
    follow: null,
    location: null,

    // mode 2
    startDate: null,
    endDate: null,
    localCollectionsName: null,

    // common
    LDA_k: null,
    LDA_timeWindow: null,
    storeIntoDB: false,
    storeIntoDBName: null,

    // __first: true,
    __mode: 0, //0:quick start 1:online stream 2:local data

    setMode1None: function () {
        this.track = this.follow = this.location = null;
    },

    setMode2None: function () {
        this.startDate = this.endDate = this.localCollectionsName = null;
    },

    setCommonNone: function () {
        this.LDA_k = this.LDA_timeWindow = null;
        this.storeIntoDB = false;
        this.storeIntoDBName = null;
    },

    update: function () {
        if (this.__mode === 0) {
            this.setMode1None();
            this.setMode2None();
            this.setCommonNone();
        }
        else {
            this.setCommonNone();

            if (this.__mode === 1) {
                this.setMode2None();

                this.track = $('#trackText').val();
                this.follow = $('#followText').val();
                this.location = $('#locationText').val();
                this.storeIntoDB = $('#streamStoreIntoDB').is(':checked');
                this.storeIntoDBName = $('#streamStoreDBName').val();
            }
            else if (this.__mode === 2) {
                this.setMode1None();
                this.startDate = $('#startDate').val();
                this.endDate = $('#endDate').val();
                this.localCollectionsName = $('#localCollectionsName').val();
            }

            this.LDA_k = $('#LdaK').val();
            this.LDA_timeWindow = $('#LdaTimeWindow').val();
        }
    },

    getParam: function () {
        if (this.__mode === 0 || this.__mode === 1) {
            return {
                'mode': 1,
                'track': this.track,
                'follow': this.follow,
                'location': this.location,
                'LDA_k': this.LDA_k,
                'LDA_timeWindow': this.LDA_timeWindow,
                'storeIntoDB': this.storeIntoDB,
                'storeIntoDBName': this.storeIntoDBName
            }
        }
        else if (this.__mode === 2) {
            return {
                'mode': this.__mode,
                'startDate': this.startDate,
                'endDate': this.endDate,
                'localCollectionsName': this.localCollectionsName,
                'LDA_k': this.LDA_k,
                'LDA_timeWindow': this.LDA_timeWindow
            }
        }
    }
};

var testData = {
    test_data: function () {
        return [
            [
                "1",
                0.04,
                [
                    ['a', 0.1],
                    ['b', 0.2],
                    ['c', 0.3],
                    ['d', 0.4]
                ],
                "This is one"
            ],
            [
                "2",
                0.03,
                [
                    ['e', 0.2],
                    ['f', 0.3],
                    ['g', 0.1],
                    ['h', 0.4]
                ],
                "This is two"
            ],
            [
                "3",
                0.03,
                [
                    ['i', 0.2],
                    ['j', 0.3],
                    ['k', 0.1],
                    ['l', 0.4]
                ],
                "This is three"
            ], [
                "4",
                0.04,
                [
                    ['a', 0.1],
                    ['b', 0.2],
                    ['c', 0.3],
                    ['d', 0.4]
                ],
                "This is one"
            ],
            [
                "5",
                0.03,
                [
                    ['e', 0.2],
                    ['f', 0.3],
                    ['g', 0.1],
                    ['h', 0.4]
                ],
                "This is two"
            ],
            [
                "6",
                0.03,
                [
                    ['i', 0.2],
                    ['j', 0.3],
                    ['k', 0.1],
                    ['l', 0.4]
                ],
                "This is three"
            ], [
                "7",
                0.04,
                [
                    ['a', 0.1],
                    ['b', 0.2],
                    ['c', 0.3],
                    ['d', 0.4]
                ],
                "This is one"
            ],
            [
                "8",
                0.03,
                [
                    ['e', 0.2],
                    ['f', 0.3],
                    ['g', 0.1],
                    ['h', 0.4]
                ],
                "This is two"
            ],
            [
                "9",
                0.03,
                [
                    ['i', 0.2],
                    ['j', 0.3],
                    ['k', 0.1],
                    ['l', 0.4]
                ],
                "This is three"
            ], [
                "10",
                0.04,
                [
                    ['a', 0.1],
                    ['b', 0.2],
                    ['c', 0.3],
                    ['d', 0.4]
                ],
                "This is one"
            ],
            [
                "11",
                0.03,
                [
                    ['e', 0.2],
                    ['f', 0.3],
                    ['g', 0.1],
                    ['h', 0.4]
                ],
                "This is two"
            ],
            [
                "12",
                0.03,
                [
                    ['i', 0.2],
                    ['j', 0.3],
                    ['k', 0.1],
                    ['l', 0.4]
                ],
                "This is three"
            ], [
                "13",
                0.04,
                [
                    ['a', 0.1],
                    ['b', 0.2],
                    ['c', 0.3],
                    ['d', 0.4]
                ],
                "This is one"
            ],
            [
                "14",
                0.03,
                [
                    ['e', 0.2],
                    ['f', 0.3],
                    ['g', 0.1],
                    ['h', 0.4]
                ],
                "This is two"
            ],
            [
                "15",
                0.03,
                [
                    ['i', 0.2],
                    ['j', 0.3],
                    ['k', 0.1],
                    ['l', 0.4]
                ],
                "This is three"
            ], [
                "16",
                0.04,
                [
                    ['a', 0.1],
                    ['b', 0.2],
                    ['c', 0.3],
                    ['d', 0.4]
                ],
                "This is one"
            ],
            [
                "17",
                0.03,
                [
                    ['e', 0.2],
                    ['f', 0.3],
                    ['g', 0.1],
                    ['h', 0.4]
                ],
                "This is two"
            ],
            [
                "18",
                0.03,
                [
                    ['i', 0.2],
                    ['j', 0.3],
                    ['k', 0.1],
                    ['l', 0.4]
                ],
                "This is three"
            ], [
                "19",
                0.04,
                [
                    ['a', 0.1],
                    ['b', 0.2],
                    ['c', 0.3],
                    ['d', 0.4]
                ],
                "This is one"
            ],
            [
                "20",
                0.03,
                [
                    ['e', 0.2],
                    ['f', 0.3],
                    ['g', 0.1],
                    ['h', 0.4]
                ],
                "This is two"
            ]
        ];
    },
    geo_test_data: function () {
        return [
            [121.15, 31.89, 9],
            [-109.781327, 39.608266, 100],
            [-120.38, 37.35, 33],
            [-122.207216, 29.985295, 44],
            [123.97, 47.33, 55],
            [120.13, 33.38, 11],
            [118.87, 42.28, 66],
            [120.33, 36.07, 77],
            [121.52, 36.89, 88],
            [102.188043, 38.520089, 123],
            [118.58, 24.93, 99],
            [-118.58, 24.73, 9],
            [-118.58, 24.83, 50],
            [-120.53, 36.86, 256],
            [119.46, 35.42, 50],
            [119.97, 35.88, 1]
        ];
    },
    hashtags_test_data: function () {
        return [['aaa', 1], ['bbb', 2], ['ccc', 3]]
    },
    hashtags_timeline_test_data: function () {
        return {
            'aaa': [1, 2, 3],
            'bbb': [4, 5, 6],
            'ccc': [6, 1, 0]
        };
    }
};


var resultStore = {
    lda_result: testData.test_data(),
    percent_data: percent_visualization_format(testData.test_data()),
    geo: testData.geo_test_data(),
    hashtags: testData.hashtags_test_data(),
    hashtags_timeline: testData.hashtags_timeline_test_data(),
    update: function (v) {
        this.lda_result = v["lda"];
        this.percent_data = percent_visualization_format(v["lda"]);
        this.geo = geo_visualization_format(v["geo"]);
        this.hashtags = v["hashtags"];
        this.hashtags_timeline = v["hashtags_timeline"];
        this.update_visual_diagrams();
    },
    // TODO add array to update visual diagrams
    update_visual_diagrams: function () {
        this.send_message($("#iframe_topic_text")[0], "topic_text");
        this.send_message($("#iframe_topic_bubble")[0]);
        this.send_message($("#iframe_topic_treemap")[0]);
        this.send_message($("#iframe_topic_sunburst")[0]);
        this.send_message($("#iframe_topic_funnel")[0]);
        this.send_message($("#iframe_heatmap")[0], "heatmap");
        this.send_message($("#iframe_hashtags_pie")[0], "hashtags_pie");
        this.send_message($("#iframe_hashtags_histogram")[0], "hashtags_histogram");
        this.send_message($("#iframe_hashtags_timeline")[0], "hashtags_timeline");
    },

    send_message: function (iframe, id) {
        if (!iframe) return;
        if (id === "topic_text") {
            iframe.contentWindow.postMessage(JSON.stringify(this.lda_result), '*');
        }
        else if (id === "heatmap") {

            iframe.contentWindow.postMessage(JSON.stringify(this.geo), '*');
        }
        else if (id === "hashtags_pie" || id === "hashtags_histogram") {
            iframe.contentWindow.postMessage(JSON.stringify(this.hashtags), '*');
        }
        else if (id === "hashtags_timeline") {
            iframe.contentWindow.postMessage(JSON.stringify(this.hashtags_timeline), '*');
        }
        else {
            iframe.contentWindow.postMessage(JSON.stringify(this.percent_data), '*');
        }

    }

};

var streamStatus = {
    mode: 0, //0 continue, 1:pause, 2:stop
    interval: null,
    continue_stream: function () {
        if (this.mode == 0) return null;
        this.mode = 0;
        this.safe_interval();
    },

    pause_stream: function () {
        if (this.mode == 1) return null;
        this.mode = 1;
        this.stop_interval();
    },

    stop_stream: function () {
        //if (this.mode == 2) return null;
        this.mode = 2;
        this.stop_interval();
        $.ajax({
            url: 'stop_trends',
            //data:'',
            success: function (v) {
                if (v == null)  return;
                console.log(v);
            },
            error: function (v) {
                console.log('------error------');
                console.log(v);
            },
            dataType: 'json'
        });
    },

    start_stream: function () {
        userTopicParam.update();
        console.log(userTopicParam.getParam());

        loading_control.start();
        this.safe_interval();
        //.__first = false;
        $('#streamParameters').modal('hide');
    },

    stop_interval: function () {
        if (this.interval) {
            clearInterval(this.interval);
            this.interval = null;
        }
    },

    safe_interval: function () { //to prevent double interval
        this.stop_interval();
        get_topic_result();
        this.interval = setInterval('get_topic_result()', 5000);
    }

};

function get_topic_result() {
    $.ajax({
        url: 'stream_trends',
        data: userTopicParam.getParam(),
        success: function (v) {
            if (v == null)  return;
            console.log(v);
            resultStore.update(v);
            loading_control.stop();
        },
        error: function (v) {
            console.log('------error------');
            console.log(v);
            loading_control.stop();
        },
        dataType: 'json'
    });
}


jQuery.fn.extend({
    disable: function (state) {
        return this.each(function () {
            var $this = $(this);
            if ($this.is('input, button, textarea, select'))
                this.disabled = state;
            else
                $this.toggleClass('disabled', state);
        });
    }
});

function cancelStoreIntoDb(checkbox_obj) {
    checkbox_obj.attr("checked", false);
    $('#streamStoreIntoDB').disable(true);
    $('#streamStoreDBName').disable(true).val('');
}

$('#streamStoreIntoDB').click(function () {
    if ($(this).is(':checked')) {
        $('#streamStoreDBName').disable(false);
    } else {
        cancelStoreIntoDb($(this));
    }
});

$('#streamParameters a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
    if ($(e.target).context.hash === '#quickStart') {
        $('#LdaK').disable(true).val('');
        $('#LdaTimeWindow').disable(true).val('');
        cancelStoreIntoDb($('#streamStoreIntoDB'));
        userTopicParam.__mode = 0;
    } else {
        $('#LdaK').disable(false);
        $('#LdaTimeWindow').disable(false);
        if ($(e.target).context.hash === '#onlineStreamSetting') {
            $('#streamStoreIntoDB').disable(false);
            userTopicParam.__mode = 1;
        }
        else if ($(e.target).context.hash === '#localDataSetting') {
            cancelStoreIntoDb($('#streamStoreIntoDB'));
            userTopicParam.__mode = 2;
        }
    }
});


function percent_visualization_format(res) {
    if (!res) res = test_data();
    // console.log(res);

    var data = {'name': "", 'children': []};

    for (var i = 0; i < res.length; i++) {
        var cur = {'name': res[i][0], 'children': [], 'size': res[i][1]};
        var row = res[i][2];
        for (var j = 0; j < row.length; j++) {
            var temp = {'name': row[j][0], 'size': row[j][1] * res[i][1] * 10};
            cur['children'].push(temp);
        }
        data['children'].push(cur);
    }
    return data;
}

function geo_visualization_format(data) {
    var res = [];
    for (var geo in data) {
        //console.log(geo);
        var temp = geo.split(",");
        if (temp == "null" || temp[0] ==='type') continue;
        res.push([temp[0], temp[1], data[geo]]);
    }
    return res;
}


$(function () {
    $('#topicToolBar input[type="checkbox"]').bootstrapSwitch();
    $('#topicToolBar input[type="checkbox"]').on('switchChange.bootstrapSwitch', function (event, state) {
        var id = $(this).attr("name");
        if (state) {
            var div = document.createElement("div");
            div.className = "embed-responsive embed-responsive-4by3";
            div.id = id;

            $("#result").append(div);

            var iframe = document.createElement("iframe");
            iframe.src = "./" + id;
            iframe.id = "iframe_" + id;

            if (iframe.attachEvent) {
                iframe.attachEvent("onload", function () {
                    resultStore.send_message(iframe, id);
                });
            } else {
                iframe.onload = function () {
                    resultStore.send_message(iframe, id);
                };
            }
            div.appendChild(iframe);
        }
        else {
            id = '#' + id;
            $(id).remove();
        }
    });

    $("#continue_stream").click(function () {
        console.log("continue");
        streamStatus.continue_stream();
    });

    $("#pause_stream").click(function () {
        console.log("pause");
        streamStatus.pause_stream();
    });

    $("#stop_stream").click(function () {
        console.log("stop");
        streamStatus.stop_stream();
    });
});