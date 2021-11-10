<html>
<head>
<title>Image Compression</title>
</head>
<body>
<p> Image Compression <br/> </p>
<form action="index.php" enctype="multipart/form-data" method="post">
Select image to compress: <input type="file" name="file"><br/><br/>
Singular value used: <input type="text" name="fname"><br/>
<input type="submit" value="Submit" name="Submit"><br/>
</form>

<?php
$filepath="";
$compressed="";
if(isset($_POST['Submit'])){ 
	global $filepath;
	global $compressed;
	$filepath = "images/" . $_FILES["file"]["name"];
	$compressed="images/compressed_" . $_FILES["file"]["name"];
	if(move_uploaded_file($_FILES["file"]["tmp_name"], $filepath)) {
		echo "Original Image: <br/>";
		echo "<img src=".$filepath." height=360> <br/>";
	} 
	else {
		echo "Error !!";
	}
	$compressed="images/compressed_" . $_FILES["file"]["name"];
	$singular=$_POST["fname"];
	$command = "py backend.py ". $filepath." ".$compressed." ".$singular;
	$time=exec($command);
	echo "<p> Compressed Image: <br/> </p>";
	$type="button";
	echo "<a href=".$compressed." download=><button type=".$type.">Download</button></a><br/><br/>";
	echo "<img src=".$compressed." height=360><br/>";
	echo "Compression time: ".$time." seconds";
}

?>

</body>
</html>