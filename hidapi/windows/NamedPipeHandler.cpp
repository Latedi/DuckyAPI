#include "NamedPipeHandler.h"

MessageCommand::MessageCommand(char MessageType, std::string optionalKey, uint8_t optionalR, uint8_t optionalG, uint8_t optionalB)
{
	this->MessageType = MessageType;
	this->optionalKey = optionalKey;
	this->optionalR = optionalR;
	this->optionalG = optionalG;
	this->optionalB = optionalB;
}

NamedPipeHandler::NamedPipeHandler()
{
	hPipe = CreateNamedPipe(TEXT("\\\\.\\pipe\\DuckyController"),
		PIPE_ACCESS_DUPLEX,
		PIPE_TYPE_BYTE | PIPE_READMODE_BYTE | PIPE_WAIT,   // FILE_FLAG_FIRST_PIPE_INSTANCE is not needed but forces CreateNamedPipe(..) to fail if the pipe already exists...
		1,
		0x400,
		0x4000,
		NMPWAIT_USE_DEFAULT_WAIT,
		NULL);

	//ReceiveMessages();
	//PrintMessageQueue();

	/*char data[] = "RESET;Escape 25 28 27;O 245 1 56;PUSH;";
	memcpy(recvBuffer, data, sizeof(data));
	bytesRead = sizeof(data);
	ParseInput();
	PrintMessageQueue();*/
}

void NamedPipeHandler::ReceiveMessages()
{
	if (hPipe != INVALID_HANDLE_VALUE)
	{
		if (ConnectNamedPipe(hPipe, NULL) != FALSE)   // wait for someone to connect to the pipe
		{
			currentMessages = std::vector<MessageCommand>();

			while (ReadFile(hPipe, recvBuffer, sizeof(recvBuffer) - 1, &bytesRead, NULL) != FALSE)
			{
				ParseInput();
				PrintMessageQueue();
			}
		}

		DisconnectNamedPipe(hPipe);
	}
}

void NamedPipeHandler::ParseInput()
{
	uint32_t startPos = 0;
	for (uint32_t i = 0; i < bytesRead; i++)
	{
		char c = (char)recvBuffer[i];
		if (c == ';')
		{
			//Replace ; with null so we can compare it easily
			recvBuffer[i] = '\0';
			std::string subString = std::string((char*)recvBuffer + startPos);

			if (subString == "RESET") //Clear out key colors
			{
				currentMessages.push_back(MessageCommand(
					'R',
					"",
					0,
					0,
					0
				));
			}
			else if (subString == "PUSH") //Write colors to keyboard
			{
				currentMessages.push_back(MessageCommand(
					'P',
					"",
					0,
					0,
					0
				));
			}
			else if (subString == "INITIALIZE") //Take control of the keyboard colors
			{
				currentMessages.push_back(MessageCommand(
					'I',
					"",
					0,
					0,
					0
				));
			}
			else if (subString == "TERMINATE") //Return control of keyboard colors
			{
				currentMessages.push_back(MessageCommand(
					'T',
					"",
					0,
					0,
					0
				));
			}
			else //Set a key color
			{
				std::string key;
				uint8_t R;
				uint8_t G;
				uint8_t B;

				uint32_t startPosColor = startPos;
				uint32_t currentParameter = 0;

				//Extract key name and RGB values
				for (uint32_t j = startPosColor; j <= i; j++)
				{
					char c2 = (char)recvBuffer[j];
					if (c2 == ' ' || j == i)
					{
						recvBuffer[j] = '\0';
						std::string subString2 = std::string((char*)recvBuffer + startPosColor);

						if (currentParameter == 0)
						{
							key = std::string(subString2);
						}
						else if (currentParameter == 1)
						{
							R = atoi(subString2.c_str());
						}
						else if (currentParameter == 2)
						{
							G = atoi(subString2.c_str());
						}
						else if (currentParameter == 3)
						{
							B = atoi(subString2.c_str());
						}

						startPosColor = j + 1;
						currentParameter++;
					}
				}

				currentMessages.push_back(MessageCommand(
					'S',
					key,
					R,
					G,
					B
				));
			}

			startPos = i + 1;
		}
	}
}

void NamedPipeHandler::PrintMessageQueue()
{
	for (uint32_t i = 0; i < currentMessages.size(); i++)
	{
		MessageCommand message = currentMessages[i];
		std::cout << "Message Type: ";
		if (message.MessageType == 'R')
		{
			std::cout << "Reset";
		}
		else if (message.MessageType == 'P')
		{
			std::cout << "Push";
		}
		else if (message.MessageType = 'S')
		{
			std::cout << "Set Color. Key: " << message.optionalKey.c_str() << ". Colors: " << unsigned(message.optionalR) <<
				" " << unsigned(message.optionalG) << " " << unsigned(message.optionalB);
		}
		std::cout << std::endl;
	}
}

std::vector<MessageCommand> NamedPipeHandler::GetMessages()
{
	return currentMessages;
}