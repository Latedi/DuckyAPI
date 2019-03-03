#pragma once

#include <windows.h>
#include <stdint.h>
#include <iostream>
#include <vector>



class MessageCommand
{
public:
	char MessageType;
	std::string optionalKey;
	uint8_t optionalR;
	uint8_t optionalG;
	uint8_t optionalB;
	MessageCommand(char MessageType, std::string optionalKey, uint8_t optionalR, uint8_t optionalG, uint8_t optionalB);
};

class NamedPipeHandler
{
private:
	HANDLE hPipe;

	uint8_t recvBuffer[0x4000];
	DWORD bytesRead;
	std::vector<MessageCommand> currentMessages;

	uint8_t sendBuffer[0x400];

	void ParseInput();
public:
	NamedPipeHandler();
	void ReceiveMessages();
	void PrintMessageQueue();
	std::vector<MessageCommand> GetMessages();
};