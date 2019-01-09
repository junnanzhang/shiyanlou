import sys
import getopt
import re
import socket

def test():
	opts, args = getopt.getopt(sys.argv[1:], '-h-p',['host=','port='])
	host = None
	port = None

	for opt_name, opt_value in opts:
		if opt_name in ('-h', '--host'):
			if opt_value == None:
				print('Parameter Error')
				return
			host = opt_value

		if opt_name in ('-p', '--port'):
			if opt_value == None:
				print('Parameter Error')
				return
			port = opt_value

	if host == None or port == None:
		print('Parameter Error')
		return
	res = re.findall(r'\d+\.\d+\.\d+\.\d+', host)
	if len(res) == 0:
		print('Parameter Error')
		return

	portArr = port.split('-')
	s = socket.socket()
	s.settimeout(0.1)

	if len(portArr) == 2:
		for item in range(int(portArr[0]), int(portArr[1])):
			try:
				s.connect((host, int(item)))
				print('{0} open'.format(item))
			except:
				print('{0} closed'.format(item))
	elif len(portArr) == 1:
		try:
			s.connect((host, int(port)))
			print('{0} open'.format(port))
		except:
			print('{0} closed'.format(port))




if __name__ == '__main__':
	test()