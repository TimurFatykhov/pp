# Semi MPI
### How to (all OS)
#### Run server first
```
python3 init_server.py --n **number_of_processes** --v **verbose**
```
If ```verbose``` is 1, then server will print logs. If set to 0 won't.
#### Run processes
```
python3 my_smpi_script.py
```
<br><br><br>
### How to (unix)
#### Run shell
```
sh mpi_run_bash.sh **number_of_processes** **verbose** **script_name**
```
If ```verbose``` is 1, then server will print logs. If set to 0 won't.
<br><br>Example:
```
sh mpi_run.sh 2 0 script.py
```

