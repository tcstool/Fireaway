#!/usr/bin/python

import socket
import sys
from thread import *

def main():
    if len(sys.argv) < 2 or sys.argv[1]  == '?' or len (sys.argv) != 2 or sys.argv[1].isdigit() == False or int(sys.argv[1]) < 1 or int(sys.argv[1]) > 65535:
        printHelp()

    else:
        startServer(sys.argv[1])

def startServer(port):
    print 'Starting Fireaway server on port ' + port

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('',int(port)))

    except socket.error,e:
        print 'Failed to start listener.  Error code ' + str(e[0]) + 'Error message ' + str(e[1])
        sys.exit()

    s.listen(5)
    print 'Ready to accept data!'

    while 1:
        conn, addr = s.accept()
        print 'Received inbound connection from ' + addr[0]
        start_new_thread(getData,(conn,))

def getData(conn):
    dataSizes = []

    while True:
        data = conn.recv(16384)

        if not data:
            break

        print 'Received ' + str(len(data)) + 'bytes.'
        dataSizes.append(len(data))

        if len(dataSizes) > 1 and dataSizes[len(dataSizes)-1] <= dataSizes[len(dataSizes)-2]:
            print 'Got the same or lower amount of data on two consecutive connections.  If sending test data, maximum data leak size may have been reached.'

        fo = open('./ReceivedData.txt','a')
        fo.write(str(data))
        fo.close()

def printHelp():
    print 'Fireaway Server v0.1'
    print 'Usage:  fa_server <listening port>'
    sys.exit()


if __name__ == '__main__':
    main()

