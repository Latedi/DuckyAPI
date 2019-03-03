import win32pipe
import win32file
import time


class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        
    def sanitize(self):
        self.r = min(self.r, 255)
        self.r = max(self.r, 0)
        self.g = min(self.g, 255)
        self.g = max(self.g, 0)
        self.b = min(self.b, 255)
        self.b = max(self.b, 0)
    
    def isZero(self):
        if(self.r == 0 and self.g == 0 and self.b == 0):
            return True
        return False
        
    def zeroOut(self):
        self.setColorValues(0, 0, 0)
        
    def setColor(self, color):
        self.setColorValues(color.r, color.g, color.b)
        
    def setColorValues(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        
    def scale(self, scaleValue):
        self.r = int(round(self.r * scaleValue))
        self.g = int(round(self.g * scaleValue))
        self.b = int(round(self.b * scaleValue))
        self.sanitize()
        
    def loopColorBySteps(self, steps):
        colors = [self.r, self.g, self.b]
        maxedCount = 0
        for i in range(0, 3):
            if(colors[i] == 255):
                previous = i - 1
                if(previous == -1):
                    previous = 2
                next = i + 1
                if(next == 3):
                    next = 0
                
                if(colors[previous] > 0):
                    #reduce previous
                    left = steps - colors[previous]
                    if(left <= 0):
                        colors[previous] -= steps
                        
                        self.r = colors[0]
                        self.g = colors[1]
                        self.b = colors[2]
                    else:
                        colors[previous] = 0
                        
                        self.r = colors[0]
                        self.g = colors[1]
                        self.b = colors[2]
                        
                        self.loopColorBySteps(left)
                        
                    break
                    
                elif(colors[next] < 255):
                    #increase next                    
                    left = colors[next] + steps - 255
                    
                    if(left <= 0):
                        colors[next] += steps
                        
                        self.r = colors[0]
                        self.g = colors[1]
                        self.b = colors[2]
                    else:
                        colors[next] = 255
                        
                        self.r = colors[0]
                        self.g = colors[1]
                        self.b = colors[2]
                                            
                        self.loopColorBySteps(left)
                    
                    break

    def printValue(self):
        print(str(self.r) + " " + str(self.g) + " " + str(self.b))

class KeyColor:
    def __init__(self, key, r, g, b):
        self.key = key
        self.color = Color(r, g, b)
        
    def constructStringPacket(self):
        self.color.sanitize()
        return self.key + " " + str(self.color.r) + " " + str(self.color.g) + " " + str(self.color.b) + ";"

def sendUntilNoException(data):
    sent = False
    while(not sent):
        #Ugly but it works
        try:
            pipeHandle = win32file.CreateFile("\\\\.\\pipe\\DuckyController", win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0, None, win32file.OPEN_EXISTING, 0, None)
            win32file.WriteFile(pipeHandle, data)
            win32file.CloseHandle(pipeHandle)
            sent = True
            #print("sent " + data.decode("utf-8"))
        except Exception as e:
            #print(e)
            time.sleep(0.01)



def reduce(steps):
    for k in keys:
        if(not k.color.isZero()):
            k.color.r -= steps
            k.color.g -= steps
            k.color.b -= steps
            k.color.sanitize()
        
def removeZero(keys):
    res = []
    for k in keys:
        if not k.color.isZero():
            res.append(k)
    return res

def checkZero(keys):
    for k in keys:
        if(not k.color.isZero()):
            return False
    return True

def charToKeyNames(char):
    if(char.isalpha()):
        prepend = ""
        if(char.isupper()):
            prepend = "LeftShift+"
        charUpper = char.upper()
        if(charUpper == "Å"):
            charUpper = "TittleA"
        elif(charUpper == "Ä"):
            charUpper = "UmlautA"
        elif(charUpper == "Ö"):
            charUpper = "UmlautO"
        return prepend + charUpper
    elif(char.isnumeric()):
        return char
    elif(char == " "):
        return "Space"
    elif(char == "!"):
        return "LeftShift+1"
        
def getKeyFromList(keys, keyName):
    for k in keys:
        if k.key == keyName:
            return k
    return None
    
def getKeyData():
    res = b''
    for k in keys:
        res += k.constructStringPacket().encode()
    return res
    
def removeZero():
    for k in keys:
        if(k.color.isZero()):
            keys.remove(k)


sendUntilNoException(b'INITIALIZE;')
time.sleep(3)
sendUntilNoException(b'RESET;PUSH')
time.sleep(2)

f = open("message.txt", "rb")
message = f.read().decode("utf-8")
f.close()

keys = []
readSpeed = 1
colorSpeedDecreaseSpeed = 100
finishedReading = False
allZero = False
currentChar = ''
currentMessageIndex = -1

nextReadTime = 0
lastLoop = time.time()

while(not allZero or not finishedReading):
    allZero = checkZero(keys)
    
    currentTime = time.time()
    deltaTime = currentTime - lastLoop
    
    steps = int(round(colorSpeedDecreaseSpeed * deltaTime))
    reduce(steps)
    removeZero()
    
    if(nextReadTime <= currentTime):
        nextReadTime = currentTime + readSpeed
        currentMessageIndex += 1
        if(len(message) > currentMessageIndex):
            currentChar = message[currentMessageIndex]
            keyNames = charToKeyNames(currentChar)
            for keyName in keyNames.split("+"):
                key = getKeyFromList(keys, keyName)
                if(key == None):
                    key = KeyColor(keyName, 255, 0, 0)
                    if(keyName == "LeftShift"):
                        key.color.r = 0
                        key.color.g = 255
                    keys.append(key)
                else:
                    key.color.r = 255
                    key.color.g = 0
                    key.color.b = 0
        else:
            currentChar = ""
            finishedReading = True
            
    keyData = getKeyData()
    
    packet = b'RESET;'
    packet += keyData
    packet += b'PUSH;'
    
    sendUntilNoException(packet)
        
    time.sleep(0.1)
        
    lastLoop = currentTime



sendUntilNoException(b'TERMINATE;')













