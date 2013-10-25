<?php

function generateMap($mapx, $mapy, $world) {
    $mapWidth = 30;
    $mapHeight = 15;

	$posX = 0;
	$posY = 0;
	$posZ = 0;

    $map = "";

	$posYStart = ( ( 640 * $mapHeight ) * $mapy ) + ($mapWidth * $mapx);

	for($y = 0; $y < $mapHeight; $y++) {
		$posY = $posYStart + (640 * $y);
		for($x = 0; $x < $mapWidth; $x++) {
			$posX = $x;
			$posZ = $posY + $posX;
		
			if(strcmp(".", $world[$posZ]) == 0) {
				$map .= "00:";
            } else {
				$map .= "01:";
	    	}
	    }
    }

    return substr($map, 0, -1);
}

function saveMap($mapId, $mapData) {

    // Create background map
    $mapTmp = "";
	if($fp = fopen("./maps/$mapId.b.txt", "w+")) {
        $dataArr = explode(":",  $mapData);
        $count = 0;
        foreach ($dataArr as $data) {
            // Define the background
            $data = "00";            

            $mapTmp .= $data;
            if($count == 29) {
                $mapTmp .= "\n";
                $count = 0;
            } else {
                $mapTmp .= ":";
                $count++;    
            }
        }
		fwrite($fp, $mapTmp);
	} else {
		echo "Failed to save\n";
    }
	fclose($fp);

    // Create wall map
    $mapTmp = "";
	if($fp = fopen("./maps/$mapId.w.txt", "w+")) {
        $dataArr = explode(":",  $mapData);
        $count = 0;
        foreach ($dataArr as $data) {
            // Define the background
            $mapTmp .= $data;
            if($count == 29) {
                $mapTmp .= "\n";
                $count = 0;
            } else {
                $mapTmp .= ":";
                $count++;    
            }
        }
		fwrite($fp, $mapTmp);
	} else {
		echo "Failed to save\n";
    }
	fclose($fp);
}

// Tile size  = 
//      width  : 32px 
//      height : 32px

// Map image size =
//      width  : 32 * 30 = 960
//      height : 32 * 15 = 480

function saveMapImage($mapId, $mapData ) {
	$tiles = explode(":", $mapData);

	$imageTmp = @ImageCreateTrueColor(960, 480); 
    $imageTmpMini = @ImageCreateTrueColor(960 / 10, 480 / 10);

	$r = 0 ;
	$c = 0 ;

	for($i = 0; $i< (15 * 30); $i++) {

        if(trim($tiles[$i] == "00")) {
	    	$tileImage = "./sprites/ground/floors_3.png";
        }

        if(trim($tiles[$i] == "01")) {
	    	$tileImage = "./sprites/wall/int_wall_bricks.png";
        }

		$source = @imagecreatefrompng($tileImage);

		if( $i % 30 == 0) {
			$imageTmpY = $r * 32;
			$r++;
			$c = 0;
		}
		$imageTmpX = $c * 32;
		$c++;
		@imagecopy($imageTmp, $source, $imageTmpX, $imageTmpY, 0, 0, 32, 32);
	}

	$mapImage = "./maps/" . $mapId . ".png";
	@imagepng($imageTmp, $mapImage);

    $mapImage = "./maps/" . $mapId . "_mini.png";
    @imagecopyresized($imageTmpMini, $imageTmp, 0, 0, 0, 0, 960 / 10, 480 / 10, 960, 480);
    @imagepng($imageTmpMini, $mapImage);
}

/*

// Refactor this function
function insertDB($carte_mini_num,$carte_mini ) {

	$table = "fjr";
	include("../../config.php");
	@mysql_connect("$dbhost","$dbuser","$dbpasswd");
	$select_base=@mysql_selectdb("$dbname"); 
	echo "Serveur : $dbhost <br> Nom de la base de donnée : $dbname <br><br>";
	$carte_mini = substr($carte_mini, 0, strlen($carte_mini)-1);
 
	if (!$select_base) {
		echo "<br><br><font color=\"#CC0000\"><b>Mauvaise configuration!!! </b></font><br>  
Vérifiez que votre login et mot de passe sont bien saisi pour la connexion 
à la base <b>$base</b>"; 
	} else {
		$result = mysql_db_query($dbname,"UPDATE ".$table."_quest_maps SET map_data='$carte_mini' WHERE id= $carte_mini_num ");

		echo "Requete : <br>";
		echo "UPDATE ".$table."_quest_maps SET map_data='$carte_mini' WHERE id=$carte_mini_num ";
		echo "<br>";

		if ($result < 1) {
			echo "<br>Pas de mise-à-jour de le carte $carte_mini_num dans la table fjr <br>";
			echo "requete : <br>";
			echo "";
		} else {
			echo "<br>Mise-à-jour de la carte $carte_mini_num de la table fjr de la base de donnée fjr<br>";
			echo "Donnees à insérer : <br>";
		}
	}
	mysql_close();
}
*/

// Initialize the world
$width  = 640; // 640 / 30 = (30 * 21) + 10
$height = 480; // 480 / 15 = (15 * 32) 

for($h = 0; $h < $height; $h++) {
	for($w = 0; $w < 640; $w++) {
		$world[($h * 640) + $w] = ".";
		}
	}

// Create world in one dimension array
if($fp = fopen("world.raw", "r")) {
	while( $data = fgets($fp, 30)) {
		$posArr = explode(":", $data);
		$position = 640 * $posArr[2] + $posArr[1];
		$world[$position] = "@";
		if(strcmp($posArr[0], "h") == 0) {
			$world[$position+1] = "@";
			$world[$position+2] = "@";
		}
		if(strcmp($posArr[0],"v") == 0) {
			$world[$position+640] = "@";
			$world[$position+1280] = "@";
			$world[$position+1920] = "@";
		}
	}
}

fclose($fp);


// Height of world in map = 32 
for($y = 0; $y < 32; $y++) {
    // Width of world in map = 21 
    for($x = 0; $x <21; $x++) {
	    $mapx = $x;
	    $mapy = $y;

	    $mapid = $mapy * 21 + $mapx;
	    $mapdata = generateMap($mapx, $mapy, $world);
	    saveMap($mapid, $mapdata);
	    saveMapImage($mapid, $mapdata);
	    //insertDB($mapid, $mapdata );	
    }
}

?>

