<?php
/**
 * Template Name: Google Maps API SQL Directions
 *
 * This template is used to demonstrate how to use Google Maps
 * in conjunction with a WordPress theme.
 *
 * @since          Twenty Fifteen 1.0
 *
 * @package        Acme_Project
 * @subpackage     Twenty_Fifteen
 */

get_header(); ?> <!––gives the side bar––>
<div id="map"></div>
<div id="right-panel">
<div>
<b>Start:</b>
<select id="start">
  <option value="Halifax, NS">Halifax, NS</option>
  <option value="Boston, MA">Boston, MA</option>
  <option value="New York, NY">New York, NY</option>
  <option value="Miami, FL">Miami, FL</option>
</select>
<br>
<b>Waypoints:</b> <br>
<i>(Ctrl+Click or Cmd+Click for multiple selection)</i> <br>
<select multiple id="waypoints">
  <option value="montreal, quebec">Montreal, QBC</option>
  <option value="toronto, ont">Toronto, ONT</option>
  <option value="chicago, il">Chicago</option>
  <option value="winnipeg, mb">Winnipeg</option>
  <option value="fargo, nd">Fargo</option>
  <option value="calgary, ab">Calgary</option>
  <option value="spokane, wa">Spokane</option>
</select>
<br>
<b>End:</b>
<select id="end">
  <option value="Vancouver, BC">Vancouver, BC</option>
  <option value="Seattle, WA">Seattle, WA</option>
  <option value="San Francisco, CA">San Francisco, CA</option>
  <option value="Los Angeles, CA">Los Angeles, CA</option>
</select>
<br>
  <input type="submit" id="submit">
</div>
<div id="directions-panel"></div>
</div>

    <style type="text/css">
/* Always set the map height explicitly to define the size of the div
 * element that contains the map. */
#map {
  height: 100%;
}
/* Optional: Makes the sample page fill the window. */
html, body {
  height: 75%;
  margin: 0;
  padding: 0;
}
#floating-panel {
  position: absolute;
  top: 10px;
  left: 25%;
  z-index: 5;
  background-color: #fff;
  padding: 5px;
  border: 1px solid #999;
  text-align: center;
  font-family: 'Roboto','sans-serif';
  line-height: 30px;
  padding-left: 10px;
}
    </style>

	<?php
		$servername = "localhost";
		$username = "root";
		$password = "";
		$dbname = "dumpstersite";

		// Create connection
		$conn = new mysqli($servername, $username, $password, $dbname);
		// Check connection
		if ($conn->connect_error) {
			die("Connection failed: " . $conn->connect_error);
			echo "failed";
		}

		//$sql = "SELECT lat, lng FROM markers ORDER BY priority ASC";
		$sql = "SELECT lat, lng FROM markers WHERE priority = 8";
		$result = $conn->query($sql);
		while($row = $result->fetch_assoc()) {
			$lat = $row["lat"];
			$lng = $row["lng"];
		}
		//waypoints
		$sql = "SELECT lat, lng FROM markers WHERE priority = 6";
		$result = $conn->query($sql);
	    while($row = $result->fetch_assoc()) {
			$mlat = $row["lat"];
			$mlng = $row["lng"];
		
		//old stuff
		//$string = sprintf("%.3f", $result); // $string = "0.123";
		//echo "$result";
		//echo "" . $row["lat"].", ". $row["lng"]. " ";
		//echo " ". $row["lat"]." ";
		//$myText = (string)$row["lat"].", ". $row["lng"];
		
		//echo $myText;
		//echo $lat;
		//echo $lng;
		//$result = $conn->query($myText);
		//echo $result;
		//echo "<tr><td>" . $row["id"]. "</td><td>" . $row["date"]. "</td><td> " . $row["time"].  "</td><td> " . $row["address"].  "</td><td> " . $row["lat"].  "</td><td> " . $row["lng"].  "</td><td> " . $row["availability"]. "</td></tr>";
		//window.alert('Directions request failed due to ' + testo);
		}
	?>
	
    <div id="map"></div>
    <script>
//do sql sort
//take first location as the starting point and the end point
//take all the other priorities and then put it into an array which will be used for the waypoints
//how does choosing all the waypoints in html get passed into the direction service?
function initMap() {
  var directionsService = new google.maps.DirectionsService;
  var directionsDisplay = new google.maps.DirectionsRenderer;
          var map = new google.maps.Map(document.getElementById('map'), {
          center: new google.maps.LatLng(43.65, -79.403),
          zoom: 13
        });
		var testo = new google.maps.LatLng(43.65, -79.403);
	directionsDisplay.setMap(map);
	document.getElementById('submit').addEventListener('click', function() {
    calculateAndDisplayRoute(directionsService, directionsDisplay);
    
  });
}

function calculateAndDisplayRoute(directionsService, directionsDisplay) {
	
	
	
  var waypts = [];
  //var checkboxArray = document.getElementById('waypoints');
  var checkboxArray = mlatlng;
/* 
 for (var i = 0; i < checkboxArray.length; i++) {
    if (checkboxArray.options[i].selected) {
      waypts.push({
        //location: checkboxArray[i].value,
        stopover: true
      });
    }
  }
  */
	var testlat = <?php echo json_encode($lat) ?>;
	var testlng = <?php echo json_encode($lng) ?>;
	var testo = new google.maps.LatLng(testlat, testlng);
	
	var mlat = <?php echo json_encode($mlat) ?>;
	var mlng = <?php echo json_encode($mlng) ?>;
	var mlatlng = new google.maps.LatLng(mlat, mlng);
	
	var dest = new google.maps.LatLng(43.65, -79.403);
  directionsService.route({
    //origin: document.getElementById('start').value,
	//origin: result,
	origin: testo,
    //destination: document.getElementById('end').value,
	destination: dest,
    //waypoints: waypts,
	//waypoints: mlatlng,
	waypoints: [{location: mlatlng, stopover: true}],
    optimizeWaypoints: true,
    travelMode: 'DRIVING'
  }, function(response, status) {
    if (status === 'OK') {
      directionsDisplay.setDirections(response);
      var route = response.routes[0];
      var summaryPanel = document.getElementById('directions-panel');
      summaryPanel.innerHTML = '';
      // For each route, display summary information.
      for (var i = 0; i < route.legs.length; i++) {
        var routeSegment = i + 1;
        summaryPanel.innerHTML += '<b>Route Segment: ' + routeSegment +
            '</b><br>';
        summaryPanel.innerHTML += route.legs[i].start_address + ' to ';
        summaryPanel.innerHTML += route.legs[i].end_address + '<br>';
        summaryPanel.innerHTML += route.legs[i].distance.text + '<br><br>';
      }
    } else {
      window.alert('Directions request failed due to ' + status);
    }
  });
}

      function downloadUrl(url, callback) {
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
	  
	function doNothing() {}
	
    </script>    

    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDfsoh48H-SKFU3dv2EcmQihtex9uO_JdA&callback=initMap"
    ">
    </script>
    
  

		<?php
		// Start the loop.
		while ( have_posts() ) : the_post();

			// Include the page content template.
			get_template_part( 'content', 'page' );

			// If comments are open or we have at least one comment, load up the comment template.
			if ( comments_open() || get_comments_number() ) :
				comments_template();
			endif;

		// End the loop.
		endwhile;
		?>

    <?php get_footer(); ?>
