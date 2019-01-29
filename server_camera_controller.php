<?php
	$method = $_GET["method"];


	if(strcmp($method, "STATE") == 0){
		echo("True");
	} else {
		echo("False");
	}
?>
