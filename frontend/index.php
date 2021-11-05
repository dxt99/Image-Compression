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
if(isset($_POST['Submit1']))
{ 
$filepath = "images/" . $_FILES["file"]["name"];

if(move_uploaded_file($_FILES["file"]["tmp_name"], $filepath)) 
{
echo "<img src=".$filepath." height=480>";
} 
else 
{
echo "Error !!";
}
} 
?>

</body>
</html>