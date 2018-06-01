import socket
import sys
import ast
import os

# Create a TCP/IP socket
def selfRFCIndex(mypath,info):
    from os import listdir
    from os.path import isfile, join
    try:
        os.stat(mypath)
    except:
        os.mkdir(mypath)
    self_RFCIndex = {}
    myRFCs = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    #print myRFCs
    for i in range(len(myRFCs)):
        #print myRFCs[i]
        temp = myRFCs[i]
        d = temp.split(".")
        self_IP = socket.gethostbyname(socket.gethostname())
        self_RFCIndex.update({int(d[0]):[myRFCs[i],info,7200]})
        #print self_RFCIndex
    return self_RFCIndex

def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z
# Connect the socket to the port where the server is listening
def get_RFCIndex(server,port,self_RFCIndex,myport):
    if (port == myport):
        return self_RFCIndex
    else:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (server,port)
        print >>sys.stderr, 'connecting to %s port %s' % server_address
        sock.connect(server_address)
        try:
            sock.sendall('RFCQuery<sp>P2P-DI/1.0<el>')
            data = sock.recv(4096)
    #amount_received += len(data)
            print >>sys.stderr, 'received "%s"' % data
            RFCIndex = ast.literal_eval(data)
            #print RFCIndex  
    
        finally:
            print >>sys.stderr, 'closing socket'
            sock.close()
        RFCIndex = merge_two_dicts(RFCIndex, self_RFCIndex)
        #print RFCIndex
        return RFCIndex
    
def check_RFCIndex(RFCIndex,RFCDownload):
    keys = RFCIndex.keys()
    #print keys
    res = False
    list1 = 0
    for i in range(0,len(keys)):
        if (RFCDownload == keys[i]):
            res, list1 = True, RFCIndex[keys[i]]
            break
        else:
            res, list1 = False, 0
    return res, list1

def get_RFC(server,port,RFCDownload,clientname,basepath):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #print RFCDownload
    server_address = (server,port)
    sock.connect(server_address)
    try:
        str1 = 'GetRFC<sp>P2P-DI/1.0<el>'+RFCDownload
        sock.sendall(str1)
        #print int(RFCDownload)
        #sock.sendall(RFCDownload)
        size = sock.recv(1024)
        print >>sys.stderr, 'received "%s"' % size   
        #size = int(size)
        size1 = int(size)
        current_size = 0
        directory = basepath
        if not os.path.exists(directory):
            os.makedirs(directory)
        buffer = b""
        with open(basepath+'\\'+RFCDownload+'.pdf', 'wb') as f:
            print 'file opened'
            while current_size < size1:
                
                print('receiving data...')
                while True:
                    data = sock.recv(1024)
                
                #print('data=%s', (data))
                    if not data:
                        break
                    if len(data) + current_size > size1:
                        data = data[:size1-current_size] # trim additional data
                    buffer += data
        # you can stream here to disk
                    current_size += len(data)
        # write data to a file
                    f.write(data)

            f.close()
        print('Successfully get the file')
        sock.close()
        print('connection closed')
    finally:
        sock.close()
        print('connection closed')

     
