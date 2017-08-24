#!/bin/sh
for file in `ls ./data`
do
	echo ./data/${file} | python3 cluster.py > ./cluster/${file}
done
