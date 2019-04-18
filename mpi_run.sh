# run server
python3 init_server.py --n $1 --v 1 &

for ((i = 0; i < "$(($1 + 1))"; i++))
do
    python3 $2 &
done