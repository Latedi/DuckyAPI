#include <chrono>
#include <thread>

#include "hidapi.h"

#include "TrafficSetup.h"
#include "HIDHandler.h"
#include "SendPreparedTraffic.h"
#include "ColorSetter.h"
#include "NamedPipeHandler.h"

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
}
