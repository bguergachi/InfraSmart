<?php
/**
 * Template Name: Google Maps API SQL v2
 *
 * This template is used to demonstrate how to use Google Maps
 * in conjunction with a WordPress theme.
 *
 * @since          Twenty Seventeen 1.0
 *
 * @package        Acme_Project
 * @subpackage     Twenty_Seventeen
 */
get_header(); ?> <!––gives the side bar––>

<h1><b>Dumpster Map </b></h1>
<h5>Displays the location of dumpsters in the city</h5>

    <style type="text/css">
    #map {
        width:    100%;
        height:   750px;
    }
	
	.site-content {
		margin-left: 10px;
	}
    </style>

	<?php
		$servername = "localhost";
		$username = "root";
		$password = "";
		$dbname = "smart_city_main";

		// Create connection
		$conn = new mysqli($servername, $username, $password, $dbname);
		// Check connection
		if ($conn->connect_error) {
			die("Connection failed: " . $conn->connect_error);
			echo "failed";
		}

		//$sql = "SELECT lat, lng FROM markers ORDER BY priority ASC";
		$sql = "SELECT DeviceNumber, Lat, Lng, Address, Data FROM sensordata ORDER BY DeviceNumber ASC";
		$result = $conn->query($sql);
			$i = 0;
		    while($row = $result->fetch_assoc()) {
				$lat[$i] = $row["Lat"];
				$lng[$i] = $row["Lng"];
				$avail[$i] = $row["Data"];
                $address[$i] = $row["Address"];
                $id[$i] = $row["DeviceNumber"];
				//echo "Location$i: $lat[$i], $lng[$i], $avail[$i], $address[$i]";
				$i=$i+1; 
			}
	?>
	
	<p><b>Click on any of the buttons below to change the markers displayed</b></p>
	<div id="floating-panel">
	<input onclick="clearMarkers();" type=button value="Hide Markers">
	<input onclick="fullMarkers(4);" type=button value="Show All Markers">
	<input onclick="fullMarkers(1);" type=button value="60-100% Full Markers">
	<input onclick="fullMarkers(2);" type=button value="30-60% Full Markers">
	<input onclick="fullMarkers(3);" type=button value="0-30% Full Markers">
	<input onclick="centerMap();" type=button value="Center Map">
	</div>
	
    <div id="map"></div>

    <script>
        var toronto = {lat: 43.65, lng: -79.403};
        var map;
		var markers = [];
        var lat = <?php echo json_encode($lat) ?>;
		var lng = <?php echo json_encode($lng) ?>;
		var avail = <?php echo json_encode($avail) ?>;
        var address = <?php echo json_encode($address) ?>;
        var id = <?php echo json_encode($id) ?>;
		//console.log(address);
		var myAvail = [];
		var latlng = [];
        var InfoWindowContent = [];
        //var secretMessages = ['1', '2', '3', '4', '5','6',];
        
        function initMap() {
          map = new google.maps.Map(document.getElementById('map'), {
          center: new google.maps.LatLng(43.65, -79.403),
          zoom: 13
        });
			
			for(var i=0; i<((Object.keys(lat).length)); i++){
				latlng[i] = new google.maps.LatLng(parseFloat(lat[i]),parseFloat(lng[i]));
				myAvail[i] = avail[i];
                //InfoWindowContent[i] = "ID:".concat(id[i], " Addr: ", address[i], ", Fill: ", myAvail[i], "%");
                InfoWindowContent[i] = 
                  '<div id="siteNotice">'+
                  '</div>'+
                  '<div id="bodyContent">'+
                  '<b>ID: </b>'+id[i] + '<br />'+
                  '<b>Address: </b>'+ address[i]+ '<br />'+
                  '<b>Fill: </b>'+ Math.round(myAvail[i]*100)+ "%"+
                  '</div>';
				//console.log(myAvail[i]);
				//console.log(address[i]);
			}
			//add all the markers when map is loaded
			//addMarker();
			fullMarkers(4);
			
        } //end of initmap
	
	//initial marker placement
	var image1 = 'http://maps.google.com/mapfiles/kml/paddle/grn-blank.png';
	var image2 = 'http://maps.google.com/mapfiles/kml/paddle/ylw-blank.png';
	var image3 = 'http://maps.google.com/mapfiles/kml/paddle/red-blank.png';	
	
      // Adds a marker to the map and push to the array.
    function addMarker() {
		clearMarkers();
		for(var i=0; i<((Object.keys(lat).length)); i++){	
			//if (myAvail[i] < 30){
			if (myAvail[i] < 0.3){
				image = image1;
			//}else if((myAvail[i]  >=30) && (myAvail[i]  <=60)){
			}else if((myAvail[i]  >=0.3) && (myAvail[i]  <=0.6)){
				image = image2;
			}else {
				image = image3;
			}
			var marker = new google.maps.Marker({ //this itself produces a marker onto the map
				map: map,
				position: latlng[i],
				icon: image
			});
			markers.push(marker);
		}
    }

      // Sets the map on all markers in the array.
    function setMapOnAll(map) {
        console.log(markers.length);
        for (var i = 0; i < markers.length; i++) {
        //for (var i = 0; i<((Object.keys(lat).length)); i++) {	
          markers[i].setMap(map); //sets marker on map too
        }
		
    }

      // Removes the markers from the map, but keeps them in the array.
    function clearMarkers() {
        setMapOnAll(null);
    }

      // Shows any markers currently in the array.
    //function showMarkers() {
     //   setMapOnAll(map);
    //}
 


      // Deletes all markers in the array by removing references to them.
    function fullMarkers(type) {
        clearMarkers();
        markers = [];
		for(var i=0; i<((Object.keys(lat).length)); i++){
			//if (myAvail[i] >60 && myAvail[i] < 101 && type == 1){
			if (myAvail[i] >0.6 && myAvail[i] < 1 && type == 1){
				image = image3;
				var marker = new google.maps.Marker({
				map: map,
				position: latlng[i],
				icon: image
				});
			markers.push(marker);	//this and the line under doesn't work when placed at the end of the if statment!
            attachInfoWindow(marker, InfoWindowContent[i]);
			//}else if(myAvail[i] >30 && myAvail[i] < 60 && type == 2){
			}else if(myAvail[i] >0.3 && myAvail[i] < 0.6 && type == 2){
				image = image2;
				var marker = new google.maps.Marker({
				map: map,
				position: latlng[i],
				icon: image
				});
			markers.push(marker);	
            attachInfoWindow(marker, InfoWindowContent[i]);
			//}else if(myAvail[i] >0 && myAvail[i] < 30 && type == 3){
			}else if(myAvail[i] >0 && myAvail[i] < 0.3 && type == 3){
				image = image1;
				var marker = new google.maps.Marker({
				map: map,
				position: latlng[i],
				icon: image
				});
			markers.push(marker);	
            attachInfoWindow(marker, InfoWindowContent[i]);
			}else if(type ==4){
				//if (myAvail[i] < 30){
				if (myAvail[i] < 0.3){
				image = image1;
				//}else if((myAvail[i]  >=30) && (myAvail[i]  <=60)){
				}else if((myAvail[i]  >=0.3) && (myAvail[i]  <=0.6)){
					image = image2;
				}else {
					image = image3;
				}
				var marker = new google.maps.Marker({ //this itself produces a marker onto the map
					map: map,
					position: latlng[i],
					icon: image
				});
            markers.push(marker);	
            attachInfoWindow(marker, InfoWindowContent[i]);            
			}  
		}
    }	
    
    function attachInfoWindow(marker, address) {
        
        var infowindow = new google.maps.InfoWindow({
          content: address        
        });
        
        marker.addListener('click', function() {
          infowindow.open(map, marker);
        });
    }	
	function centerMap() {
		map.setCenter(toronto);
    }
	

    function doNothing() {}
    </script>
    <script async defer
		src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDfsoh48H-SKFU3dv2EcmQihtex9uO_JdA
		&callback=initMap">
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
