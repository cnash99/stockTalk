<?php

$filename = "companylist.csv"; //example name for your CSV file with classes - this file would exist in the same directory as this PHP file
$classArray = array(); //declare an array to store your classes

if (($handle = fopen($filename, "r")) !== FALSE) {

while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
    foreach($data as $v) { //loop through the CSV data and add to your array
    array_push($classArray, $v);         
    }
  }    
}
?>

<div class="CourseInfo">
<div class="Add">
<span>
COMPANIES TO BE ADDED:
<table>
<tbody>
<tr>
<th style="width: 5%">Symbol</th>
<th style="width: 40%;">Name</th>
</tr>
<div id="courseTable">
<tr>
<td>##</td>
<td><input list="courses" name="course" placeholder="Course">
<datalist id="courses">
<?php 

for ($i = 0; $i < count($classArray); $i++) { // this is embedded PHP that allows you to loop through your array and echo the values of the PHP array within an HTML option tag
echo "<option value='$classArray[$i]'>";    
}

?>
</datalist></td>
</datalist></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</div>
<tr>
<td>##</td>
<td><input list="courses" name="course" placeholder="Course">
<datalist id="courses">
<?php 

for ($i = 0; $i < count($classArray); $i++) {
echo "<option value='$classArray[$i]'>";    
}

?>
</datalist></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>##</td>
<td><input list="courses" name="course" placeholder="Course">
<datalist id="courses">
<?php 

for ($i = 0; $i < count($classArray); $i++) {
echo "<option value='$classArray[$i]'>";    
}

?>
</datalist></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>