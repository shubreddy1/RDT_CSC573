from socket import *
import os
import pickle
import signal
import thread
from threading import Thread
from time import sleep
import datetime
import time
from random import randint
import hashlib
import sys

if len(sys.argv)<4:
	print "insufficient arguments"
	exit(1)
port = int(sys.argv[1])
filename=sys.argv[2]
prob=float(sys.argv[3])
#print port,filename,prob
#prob=0.05
prob*=100
prob=int(prob)
print prob
#filename='rfc2.txt'
#signal.signal(signal.SIGALRM,handler)
#serverPort = 12003
serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(("10.0.0.3",port)) #type in the IP of the PC on which the server is executing
sentence,addr = serverSocket.recvfrom(16)
mss=int(sentence,2)
print mss
sentence,addr = serverSocket.recvfrom(mss+64)
cspair=addr
tarr=""
seq=1
f=open(filename,'wb')
start_time=time.time()
while "e_c01" not in sentence:
	#print seq,"      ",sentence[:100]
	l=randint(0,100)
	header1=sentence[:32]
	#print header1
	header1=str(header1)
	#print header1
	hd1=int(header1,2)
	header1=hd1
	header2=sentence[32:48]
	#print header1,seq,header2
	header3=sentence[48:64]
	sentence=sentence[64:]
	#print "checking packet"
	if l>prob and seq==header1:
		#print "wrote packet ",seq
		f.write(sentence)
		header1=format(seq,'032b')
		header2="0000000000000000"
		header3="1010101010101010"
		seq+=1
		serverSocket.sendto(header1+header2+header3,cspair)	
	else:
		if l<prob:
			t_var=0
			#print "Packet Loss, sequence number = ",seq
		else:
			t_var=0
			#print "early client timeout"
	sentence,tarr=serverSocket.recvfrom(mss+64)
#print sentence
header1=format(seq,'032b')
header2="0000000000000000"
header3="1010101010101010"
seq+=1
serverSocket.sendto(header1+header2+header3,cspair)
sentence=sentence[64:-5]
f.write(sentence)
finish_time=time.time()
print "total time taken ",finish_time-start_time


