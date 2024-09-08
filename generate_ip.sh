#!/bin/bash

if [ -z "$1" ]; then
	echo "Please enter the count that you want to generate."
	exit 1
fi

count=$1
src_ip=$2

> src_ip.txt #clean the file

if [ -n "$src_ip" ]; then
	for i in $(seq 1 $count); do
		echo $src_ip >> src_ip.txt
	done
	echo "$count identical IPs have been added to the file."
else
	for i in $(seq 1 $count); do
		third=$((RANDOM % 255))
		fourth=$((RANDOM % 255))
		echo "192.168.$third.$fourth" >> src_ip.txt
	done
	echo "$count random IPs have been added to the file."
fi
