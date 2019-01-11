<?php
/**
 * Template Name: Google Maps API SQL version2
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

    <style type="text/css">

    #map {
        
        width:    100%;
        height:   750px;
        
    }
    </style>

    <div id="map"></div>

    <script>
	
        function initMap() {
        var map = new google.maps.Map(document.getElementById('map'), {
          center: new google.maps.LatLng(43.65, -79.403),
          zoom: 13
        });
        
          // Change this depending on the name of your PHP or XML file
          downloadUrl('http://localhost/DumpsterSite/wp-content/themes/twentyfifteen/SQLtable-script.php', function(data) {
            var xml = data.responseXML;
            var markers = xml.documentElement.getElementsByTagName('marker');
            Array.prototype.forEach.call(markers, function(markerElem) { //this is techinically the loop
              var id = markerElem.getAttribute('id');
              var date = markerElem.getAttribute('date');
			  var time = markerElem.getAttribute('time');
              var address = markerElem.getAttribute('address');
              var point = new google.maps.LatLng(
                  parseFloat(markerElem.getAttribute('lat')),
                  parseFloat(markerElem.getAttribute('lng')));
			  var availability = markerElem.getAttribute('availability');
              var infowincontent = document.createElement('div');
			  
			  //Info window content
              var strong = document.createElement('strong');
              strong.textContent = name
              infowincontent.appendChild(strong);
              infowincontent.appendChild(document.createElement('br'));

			  /*var text2 = document.createElement('text2');
			  text2.textContent = "ID:";
			  infowincontent.appendChild(text2);
			  
			  var text_id = document.createElement('text');
              text_id.textContent = id;
			  infowincontent.appendChild(text_id);
			  
			  var text2 = document.createElement('text2');
			  text2.textContent = " Address: ";
			  infowincontent.appendChild(text2);
			  
			  var text3 = document.createElement('text3');
			   text3.textContent = address;
			   infowincontent.appendChild(text3); */
			 
			 var testtext = "ID: "
			var contentString = 
		
			'<div id="content">'+
			  '<div id="siteNotice">'+
			  '</div>'+
			'<div id="bodyContent">'+
			'<p><b>ID#: </b>' + id + '<b> Address: </b>'+ address +'</p>'
			+'<b>Availability: </b>' + availability +
			'</div>'+
			'</div>';
			
						
              //var icon = customLabel[date] || {}; //icon is declared by default
			  var image1 = 'http://maps.google.com/mapfiles/kml/paddle/grn-blank.png';
			   var image2 = 'http://maps.google.com/mapfiles/kml/paddle/ylw-blank.png';
			   var image3 = 'http://maps.google.com/mapfiles/kml/paddle/red-blank.png';
			   
			  if (availability < 30){
				  image = image1;
			  }else if((availability >=30) && (availability <=60)){
				  image = image2;
			  }else {
				  image = image3;
			  }  
			   
              var marker = new google.maps.Marker({
                map: map,
                position: point,
                
				icon: image
			  });
			  //content box
			  //var infoWindow = new google.maps.InfoWindow;
			    var infoWindow = new google.maps.InfoWindow({
					content: contentString,
					 maxWidth: 150
				});
		
              marker.addListener('click', function() {
                //infoWindow.setContent(infowincontent);
                infoWindow.open(map, marker);
              });
            });
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
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyA-y5nufBunnq4ne8E8TMLyCpTkrKVxvvI&callback=initMap">
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
