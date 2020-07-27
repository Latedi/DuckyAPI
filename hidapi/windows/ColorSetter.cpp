#include "ColorSetter.h"



#include <ios>
#include <iostream>
#include <ostream>
#include <valarray>


ColorSetter::ColorSetter(HIDHandler *handler)
{
	this->handler = handler;
	GenerateKeys();
}

void ColorSetter::GenerateKeys()
{
	keys = std::vector<KeyColorData>();

	// Packet 0
	AddKey("Escape", 0, 0x08);
	AddKey("SectionSign", 0, 0x0b);
	AddKey("Tab", 0, 0x0e);
	AddKey("CapsLock", 0, 0x11);
	AddKey("LeftShift", 0, 0x14);
	AddKey("LeftControl", 0, 0x17);
	// 0 0x1a
	AddKey("1", 0, 0x1d);
	AddKey("Q", 0, 0x20);
	AddKey("A", 0, 0x23);
	// 0 0x26
	AddKey("LeftWindows", 0, 0x29);
	AddKey("F1", 0, 0x2c);
	AddKey("2", 0, 0x2f);
	AddKey("W", 0, 0x32);
	AddKey("S", 0, 0x35);
	AddKey("Z", 0, 0x38);
	AddKey("LeftAlt", 0, 0x3b);

	// Packet 1
	AddKey("F2", 1, 0x08);
	AddKey("3", 1, 0x0b);
	AddKey("E", 1, 0x0e);
	AddKey("D", 1, 0x11);
	AddKey("X", 1, 0x14);
	// 1 0x17
	AddKey("F3", 1, 0x1a);
	AddKey("4", 1, 0x1d);
	AddKey("R", 1, 0x20);
	AddKey("F", 1, 0x23);
	AddKey("C", 1, 0x26);
	// 1 0x29
	AddKey("F4", 1, 0x2c);
	AddKey("5", 1, 0x2f);
	AddKey("T", 1, 0x32);
	AddKey("G", 1, 0x35);
	AddKey("V", 1, 0x38);
	// 1 0x3b

	// Packet 2
	// 2 0x08
	AddKey("6", 2, 0x0b);
	AddKey("Y", 2, 0x0e);
	AddKey("H", 2, 0x11);
	AddKey("B", 2, 0x14);
	AddKey("Space", 2, 0x17);
	AddKey("F5", 2, 0x1a);
	AddKey("7", 2, 0x1d);
	AddKey("U", 2, 0x20);
	AddKey("J", 2, 0x23);
	AddKey("N", 2, 0x26);
	// 2 0x29
	AddKey("F6", 2, 0x2c);
	AddKey("8", 2, 0x2f);
	AddKey("I", 2, 0x32);
	AddKey("K", 2, 0x35);
	AddKey("M", 2, 0x38);
	// 2 0x3b

	// Packet 3
	AddKey("F7", 3, 0x08);
	AddKey("9", 3, 0x0b);
	AddKey("O", 3, 0x0e);
	AddKey("L", 3, 0x11);
	AddKey(",", 3, 0x14);
	// 3 0x17
	AddKey("F8", 3, 0x1a);
	AddKey("0", 3, 0x1d);
	AddKey("P", 3, 0x20);
	AddKey("Semicolon", 3, 0x23);
	AddKey(".", 3, 0x26);
	AddKey("RightAlt", 3, 0x29);
	AddKey("F9", 3, 0x2c);
	AddKey("-", 3, 0x2f);
	AddKey("[", 3, 0x32);
	AddKey("'", 3, 0x35);
	AddKey("FSlash", 3, 0x38);
	// 3 0x3b

	// Packet 4
	AddKey("F10", 4, 0x08);
	AddKey("=", 4, 0x0b);
	AddKey("]", 4, 0x0e);
	// 4 0x11
	// 4 0x14
	AddKey("RightWindows", 4, 0x17);
	AddKey("F11", 4, 0x1a);
	// 4 0x1d
	// 4 0x20
	// 4 0x23
	AddKey("RightShift", 4, 0x26);
	AddKey("Function", 4, 0x29);
	AddKey("F12", 4, 0x2c);
	AddKey("Backspace", 4, 0x2f);
	AddKey("BSlash", 4, 0x32);
	AddKey("Enter", 4, 0x35);
	// 4 0x38
	AddKey("RightControl", 4, 0x3b);

	// Packet 5
	AddKey("PrintScreen", 5, 0x08);
	AddKey("Insert", 5, 0x0b);
	AddKey("Delete", 5, 0x0e);
	// 5 0x11
	// 5 0x14
	AddKey("LeftArrow", 5, 0x17);
	AddKey("ScrollLock", 5, 0x1a);
	AddKey("Home", 5, 0x1d);
	AddKey("End", 5, 0x20);
	// 5 0x23
	AddKey("UpArrow", 5, 0x26);
	AddKey("DownArrow", 5, 0x29);
	AddKey("Pause", 5, 0x2c);
	AddKey("PageUp", 5, 0x2f);
	AddKey("PageDown", 5, 0x32);
	// 5 0x35
	// 5 0x38
	AddKey("RightArrow", 5, 0x3b);

	// Packet 6
	AddKey("Calc", 6, 0x08);
	AddKey("NumLock", 6, 0x0b);
	AddKey("N7", 6, 0x0e);
	AddKey("N4", 6, 0x11);
	AddKey("N1", 6, 0x14);
	AddKey("N0", 6, 0x17);
	AddKey("Mute", 6, 0x1a);
	AddKey("Divide", 6, 0x1d);
	AddKey("N8", 6, 0x20);
	AddKey("N5", 6, 0x23);
	AddKey("N2", 6, 0x26);
	// 6 0x29
	AddKey("VolumeDown", 6, 0x2c);
	AddKey("Multiply", 6, 0x2f);
	AddKey("N9", 6, 0x32);
	AddKey("N6", 6, 0x35);
	AddKey("N3", 6, 0x38);
	AddKey("NDelete", 6, 0x3b);

	// Packet 7
	AddKey("VolumeUp", 7, 0x08);
	AddKey("Subtract", 7, 0x0b);
	AddKey("Add", 7, 0x0e);
	// 7 0x11
	// 7 0x14
	AddKey("RightEnter", 7, 0x17);
}

std::vector<std::string> ColorSetter::GetKeyList()
{
	std::vector<std::string> allKeys;
	for (uint32_t i = 0; i < keys.size(); i++)
	{
		allKeys.push_back(keys[i].name);
	}
	return allKeys;
}

void ColorSetter::AddKey(char name[], uint8_t packetNumber, uint8_t offset)
{
	uint8_t initColor = 0;
	uint8_t finalOffset = offset - 1;

	KeyColorData key = KeyColorData
	{
		std::string(name),
		packetNumber,
		finalOffset, //The documented offsets were more like byte numbers, so reduce by 1
		initColor,
		initColor,
		initColor
	};
	keys.push_back(key);
}

bool ColorSetter::SetKeyColor(std::string key, uint8_t R, uint8_t G, uint8_t B)
{
	for (uint32_t i = 0; i < keys.size(); i++)
	{
		if (keys[i].name == key)
		{
			keys[i].R = R;
			keys[i].G = G;
			keys[i].B = B;
			return true;
		}
	}
	return false;
}

bool ColorSetter::SetKeyColor(uint32_t index, uint8_t R, uint8_t G, uint8_t B)
{
	keys[index].R = R;
	keys[index].G = G;
	keys[index].B = B;
	return true;
}

void ColorSetter::constructBytesToSend()
{
	//Technically the headers won't need to be zeroed out, but it's easier
	memset(bytes, 0, sizeof(bytes));

	// //Set initialize color packet
	// bytes[0] = 0x56;
	// bytes[1] = 0x81;
	// bytes[4] = 0x1;
	// bytes[8] = 0x08;
	// bytes[12] = 0xAA;
	// bytes[13] = 0xAA;
	// bytes[14] = 0xAA;
	// bytes[15] = 0xAA;
	//
	// //Set color packet headers
	// for (uint32_t i = 0; i < 8; i++)
	// {
	// 	uint32_t packetStartIndex = (i + 1) * 64;
	// 	bytes[packetStartIndex + 0] = 0x56;
	// 	bytes[packetStartIndex + 1] = 0x83;
	// 	bytes[packetStartIndex + 2] = (uint8_t) i;
	// }
	//
	// //First color packet has some specific headers
	// bytes[64 + 4] = 0x1;
	// bytes[64 + 8] = 0x80;
	// bytes[64 + 9] = 0x01;
	// bytes[64 + 11] = 0xC1;
	// bytes[64 + 16] = 0xFF;
	// bytes[64 + 17] = 0xFF;
	// bytes[64 + 18] = 0xFF;
	// bytes[64 + 19] = 0xFF;
	//
	// //Grab all individual key colors
	// for (uint32_t i = 0; i < keys.size(); i++)
	// {
	// 	KeyColorData key = keys[i];
	// 	uint32_t startOffset = (key.packetNumber + 1) * 64 + key.offset + 1;
	// 	uint32_t finalPacketByte = (key.packetNumber + 2) * 64;
	//
	// 	uint32_t offsets[3] = {
	// 		startOffset + 0,
	// 		startOffset + 1,
	// 		startOffset + 2
	// 	};
	//
	// 	for (uint8_t i = 0; i < 3; i++)
	// 	{
	// 		if (offsets[i] >= finalPacketByte)
	// 		{
	// 			offsets[i] += 4;
	// 		}
	// 	}
	//
	// 	bytes[offsets[0]] = key.R;
	// 	bytes[offsets[1]] = key.G;
	// 	bytes[offsets[2]] = key.B;
	//
	// 	/*if (key.R != 0 || key.G != 0 || key.B != 0)
	// 	{
	// 		std::cout << "Setting color for " << key.name.c_str() << std::endl;
	// 	}*/
	// }
	//
	//
	// //Set terminate color packet
	// bytes[64 * 9 + 0] = 0x51;
	// bytes[64 * 9 + 1] = 0x28;
	// bytes[64 * 9 + 4] = 0xFF;
	

	// Set color packet headers
	for (uint32_t i = 0; i < 8; i++)
	{
		uint32_t packetStartIndex = i * 64;
		bytes[packetStartIndex + 0] = 0x56;
		bytes[packetStartIndex + 1] = 0x42;
		bytes[packetStartIndex + 4] = 0x02;
		if(i == 7) {
			bytes[packetStartIndex + 5] = 0x06;
		} else {
			bytes[packetStartIndex + 5] = 0x12;
		}
		bytes[packetStartIndex + 6] = (uint8_t) (18 * i);
		// printf("%02x %02x", bytes[packetStartIndex + 6], (uint8_t) (18 * i));
		// std::cout << std::endl;
		
	}

	//Grab all individual key colors
	for (uint32_t i = 0; i < keys.size(); i++)
	{
		KeyColorData key = keys[i];
		uint32_t startOffset = (key.packetNumber + 0) * 64 + key.offset + 1;
		uint32_t finalPacketByte = (key.packetNumber + 1) * 64;
	
		uint32_t offsets[3] = {
			startOffset + 0,
			startOffset + 1,
			startOffset + 2
		};
	
		for (uint8_t j = 0; i < 3; i++)
		{
			if (offsets[j] >= finalPacketByte)
			{
				offsets[j] += 4;
			}
		}
	
		bytes[offsets[0]] = key.R;
		bytes[offsets[1]] = key.G;
		bytes[offsets[2]] = key.B;
	
		/*if (key.R != 0 || key.G != 0 || key.B != 0)
		{
			std::cout << "Setting color for " << key.name.c_str() << std::endl;
		}*/
	}
	
}

void ColorSetter::TestOffset(uint8_t packet, uint8_t offset) {
	memset(bytes, 0, sizeof(bytes));
	// Set color packet headers
	std::cout << "Testing " << static_cast<int>(packet) << " 0x" <<std::hex << static_cast<int>(offset) << std::endl;
	for (uint32_t i = 0; i < 8; i++)
	{
		uint32_t packetStartIndex = i * 64;
		bytes[packetStartIndex + 0] = 0x56;
		bytes[packetStartIndex + 1] = 0x42;
		bytes[packetStartIndex + 4] = 0x02;
		if(i == 7) {
			bytes[packetStartIndex + 5] = 0x06;
		} else {
			bytes[packetStartIndex + 5] = 0x12;
		}
		bytes[packetStartIndex + 6] = (uint8_t) (18 * i);
		// printf("%02x %02x", bytes[packetStartIndex + 6], (uint8_t) (18 * i));
		// std::cout << std::endl;
		
	}

	bytes[packet * 64 + offset + 0] = 0xFF;
	bytes[packet * 64 + offset + 1] = 0xFF;
	bytes[packet * 64 + offset + 2] = 0xFF;

	PushColors();
}

void ColorSetter::PushColors()
{
	//std::cout << "Pusing colors" << std::endl;
	constructBytesToSend();

	for (uint32_t i = 0; i < 8; i++)
	{
		std::vector<uint8_t> packetBytes; //Inefficiency at it's best
		
		for (uint32_t j = i * 64; j < (i + 1) * 64; j++)
		{
			packetBytes.push_back(bytes[j]);
			// printf("%02x", bytes[j]);
		}
		// std::cout << std::endl;

		Packet debugPacket =
		{
			HostToUSB,
			64,
			packetBytes
		};
		// PacketStream::PrintPacket(debugPacket);

		handler->Send64(packetBytes);

		// Wait for response
		uint32_t bytesReceived;
		uint8_t *result = handler->Recv64(&bytesReceived);
	}
}

void ColorSetter::ResetColors()
{
	//std::cout << "Resetting colors" << std::endl;
	for (uint32_t i = 0; i < keys.size(); i++)
	{
		keys[i].R = 0;
		keys[i].G = 0;
		keys[i].B = 0;
	}
}

void ColorSetter::RunTest()
{
	for (uint32_t i = 0; i < keys.size(); i++)
	{
		ResetColors();
		SetKeyColor(i, 0xFF, 0xFF, 0xFF);
		PushColors();
		std::this_thread::sleep_for(std::chrono::milliseconds(250));
	}
}