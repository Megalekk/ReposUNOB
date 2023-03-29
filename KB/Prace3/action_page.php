<html>
<body>
Vitejte <?php echo $_POST["name"]; ?><br><br>
Tvuj email je: <?php echo $_POST["email"]; ?><br><br>
Zvolene jidlo: <?php echo  $_POST["jidlo"]; ?> <br><br>
Mas ho rad protoze: <?php echo  $_POST["proc"]; ?> <br><br>
<?php 
if (isset($_POST['vehicle1'])) {
	$option1 = $_POST['vehicle1'];
	echo "Vlastnis kolo";
}
if (isset($_POST['vehicle2'])) {
	$option2 = $_POST['vehicle2'];
	echo "Vlastnis auto";
}
if (isset($_POST['vehicle3'])) {
	$option2 = $_POST['vehicle3'];
	echo "Vlastnis lod";
}
?><br><br>

<?php if (isset($_POST['color'])) {
	$color = $_POST['color'];
	echo "Preferujete barvu: $color";
} 
?><br>

</body>
</html>