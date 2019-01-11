<?php
/**
 * Template Name: SQL Table
 *
 * This template is used to demonstrate how to use Google Maps
 * in conjunction with a WordPress theme.
 *
 * @since          Twenty Fifteen 1.0
 *
 * @package        Acme_Project
 * @subpackage     Twenty_Fifteen
 */
get_header();
?> <!––gives the side bar––>

    <style type="text/css">
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

$sql = "SELECT id, date, time, address, lat, lng, availability FROM markers ORDER BY id ASC";
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
    echo "<table><tr><th>ID</th><th>Date</th><th>Time</th><th>Address</th><th>Latitude</th><th>Longitude</th><th>Availability</th></tr>";
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo "<tr><td>" . $row["id"]. "</td><td>" . $row["date"]. "</td><td> " . $row["time"].  "</td><td> " . $row["address"].  "</td><td> " . $row["lat"].  "</td><td> " . $row["lng"].  "</td><td> " . $row["availability"]. "</td></tr>";
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
