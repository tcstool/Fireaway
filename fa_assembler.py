#!/usr/bin/python

#Fireaway Reassembler Copyright 2017 Russell Butturini
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

import sys
import base64

def main():
    chunks = []
    times = []
    validModes = ['1','2','3']

    if len(sys.argv) != 3 or sys.argv[1] not in validModes:
        printHelp()

    else:
        if sys.argv[1] == '1':
            timestampAssembler(sys.argv[2].split(','))

        if sys.argv[1] =='2':
            randomAssembler(sys.argv[2].split(','))

        if sys.argv[1]  == '3':
            spooferAssembler(sys.argv[2].split(','))

def randomAssembler(fileArray):
    chunks = []
    chunkReceiveTimes = []
    orderedChunks = []
    outputFile = raw_input('Enter the file name for the assembled file: ')
    seqKeyFile = raw_input('Enter the path to the file containg the sequence key: ')

    #parse the sequence key
    sequnceNumber = ''
    with open (seqKeyFile) as f:
        unconvertedKey = f.read()[:-1].split(',')
        f.close()

    receiveOrder = [int(convert) for convert in unconvertedKey]

    for i in range(max(receiveOrder)+1): #Insert as many empty values into the reassembly list as you have chunks, then update these after calculation of which position the chunk needs
        orderedChunks.append(None)

    for fileName in fileArray:
        chunkKey = raw_input('Enter the 4 character reassembly key for the file ' + fileName + ': ')

        with open(fileName) as f:
            unparsedWhole = f.read()
            f.close()
            unparsedChunks = unparsedWhole.split(chunkKey)

        while len(unparsedChunks) > 0:
            if (unparsedChunks[0]) != '': #Not EOF
                chunkReceiveTimes.append(float(unparsedChunks[0]))
                chunks.append(unparsedChunks[1])
                unparsedChunks.pop(0)
                unparsedChunks.pop(0)

            else:
                break

    while len(chunks) > 0:
        curChunk = chunks[chunkReceiveTimes.index(min(chunkReceiveTimes))]
        orderedChunks[receiveOrder[0]] = curChunk
        chunks.pop(chunkReceiveTimes.index(min(chunkReceiveTimes)))
        chunkReceiveTimes.pop(chunkReceiveTimes.index(min(chunkReceiveTimes)))
        receiveOrder.pop(0)

    for piece in orderedChunks:
        fo = open(outputFile, 'a')
        fo.write(piece)
        fo.close()

    print 'Reassembly complete.  check output at ' + outputFile + '.'
    sys.exit()


def timestampAssembler(fileArray):
    chunks = []
    chunkReceiveTimes = []
    outputFile = raw_input('Enter the file name for the assembled file: ')

    for fileName in fileArray:
        chunkKey = raw_input('Enter the 4 character reassembly key for the file '+ fileName + ': ')

        with open(fileName) as f:
            unparsedWhole = f.read() #read the whole thing in as a string and parse based on key
            f.close()
            unparsedChunks = unparsedWhole.split(chunkKey)

            while len(unparsedChunks) > 0: #loop through as long as there is stuff to add.
                if(unparsedChunks[0]) != '': #Not EOF
                    chunkReceiveTimes.append(float(unparsedChunks[0]))
                    chunks.append(unparsedChunks[1])
                    unparsedChunks.pop(0)
                    unparsedChunks.pop(0)

                else:
                    break


    while len(chunks) > 0:
        fo = open(outputFile,'a')
        fo.write(chunks[chunkReceiveTimes.index(min(chunkReceiveTimes))])
        chunks.pop(chunkReceiveTimes.index(min(chunkReceiveTimes)))
        chunkReceiveTimes.pop(chunkReceiveTimes.index(min(chunkReceiveTimes)))
        fo.close()

    print 'Reassembly complete. Check output at ' + outputFile + '.'
    sys.exit()

def spooferAssembler (fileArray): #This is basically the same as timestamp assembler.  I'm lazy.  Fix this later.
    chunks = []
    chunkReceiveTimes = []
    decoderWork = ''
    decoded = ''
    outputFile = raw_input('Enter the file name for the assembled file: ')

    for fileName in fileArray:
        chunkKey = raw_input('Enter the 4 character reassembly key for the file ' + fileName + ': ')

        with open(fileName) as f:
            unparsedWhole = f.read()  # read the whole thing in as a string and parse based on key
            f.close()
            unparsedChunks = unparsedWhole.split(chunkKey)

            while len(unparsedChunks) > 0:  # loop through as long as there is stuff to add.
                if (unparsedChunks[0]) != '':  # Not EOF
                    chunkReceiveTimes.append(float(unparsedChunks[0]))
                    chunks.append(unparsedChunks[1])
                    unparsedChunks.pop(0)
                    unparsedChunks.pop(0)

                else:
                    break


    while len(chunks) > 0:
        decoderWork += chunks[chunkReceiveTimes.index(min(chunkReceiveTimes))].rstrip()
        chunks.pop(chunkReceiveTimes.index(min(chunkReceiveTimes)))
        chunkReceiveTimes.pop(chunkReceiveTimes.index(min(chunkReceiveTimes)))


    decoded = base64.b64decode(decoderWork)
    fo = open(outputFile,'a')
    fo.write(decoded)
    fo.close()
    print 'Reassembly complete. Check output at ' + outputFile + '.'
    sys.exit()

def printHelp():
    print 'Fireaway Reassembler v0.1'
    print 'Usage:  fa_assembler <mode> <comma separated list of files from FireAway servers to reassemble>'
    print 'Valid options for mode:'
    print 'mode 1-Use timestamp data for reassembly (data received sequentially)'
    print 'mode 2-Use timestamp data for reassembly (data received randomly)'
    print 'mode 3-Reassemble Base64 encoded data from spoofed app headers'
    sys.exit()


if __name__ == '__main__':
    main()


