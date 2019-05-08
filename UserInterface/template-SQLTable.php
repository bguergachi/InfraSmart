<?php
/**
 * Template Name: SQL Table
 *
 * April 3 - changed database name
 *
 * @since          Twenty Nineteen 1.0
 *
 * @package        Acme_Project
 * @subpackage     Twenty_Fifteen
 */
get_header();
?> <!––gives the side bar––>
<h1><b>Dumpster Location Table </b></h1>
<h5>Displays the location of dumpsters in table format</h5>
    <style type="text/css">
	table,td, tr {
	  border: 1px solid #dddddd;
	  text-align: left;
	  padding: 8px;
	  margin-left: 30px;
	  
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

$sql = "SELECT DeviceNumber, CollectTime, Address, Lat, Lng, DataType, Data FROM sensordata ORDER BY DeviceNumber ASC";
$result = $conn->query($sql);
?>

<?php
// Start the loop.
while (have_posts()):
    the_post();

    // Include the page content template.
    get_template_part('content', 'page');

	//output the table
    if ($result->num_rows > 0) {
    //echo "<table><tr><th>ID</th><th>Date</th><th>Time</th><th>Address</th><th>Latitude</th><th>Longitude</th><th>Availability (0-1) </th><th>Day of the Week</th></tr>";
		echo "<table><tr><th>Device Number</th><th>CollectTime</th><th>Address</th><th>Lat</th><th>Lng</th><th>DataType</th><th>Data (0-1) </th></tr>";

	// output data of each row
    while($row = $result->fetch_assoc()) {
        echo "<tr><td>" . $row["DeviceNumber"]. "</td><td>" . $row["CollectTime"]. "</td><td> " . $row["Address"].  "</td><td> " . $row["Lat"].  "</td><td> " . $row["Lng"].  "</td><td> " . $row["DataType"].  "</td><td> " . $row["Data"]. "</td><td> " . $row["DayOfTheWeek"]. "</td></tr>";
    }
    echo "</table>";
} else {
    echo "0 results";
}

$conn->close();
    // If comments are open or we have at least one comment, load up the comment template.
    if (comments_open() || get_comments_number()):
        comments_template();
    endif;
// End the loop.
endwhile;
?>
       
    <?php
get_footer();
?>
