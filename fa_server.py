#!/usr/bin/python

#Fireaway Server Copyright 2017 Russell Butturini
#This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import socket
import sys
import time
from thread import *
from random import randint
def main():
    if len(sys.argv) < 2 or sys.argv[1]  == '?' or len (sys.argv) != 3 or sys.argv[1].isdigit() == False or int(sys.argv[1]) < 1 or int(sys.argv[1]) > 65535:
        printHelp()

    else:
        startServer(sys.argv[1],sys.argv[2])

def startServer(port,mode):
    sequenceKeyID = None
    parserChars = '!@#$%^&*()'
    uniqueString = ''
    print '-Starting Fireaway server on port ' + port + '...'

    if mode == '0':
        print '-Server started in sequential/test data mode.'

    elif mode == '1':
        for i in range(0,4):
            uniqueString = uniqueString + parserChars[randint(0,9)]

        print '-Server started in timestamp reassembly mode.'
        print '-Using ' + uniqueString + ' as reassembly key.  Use this with fa_assembler.py.\n'


    elif mode == '2':
        for i in range(0,4):
            uniqueString = uniqueString + parserChars[randint(0,9)]

        sequenceKeyID = raw_input('Enter the identifier for the sequence key: ')
        print '-Server started in sequence key based reassembly mode.'
        print '-Using ' + sequenceKeyID + ' as the key ID.'
        print '-BE SURE ALL SERVERS ARE USING THE SAME SEQUENCE KEY ID!'
        print '-Using ' + uniqueString + ' as reassembly key.  Use this with fa_assembler.py.'
        print '-Ready to receive randomized data chunks.\n'

    elif mode == '3':
        for i in range(0,4):
            uniqueString = uniqueString + parserChars[randint(0,9)]

        print '-Server started in spoofed app mode.'
        print '-Using ' + uniqueString + ' as the reassembly key.  use this with fa_assembler.py'


    else:
        print 'Invalid server mode specified.  Shutting down.'
        sys.exit()

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
        start_new_thread(getData,(conn,mode,uniqueString,sequenceKeyID))

def getData(conn,mode,parserString,seqKeyID):
    dataSizes = []

    while True:
        data = conn.recv(16384)

        if not data:
            break

        print 'Received ' + str(len(data)) + ' bytes.'
        dataSizes.append(len(data))

        if len(dataSizes) > 1 and dataSizes[len(dataSizes)-1] <= dataSizes[len(dataSizes)-2]:
            print 'Got the same or lower amount of data on two consecutive connections.  If sending test data, maximum data leak size may have been reached.'

        fo = open('./ReceivedData.txt','a')

        if mode == '0':
            fo.write(str(data))
            fo.close()

        elif mode == '1': #Use Unix epoch time to record time data chunk received, reassemble in epoch time order
            #Use the randomly generated parser key to write the data to the file.  File sequence is key, Unix epoch time, key, chunk data
            fo.write(str(float(time.time())) + parserString + str(data) + parserString)
            fo.close()

        elif mode == '2': #File chunks will be sent randomly.  Look for the sequence key by input ID to identify the order of data received
            delimiters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()'
            output_handler = open('./ReceivedData.txt','a')
            seqNumber = ''
            if data.find(seqKeyID) != -1: #Sequence key present in received data, process the key into sequencing array
                key_handler = open('./SequenceKey.txt', 'a')
                for seqChar in data.strip(seqKeyID):
                    if seqChar in delimiters: #end of sequence number, write to key file
                        key_handler.write(seqNumber+',')
                        seqNumber = ''

                    else: #character in sequence number
                        seqNumber += seqChar
                key_handler.close()

            else: #This is real data
                output_handler.write(str(float(time.time())) + parserString + str(data) + parserString)
                output_handler.close()

        elif mode == '3': #extract data from spoofed app HTTP headers
            fo.write(str(float(time.time())) + parserString + str(data.split('\n')[3].split(':')[1][1:].rstrip()) + parserString)
            fo.close()


def printHelp():
    print 'Fireaway Server v0.2'
    print 'Usage:  fa_server <listening port> <mode>\n'
    print 'mode 0-Sequential/test data, single server, no reassembly required'
    print 'mode 1-Receive sequential chunks/Use timestamp data for reassembly'
    print 'mode 2-Receive random chunks/Use sequence key for reassembly'
    print 'mode 3-Receive Base64 chunks/Use spoofed app header data for reassembly'
    sys.exit()


if __name__ == '__main__':
    main()

