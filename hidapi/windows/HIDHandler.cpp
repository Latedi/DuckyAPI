#include "HIDHandler.h"

void HIDHandler::Setup()
{
	handle = hid_open(DuckyVID, DuckyPID, NULL);

	if (!handle) {
		std::cout << "Unable to open device" << std::endl;
		return;
	}

	hid_set_nonblocking(handle, 1);
	memset(bufIn, 0, sizeof(bufIn));
	memset(bufOut, 0, sizeof(bufOut));
}

HIDHandler::HIDHandler()
{
	Setup();
}

HIDHandler::~HIDHandler()
{
	hid_close(handle);
	hid_exit();
}

void HIDHandler::Send64(std::vector<uint8_t>bytes)
{
	Send(bytes, 64);
}

void HIDHandler::Send(std::vector<uint8_t> bytes, uint32_t length)
{
	memset(bufOut, 0, sizeof(bufOut));

	bufOut[0] = 0x1;

	for (uint32_t i = 0; i < length; i++)
	{
		bufOut[i + 1] = bytes[i];
	}

	hid_write(handle, bufOut, length + 1); //The HID header thing adds 0x1 at the start?
}

uint8_t* HIDHandler::Recv64(uint32_t *bytesReceived)
{
	return Recv(64 + 1, bytesReceived); //The HID header thing here too? Not sure
}

uint8_t* HIDHandler::Recv(uint32_t length, uint32_t *bytesReceived)
{
	memset(bufIn, 0, sizeof(bufIn));

	uint32_t result = 0;
	while (result == 0) //Why loop instead of using a blocking read ???
	{
		result = hid_read(handle, bufIn, length);

		if (result < 0)
		{
			std::cout << "Error receiving" << std::endl;
		}
	}

	*bytesReceived = result;
	return bufIn;
}