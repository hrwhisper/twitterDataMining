/**
 * Created by hrwhisper on 2016/4/16.
 */

var userTopicParam = {
    // mode 2
    track: null,
    follow: null,
    location: null,

    // mode 3
    startDate: null,
    endDate: null,
    localCollectionsName: null,

    // common
    LDA_k: null,
    LDA_timeWindow: null,
    storeIntoDB: false,
    storeIntoDBName: null,

    __first: true,
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
                this.storeIntoDB = $('#streamStoreIntoDB').is(':checked'); //TODO check is it ok?
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
                'mode': this.__mode,
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


var res = [
    ['1', '50%', ['a', 'b', 'c'], 'hahahahh laal'],
    ['2', '30%', ['h', 'b', 'c'], 'hahahahh laal'],
    ['3', '20%', ['a', 'e', 'd'], 'hahahahh xxlaal']
];

append_topic_text(res);

function append_topic_text(res) {
    var topicText = $('#topicText');
    topicText.empty();
    for (var i = 0; i < res.length; i++) {
        var topic_html = '<h3><a role="button" data-toggle="collapse" href="#collapseTopic' + res[i][0] + '" ' +
            'aria-expanded="false" aria-controls="collapseTopic' + res[i][0] + '">Topic ' + res[i][0] + ' ' +
            res[i][1] + '</a></h3>' + '<div class="collapse in" id="collapseTopic' + res[i][0] + '">' +
            '<p>' + res[i][2] + '</p>' + '<p>' + res[i][3] + '</p></div>';
        if (i != res.length - 1) topic_html += '<hr>';
        topicText.append(topic_html);
    }
}


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


function startStream() {
    userTopicParam.update();
    console.log(userTopicParam.getParam());
    get_topic_result();
    if (userTopicParam.__first)
        setInterval('get_topic_result()', 10000);
    userTopicParam.__first = false;
    //          TODO wait css cancel
    $('#streamParameters').modal('hide');
}


//TODO a new request , cancle previous
function get_topic_result() {
    $.ajax({
        url: 'stream_trends',
        data: userTopicParam.getParam(),
        success: function (v) {
            if (v == null)  return;
            console.log(v);
            append_topic_text(v);
        },
        error: function (v) {
            console.log(error + v);
        },
        dataType: 'json'
    });
}

function test_data() {
    var res = [
        [
            "1",
            0.6,
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
            0.1,
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
            0.3,
            [
                ['i', 0.2],
                ['j', 0.3],
                ['k', 0.1],
                ['l', 0.4]
            ],
            "This is three"
        ]
    ];

    console.log(res);

    var data = {'name': new Date().toString().slice(0, 25), 'children': []};

    for (var i = 0; i < res.length; i++) {
        var cur = {'name': res[i][0], 'children': []};
        var row = res[i][2];
        for (var j = 0; j < row.length; j++) {
            var temp = {'name': row[j][0], 'size': row[j][1] * res[i][1]};
            cur['children'].push(temp);
        }
        data['children'].push(cur);
    }
    //	console.log(data);
    return data;
}


function send_message(iframe) {
    console.log('send' + test_data());
    iframe.contentWindow.postMessage(JSON.stringify(test_data()), '*');
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

            if (iframe.attachEvent) {
                iframe.attachEvent("onload", function () {
                    send_message(iframe);
                });
            } else {
                iframe.onload = function () {
                    send_message(iframe);
                };
            }
            div.appendChild(iframe);
        }
        else {
            id = '#' + id;
            $(id).remove();
        }
    });
});