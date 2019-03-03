import pyaudio
import os
import numpy as np
import win32pipe
import win32file
import time
import keyboard

# https://github.com/intxcc/pyaudio_portaudio/blob/master/example/echo_python3.py
# https://www.swharden.com/wp/2016-07-19-realtime-audio-visualization-in-python/
# https://stackoverflow.com/questions/35970282/what-are-chunks-samples-and-frames-when-using-pyaudio

np.set_printoptions(suppress=True) # don't use scientific notation
defaultframes = 1024

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

def normalizeArray(arr):
    minVal = min(arr)
    maxVal = max(arr)
    divide = maxVal - minVal
    res = []
    for a in arr:
        normalizedValue = (a - minVal) / divide
        res.append(normalizedValue)
    return res

def binAverageFreqs(freqs, numBins):
    numPerBin = len(freqs) / numBins
    bins = []
    i = 0
    
    while(i < len(freqs)):
        start = int(round(i))
        end = int(round(i + numPerBin))
        if(end > len(freqs)):
            end = len(freqs)
        
        total = 0
        count = 0
        for j in range(start, end):
            total += freqs[j]
            count += 1
        if(count > 0):
            bins.append(total)
            
        i += numPerBin
        
    normalized = normalizeArray(bins)

    return normalized    

class AudioVisualizer:
    def __init__(self):
        self.defineKeyboardGrid()
        self.colorSpeed = 200
        self.lastUpdate = time.time()
        
    def defineKeyboardGrid(self):
        nameGrid = [
            ["Escape", "SectionSign", "Tab", "CapsLock", "LeftShift", "LeftControl"],
            ["", "1", "Q", "A", "<", "LeftWindows"],
            ["F1", "2", "W", "S", "Z", "LeftAlt"],
            ["F2", "3", "E", "D", "X", ""],
            ["F3", "4", "R", "F", "C", ""],
            ["F4", "5", "T", "G", "V", ""],
            ["", "6", "Y", "H", "B", "Space"],
            ["F5", "7", "U", "J", "N", ""],
            ["F6", "8", "I", "K", "M", ""],
            ["F7", "9", "O", "L", ",", ""],
            ["F8", "0", "P", "UmlautO", ".", "AltGr"],
            ["F9", "+", "TittleA", "UmlautA", "-", "RightWindows"],
            ["F10", "AcuteAccent", "Umlaut", "''", "RightShift", "Function"],
            ["F11", "Backspace", "", "Enter", "", "RightControl"], #F12 doesn't fit. It might be a good idea to put together with F11
            ["PrintScreen", "Insert", "Delete", "", "", "LeftArrow"],
            ["ScreenLock", "Home", "End", "", "UpArrow", "DownArrow"],
            ["Pause", "PageUp", "PageDown", "", "", "RightArrow"],
            ["Calc", "NumLock", "N7", "N4", "N1", "N0"],
            ["Mute", "Divide", "N8", "N5", "N2", ""],
            ["VolumneDown", "Multiply", "N9", "N6", "N3", "NDelete"],
            ["VolumeUp", "Subtract", "", "Add", "", "RightEnter"]
        ]
        
        self.keyGrid = []
        self.columnColors = []
        self.columnHeightHistory = []
        columnHeightHistoryLength = 5
        currentColor = Color(255, 0, 0)
        for column in nameGrid:
            keyColumn = []
            for name in column:
                if(name == ""):
                    keyColumn.append(None)
                else:
                    columnColor = Color(0, 0, 0)
                    columnColor.setColor(currentColor)
                    self.columnColors.append(columnColor)
                    keyColumn.append(KeyColor(name, currentColor.r, currentColor.g, currentColor.b))
            self.keyGrid.append(keyColumn)
            currentColor.loopColorBySteps(250)
            self.columnHeightHistory.append([0] * columnHeightHistoryLength)

    def updateColor(self, deltaTime):
        steps = int(round(self.colorSpeed * deltaTime))
        for i in range(0, len(self.keyGrid)):
            columnColor = self.columnColors[i]
            column = self.keyGrid[i]
            columnColor.loopColorBySteps(steps)
            for key in column:
                if(key != None):
                    key.color.setColor(columnColor)
                
    def constructPacket(self):
        packet = b''
        for column in self.keyGrid:
            for key in column:
                if(key != None):
                    packet += key.constructStringPacket().encode()
        return packet
        

    #Already normalized input
    def colorByAudio(self, normalizedAudioBins):
        assert(len(self.keyGrid) == len(normalizedAudioBins))
        
        currentTime = time.time()
        deltaTime = currentTime - self.lastUpdate
        
        #All columns have full color
        self.updateColor(deltaTime)
        
        #Blacken top keys depending on values in audio bins
        columnHeight = len(self.keyGrid[0])
        for i in range(0, len(normalizedAudioBins)):
            audioBin = normalizedAudioBins[i]
            column = self.keyGrid[i]
            heightHistory = self.columnHeightHistory[i]
            
            #Update height history to average the values to prevent it looking completely random
            newHeight = int(round(columnHeight * audioBin))
            for j in range(0, len(heightHistory) - 1):
                heightHistory[j] = heightHistory[j + 1]
            heightHistory[-1] = newHeight
            self.columnHeightHistory[i] = heightHistory
            average = int(round(np.average(heightHistory)))
            
            for j in range(0, average):
                key = column[j]
                if(key != None):
                    key.color.zeroOut()
        
        self.lastUpdate = currentTime



recorded_frames = []
device_info = {}
useloopback = False
recordtime = 5

p = pyaudio.PyAudio()

try:
    default_device_index = p.get_default_input_device_info()
except IOError:
    default_device_index = -1



#6:       Speakers (High Definition Audio Device)   <-- This is my speaker device, so I hardcoded it.
# Uncomment code here to input manually or hardcode the indices to find your audio device.
# This might vary depending on your pc, drivers, etc so you will need to find it.
# In case of multiple devices with the same name you might want to use hardcoded indices.

#Select Device
#print ("Available devices:\n")
for i in range(0, p.get_device_count()):
    info = p.get_device_info_by_index(i)
    #print (str(info["index"]) + ": \t %s \n \t %s \n" % (info["name"], p.get_host_api_info_by_index(info["hostApi"])["name"]))
    if("Speakers (Realtek High Definiti" in info["name"]):
        default_device_index = info["index"]

    #if default_device_index == -1:
    #    default_device_index = info["index"]

#Handle no devices available
if default_device_index == -1:
    print ("No device available. Quitting.")
    exit()


#Get input or default
#device_id = int(input("Choose device [" + str(default_device_index) + "]: ") or default_device_index)
#print ("")

#Get device info
device_info = p.get_device_info_by_index(default_device_index)
#try:
    #device_info = p.get_device_info_by_index(device_id)
#except IOError:
    #device_info = p.get_device_info_by_index(default_device_index)
    #print ("Selection not available, using default.")

#Choose between loopback or standard mode

is_input = device_info["maxInputChannels"] > 0
is_wasapi = (p.get_host_api_info_by_index(device_info["hostApi"])["name"]).find("WASAPI") != -1
if is_input:
    #print ("Selection is input using standard mode.")
    pass
else:
    if is_wasapi:
        useloopback = True;
        #print ("Selection is output. Using loopback mode.")
    else:
        print ("Selection is input and does not support loopback mode. Quitting.\n")
        exit()

#recordtime = int(input("Record time in seconds [" + str(recordtime) + "]: ") or recordtime)

#Open stream
channelcount = device_info["maxInputChannels"] if (device_info["maxOutputChannels"] < device_info["maxInputChannels"]) else device_info["maxOutputChannels"]
stream = p.open(format = pyaudio.paInt16,
                channels = channelcount,
                rate = int(device_info["defaultSampleRate"]),
                input = True,
                frames_per_buffer = defaultframes,
                input_device_index = device_info["index"],
                as_loopback = useloopback)

sendUntilNoException(b'INITIALIZE;')
time.sleep(3) #Wait for startup
updateRate = 1 / 100
visualizer = AudioVisualizer()

#Exit when escape is pressed
running = True
def escapePressed():
    global running
    running = False
keyboard.add_hotkey('escape', escapePressed)

nextUpdate = time.time() + updateRate
while(running):
    freqDataToUse = None
    while True:
        frames = stream.read(defaultframes)
        data = stream.read(defaultframes)
        sig = np.frombuffer(data, dtype='<i2').reshape(-1, channelcount)
        
        #Some visualization to help understand the audio stream
        #npData = np.fromstring(stream.read(CHUNK),dtype=np.int16)
        #npData = npData * np.hanning(len(data))
        #sampleSize = pyaudio.get_sample_size(pyaudio.paInt16)
        #print(sig)
        
        freqs = []
        for freq in sig:
            LRaverage = int(round((freq[0] + freq[1]) / 2))
            freqs.append(LRaverage)
        
        bins = binAverageFreqs(freqs, 21)
        
        if(time.time() >= nextUpdate):
            break
        
    if(len(bins) != 0):
        nextUpdate = time.time() + updateRate
        visualizer.colorByAudio(bins)
        visualizerData = visualizer.constructPacket()
        packet = b'RESET;' + visualizerData + b'PUSH;'
        sendUntilNoException(packet)
            
    time.sleep(updateRate)
        

# Shutdown

stream.stop_stream()
stream.close()

p.terminate()

sendUntilNoException(b'TERMINATE;')


