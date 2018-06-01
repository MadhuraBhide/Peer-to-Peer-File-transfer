####################################### RS CODE################################

################### Importing Libraries######################################
import socket
import sys
import re
import ast
import datetime
from threading import Timer
import time
import thread


###################################Main Program################################

##### Variables#####
# Register which contains information of active peers
#register={cookie:[ipaddress,flag,TTL,RFCserverportnumber,Times peer is active in last 30 days, date peer registered,hostname]}
with open ("C:\Users\Madhura\Desktop\IP Project\Data.txt", "r") as myfile:
    data=myfile.readlines()
temp = data[0].split("=")
rs = temp[1].split(",")
ip = rs[0]

register={}
cookie=[]
c=0
t={}

######## Register update#################
def update(c,data):
    time= datetime.date.today()
    if (c in cookie):
        register[c][2]=7200
        if(str(time)==t[c]):
            t[c]=str(time)
        else:
            register[c][4]=register[c][4]+1
        print("Updated Register:")
        print(register)
    else:
        d=[data[2],bool(1),7200,int(data[1]),1,str(time),data[0]]
        register.update({c:d})
        thread.start_new_thread(TTL, (c,))
        print("Updated Register:")
        print(register)
        s30=datetime.date.today() + datetime.timedelta(30)
        t.update({c:str(s30)})

######## TTL function #################    
def TTL(c):
    while register[c][2] != 0:
        time.sleep(60)
        register[c][2]=register[c][2]-60
        print('TTL for:{0}'.format(register[c][0]))
        print register[c]
        if register[c][1]==bool(0):
            break
    register[c][1]=bool(0)
    print('TTL for:{0} closed'.format(register[c][0]))
    register[c][2]=0
    print register[c]

######## Socket creation################# 
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port 65423 
server_address = (ip, 65423)
sock.bind(server_address)

# Listen for incoming connections
print("RS socket listening on port number 65423!")
sock.listen(1)

while True:
    connection, client_address = sock.accept()
    try:
        #Established connection with peer
        print >>sys.stderr, 'connection from', client_address

        #data bifurcates between various communication
        while True:
            data = connection.recv(1024)
######## PQuery Code #################    
            d={}
            s="PQ_Response<sp>P2P-DI/1.0<sp>OS: Mac OS 10.4.1<el>"
            if re.match('PQuery',data):
                print >>sys.stderr, "%s" %data
                #send header and data together
                if bool(register):
                    for key in register.iterkeys():
                        if register[key][1]==bool(1):
                            d.update({key:['Host:%s<sp>'%register[key][0],
                                           'IP:%s<sp>'%register[key][6],
                                           'RFCPort:%s<el>'%register[key][3]]})
                    a=[]
                    for k,i in d.iteritems():
                        for j in xrange(len(i)):
                            a.append(i[j])
                    s=""
                    s=s.join(a)
                else:
                    s=""
                s="PQ_Response<sp>P2P-DI/1.0 <sp>OS: Mac OS 10.4.1<el>"+s
                connection.sendall(s)
                print("PQuery successful!")
                break
                
######## Register Code #################   
            if re.match('Register',data):
                print >>sys.stderr, '%s' %data
                connection.sendall("ok")
                data1=connection.recv(1024)
                y=data1.split("Host:")
                k=y[1].split("<sp>")[0]
                s=zip(client_address)
                s=s[0]
                s=s[0]
                x=0
                for keys in register.iterkeys():
                    if k in register[keys]:
                        x=1
                        k=keys
                if (x==0):
                    c=c+1
                    connection.sendall(str(c))
                else:
                    print "Peer already in record! Marking active!"
                    register[k][1]=bool(1)
                    connection.sendall(str(k))
                print("Registration successful!")
                    
            #process data1 and add other fields in register1
                y=data1.split("Host:")
                z=data1.split("RFCPort:")
                k=[s,z[1].split("<el>")[0],y[1].split("<sp>")[0]]
                while True:
                    update(c,k)
                    break
                if (c not in cookie):
                    cookie.append(c)
                break
               
######## Leave Code #################   
            if re.match('Leave',data):
                print >>sys.stderr, '%s' %data
                s=data.split("Cookie:")[1].split("<el>")[0]
                s=int(s)
                if s in register:
                    register[s][1]=bool(0)
                print("Updated Register:")
                print(register)
                break
                
######## Keepalive Code #################   
            if re.match('Keepalive',data):
                print >>sys.stderr, data
                s=data.split("Cookie:")[1].split("<el>")[0]
                s=int(s)
                if register[s][1]==bool(1):
                    connection.sendall("ok")
                if register[s][1]==bool(0):
                    connection.sendall("NO")
                    break
                break
                
    finally:
        # Clean up the connection
        connection.close()

