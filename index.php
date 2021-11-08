<html>
<head>
<title>Image Compression</title>
</head>
<body>
<p> Image Compression <br/> </p>
<form action="index.php" enctype="multipart/form-data" method="post">
Select image to compress:
<input type="file" name="file"><br/>
<input type="submit" value="Upload" name="Submit1"> <br/>


</form>
<?php
if(isset($_POST['Submit1'])){ 
	$filepath = "images/" . $_FILES["file"]["name"];
	$compressed="images/compressed_" . $_FILES["file"]["name"];
	if(move_uploaded_file($_FILES["file"]["tmp_name"], $filepath)) {
		echo "<img src=".$filepath." height=360> <br/>";
		$command = "py backend.py ". $filepath." ".$compressed;
		$time=exec($command);
		echo "<p> Compressed Image: <br/> </p>";
		$type="button";
		echo "<a href=".$compressed." download=><button type=".$type.">Download</button></a><br/>";
		echo "<img src=".$compressed." height=360><br/>";
		echo "Compression time: ".$time." seconds";
	} 
	else {
		echo "Error !!";
	}
}
?>

</body>
</html>