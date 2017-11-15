from queue import Queue,Empty
from threading import Thread
import socket,sys,errno

BUFLN = 1000

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except:
	print("Cannot open socket")
	sys.exit(1)

try:	
	s.bind(('', int(sys.argv[1])))
except:
	print("Cannot bind socket to port")
	sys.exit(1)

class Receiver(Thread):
	def __init__(self, queue):
		Thread.__init__(self)
		self.queue = queue

	def run(self):
		while True:
			data, addr = s.recvfrom(BUFLN)
			self.queue.put(data.decode())

def main():
	queue = Queue()
	receiver = Receiver(queue)
	receiver.daemon = True
	receiver.start()

	print("Welcome to the chat app!\nMake a selection:\ns)end\np)rint\nq)uit\n")
	cmd = input('Choice: ')
	while(cmd[0] != 'q'):
		if(cmd[0] == 'P' or cmd[0] == 'p'):
			try:
				while(True):
					msg = queue.get(False, None)
					print(msg)
			except Empty:
				print('**End of messages**\n')
		if(cmd[0] == 'S' or cmd[0] == 's'):
			# str = input("Enter your message: ")
			str = cmd[2:]
			b = str.encode()
			s.sendto(b, (sys.argv[2], int(sys.argv[3])))
		cmd = input('Choice: ')
	print("Thank you")
main()