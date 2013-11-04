#!/bin/sh

rm maps/*.b.txt
rm maps/*.w.txt
./angKomando.bin > world.raw

./generateMaps.py

cp world.raw maps

firefox displayWorld.html
