<html>
<head>
	<title>Image Compression</title>
	<link rel="stylesheet" href="style.css">
</head>
<body>
	<h1>Image Compression</h1><hr>
	<form action="index.php" enctype="multipart/form-data" method="post">
		Select image to compress: <input type="file" name="file"><br><br>
		Singular value used: <input type="text" name="fname"><br><br>
		<input type="submit" value="Submit" name="Submit"><br>
	</form>

<?php
if(isset($_POST['Submit'])){ 
	$file=str_replace(' ', '-', $_FILES["file"]["name"]);
	$filepath = "images/" . $file;
	$compressed="images/compressed_" .$file;
	if(move_uploaded_file($_FILES["file"]["tmp_name"], $filepath)) {
		echo "Original Image: <br/><br/>";
		echo "<img src=".$filepath." height=360> <br/>";
	} 
	else {
		echo "Error!!! <br/>";
	}
	$singular=$_POST["fname"];
	$command = "py backend.py ". $filepath." ".$compressed." ".$singular;
	$time=exec($command);
	echo "<p> Compressed Image: <br/> </p>";
	$type="button";
	echo "<a href=".$compressed." download=><button type=".$type.">Download</button></a><br/><br/>";
	echo "<img src=".$compressed." height=360><br/><br/>";
	echo "Compression time: ".$time." seconds";
}
?>

</body>
</html>