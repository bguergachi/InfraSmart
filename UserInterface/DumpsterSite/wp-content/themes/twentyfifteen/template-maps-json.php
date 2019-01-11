<?php
/**
 * Template Name: Google Maps API JSON version
 *
 * This template is used to demonstrate how to use Google Maps
 * in conjunction with a WordPress theme.
 *
 * @since          Twenty Fifteen 1.0
 *
 * @package        Acme_Project
 * @subpackage     Twenty_Fifteen
 */
?>

<?php get_header(); ?>

<style type="text/css">

#map {
	
	width:    100%;
	height:   750px;
	
}
</style>

<div id="map"></div><!-- #map-canvas -->
<script>
    function downloadUrl(url,callback) {
     var request = window.ActiveXObject ?
         new ActiveXObject('Microsoft.XMLHTTP') :
         new XMLHttpRequest;

     request.onreadystatechange = function() {
       if (request.readyState == 4) {
         request.onreadystatechange = doNothing;
         callback(request, request.status);
       }
     };

     request.open('GET', url, true);
     request.send(null);
    }
      var map;
      function initMap() {
        map = new google.maps.Map(document.getElementById('map'), {
          zoom: 14,
          center: new google.maps.LatLng(43.66110569,-79.37084870),
          mapTypeId: 'terrain'
        });

        // Create a <script> tag and set the USGS URL as the source.
        //var script = document.createElement('script');
        // This example uses a local copy of the GeoJSON stored at
        // http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojsonp
        //script.src = 'https://developers.google.com/maps/documentation/javascript/examples/json/earthquake_GeoJSONP.js';
        //script.src = 'http://localhost/DumpsterSite/torontodata.json'; //place location of json file 
        //script.data.loadGeoJson('http://localhost/DumpsterSite/torontodata.js');
        //document.getElementsByTagName('head')[0].appendChild(script); //assigns each header in the json file as an element
        
        //want to load geojson 
        //map.data.loadGeoJson('https://storage.googleapis.com/mapsdevsite/json/google.json');
        map.data.loadGeoJson('http://localhost/DumpsterSite/torontodata.json');
        

 
        //var myObj = JSON.parse(myJSON);
        //document.getElementById("demo").innerHTML = myObj.name;
        
        var image = 'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png';
          var beachMarker = new google.maps.Marker({
            position: {lat: 43.66110569, lng: -79.37084870},
            map: map, //this one puts the icon on the map
            icon: image
          });
          

      
      } //end of map init
 
      
      var script = document.createElement('script');
        script.src = 'http://localhost/DumpsterSite/torontodata.json';
        //script.src = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojsonp';
        document.getElementsByTagName('head')[0].appendChild(script);
    
        function eqfeed_callback(response) {
            //map.data.addGeoJson(response); //creates markers
            //new beachMarker;
        }  

        
       
      // Loop through the results array and place a marker for each
      // set of coordinates. (the data isn't actually put into an array, althgouh it should be)
      window.eqfeed_callback = function(results) {
        for (var i = 0; i < results.features.length; i++) {
          var coords = results.features[i].geometry.coordinates;
          var latLng = new google.maps.LatLng(coords[1],coords[0]);
          var marker = new google.maps.Marker({
            position: latLng,
            //map: map
          });
        marker.setMap(map);
              var infowindow;
      infowindow = new google.maps.InfoWindow({
          content: document.getElementById('location')
      });
      
      google.maps.event.addListener(marker, "click", function() {
          infowindow.open(map, marker);
      });
        }
      }
      
</script>
<script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?key=AIzaSyA-y5nufBunnq4ne8E8TMLyCpTkrKVxvvI&callback=initMap"></script>
<?php get_footer(); ?>