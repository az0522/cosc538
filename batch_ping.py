# ping test for all potentially hostnames
from queue import Queue
import threading
import subprocess
import time
import csv


# threads
THREADS = 60


# Add hostnames to queue from file
Name_QUEUE = Queue()
with open('potentially_blocked_6.txt', 'r') as f:
	for line in f.readlines():
		line = line.strip()
		Name_QUEUE.put(line)



# ping function
def ping_ip(result):
	i = 1
	while not Name_QUEUE.empty():
		name = Name_QUEUE.get()
		# res = subprocess.call('ping -n 3 -w 100 %s' % ip,stdout=subprocess.PIPE)  # linux 系统将 '-n' 替换成 '-c'
		p = subprocess.Popen('ping -n 2 %s' % name, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		pingStatus = 'ok'
		for line in p.stdout:
			output = line.rstrip().decode('UTF-8')
			# print(output)
			if output.endswith('unreachable.'):
				pingStatus = 'unreacheable'
				break
			elif output.startswith('Ping request could not find host'):
				pingStatus = 'host_not_found'
				break
			elif output.startswith('Request timed out.'):
				pingStatus = 'timed_out'
				break

		result[name] = pingStatus
		print(i, ": ", name, ": ", result[name])
		i += 1

	# Save result
	with open('result6.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		for key, value in result.items():
			# print(key, "", value)
			writer.writerow([key, value])


if __name__ == '__main__':
	start_time = time.time()
	threads = []
	result = {}

	for i in range(THREADS):
		thread = threading.Thread(target=ping_ip(result))
		thread.start()
		threads.append(thread)

	for thread in threads:
		thread.join()

	print('Elapsed Time：%s' % (time.time() - start_time))
# print("Result Dict: ", result)
