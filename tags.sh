#!/bin/sh
for file in `ls ./data`
do
	echo ./data/${file} | python3 partition.py > ./tags/${file}
done