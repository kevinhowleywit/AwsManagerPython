import sys
import subprocess

print("Returning Information............")
print("---------------------------------")

subprocess.run('vmstat', shell=True)
print("---------------------------------")
subprocess.run('ps', shell=True)
print("---------------------------------")
subprocess.run('netstat', shell=True)
print("---------------------------------")
