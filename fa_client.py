#!/usr/bin/python
__author__ = 'Russell Butturini'

import socket
import sys
import string
from random import choice


def main():
    if len(sys.argv) != 4 or sys.argv[2].isdigit == False or int(sys.argv[2]) < 1 or int(sys.argv[2]) > 65535 or \
                    sys.argv[3].isdigit == False or int(sys.argv[3]) < 0 or int(sys.argv[3]) > 1:
        printHelp()

    else:
        if sys.argv[3] == '0':
            testChunk(sys.argv[1], int(sys.argv[2]))

        elif sys.argv[3] == '1':
            sendFile(sys.argv[1], int(sys.argv[2]))


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
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(15)
            s.connect((server, port))
            print 'sending ' + str(curBytes) + ' of test data.  Watch the server to see how much is received.'
            s.send(testData)
            s.close()

        except:
            # Handle aggressive network traffic from the firewall gracefully and keep going.
            pass

        curBytes = curBytes + increment


    if raw_input('Done sending test data.  Check the server output for any issues.  Move on to sending a real file?').lower() == 'y':
        sendFile(server,port)

    else:
        sys.exit()

def sendFile(server, port):
    print 'SendFile stuff goes here.'


def printHelp():
    print 'Fireaway Exfiltration Client v0.1'
    print 'Usage:  fa_client <fa_server IP> <port> <mode>'
    print 'Valid options for mode:'
    print '0-Send random test data to find maximum leaked data fragment size'
    print '1-Open a file for exfiltration'
    sys.exit()


if __name__ == '__main__':
    main()