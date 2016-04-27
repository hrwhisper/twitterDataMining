/**
 * Created by hrwhisper on 2016/4/25.
 */
var loading_control = {
    opts: {
        // more options: http://fgnass.github.io/spin.js/
        length: 28,
        width: 14,
        radius: 42,
        color: "#fff",
        scale: 0.5,
        opacity: 0.2,
        position: "fixed"
    },
    spinner: null,
    div_wait: null,
    div_wait_bg: null,

    start: function () {
        if (!this.div_wait) {
            var div = document.createElement("div");
            div.id = "foo";
            document.body.appendChild(div);
            this.div_wait = div;
        }

        if (!this.div_wait_bg) {
            var div = document.createElement("div");
            div.id = "waiting-bg";
            div.style.cssText = "width:100%; height:100%; background-color:#000; filter:alpha(opacity=60);-moz-opacity:0.6; opacity:0.6; position:fixed; left:0px; top:0px; display:none;  z-index:1000;";

            document.body.appendChild(div);
            this.div_wait_bg = div;
        }

        if (!this.spinner) {
            this.spinner = new Spinner(this.opts);
        }

        this.div_wait_bg.style.display = "block";
        this.spinner.spin(this.div_wait)
    },

    stop: function () {
        if(this.spinner)
            this.spinner.stop();
        this.div_wait_bg.style.display = "none";
    }
};