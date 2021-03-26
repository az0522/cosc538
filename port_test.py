# use telnet to test port open or not
import socket, csv, time
from queue import Queue

socket.setdefaulttimeout(1)

# port 80 test
def PortOpen_80(name):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((name, 80))
		s.shutdown(1)
		print(name, ' 80: ', 'ok')
		return 0
	except socket.timeout:
		print(name, ' 80: ', 'timeout')
		return 1

	except:
		print(name, ' 80: ', 'other error')
		return 2


# port 443 test
def PortOpen_443(name):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((name, 443))
		s.shutdown(1)
		print(name, ' 443: ', 'ok')
		return 0

	except socket.timeout:
		print(name, ' 443: ', 'timeout')
		return 1

	except:
		print(name, ' 443: ', 'other_error')
		return 2


# port test
def PortOpen(Name_QUEUE, result):
	while not Name_QUEUE.empty():
		name = Name_QUEUE.get()
		result_80 = ''
		result_443 = ''

		test_80 = PortOpen_80(name)
		if test_80 == 0:
			result_80 = 'ok'
		elif test_80 == 1:
			result_80 = 'timeout'
		elif test_80 == 2:
			result_80 = 'other_error'

		test_443 = PortOpen_443(name)
		if test_443 == 0:
			result_443 = 'ok'
		elif test_443 == 1:
			result_443 = 'timeout'
		elif test_443 == 2:
			result_443 = 'other_error'

		result[name] = [result_80, result_443]

	# print(result)


if __name__ == '__main__':
	start_time = time.time()
	Name_QUEUE = Queue()
	result = {}

	# read hostname list
	with open('potentially_blocked_5.txt', 'r') as f:
		for line in f.readlines():
			line = line.strip()
			Name_QUEUE.put(line)

	# run port test
	PortOpen(Name_QUEUE, result)

	# save test result
	with open('result_telnet5.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		for key, value in result.items():
			# print(key, "", value)
			writer.writerow([key, value[0], value[1]])

	print('Elapsed Time：%s' % (time.time() - start_time))
