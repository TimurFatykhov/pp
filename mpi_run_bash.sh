#!/bin/bash

python3 init_server.py --n $1 --v $2 &

for ((i = 0; i < "$(($1))"; i++))
do
    python3 $3 &
done
wait