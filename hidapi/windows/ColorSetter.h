#pragma once

#include <chrono>
#include <thread>

#include "TrafficSetup.h"
#include "HIDHandler.h"

struct KeyColorData
{
	std::string name;
	uint8_t packetNumber;
	uint8_t offset;
	uint8_t R;
	uint8_t G;
	uint8_t B;
};

class ColorSetter
{
private:
	std::vector<KeyColorData> keys;
	HIDHandler* handler;
	uint8_t bytes[512];

	void GenerateKeys();
	void AddKey(char name[], uint8_t packetNumber, uint8_t offset);
	void constructBytesToSend();
public:
	ColorSetter(HIDHandler *handler);
	std::vector<std::string> GetKeyList();
	bool SetKeyColor(std::string key, uint8_t R, uint8_t G, uint8_t B);
	bool SetKeyColor(uint32_t index, uint8_t R, uint8_t G, uint8_t B);
	void PushColors();
	void ResetColors();
	void RunTest();
	void TestOffset(uint8_t packet, uint8_t offset);
};

