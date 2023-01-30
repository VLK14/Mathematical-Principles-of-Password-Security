#!/bin/sh
if [ $# -eq 0 ]
then
        printf "Missing Word Size.\nUsage: $0 <Word Size> <Input File> <Output File>\n"
        exit
elif [ $# -eq 1 ]
then
        printf "Missing Input File.\nUsage: $0 <Input File> <Output File>\n"
        exit
elif [ $# -eq 2 ]
then
	printf "Missing Output File.\nUsage: $0 <Input File> <Output File>\n"
        exit
fi
grep -x '.\{'$1'\}' $2 > $3