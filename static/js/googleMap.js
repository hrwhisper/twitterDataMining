var googleMap = {
    map: null,
    markers: {},
    currentId: 0,

    uniqueId: function () {
        return ++this.currentId;
    },

    infowindow: new google.maps.InfoWindow({
        size: new google.maps.Size(150, 50)
    }),


    initialize: function () {
        if (this.map) return null;

        var myOptions = {
            zoom: 2,
            center: new google.maps.LatLng(43.907787, 0),
            mapTypeControl: true,
            mapTypeControlOptions: {style: google.maps.MapTypeControlStyle.DROPDOWN_MENU},
            navigationControl: true,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        this.map = new google.maps.Map(document.getElementById("map_canvas"),
            myOptions);

        google.maps.event.addListener(this.map, 'click', function () {
            googleMap.infowindow.close();
        });

        google.maps.event.addListener(this.map, 'click', function (event) {
            var Latitude = event.latLng.lng().toFixed(2);
            var longitude = event.latLng.lat().toFixed(2);
            googleMap.addMarker(event.latLng, "name", "<b>Location</b><br>" +Latitude +","+ longitude,
                Latitude +","+ longitude);
        });

        //google.maps.event.addListener(this.map, 'click', function (event) {
        //    console.log("Latitude: " + event.latLng.lat() + " " + ", longitude: " + event.latLng.lng());
        //});
    },


    addMarker: function (Gpoint, name, contentString, geo) {
        var id = this.uniqueId(); // get new id
        marker = new google.maps.Marker({
            id: id,
            position: Gpoint,
            geo: geo,
            map: googleMap.map,
            draggable: true,
            animation: google.maps.Animation.DROP
        });

        google.maps.event.addListener(marker, 'click', function () {
            googleMap.infowindow.setPosition(this.position);
            googleMap.infowindow.setContent(contentString);
            googleMap.infowindow.open(googleMap.map, marker);
        });
        google.maps.event.trigger(marker, 'click');

        googleMap.map.panTo(Gpoint);

        this.markers[id] = marker;

        google.maps.event.addListener(marker, "rightclick", function (point) {
            googleMap.delMarker(this.id)
        });
        //var res = '';
        //for (i in googleMap.markers){
        //   res += googleMap.markers[i].geo + ',';
        //}
        //res = res.substring(0,res.length-1)
        //console.log(res);
    },

    delMarker: function (id) {
        this.markers[id].setMap(null);
        delete  this.markers[id];
    }
};