import win32pipe
import win32file
import time
import keyboard
import random

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

class LoopyThing():
    def __init__(self):
        self.keys = []
        keyNames = ["PrintScreen", "Insert", "Delete", "End", "PageDown", "PageUp", "Pause", "ScreenLock"]
        for k in keyNames:
            self.keys.append(KeyColor(k, 0, 0, 0))
        self.currentKeyIndex = 0

        self.timeOfFirstUpdate = -1
        self.minTimeOnKey = 0.1
        self.nextTimeToChange = time.time() + self.minTimeOnKey
        
        self.currentColor = Color(255, 0 , 0)
        self.colorStepsPerSecond = 500
        
    def update(self, currentTime, deltaTime):        
        for k in self.keys:
            k.color.zeroOut()
        
        if(currentTime > self.nextTimeToChange):
            self.changeKey()
        
        self.updateColor(deltaTime)
        self.keys[self.currentKeyIndex].color.setColor(self.currentColor)
        
    def changeKey(self):        
        self.currentKeyIndex += 1
        self.currentKeyIndex %= len(self.keys)
        
        self.nextTimeToChange += self.minTimeOnKey
        
    def updateColor(self, deltaTime):
        steps = int(round(self.colorStepsPerSecond * deltaTime))
        self.currentColor.loopColorBySteps(steps)
        
    def constructPacket(self):
        key = self.keys[self.currentKeyIndex]
        packet = key.constructStringPacket().encode()
        packet += self.createTail()
        packet += self.createLeadingKey()
        return packet

    def createTail(self):
        tailKeys = []
        for i in range(1, 4):
            tail = (self.currentKeyIndex - i + 8) % 8
            key = self.keys[tail]
            key.color.setColor(self.currentColor)
            
            tailKeys.append(key)
            
        tailKeys[0].color.scale(0.75)
        tailKeys[1].color.scale(0.5)
        tailKeys[2].color.scale(0.25)
                    
        data = b''
        for i in range(0, len(tailKeys)):
            data += tailKeys[i].constructStringPacket().encode()
                    
        return data
        
    def createLeadingKey(self):
        leadIndex = (self.currentKeyIndex + 1) % 8
        key = self.keys[leadIndex]
        key.color.setColor(self.currentColor)
        key.color.scale(0.2)
        return key.constructStringPacket().encode()

class Walls:
    def __init__(self):
        self.currentColor = Color(255, 255, 0)
        keyNames = self.calculateKeyNames()
        self.keys = []
        for name in keyNames:
            key = KeyColor(name, 0, 0, 0)
            self.keys.append(key)
        self.colorStepsPerSecond = 150     
        
    def calculateKeyNames(self):
        keyNames = ["Escape", "SectionSign", "Tab", "CapsLock", "LeftShift", "<", "LeftControl", "LeftWindows", "LeftAlt",
            "Space", "AltGr", "RightWindows", "Function", "RightControl", "RightShift", "Enter", "Backspace", "AcuteAccent",
            "+", "Umlaut", "'", "TittleA", "UmlautA"]
        for i in range(1, 13):
            keyNames.append("F" + str(i))
        return keyNames
        
    def update(self, deltaTime):
        steps = int(round(self.colorStepsPerSecond * deltaTime))
        self.currentColor.loopColorBySteps(steps)
        for k in self.keys:
            k.color.setColor(self.currentColor)
            k.color.scale(0.5)
        
    def constructPacket(self):
        packet = b''
        for k in self.keys:
            packet += k.constructStringPacket().encode()
        return packet

#Max score = 999
class Score:
    def __init__(self):            
        self.score = 0
        self.keys = []
        for i in range(0, 10):
            self.keys.append(KeyColor("N" + str(i), 0, 0, 0))
        
    def increaseScore(self, incrementBy=1):
        self.score += incrementBy
    
    def update(self):
        for k in self.keys:
            k.color.zeroOut()
            
        scoreStr = str(self.score)
        scoreStrLen = len(scoreStr)
        
        r = scoreStr[-1]
        g = -1
        b = -1
        if(scoreStrLen >= 2):
            g = scoreStr[-2]
            
            if(scoreStrLen >= 3):
                b = scoreStr[-3]

        rKey = self.findKeyByNumber(r)
        rKey.color.setColorValues(255, rKey.color.g, rKey.color.b)
        
        if(g != -1):
            gKey = self.findKeyByNumber(g)
            gKey.color.setColorValues(gKey.color.r, 255, gKey.color.b)
            
            if(b != -1):
                bKey = self.findKeyByNumber(b)
                bKey.color.setColorValues(bKey.color.r, bKey.color.g, 255)
        
    def findKeyByNumber(self, value):
        name = "N" + str(value)
        for k in self.keys:
            if(k.key == name):
                return k
        return None
        
    def constructPacket(self):
        packet = b''
        for k in self.keys:
            packet += k.constructStringPacket().encode()
        return packet

class ReactiveArrows:
    def __init__(self):
        keyNames = ["UpArrow", "DownArrow", "LeftArrow", "RightArrow"]
        
        self.keys = []        
        for name in keyNames:
            self.keys.append(KeyColor(name, 0, 0, 0))
            
        self.colors = []
        self.colors.append(Color(255, 0, 0))
        self.colors.append(Color(0, 255, 0))
        self.colors.append(Color(0, 0, 255))
        self.colors.append(Color(255, 255, 0))
        self.colors.append(Color(255, 0, 255))
        self.colors.append(Color(0, 255, 255))
        
        self.reductionSpeed = 1000
        
    def update(self, deltaTime):
        steps = int(round(self.reductionSpeed * deltaTime))
        for k in self.keys:
            k.color.r -= steps
            k.color.g -= steps
            k.color.b -= steps
            k.color.sanitize()
            #print(k.color.printValue())
        
    def spike(self, keyName):
        newColor = self.getRandomColor()
        #print("Spiking " + keyName)
        for k in self.keys:
            if(k.key == keyName):
                k.color.setColor(newColor)
                break

    def getRandomColor(self):
        return random.choice(self.colors)
        
    def constructPacket(self):
        packet = b''
        for k in self.keys:
            packet += k.constructStringPacket().encode()
        return packet

class Tile:
    def __init__(self, keyName, position):
        self.key = KeyColor(keyName, 0, 0, 0)
        self.position = position

class SnakeTile:
    def __init__(self, position):
        self.color = Color(0, 0, 0)
        self.position = position
    
    def setColor(self, color):
        self.color = Color(color.r, color.g, color.b)
        
    def applyColor(self, tile):
        tile.key.color.setColor(self.color)
        
    def moveUp(self, otherSnakeTile):
        self.position = otherSnakeTile.position
        self.color.setColor(otherSnakeTile.color)

class Snake:
    def __init__(self):
        self.reset()
        self.deaths = 0
        
    def reset(self):
        self.isDead = False
        self.timeToRespawn = 3
        self.generateGrid()
        self.createSnake()
        self.score = Score()
        self.spawnTarget()
        self.colorize()
        self.arrows = ReactiveArrows()
        
    def generateGrid(self):
        self.gridNames = [
            ["1", "Q", "A", "Z"],
            ["2", "W", "S", "X"],
            ["3", "E", "D", "C"],
            ["4", "R", "F", "V"],
            ["5", "T", "G", "B"],
            ["6", "Y", "H", "N"],
            ["7", "U", "J", "M"],
            ["8", "I", "K", ","],
            ["9", "O", "L", "."],
            ["0", "P", "UmlautO", "-"]
        ]
        
        self.gridWidth = len(self.gridNames)
        self.gridHeight = len(self.gridNames[0])
        
        self.grid = []
        for i in range(0, len(self.gridNames)):
            column = self.gridNames[i]
            newColumn = []
            for j in range(0, len(column)):
                keyName = column[j]
                position = (i, j)
                newColumn.append(Tile(keyName, position))
            self.grid.append(newColumn)
    
    def createSnake(self):
        self.snakeSpeed = 0.5
        self.nextSnakeMovementTime = time.time() + self.snakeSpeed
        self.colorStep = 50
        self.snakeTiles = []
        
        for x in range(4, -1, -1):
            snakeTile = SnakeTile((x, 2))
            self.snakeTiles.append(snakeTile)
        
        initColor = Color(0, 255, 0)
        for s in reversed(self.snakeTiles):
            s.setColor(initColor)
            initColor.loopColorBySteps(self.colorStep)
                        
        self.movementDirection = (1, 0)
        
    def spawnTarget(self):
        potentialPositions = []
        for column in self.grid:
            for tile in column:
                tilePosition = tile.position
                isInSnake = False
                for snakeTile in self.snakeTiles:
                    snakePosition = snakeTile.position
                    if(tilePosition[0] == snakePosition[0] and tilePosition[1] == snakePosition[1]):
                        isInSnake = True
                        break
                if(not isInSnake):
                    potentialPositions.append(tilePosition)
        randomPosition = random.choice(potentialPositions)
        
        self.targetPosition = randomPosition
        self.targetColor = Color(255, 0, 255)
        self.targetColorSpeed = 255
        
    def updateTarget(self, deltaTime):
        steps = int(round(self.targetColorSpeed * deltaTime))
        self.targetColor.loopColorBySteps(steps)
    
    def colorizeTarget(self):
        tile = self.grid[self.targetPosition[0]][self.targetPosition[1]]
        tile.key.color.setColor(self.targetColor)
        
    def colorize(self):
        for column in self.grid:
            for tile in column:
                tile.key.color.zeroOut()
        self.colorizeTarget()
        for snakeTile in self.snakeTiles:
            tile = self.grid[snakeTile.position[0]][snakeTile.position[1]]
            snakeTile.applyColor(tile)
            
    def getDeaths(self):
        return self.deaths
        
    def constructPacket(self):
        packet = b''
        for column in self.grid:
            for tile in column:
                packet += tile.key.constructStringPacket().encode()
        packet += self.score.constructPacket()
        packet += self.arrows.constructPacket()
        return packet
        
    def moveSnake(self):
        frontTile = self.snakeTiles[0]
        newPosition = (frontTile.position[0] + self.movementDirection[0],
            frontTile.position[1] + self.movementDirection[1])
        
        if(newPosition[0] < 0 or newPosition[0] >= self.gridWidth or
            newPosition[1] < 0 or newPosition[1] >= self.gridHeight):
            return False
            
        for i in range(1, len(self.snakeTiles)):
            otherTile = self.snakeTiles[i]
            if(otherTile.position[0] == frontTile.position[0] and
                otherTile.position[1] == frontTile.position[1]):
                return False
        
        for i in range(len(self.snakeTiles) - 1, 0, -1):
            snakeTile = self.snakeTiles[i]
            nextSnakeTile = self.snakeTiles[i - 1]
            snakeTile.moveUp(nextSnakeTile)
        
        newTile = self.grid[newPosition[0]][newPosition[1]]
        frontTile.position = newPosition
        frontTile.color.loopColorBySteps(self.colorStep)

        return True
        
    def ifHitTarget(self):
        frontPosition = self.snakeTiles[0].position
        if(self.targetPosition[0] == frontPosition[0] and self.targetPosition[1] == frontPosition[1]):
            return True
        return False
        
    def update(self, currentTime, deltaTime):
        if(not self.isDead):
            self.arrows.update(deltaTime)
            self.updateTarget(deltaTime)
            
            if(currentTime >= self.nextSnakeMovementTime):
                self.score.increaseScore()
                self.score.update()
                self.nextSnakeMovementTime += self.snakeSpeed
                result = self.moveSnake()
                if(result == False):
                    self.deaths += 1
                    self.isDead = True
                    self.snakeDed()
                if(self.ifHitTarget()):
                    self.score.increaseScore(5)
                    self.spawnTarget()
                self.colorize()
        else:
            if(currentTime >= self.nextRespawn):
                self.reset()
            else:
                self.flashRed(deltaTime)
                self.colorize()
            

    def receiveInput(self, input):
        if(input == "u"):
            if(self.movementDirection != (0, 1)):
                self.movementDirection = (0, -1)
                self.arrows.spike("UpArrow")
        elif(input == "d"):
            if(self.movementDirection != (0, -1)):
                self.movementDirection = (0, 1)
                self.arrows.spike("DownArrow")
        elif(input == "l"):
            if(self.movementDirection != (1, 0)):
                self.movementDirection = (-1, 0)
                self.arrows.spike("LeftArrow")
        elif(input == "r"):
            if(self.movementDirection != (-1, 0)):
                self.movementDirection = (1, 0)
                self.arrows.spike("RightArrow")
            
    def snakeDed(self):
        self.nextRespawn = time.time() + self.timeToRespawn
        self.flashColor = Color(0, 0, 0)
        self.flashDirection = 1
            
    def flashRed(self, deltaTime):
        flashSpeed = 1000
        steps = int(round(deltaTime * flashSpeed * self.flashDirection))
        
        newR = self.flashColor.r + steps
        if(newR >= 255):
            newR = 255
            self.flashDirection = -1
        elif(newR <= 0):
            newR = 0
            self.flashDirection = 1
        
        self.flashColor = Color(newR, 0, 0)
        
        for s in self.snakeTiles:
            s.color.setColor(self.flashColor)
    
    
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
        
sendUntilNoException(b'INITIALIZE;')
time.sleep(3)

intendedUpdateRate = 1 / 100

loop = LoopyThing()
snakeWalls = Walls()
snake = Snake()

keyboard.add_hotkey('up', snake.receiveInput, args=('u'))
keyboard.add_hotkey('down', snake.receiveInput, args=('d'))
keyboard.add_hotkey('left', snake.receiveInput, args=('l'))
keyboard.add_hotkey('right', snake.receiveInput, args=('r'))

counter = 0
lastTime = time.time()
deaths = 0
while(deaths < 5):
    currentTime = time.time()
    deltaTime = currentTime - lastTime
    
    loop.update(currentTime, deltaTime)
    snakeWalls.update(deltaTime)
    snake.update(currentTime, deltaTime)
    
    loopData = loop.constructPacket()
    wallData = snakeWalls.constructPacket()
    snakeData = snake.constructPacket()
    deaths = snake.getDeaths()
    
    #print("Snake Packet:")
    #print(snakeData)
    
    finalPacket = b'RESET;' + loopData + wallData + snakeData + b'PUSH;'
    sendUntilNoException(finalPacket)
    #print("Pushing: " + finalPacket.decode("utf-8"))
    counter += 1
    
    time.sleep(intendedUpdateRate)
    
    lastTime = currentTime
    
sendUntilNoException(b'TERMINATE;')

