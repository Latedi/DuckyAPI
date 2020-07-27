#include "HIDHandler.h"


#include <ostream>
#include <string>

void HIDHandler::Setup()
{
	// handle = hid_open(DuckyVID, DuckyPID, NULL);

	printf("Enumerating through Ducky Products");
	struct hid_device_info *devs, *cur_dev;
	char foundpath[1024];
	devs = hid_enumerate(DuckyVID, DuckyPID);
	cur_dev = devs;
	while (cur_dev) {
		printf("Device: vid/pid: %04hx/%04hx\n  path: %s\n  serial_number: %ls usage_page: %x, usage: %x",
          cur_dev->vendor_id, cur_dev->product_id, cur_dev->path, cur_dev->serial_number, cur_dev->usage_page, cur_dev->usage);
		printf("\n");
		printf("  Manufacturer: %ls\n", cur_dev->manufacturer_string);
		printf("  Product:      %ls\n", cur_dev->product_string);
		printf("\n");
		if( cur_dev->vendor_id == DuckyVID && cur_dev->product_id == DuckyPID && cur_dev->usage_page == UsagePage) { // && cur_dev->usage_page == 0xFFAB && cur_dev->usage == 0x200 ) {
			printf("Found our device!\n");
			strcpy( foundpath, cur_dev->path );
		}
		cur_dev = cur_dev->next;
	}
	handle = hid_open_path(foundpath); 

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

	// std::cout << "writing" << std::endl;
	hid_write(handle, bufOut, length + 1); //The HID header thing adds 0x1 at the start?
	// std::cout << "wrote" << std::endl;
}

uint8_t* HIDHandler::Recv64(uint32_t *bytesReceived)
{
	return Recv(64, bytesReceived); //The HID header thing here too? Not sure
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