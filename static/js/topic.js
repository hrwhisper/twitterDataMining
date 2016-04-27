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

var resultStore = {
    res: test_data(),
    percent_data: percent_visualization_format(test_data()),
    update: function (res) {
        this.res = res;
        this.percent_data = percent_visualization_format(res);
        this.update_visual_diagrams();
    },
    // TODO add array to update visual diagrams
    update_visual_diagrams: function () {
        this.send_message($("#iframe_topic_text")[0], true);
        this.send_message($("#iframe_topic_bubble")[0]);
        this.send_message($("#iframe_topic_treemap")[0]);
        this.send_message($("#iframe_topic_sunburst")[0]);
        this.send_message($("#iframe_topic_funnel")[0]);
    },

    send_message: function (iframe, not_percent_data) {
        if (!iframe) return;
        iframe.contentWindow.postMessage(JSON.stringify(not_percent_data ? this.res : this.percent_data), '*');
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
        if (this.mode == 2) return null;
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
                console.log('------error------' + v);
            },
            dataType: 'json'
        });
    },

    start_stream: function () {
        userTopicParam.update();
        console.log(userTopicParam.getParam());

        loading_control.start();
        if (this.interval) {
            this.interval.clearInterval();
            this.interval = null;
        }
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
            console.log('------error------' + v);
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


function test_data() {
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
}

function getCurrentDate() {
    var a = new Date();
    return a.getFullYear() + "-" + (a.getMonth() + 1) + "-" + a.getDate() + " " + a.getHours() + ":" + a.getMinutes() + ":" + a.getSeconds();
}

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
                    resultStore.send_message(iframe, id === 'topic_text');
                });
            } else {
                iframe.onload = function () {
                    resultStore.send_message(iframe, id === 'topic_text');
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