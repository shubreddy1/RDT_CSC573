from socket import *
import os
import pickle
import signal
import thread
from threading import Thread
from time import sleep
import datetime
from random import randint
import hashlib

prob=0.05
l=len(str(prob))
for x in range(2,l):
	prob*=10
filename='rfc2.txt'
#signal.signal(signal.SIGALRM,handler)
serverPort = 12003
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(("10.0.0.1",12003))
serverSocket.listen(1)
connectionSocket, addr = serverSocket.accept()
sentence = connectionSocket.recv(1024+64)
seq=1
f=open(filename,'wb')
while "e_c01" not in sentence:
	#print seq,"      ",sentence[:100]
	l=randint(0,100)
	header1=sentence[:32]
	#print header1
	header1=str(header1)
	hd1=int(header1,2)
	header1=hd1
	header2=sentence[32:48]
	header3=sentence[48:64]
	sentence=sentence[64:]
	#print "checking packet"
	if l>prob and seq==header1:
		print "wrote packet ",seq
		f.write(sentence)
		header1=format(seq,'032b')
		header2="0000000000000000"
		header3="1010101010101010"
		seq+=1
		connectionSocket.send(header1+header2+header3)	
	else:
		print "discarded packet ",seq, " cause ",l,"less than ",prob
	sentence=connectionSocket.recv(1024+64)
#print sentence
header1=format(seq,'032b')
header2="0000000000000000"
header3="1010101010101010"
seq+=1
connectionSocket.send(header1+header2+header3)
sentence=sentence[64:-5]
f.write(sentence)
connectionSocket.close()

