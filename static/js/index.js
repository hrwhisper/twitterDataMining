/**
 * Created by hrwhisper on 2016/4/13.
 */

(function () {

    $(function () {
        $('#myCarousel').on('slide.bs.carousel', function (e) {
//                var slideFrom = $(this).find('.active').index();
            var slideTo = $(e.relatedTarget).index();
//               console.log(slideFrom + ' => ' + slideTo);
            var change_obj = $("#header_info_button");
            if (slideTo == 1) {
                change_obj.attr("href", "/topic");
                change_obj.text("Start topic Now");
            } else {
                change_obj.attr("href", "/sentiment");
                change_obj.text("Start sentiment Now");
            }
        });
    });
    "use strict";

    var π = Math.PI;
    var τ = 2 * Math.PI;

    var types = {
        square: function (n) {
            return (((n + 1) % 2) ? 0 : 1) / n;
        },
        triangle: function (n) {
            if (!(n % 2)) return 0;
            return ((n % 4 === 1) ? 1 : -1) / (n * n);
        },
        sawtooth: function (n) {
            return ((n % 2) ? -1 : 1) / (n + 1);
        },
        pulse: function (n) {
            return 0.1;
        }
    };

    function FT(A, N, φ) {
        φ = φ || 0;
        return function (x) {
            var n = -1, y = 0;
            while (++n < N) {
                y += A[n] * Math.sin(τ * (n + 1) * x + φ);
            }
            return y;
        }
    }

    var
        margin = {top: 0, right: 0, bottom: 0, left: 0},
        W = 450,
        H = 450,
        h = H - margin.top - margin.bottom,

        radius = 140,
        theta = 0,
        xmax = 1.5,
        rate = 1 / 60,

        tDomain = d3.range(0, 1.1, 1 / 1000),   // trace domain
        gDomain = d3.range(0, xmax, xmax / 1000), // graph domain

        C = types.square, // coeffiecients
        L = 6,            // size
        F = 0.3,          // frequence

        yCirc = d3.scale.linear().domain([-1, 1]).range([h / 2 + radius, h / 2 - radius]),
        xCirc = d3.scale.linear().domain([-1, 1]).range([0, 2 * radius]),
        rAxis = d3.scale.linear().domain([0, 1]).range([0, radius]),
        xAxis = d3.scale.linear().range([radius, W - margin.left]),

        Fxy, fx, fy,

        timer, data = [];

    var graph = d3.svg.line()
        .x(function (d) {
            return xAxis(d);
        })
        .y(function (d) {
            return yCirc(fy(theta - d));
        });

    var proj = d3.svg.line()
        .x(function (d) {
            return xCirc(d.x);
        })
        .y(function (d) {
            return yCirc(d.y);
        });

    var trace = d3.svg.line()
        .x(function (d) {
            return xCirc(fx(d));
        })
        .y(function (d) {
            return yCirc(fy(d));
        });

    function gTransform(d) {
        return "translate(" + xCirc(d.x) + "," + yCirc(d.y) + ")";
    }

    var svg = d3.select(".visualization")
        .append("svg")
        .attr("width", W)
        .attr("height", H);

    svg.append("line")
        .attr("class", "axis")
        .attr("y1", margin.top + yCirc(0)).attr("x1", 0)
        .attr("y2", margin.top + yCirc(0)).attr("x2", W);

    svg.append("line")
        .attr("class", "axis")
        .attr("x1", margin.left + xCirc(0)).attr("y1", 0)
        .attr("x2", margin.left + xCirc(0)).attr("y2", H);

    var vis = svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var gPath = vis.append("path").attr("class", "graph");
    var tPath = vis.append("path").attr("class", "trace");
    var pPath = vis.append("path").attr("class", "proj");

    function cache() {
        var A;
        if (typeof C === "function") {
            A = d3.range(1, L + 1).map(C);
        } else {
            A = C.slice(0, L);
        }

        fx = FT(A, L - 1, π / 2);
        fy = FT(A, L - 1, 0);

        Fxy = A.map(function (a, i) {
            return {X: FT(A, i, π / 2), Y: FT(A, i, 0), r: Math.abs(a)};
        });
    }

    function calc() {
        if (!Fxy) cache();
        Fxy.forEach(function (f, i) {
            var d = data[i] || (data[i] = {x: 0, y: 0, r: 0});
            d.x = f.X(theta);
            d.y = f.Y(theta);
            d.r = f.r;
            d.f = i + 1;
        });
        data.length = Fxy.length;
        return data;
    }

    function coeff() {
        var co = vis.selectAll(".coeff").data(calc());

        // exit
        co.exit().remove();

        // enter
        var en = co.enter().append("g").attr("class", "coeff");

        en.append("circle").attr("class", "circle");
        en.append("circle").attr("class", "dot").attr("r", 3);

        // update
        co.classed("last", function (d, i) {
            return i === L - 1;
        });
        co.classed("first", function (d, i) {
            return i === 0;
        });

        co.select(".circle").attr("r", function (d) {
            return rAxis(d.r);
        });

        return co;
    }

    function drawGraph() {
        xAxis.domain([0, xmax]);
        coeff().attr("transform", gTransform);
        var last = data[data.length - 1];
        pPath.attr("d", proj([last, {x: 0, y: last.y}]));
        gPath.attr("d", graph(gDomain));
        tPath.attr("d", trace(tDomain));
    }

    function play() {
        if (timer) return;
        (function loop() {
            drawGraph();
            theta += F * rate;
            timer = setTimeout(loop, rate * 1000);
        })();
    }

    C = types['sawtooth'];

    play();

})();
