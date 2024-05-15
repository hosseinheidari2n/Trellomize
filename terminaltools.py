import os
import sys
import subprocess

def cls():
    os.system("cls")
"bruh".encode()

#TBI
def vim_as_input():
    result = subprocess.run(['vim', '-c', 'qa!'], capture_output=True, text=True)
    return result.stdout

#testing
vim_as_input()