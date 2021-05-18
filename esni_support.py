# the file is used to check if the top 250 websites has /cdn-cgi/trace page

import subprocess, time
from queue import Queue


def esni_support(top250_queue):
	i = 0
	result = []
	while not top250_queue.empty():
		hostname = top250_queue.get()
		cmd = "curl https://" + hostname + "/cdn-cgi/trace -I"
		sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
		sp.stdin.close()
		result.append([hostname])
		for line in sp.stdout:
			line = line.strip().decode('UTF-8')
			result[i].append(line)
			# print(line)
		print(i, " done")
		i += 1
		time.sleep(1)

	with open('esni_india_candidate_50_result.txt', 'w', newline='', encoding='utf-8') as f:
		j = 0
		for l in result:
			f.write(str(j) + '\n')
			j += 1
			for e in l:
				f.write(e + '\n')
			f.write('\n')


if __name__ == '__main__':
	time.sleep(2)
	start_time = time.time()
	top250_queue = Queue()

	with open('esni_india_candidate_50.txt', 'r', encoding='utf-8') as f:
		for line in f.readlines():
			line = line.strip()
			top250_queue.put(line)

	esni_support(top250_queue)

	print('Elapsed Time：%s' % (time.time() - start_time))
