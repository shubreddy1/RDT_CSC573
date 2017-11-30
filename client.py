from socket import *
import socket as skt
import os
import math
from random import *
import pickle
import time
from time import sleep
import thread
import hashlib
import signal
import sys
if len(sys.argv)<5:
	print "insufficient arguments"
	exit(1)
serverlist=sys.argv[1:-3]
mss=int(sys.argv[-1])
filename=sys.argv[-2]
serverPort=int(sys.argv[-3])
#print serverlist,mss,filename,serverPort
#mss=500
#filename="rfc5.txt"
#serverlist = ['10.0.0.1','10.0.0.3','10.0.0.4']
#signal.signal(signal.SIGALRM,handler)
#serverPort = 12003 #default given port number
conarr=[]
b=format(mss,'016b')
clientSocket = socket(AF_INET, SOCK_DGRAM)
for ip in serverlist:
	cspair=(ip,serverPort)
	conarr.append(cspair)
	clientSocket.sendto(b,cspair)
fl2=0
print "starting transmission"
irtt=0.01
tarr=0
diff=0.01
#print conarr
#print "executing part"
#clientSocket = socket(AF_INET, SOCK_STREAM)
#clientSocket.connect((ip,port))
f=open(filename,"rb")
kt=len(f.read())
segments=math.ceil(kt/mss)
f.seek(0)
while fl2==0:		
	cont="ok"
	seqno=1
	m=hashlib.md5()
	cont=f.read(mss)
	while cont!="":
		#ic="ok2"
		#cont=""
		m.update(cont)
		s=m.hexdigest()
		s=s[0:-16]
		#print "hexdigest is ",s
		#print cont[:20],cont[-20:0]
		header1=format(seqno,'032b')
		header2=s
		header3="0101010101010101"
		for cspair in conarr:
			#print cspair
			fl=0
			while fl==0:
				try:
					if seqno==segments+1:
						clientSocket.sendto(header1+header2+header3+cont+"e_c01",cspair)
						fl2=1
					else:
						clientSocket.sendto(header1+header2+header3+cont,cspair)
					tdtime=irtt
					clientSocket.settimeout(tdtime)	
					#print "waiting for reply"		
					reply,tarr=clientSocket.recvfrom(64)
					rseq=reply[:32]
					#print rseq
					rseq=int(rseq,2)
					if rseq==seqno:
						fl=1
						diff=max(1,diff-1)
					#irtt=irtt*0.85
				except timeout:
					#irtt=irtt*2
					t_var=0
					#print "Timeout, sequence number = ",seqno
				clientSocket.settimeout(None)
		seqno+=1
		cont=f.read(mss)
		#print cont[:50]
	print "finished transmitting"





