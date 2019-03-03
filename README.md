# DuckyAPI
Control your Ducky Keyboard's RGB lighting via a named pipe. Can be used to create
your own custom effects and interact with other software, etc. This was developed
for Ducky Shine 7 but might work for other keyboard (untested).

The following is a video of some sample programs in action.
[![Hacked Ducky Shine 7](https://img.youtube.com/vi/qrfjqkIY_k0/0.jpg)](https://youtu.be/qrfjqkIY_k0)

## The API
The API itself is a named pipe created by a c++ program based on hidapi. The code is
based on the hidapi sample. To talk to the API, send commands to the named pipe
** \\.\pipe\DuckyController **

The commands are sent in batches separated by ;

The following commands can be sent:
* INITIALIZE - Takes control of the keyboard
* RESET - Set all key colors to black (no lighting)
* PUSH - Pushe the current set of colors to the keyboard
* TERMINATE - Give control back to the keyboard firmware
* <Key name> <R> <G> <B> - Set the color of a key

The different key names can be found in ColorSetter.cpp.
Note that the keyboard used had Scandinavian key caps and the keys has been named
using a Swedish layout. It should be fairly easy to replace the names should you
prefer another language.

Some examples:

INITIALIZE;F 40 255 255;PUSH;
RESET;H 20 20 20;R 160 56 14;UmlatA 0 0 2;PUSH;
RESET;TERMINATE;

When compiling you might need to copy the .txt files into the directory. In the
release directory you can find the exe and dll should you not want to compile the
project.

## Sample Programs
In the scripts directory you can find the source code for the programs shown in
the video.
Python dependencies:
* pywin32
* keyboard
* numpy
* The following fork of PyAudio: https://github.com/intxcc/pyaudio_portaudio

### snake.py
This one shows some different color changing effects you can use

### audio.py
Visualizes audio output on the keyboard. You will need to find your audio device
for this to work though. There are some comments in the code regarding this.

### message.py
Displays a message on the keyboard

## How To

Here's some text regarding how you can attempt to reproduce this project should
something not work, if you have a similar keyboard, other firmware etc.

...........


