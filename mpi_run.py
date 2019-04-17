import subprocess
import argparse
import time

# parse option with number of clients
parser = argparse.ArgumentParser()
parser.add_argument("--s", help="python script (source code)")
parser.add_argument("--n", help="maximum of clients")
args = parser.parse_args()
MAX_NUM_OF_CLIENTS = int(args.n)
PYTHON_SCRIPT_NAME = args.s

subprocess.Popen(['./server_mega.py', '--n', str(MAX_NUM_OF_CLIENTS)])

for i in range(MAX_NUM_OF_CLIENTS):
    subprocess.Popen(['./' + PYTHON_SCRIPT_NAME])