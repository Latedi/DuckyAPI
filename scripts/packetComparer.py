import binascii
import sys
from enum import Enum

DEBUG = True

#Compare packets from two packet streams
#Assumes that packets in the PacketStreams are ordered correctly, but can
#handle missing packets at the end of one stream
class PacketComparer:
    def __init__(self, packetStream1, packetStream2):
        self.packetStream1 = packetStream1
        self.packetStream2 = packetStream2
        self.perfectMatch = False
        
    def compare(self):
        self.perfectMatch = True
        
        if(DEBUG):
            print("Starting comparison...")
            
        self.compareNumberOfPackets()
        self.compareAllPackets()
        self.compareDirectionMismatches()
        
        return True
        
    def compareNumberOfPackets(self):
        packetsLen1 = len(self.packetStream1.packets)
        packetsLen2 = len(self.packetStream2.packets)
        
        if(DEBUG):
            if(packetsLen1 != packetsLen2):
                print("Informational number of packages do not match")
                self.perfectMatch = False
            else:
                print("Number of packages matches")
        
    def comparePacketLengths(self):
        shortest = min(len(self.packetStream1.packets), len(self.packetStream2.packets))
        for i in range(0, shortest):
            packetLen1 = len(self.packetStream1.packets[i].frameData)
            packetLen2 = len(self.packetStream2.packets[i].frameData)
            
            if(packetLen1 != packetLen2):
                print("Package length mismatch (" + str(packetLen1) + " - " + str(packetLen2) + ") at index " + str(i))
                self.perfectMatch = False
                
    def compareAllPackets(self):
        comparisonCounter = 0
        shortest = min(len(self.packetStream1.packets), len(self.packetStream2.packets))
        for i in range(0, shortest):
            packet1 = self.packetStream1.packets[i]
            packet2 = self.packetStream2.packets[i]
            compareResult = self.comparePackets(packet1, packet2)
            if(compareResult == True):
                comparisonCounter += 1
        print("Packets matching: " + str(comparisonCounter) + " of " + str(shortest))
            
    def comparePackets(self, packet1, packet2):
        errors = []
        
        if(packet1.frameNumber != packet2.frameNumber):
            errors.append("Frame number mismatch: " + str(packet1.frameNumber) + " - " + str(packet2.frameNumber))
        
        if(packet1.packetDirection != packet2.packetDirection):
            errors.append("Packet direction mismatch: " + str(packet1.packetDirection) + " - " + str(packet2.packetDirection))
        
        packetLen1 = len(packet1.frameData)
        packetLen2 = len(packet2.frameData)
        if(packetLen1 != packetLen2):
            errors.append("Package length mismatch (" + str(packetLen1) + " - " + str(packetLen2) + ") at index " + str(i))
            
        shortest = min(packetLen1, packetLen2)
        byteMismatch = False
        for i in range(0, shortest):
            byte1 = packet1.frameData[i]
            byte2 = packet2.frameData[i]
            if(byte1 != byte2):
                byteMismatch = True
                break
        if(byteMismatch):
            errors.append("Packet data mismatch:")
            errors.append(self.generatePacketDiff(packet1.frameData, packet2.frameData))
            
        if(errors != []):
            print("\nPacket mistmatch for frame " + str(packet1.frameNumber) + " (" + str(packet2.frameNumber) + ")")
            for i in range(0, len(errors)):
                print(errors[i])
            return False
            
        return True
        
    def generatePacketDiff(self, packetData1, packetData2):
        
        lineLength = 2*8 + 7
        padding = 4
        headerSpaces = lineLength + padding - len("Packet 1")
        
        res = "Packet 1"
        res += " " * headerSpaces
        res += "Packet2\n"
        
        arranged1 = self.arrangePacketBytes(packetData1)
        arranged2 = self.arrangePacketBytes(packetData2)
        
        index = 0
        while(True):
            WroteAtLeastOneLine = False
            if(index < len(arranged1)):
                res += arranged1[index]
                WroteAtLeastOneLine = True
            if(index < len(arranged2)):
                if(WroteAtLeastOneLine == True):
                    res += " " * padding
                else:
                    res += " " * (lineLength + padding)
                res += arranged2[index]
                WroteAtLeastOneLine = True
            index += 1
            if(WroteAtLeastOneLine == False):
                break
            else:
                res += "\n"
        
        return res
        
    def arrangePacketBytes(self, packetData):
        res = []
        current = ""
        for i in range(0, len(packetData)):
            byte = packetData[i]
            hex = str(binascii.hexlify(byte))[2:-1]
            
            if(i % 8 != 0):
                current += " "
            elif(i != 0):
                res.append(current)
                current = ""
                
            current += hex
        return res
        
    def compareDirectionMismatches(self):
        streams = [self.packetStream1, self.packetStream2]
        singleStreamMismatches = 0
        
        for i in range(0, 2):
            first = streams[i]
            second = streams[1 - i]
            
            for firstMismatch in first.directionMismatches:
                found = False
                
                for secondMismatch in second.directionMismatches:
                    if(firstMismatch[0] == secondMismatch[0] and firstMismatch[1] == secondMismatch[1]):
                        found = True
                        break
                        
                if(not found):
                    singleStreamMismatches += 1
                    print("Packet mismatch (" + str(firstMismatch[0]) + "-" + str(firstMismatch[1]) + ") only found in stream " + str(i + 1))
                    
        if(singleStreamMismatches > 0):
            print("Packet direction mismatches not identical. Stream1: " + str(len(self.packetStream1.directionMismatches)) + ". Stream2: " +
                str(len(self.packetStream2.directionMismatches)) + ". Non identical: " + str(singleStreamMismatches))
        else:
            print("Packet direction mismatches identical")
        
class PacketDirection(Enum):
    HostToUSB = 1
    USBToHost = 2

class Packet:
    def __init__(self, frameNumber, frameData, packetDirection):
        self.frameNumber = frameNumber
        self.frameData = frameData
        self.packetDirection = packetDirection

#Contains a set of packets sent to/from the host from a USB device
#The packets are ordered by wireshark, so it will in all likelihood
#be chronological.
class PacketStream:
    def __init__(self, plainPath, CArrPath):
        self.packets = []
        self.directionMismatches = []
        
        self.parseFrames(CArrPath)
        self.parsePlain(plainPath)
        
        self.matchRequestResponse()
    
    #Combines the metadata with the framedata
    #Assumes identical indexing of the two lists, but will fail with an error
    #if it is different.
    def combine(self, frameNumber, frameLength, frameDataLength, frameDirection, frameByteSample):        
        targetFrame = self.rawFrames[frameNumber - 1]        
        
        #Compares the frame lengths, if they are not the same these are different frames
        if(len(targetFrame) != frameLength):
            print("Error frame length mismatch")
            sys.exit()
            
        #Extract the complete data from the raw frame
        frameData = targetFrame[-frameDataLength:]
            
        #Compare the sample data from the plaintext file with the raw data.
        #If there is a mismatch, the frames are different.
        for i in range(0, len(frameByteSample)):
            if(frameByteSample[i] != frameData[i]):
                print("Error frame data mismatch in frame " + str(frameNumber))
                sys.exit()
                
        packet = Packet(frameNumber, frameData, frameDirection)
        self.packets.append(packet)
    
    #Get data from plaintext export, which is more like metadata since it's missing part of the bytes
    def parsePlain(self, plainPath):
        if(DEBUG):
            print("Parsing metadata from " + plainPath)
        
        with open(plainPath, "r") as f:
            
            currentFrameNumber = 0
            currentFrameLength = 0
            currentFrameDataLength = 0
            currentDirection = None
            currentBytes = []
            
            for line in f:
                line = line.strip()
                
                #Start of a new frame
                if(line.startswith("No.")):                    
                    currentFrameNumber = 0
                    currentFrameLength = 0
                    currentFrameDataLength = 0
                    currentDirection = None
                    currentBytes = []
                    
                #Get the frame number and frame length
                elif(line.startswith("Frame")):
                    currentFrameNumber = int(line.split(" ")[1][:-1])
                    currentFrameLength = int(line.split(" ")[2])
                    #print("Frame Number: " + str(currentFrameNumber))
                    #print("Frame Length: " + str(currentFrameLength))
                    
                #If source == host the host is the source, otherwise assume it's a USB endpoint
                elif(line.startswith("[Source:")):
                    source = line.split(" ")[1][:-1]
                    if(source == "host"):
                        currentDirection = PacketDirection.HostToUSB
                    else:
                        currentDirection = PacketDirection.USBToHost
                    #print("Direction: " + str(currentDirection))
                    
                #Get the length of the data segment in the packet
                elif(line.startswith("Packet")):
                    currentFrameDataLength = int(line.split(" ")[-1])
                    #print("Frame data length: " + str(currentFrameDataLength))
                    
                #Get a sample of the data from the packet
                #This is the last line for the frame, so try to combine the retrieved metadata with the raw frames
                elif(line.startswith("Leftover")):
                    startIndex = line.index(":") + 2
                    endIndex = line.index(".")
                    cutout = line[startIndex:endIndex]
                    
                    for i in range(0, len(cutout), 2):
                        hexByte = cutout[i:i+2]
                        byte = binascii.unhexlify(hexByte)
                        currentBytes.append(byte)
                    #print("Parsed bytes: " + str(currentBytes))
                    
                    self.combine(currentFrameNumber, currentFrameLength, currentFrameDataLength, currentDirection, currentBytes)
        
        if(DEBUG):
            print("Combined plaintext and frame data for a total of " + str(len(self.packets)) + " packets")
        
    #Get data from exported C Arrays
    def parseFrames(self, CArrPath):
        self.rawFrames = []
        
        if(DEBUG):
            print("Parsing frames from: " + CArrPath)
        
        with open(CArrPath, "r") as f:
            
            byteArray = []
            skipNumberOfLines = 0
            lineCounter = 1
            
            numberOfBytesToParse = 0
            bytesParsedForFrame = 0
            totalBytesParsed = 0
            numberOfFramesParsed = 0
            
            for line in f:
                lineCounter += 1
                
                if(skipNumberOfLines > 0):
                    skipNumberOfLines -= 1
                    continue
                    
                #Start of a new frame
                elif("/* Frame" in line):
                    numberOfBytesToParse = int(line.split(" ")[2][1:])
                    bytesParsedForFrame = 0
                    byteArray = []
                    skipNumberOfLines = 1
                    numberOfFramesParsed += 1
                    #print("Parsing frame: " + str(numberOfFramesParsed))
                    
                #Try to parse the line as a set of bytes in hexadecimal
                #The skipNumberOfLines has been set so that this part should never
                #trigger with invalid data. Will probably break if something goes
                #wrong.
                else:
                    endIndex = line.index("/*")
                    split = line[:endIndex].split(",")
                    for hexByte in split:
                        if(hexByte.isspace()):
                            continue
                        hexByte = hexByte.strip()
                        if(not hexByte.startswith("0x") or not len(hexByte) == 4):
                            print("Error during parsing of hex byte")
                            print("Line number: " + str(lineCounter))
                            print("Line content: " + line.strip())
                            print("Hex byte: " + hexByte)
                            sys.exit()
                        hexByte = hexByte[2:]
                        byte = binascii.unhexlify(hexByte)
                        byteArray.append(byte)
                        bytesParsedForFrame += 1
                        
                #If the correct number of bytes has been read, push to the raw frames list
                #This assumes that the number of bytes is always listed correctly
                if(bytesParsedForFrame == numberOfBytesToParse):
                    skipNumberOfLines = 2
                    self.rawFrames.append(byteArray)
                    totalBytesParsed += len(byteArray)
        
        if(DEBUG):
            print("Frames: " + str(len(self.rawFrames)) + "\tTotal Bytes: " + str(totalBytesParsed))
            
    #See if there are several packets in a row going the same direction
    def matchRequestResponse(self):    
        if(len(self.packets) < 2):
            return
                
        lastDirection = self.packets[0].packetDirection
        
        for i in range(1, len(self.packets)):
            newDirection = self.packets[i].packetDirection
            
            if(lastDirection == newDirection):
                #print("Direction mismatch in stream at frames " + str(i-1) + "-" + str(i))
                self.directionMismatches += (str(i-1), str(i))
            
            lastDirection = newDirection
            
        if(len(self.directionMismatches) > 0):
            print("Stream input/output mismatches exist")
        else:
            print("Input/output matches for both streams")
                
#This class saves down data into a format to be easily read in c++
#Code specific for the Ducky usecase only
class PacketSaver:
    def __init__(self, packetStream):
        self.packetStream = packetStream
        self.delimiter = " "
        
    def save(self, outputPath, startPacketIndex, endPacketIndex):
        if(DEBUG):
            print("Saving packet data from " + str(startPacketIndex) + "-" + str(endPacketIndex) + " to " + outputPath)
        if(startPacketIndex < 0 or endPacketIndex > len(self.packetStream.packets)):
            print("Erorr saving. Indices out of range")
            sys.exit()
            
        with open(outputPath, "w") as f:
            for i in range(startPacketIndex, endPacketIndex):
                packet = self.packetStream.packets[i]
                line = ""
                if(packet.packetDirection == PacketDirection.HostToUSB):
                    line += "O"
                else:
                    line += "I"
                line += self.delimiter
                for byte in packet.frameData:
                    line += binascii.hexlify(byte).decode("utf-8")
                line += "\n"
                f.write(line)

packets1 = PacketStream("C:/Users/jonat/Desktop/c4Plain", "C:/Users/jonat/Desktop/c4CArr")
packets2 = PacketStream("C:/Users/jonat/Desktop/c5Plain", "C:/Users/jonat/Desktop/c5CArr")
comparer = PacketComparer(packets1, packets2)
comparer.compare()

saver = PacketSaver(packets1)
saver.save("Traffic_Init.txt", 0, 1023)
saver.save("Traffic_Exit.txt", 1023, len(packets1.packets))


