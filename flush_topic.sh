#!/bin/bash

for a in {0..99}
do
#	#echo "$a"
	#/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --topic test
	/usr/local/kafka/bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic video$a
done    

#/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
