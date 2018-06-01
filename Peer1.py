import socket
import sys
import threading
import thread
import re
import time
import Peer_Register
import Peer_PQuery
import Peer_Leave
import Peer_Client1
import os
import thread
import time
import re
import Queue

#################Take input from file######################
with open ("C:\Users\Madhura\Desktop\IP Project\Data.txt", "r") as myfile:
    data=myfile.readlines()
temp = data[0].split("=")
rs = temp[1].split(",")
RS_IP = rs[0]
RS_port = rs[1]

temp1 = data[1].split("basepath=")
basepath = temp1[1].split("\n")
me =  os.path.basename(sys.argv[0]).split(".py")
for i in range(len(data)):
    if me[0] in data[i]:
        temp = data[i].split("=")
        my = temp[1].split(",")
        info = my[0]
        myIP = my[1]
        myport = int(my[2])


#function for Register()
def register(cookie):
    
    #register=[self_IP,"1000"]
    c=Peer_Register.register(info,myport,RS_IP)
    #contact has information about the cookie given by RS server
    if c=='NO':
        pass
    else:
        cookie=c
        contact.update({cookie:register})
        thread1(cookie)
    return(cookie)
    
#function for PQuery()
def Pquery(cookie):
    info=Peer_PQuery.PQuery(cookie,RS_IP)
    x=info.split("Host:")
    y=info.split("IP:")
    z=info.split("RFCPort:")
    n = info.count("Host:")
    d={}
    for i in range(1,n+1):
        d.update({i:[x[i].split("<sp>")[0],y[i].split("<sp>")[0],int(z[i].split("<el>")[0])]})
    return d


#function for Leave()
def leave(cookie):
    Peer_Leave.leave(cookie,RS_IP)

#function for Keepalive()
def Keepalive(cookie):
    while True:
        sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the RS server is listening
        server_address = (RS_IP, 65423)
        # status of the connection
        print >>sys.stderr, 'connecting to %s port %s' % server_address
        data ='Keepalive<sp>Host:{0}<sp>Cookie:{1}<el>'.format(r[0],cookie)
        sock1.connect(server_address)
        sock1.send(data)
        time.sleep(5)
        data1= sock1.recv(256)
        if data1=='NO':
            print("Keepalive dead")
            sock1.close()
            break
        sock1.close()
                
def thread1(cookie):
    t=thread.start_new_thread(Keepalive,(cookie,))

#function to download files
def client_code(self_RFCIndex,RFCDownload,q1,PQ,myport):
    time.sleep(15);
    for i in range(len(RFCDownload)):
        start_time = time.time()
        res = False
        res = check_RFCIndex(self_RFCIndex,int(RFCDownload[i]))
        if (res == False):
            keys = PQ.keys()
            for j in range(0,len(keys)):
                RFCIndex = Peer_Client1.get_RFCIndex(PQ[keys[j]][1],PQ[keys[j]][2],self_RFCIndex,myport)
                res, list1 = Peer_Client1.check_RFCIndex(RFCIndex,int(RFCDownload[i]))
                if (res == True):
                    break
            for k in range(0,len(keys)):
                if (list1[1] == PQ[keys[k]][0]):
                    IP = PQ[keys[k]][1]
                    port = PQ[keys[k]][2]
                    break
            Peer_Client1.get_RFC(IP,port,RFCDownload[i],d[0],mypath)
            #RFCIndex = q.get()
            #print RFCIndex
            a.append(time.time()- start_time)
            thread.start_new_thread(RFCIndex_TTL, (RFCIndex,info,))
            #q.put(RFCIndex)
    timefile = open('C:\\Users\\Madhura\\Desktop\\IP Project\\time1.txt','w')
    for r in range(len(a)):
        timefile.write(str(a[r])+" ")
        timefile.write
    timefile.close()
    time.sleep(500)

def SendRFCIndex(conn,RFCIndex):
        try: 
            conn.sendall(str(RFCIndex))      
        finally:
                print 'Clean up the connection'
                conn.close()
def check_RFCIndex(RFCIndex,RFCreq):
        res = False
        keys = RFCIndex.keys()
        for i in range(0,len(keys)):
            if (RFCreq == keys[i]):
                res =  True
                break
        return res
def sendRFC(conn,data,mypath,myport):
    try:
        d = data.split("<el>")
        RFCIndex = Peer_Client1.selfRFCIndex(mypath,info)
        res = check_RFCIndex(RFCIndex,int(d[1]))
        if (res == True):
            basePath = mypath
            restofPath = d[1] +'.pdf'
            filename = os.path.join(basePath,restofPath)
            length = os.path.getsize(filename)
            conn.sendall(str(length))
            f = open(filename,'rb')
            l = f.read(1024)
            while (l):
                conn.send(l)
                l = f.read(1024)
            #print('Sent ',repr(l))
            f.close()
            print('Done sending')
            conn.send('Thank you for connecting')
                #conn.close()
        else:
            conn.send('RFC is not in my database')
                #conn.close()
    finally:
            conn.close()
def client_thread(conn,mypath,myport,RFCIndex):
        data = conn.recv(2048)
        if re.match('GetRFC',data):
            sendRFC(conn,data,mypath,myport)
        if re.match('RFCQuery',data):
            #RFCIndex = Peer_Client.selfRFCIndex(mypath)
            SendRFCIndex(conn,RFCIndex)

def RFCIndex_TTL(RFCIndex,info):
    keys = RFCIndex.keys()
    for i in range(0,len(keys)):
        #TTL =  RFCIndex[i][2]
        mins = 0
        #self_IP = socket.gethostbyname(socket.gethostname())
        if (RFCIndex[keys[i]][1]!=info):
            while RFCIndex[keys[i]][2] != 0:
                time.sleep(60)
                RFCIndex[keys[i]][2] = RFCIndex[keys[i]][2] - 60
                #print RFCIndex

#################Initialize variables######################              
a=[]
r = [info,myport]
cookie=0
contact={}
c=0
flag = 0
c=cookie
cookie=register(c)
time.sleep(15)
if cookie:
    active=Pquery(cookie)
#################Specify files to be downloaded######################
RFCDownload = ['7501','7502']

#################Take input from file################################
mypath = basepath[0]+me[0]
self_RFCIndex = {}
q = Queue.Queue()
filename = sys.argv[0]
filename = str(filename)
d = filename.split(".py")
q1 = Queue.Queue()
#################Create a TCP/IP socket###############################
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#################Bind the socket to the port##########################
server_address = (myIP, myport)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
self_RFCIndex = Peer_Client1.selfRFCIndex(mypath,info)
RFCIndex = self_RFCIndex
##############Creating new thread for client process##################
thread.start_new_thread(client_code, (RFCIndex,RFCDownload,q1,active,myport))
sock.listen(10)
while True:  
    print >>sys.stderr, 'waiting for a connection'
    conn, client_address = sock.accept()
    print >>sys.stderr, 'connection from', client_address
##############Creating new thread for server process##################
    thread.start_new_thread(client_thread, (conn,mypath,myport,RFCIndex))




