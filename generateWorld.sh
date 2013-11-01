#!/bin/sh

rm maps/*.b.txt
rm maps/*.w.txt
./angKomando.bin > world.raw

/opt/lampp/bin/php ./generateMaps.php
#php ./generateMaps.php

cp world.raw maps

firefox displayWorld.html
