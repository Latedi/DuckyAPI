#include <chrono>
#include <thread>

#include "hidapi.h"

#include "../windows/TrafficSetup.h"
#include "../windows/SendPreparedTraffic.h"
#include "../windows/ColorSetter.h"
#include "../windows/NamedPipeHandler.h"
#include "../windows/HIDHandler.h"

int main(int argc, char* argv[])
{
	NamedPipeHandler pipeHandler = NamedPipeHandler();
	HIDHandler handler = HIDHandler();
	SendPreparedTraffic prepared = SendPreparedTraffic(&handler);
	ColorSetter setter = ColorSetter(&handler);
	
	/*prepared.Initialize();
	setter.RunTest();
	prepared.Terminate();
	return 0;*/
	
	while (true)
	{
		pipeHandler.ReceiveMessages();
		std::vector<MessageCommand> messages = pipeHandler.GetMessages();
	
		for (uint32_t i = 0; i < messages.size(); i++)
		{
			MessageCommand message = messages[i];
	
			if (message.MessageType == 'I')
			{
				prepared.Initialize();
			}
			else if (message.MessageType == 'T')
			{
				setter.ResetColors();
				setter.PushColors();
				prepared.Terminate();
				break;
			}
			else if (message.MessageType == 'P')
			{
				setter.PushColors();
			}
			else if (message.MessageType == 'R')
			{
				setter.ResetColors();
			}
			else if (message.MessageType == 'S')
			{
				setter.SetKeyColor(message.optionalKey, message.optionalR, message.optionalG, message.optionalB);
			}
		}
	}
	
	return 0;
	//
	//
	//
	//
	//
	// NamedPipeHandler pipeHandler = NamedPipeHandler();
	// HIDHandler handler = HIDHandler();
	// SendPreparedTraffic prepared = SendPreparedTraffic(&handler);
	// ColorSetter setter = ColorSetter(&handler);
	//
	// prepared.Initialize();
	// std::cin.ignore();
	// // setter.ResetColors();
	// // std::cin.ignore();
	// for(uint8_t i = 0; i < 8; i++) {
	// 	for(uint8_t j = 0x08; j < 0x3e; j += 0x03) {
	// 		setter.TestOffset(i, j);
	// 		std::cin.ignore();
	// 	}
	// }
	// prepared.Terminate();
}