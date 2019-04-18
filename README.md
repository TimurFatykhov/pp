# Semi MPI
---
### HOW TO (all OS)
#### Run server first
```
python3 init_server.py --n **number_of_processes** --v **verbose**
```
If ```verbose``` is 1, then server will print logs.
#### Run processes
```
python3 my_smpi_script.py
```
---
### HOW TO (unix)
#### Run shell
```
sh mpi_run.sh **number_of_processes** **verbose** **script_name**
```
If ```verbose``` is 1, then server will print logs.
Example:
```
sh mpi_run.sh 2 0 script.py
```

