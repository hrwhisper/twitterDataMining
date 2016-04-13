/**
 * Created by hrwhisper on 2016/2/9.
 */

function network_retweet_iframe() {
    $('body').append('<iframe src="/network/retweet" ' +
        'width="1200px" height="700px" id="network_retweet_iframe"></iframe>');
}

function statistic_hashtag_timeline() {
    $('body').append('<iframe src="/statistic/hashtag_timeline?date=2015-12-20&hashtag=Christmas" ' +
        'width="1200px" height="700px" id="statistic_hashtag_timeline_iframe"></iframe>');
}

function statistic_hashtag_compare() {
    $('body').append('<iframe src="/statistic/hashtag_compare?date=2015-12-20&hashtag1=Christmas&hashtag2=christmas" ' +
        'width="1200px" height="700px" id="statistic_hashtag_compare_iframe"></iframe>');
}

function statistic_hashtag_pie(){
     $('body').append('<iframe src="/statistic/hashtag_pie?date=2015-12-20" ' +
        'width="1200px" height="700px" id="statistic_hashtag_compare_iframe"></iframe>');

}