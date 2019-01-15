<?php
//require("phpsqlajax_dbinfo.php"); //wasn't working, but it was just holding the username stuff below anyways
$username="root";
$password="";
$database="dumpstersite";
//using php's echo to output XML
function parseToXML($htmlStr)
{
$xmlStr=str_replace('<','&lt;',$htmlStr);
$xmlStr=str_replace('>','&gt;',$xmlStr);
$xmlStr=str_replace('"','&quot;',$xmlStr);
$xmlStr=str_replace("'",'&#39;',$xmlStr);
$xmlStr=str_replace("&",'&amp;',$xmlStr);
return $xmlStr;
}

// Opens a connection to a MySQL server
$connection=mysqli_connect ('localhost', $username, $password);
if (!$connection) {
  die('Not connected : ' . mysqli_error($connection));
}

// Set the active MySQL database
$db_selected = mysqli_select_db($connection,$database); //needed to be connection first (link) then the database name
if (!$db_selected) {
  die ('Can\'t use db : ' . mysqli_error($connection));
}

// Select all the rows in the markers table
$query = "SELECT * FROM markers WHERE 1";
$result = mysqli_query($connection, $query);
if (!$result) {
  die('Invalid query: ' . mysqli_error($connection));
}

header("Content-type: text/xml");

// Start XML file, echo parent node
echo "<?xml version='1.0' ?>";
echo '<markers>';
$ind=0;
// Iterate through the rows, printing XML nodes for each
while ($row = @mysqli_fetch_assoc($result)){
  // Add to XML document node
  echo '<marker ';
  echo 'id="' . $row['id'] . '" ';
  echo 'priority="' . $row['priority'] . '" ';
  //if(isset($_POST['date'])){ $name = $_POST['date']; }
  echo 'date="' . parseToXML($row['date']) . '" ';
  echo 'time="' . parseToXML($row['time']) . '" ';
  echo 'address="' . parseToXML($row['address']) . '" ';
  echo 'lat="' . $row['lat'] . '" ';
  echo 'lng="' . $row['lng'] . '" ';
  echo 'availability="' . $row['availability'] . '" ';
  echo '/>';
  $ind = $ind + 1;
}

// End XML file
echo '</markers>';

?>