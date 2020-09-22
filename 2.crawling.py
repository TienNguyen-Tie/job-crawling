import threading
import time
import glob
import subprocess
import os

cp = os.getcwd()

class SingleThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter 

    def run(self):
        print(f'Start running {cp}{self.name}')
        subprocess.run(["python3", f'{cp}{self.name}'])
        
        print("Exiting " + self.name)


scripts = glob.glob("./outputs/*.py")

threads = []
count = 1
for script in scripts:
    init_thread = SingleThread(count, f'{script[1:]}', count)
    count = count+1
    init_thread.start()
    threads.append(init_thread)

for t in threads:
    t.join()

print("Exiting Main Thread")

subprocess.run(["mv", "./*.csv", "./outputs-csv"])