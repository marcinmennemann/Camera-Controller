<?php

	$file = "data/record_state.txt";

	$serverkey = "cameracontroller";
	$clientkey = $_GET["authkey"];
	$method = $_GET["method"];
	$text = $_GET["text"];

	if(strcmp($serverkey, $clientkey) == 0){
		if(strcmp($method, "STATE") == 0){
			echo("True");
		}
		if(strcmp($method, "START_RECORD") == 0){
			echo("START");
			$handlewriter = fopen($file, "w");
			fwrite($handlewriter, "true");
			fclose($handlewriter);
		}
		if(strcmp($method, "STOP_RECORD") == 0){
			echo("STOP");
			$handlewriter = fopen($file, "w");
                        fwrite($handlewriter, "false");
                        fclose($handlewriter);

		}
		if(strcmp($method, "DOWNLOAD") == 0){
			echo("STOP");
			$handlewriter = fopen($file ,"w");
			fwrite($handlewriter, "download");
			fclose($handlewriter);
		}
		if(strcmp($method, "SUMMARY") == 0){
			$handlereader = fopen("data/message.txt", "r");
			echo (fread($handlereader, filesize("data/message.txt")));
			fclose($handlereader);
		}
		if(strcmp($method, "GET") == 0){
			$handlereader = fopen($file, "r");
			echo (fread($handlereader, filesize($file)));
			fclose($handlereader);
		}
		if(strcmp($method, "STD") == 0){
			$handlewriter = fopen("data/message.txt", "w")or die("hik");
			fwrite($handlewriter, $text);
			fclose($handlewriter);
			echo("hi");
		}
	}


?>
