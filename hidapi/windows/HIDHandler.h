#pragma once

#include <stdint.h>
#include <iostream>
#include <vector>

#include "hidapi.h"

class HIDHandler
{
private:
	const uint32_t DuckyVID = 0x04d9;
	const uint32_t DuckyPID = 0x0348;
	const uint32_t UsagePage = 0xff00;
	unsigned char bufIn[256];
	unsigned char bufOut[256];

	hid_device *handle;

	void Setup();
public:
	HIDHandler();
	~HIDHandler();
	void Send64(std::vector<uint8_t> bytes);
	void Send(std::vector<uint8_t> bytes, uint32_t length);
	uint8_t* Recv64(uint32_t *bytesReceived);
	uint8_t* Recv(uint32_t length, uint32_t *bytesReceived);
};