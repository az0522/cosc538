# use tls handshake to test SNI-censorship
import subprocess, time
from queue import Queue


def handshake(SNI_QUEUE, help_ip):
	i = 1
	while not SNI_QUEUE.empty():
		sni = SNI_QUEUE.get()
		# tls
		sp = subprocess.Popen("openssl s_client -state -connect %s -servername %s -tls1_3" % (help_ip, sni), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
		sp.stdin.close()
		# for line in sp.stdout:
		# 	output = line.rstrip().decode('UTF-8')
		# 	print(output)
		print(i, " done")
		i += 1
		time.sleep(2)


if __name__ == '__main__':
	time.sleep(2)
	start_time = time.time()
	SNI_QUEUE = Queue()
	help_ip = '172.217.160.68:443'

	with open('hostname_list.txt', 'r') as f:
		for line in f.readlines():
			line = line.strip()
			SNI_QUEUE.put(line)

	handshake(SNI_QUEUE, help_ip)

	print('Elapsed Time：%s' % (time.time() - start_time))
