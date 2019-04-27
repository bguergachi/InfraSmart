<?php
/**
 * Template Name: Google Maps API SQL Directions
 *April 2nd, Added Zones
 */

get_header(); ?> <!––gives the side bar––>

<h1><b>Waypoints </b></h1>
<div id="map"></div>
<div id="right-panel">
<div>
<h6>Select the route to display:</h6> 
<message>Day of the Week:</message>
<select id="dayoftheweek">
  <option value="m">Monday</option>
  <option value="tu">Tuesday</option>
  <option value="w">Wednesday</option>
  <option value="th">Thursday</option>
  <option value="f">Friday</option>
</select>
<h6>Select the zone:</h6> 
<message>Zone:</message>
<select id="zone">
  <option value="Zone1">Zone 1</option>
  <option value="Zone2">Zone 2</option>
  <option value="Zone3">Zone 3</option>
  <option value="Zone4">Zone 4</option>
</select>
<br>
<br>
<!--<input type="button" value="Reload Page" onClick="document.location.reload(true)"> -->
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
  height: 80%;
  margin: 0;
  padding: 5;
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
		//$dbname = "smart_city_main";
		// Create connection
		//$conn = new mysqli($servername, $username, $password, $dbname);
		$conn1 = new mysqli($servername, $username, $password, "zone_1");
		$conn2 = new mysqli($servername, $username, $password, "zone_2");
		$conn3 = new mysqli($servername, $username, $password, "zone_3");
		$conn4 = new mysqli($servername, $username, $password, "zone_4");

		// Check connection
		if ($conn1->connect_error |$conn2->connect_error |$conn3->connect_error |$conn4->connect_error) {
			die("Connection failed: " . $conn->connect_error);
			echo "failed";
		}
		//Get the starting location end location
		$sql = "SELECT lat, lng FROM markers WHERE priority = 1";
		$result = $conn1->query($sql);
		    while($row = $result->fetch_assoc()) {
				$lat = $row["lat"];
				$lng = $row["lng"];
			}
		$sql = "SELECT lat, lng FROM markers WHERE priority = 1";	
		$result2 = $conn2->query($sql);
		    while($row2 = $result2->fetch_assoc()) {
				$lat2 = $row2["lat"];
				$lng2 = $row2["lng"];
			}
		$sql = "SELECT lat, lng FROM markers WHERE priority = 1";
		$result3 = $conn3->query($sql);
		    while($row3 = $result3->fetch_assoc()) {
				$lat3 = $row3["lat"];
				$lng3 = $row3["lng"];
			}
		$sql = "SELECT lat, lng FROM markers WHERE priority = 1";
		$result4 = $conn4->query($sql);
		    while($row4 = $result4->fetch_assoc()) {
				$lat4 = $row4["lat"];
				$lng4 = $row4["lng"];
			}	
		//waypoints from sql ex. $day = 'Tuesday';
		$day = array("m", "tu", "w", "th", "f", "s", "su");

		for($d = 0; $d <7; $d++){
			$sqlw = "SELECT lat, lng FROM markers WHERE Dayoftheweek='$day[$d]' AND priority > 1 ORDER BY priority ASC ";
			$resultw = $conn1->query($sqlw);
			$resultw2 = $conn2->query($sqlw);
			$resultw3 = $conn3->query($sqlw);
			$resultw4 = $conn4->query($sqlw);
			$i = 1; $i2 = 1; $i3 = 1; $i4 = 1;
				while($row = $resultw->fetch_assoc()) {
					$latw[$day[$d]][$i] = $row["lat"];
					$lngw[$day[$d]][$i] = $row["lng"]; //note how it is day first and then the lng
					//echo "Location$i: $latw[$i], $lngw[$i]";
					$id[$i] = $row["priority"];
					$i=$i+1; 
					$zoneday[1] = $day[$d];
				}
				while($row2 = $resultw2->fetch_assoc()) {
					$latw2[$day[$d]][$i2] = $row2["lat"];
					$lngw2[$day[$d]][$i2] = $row2["lng"]; //note how it is day first and then the lng
					$id2[$i2] = $row2["priority"];
					$i2=$i2+1; 
					$zoneday[2] = $day[$d];
				}
				while($row3 = $resultw3->fetch_assoc()) {
					$latw3[$day[$d]][$i3] = $row3["lat"];
					$lngw3[$day[$d]][$i3] = $row3["lng"]; //note how it is day first and then the lng
					$id3[$i3] = $row3["priority"];
					$i3=$i3+1; 
					$zoneday[3] = $day[$d];
				}
				while($row4 = $resultw4->fetch_assoc()) {
					$latw4[$day[$d]][$i4] = $row4["lat"];
					$lngw4[$day[$d]][$i4] = $row4["lng"]; //note how it is day first and then the lng
					$id4[$i4] = $row4["priority"];
					$i4=$i4+1; 
					$zoneday[4] = $day[$d];
				}					
		}
		
		echo "Zone 1: $zoneday[1] "; 
		echo "Zone 1: $zoneday[2] ";
		echo "Zone 1: $zoneday[3] ";
		echo "Zone 1: $zoneday[4] ";
		
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
		
	directionsDisplay.setMap(map);
	//no waypoints until the submit button is clicked
	document.getElementById('submit').addEventListener('click', function() {
		calculateAndDisplayRoute(directionsService, directionsDisplay);
    });
}

function calculateAndDisplayRoute(directionsService, directionsDisplay) {
	
	var waypts = [];
	//origin
	var lat = <?php echo json_encode($lat) ?>;
	var lng = <?php echo json_encode($lng) ?>;
	
	var lat2 = <?php echo json_encode($lat2) ?>;
	var lng2 = <?php echo json_encode($lng2) ?>;
	
	var lat3 = <?php echo json_encode($lat3) ?>;
	var lng3 = <?php echo json_encode($lng3) ?>;
	
	var lat4 = <?php echo json_encode($lat4) ?>;
	var lng4 = <?php echo json_encode($lng4) ?>;
	//waypoints
	var latw = <?php echo json_encode($latw, JSON_PRETTY_PRINT) ?>;
	var lngw = <?php echo json_encode($lngw, JSON_PRETTY_PRINT) ?>;
	var latlngw = [];
	var latw2 = <?php echo json_encode($latw2, JSON_PRETTY_PRINT) ?>;
	var lngw2 = <?php echo json_encode($lngw2, JSON_PRETTY_PRINT) ?>;
	var latlngw2 = [];
	var latw3 = <?php echo json_encode($latw3, JSON_PRETTY_PRINT) ?>;
	var lngw3 = <?php echo json_encode($lngw3, JSON_PRETTY_PRINT) ?>;
	var latlngw3 = [];
	var latw4 = <?php echo json_encode($latw4, JSON_PRETTY_PRINT) ?>;
	var lngw4 = <?php echo json_encode($lngw4, JSON_PRETTY_PRINT) ?>;
	var latlngw4 = [];
	//console.log(latw2);
    //just need to change foo below to the right day
    var HTMLday = document.getElementById('dayoftheweek').value;
	var HTMLzone = document.getElementById('zone').value;
    //console.log(HTMLday);
	//console.log(latw[HTMLday][1]);
	//console.log(latw2[HTMLday][1]);
    //console.log(lngw[HTMLday][1]);
    //console.log(Object.keys(lngw[HTMLday]).length);
	if(HTMLzone =="Zone1"){
		console.log(HTMLzone);
		lngw = lngw;
		latw = latw;
		lat = lat;
		lng = lng;
	}else if(HTMLzone =="Zone2"){
		console.log(HTMLzone);
		lngw = lngw2;
		latw = latw2;
		lat = lat2;
		lng = lng2;
	}else if(HTMLzone =="Zone3"){
		console.log(HTMLzone);
		lngw = lngw3;
		latw = latw3;
		lat = lat3;
		lng = lng3;
	}else if(HTMLzone =="Zone4"){
		console.log(HTMLzone);
		lngw = lngw4;
		latw = latw4;
		lat = lat4;
		lng = lng4;
	}
	//for zone1-4
	try{
		for(var i=1; i<=(Object.keys(lngw[HTMLday]).length); i++){
			latlngw[i] = ((latw[HTMLday][i]).concat(", ").concat(lngw[HTMLday][i]));
			waypts.push({
				location: latlngw[i],
				stopover: true
			});
			var orig = new google.maps.LatLng(lat, lng);
			var dest = new google.maps.LatLng(lat, lng);
		}
	}catch(err){
		console.log("fail!");
		window.alert("No schedule for the chosen zone and day of the week!");
	}

////------------------------------
	//console.log(orig);
    directionsService.route({
		origin: orig,
		destination: dest,
		waypoints: waypts,
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
        summaryPanel.innerHTML += '<b>Route Segment: ' + routeSegment +'</b><br>';
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
