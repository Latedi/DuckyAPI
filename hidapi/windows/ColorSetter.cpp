#include "ColorSetter.h"


ColorSetter::ColorSetter(HIDHandler *handler)
{
	this->handler = handler;
	GenerateKeys();
}

void ColorSetter::GenerateKeys()
{
	keys = std::vector<KeyColorData>();

	AddKey("Escape", 0, 0x18);
	AddKey("SectionSign", 0, 0x1B);
	AddKey("Tab", 0, 0x1E);
	AddKey("CapsLock", 0, 0x21);
	AddKey("LeftShift", 0, 0x24);
	AddKey("LeftControl", 0, 0x27);
	AddKey("1", 0, 0x2D);
	AddKey("Q", 0, 0x30);
	AddKey("A", 0, 0x33);
	AddKey("<", 0, 0x36);
	AddKey("LeftWindows", 0, 0x39);
	AddKey("F1", 0, 0x3C);
	AddKey("2", 0, 0x3F);

	AddKey("W", 1, 0x6);
	AddKey("S", 1, 0x9);
	AddKey("Z", 1, 0xC);
	AddKey("LeftAlt", 1, 0xF);
	AddKey("F2", 1, 0x12);
	AddKey("3", 1, 0x15);
	AddKey("E", 1, 0x18);
	AddKey("D", 1, 0x1B);
	AddKey("X", 1, 0x1E);
	AddKey("F3", 1, 0x24);
	AddKey("4", 1, 0x27);
	AddKey("R", 1, 0x2A);
	AddKey("F", 1, 0x2D);
	AddKey("C", 1, 0x30);
	AddKey("F4", 1, 0x36);
	AddKey("5", 1, 0x39);
	AddKey("T", 1, 0x3C);
	AddKey("G", 1, 0x3F);

	AddKey("V", 2, 0x6);
	AddKey("6", 2, 0xF);
	AddKey("Y", 2, 0x12);
	AddKey("H", 2, 0x15);
	AddKey("B", 2, 0x18);
	AddKey("Space", 2, 0x1B);
	AddKey("F5", 2, 0x1E);
	AddKey("7", 2, 0x21);
	AddKey("U", 2, 0x24);
	AddKey("J", 2, 0x27);
	AddKey("N", 2, 0x2A);
	AddKey("F6", 2, 0x30);
	AddKey("8", 2, 0x33);
	AddKey("I", 2, 0x36);
	AddKey("K", 2, 0x39);
	AddKey("M", 2, 0x3C);

	AddKey("F7", 3, 0x6);
	AddKey("9", 3, 0x9);
	AddKey("O", 3, 0xC);
	AddKey("L", 3, 0xF);
	AddKey(",", 3, 0x12);
	AddKey("F8", 3, 0x18);
	AddKey("0", 3, 0x1B);
	AddKey("P", 3, 0x1E);
	AddKey("UmlautO", 3, 0x21);
	AddKey(".", 3, 0x24);
	AddKey("AltGr", 3, 0x27);
	AddKey("F9", 3, 0x2A);
	AddKey("+", 3, 0x2D);
	AddKey("TittleA", 3, 0x30);
	AddKey("UmlautA", 3, 0x33);
	AddKey("-", 3, 0x36);
	AddKey("F10", 3, 0x3C);
	AddKey("AcuteAccent", 3, 0x3F);

	AddKey("Umlaut", 4, 0x6);
	AddKey("'", 4, 0x9);
	AddKey("RightWindows", 4, 0xF);
	AddKey("F11", 4, 0x12);
	AddKey("RightShift", 4, 0x1E);
	AddKey("Function", 4, 0x21);
	AddKey("F12", 4, 0x24);
	AddKey("Backspace", 4, 0x27);
	AddKey("Enter", 4, 0x2D);
	AddKey("RightControl", 4, 0x33);
	AddKey("PrintScreen", 4, 0x36);
	AddKey("Insert", 4, 0x39);
	AddKey("Delete", 4, 0x3C);

	AddKey("LeftArrow", 5, 0x9);
	AddKey("ScreenLock", 5, 0xC);
	AddKey("Home", 5, 0xF);
	AddKey("End", 5, 0x12);
	AddKey("UpArrow", 5, 0x18);
	AddKey("DownArrow", 5, 0x1B);
	AddKey("Pause", 5, 0x1E);
	AddKey("PageUp", 5, 0x21);
	AddKey("PageDown", 5, 0x24);
	AddKey("RightArrow", 5, 0x2D);
	AddKey("Calc", 5, 0x30);
	AddKey("NumLock", 5, 0x33);
	AddKey("N7", 5, 0x36);
	AddKey("N4", 5, 0x39);
	AddKey("N1", 5, 0x3C);
	AddKey("N0", 5, 0x3F);

	AddKey("Mute", 6, 0x6);
	AddKey("Divide", 6, 0x9);
	AddKey("N8", 6, 0xC);
	AddKey("N5", 6, 0xF);
	AddKey("N2", 6, 0x12);
	AddKey("VolumeDown", 6, 0x18);
	AddKey("Multiply", 6, 0x1B);
	AddKey("N9", 6, 0x1E);
	AddKey("N6", 6, 0x21);
	AddKey("N3", 6, 0x24);
	AddKey("NDelete", 6, 0x27);
	AddKey("VolumeUp", 6, 0x2A);
	AddKey("Subtract", 6, 0x2D);
	AddKey("Add", 6, 0x30);
	AddKey("RightEnter", 6, 0x39);
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

	//Set initialize color packet
	bytes[0] = 0x56;
	bytes[1] = 0x81;
	bytes[4] = 0x1;
	bytes[8] = 0x08;
	bytes[12] = 0xAA;
	bytes[13] = 0xAA;
	bytes[14] = 0xAA;
	bytes[15] = 0xAA;

	//Set color packet headers
	for (uint32_t i = 0; i < 8; i++)
	{
		uint32_t packetStartIndex = (i + 1) * 64;
		bytes[packetStartIndex + 0] = 0x56;
		bytes[packetStartIndex + 1] = 0x83;
		bytes[packetStartIndex + 2] = (uint8_t) i;
	}

	//First color packet has some specific headers
	bytes[64 + 4] = 0x1;
	bytes[64 + 8] = 0x80;
	bytes[64 + 9] = 0x01;
	bytes[64 + 11] = 0xC1;
	bytes[64 + 16] = 0xFF;
	bytes[64 + 17] = 0xFF;
	bytes[64 + 18] = 0xFF;
	bytes[64 + 19] = 0xFF;

	//Grab all individual key colors
	for (uint32_t i = 0; i < keys.size(); i++)
	{
		KeyColorData key = keys[i];
		uint32_t startOffset = (key.packetNumber + 1) * 64 + key.offset + 1;
		uint32_t finalPacketByte = (key.packetNumber + 2) * 64;

		uint32_t offsets[3] = {
			startOffset + 0,
			startOffset + 1,
			startOffset + 2
		};

		for (uint8_t i = 0; i < 3; i++)
		{
			if (offsets[i] >= finalPacketByte)
			{
				offsets[i] += 4;
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


	//Set terminate color packet
	bytes[64 * 9 + 0] = 0x51;
	bytes[64 * 9 + 1] = 0x28;
	bytes[64 * 9 + 4] = 0xFF;
}

void ColorSetter::PushColors()
{
	//std::cout << "Pusing colors" << std::endl;
	constructBytesToSend();

	for (uint32_t i = 0; i < 10; i++)
	{
		std::vector<uint8_t> packetBytes; //Inefficiency at it's best
		for (uint32_t j = i * 64; j < (i + 1) * 64; j++)
		{
			packetBytes.push_back(bytes[j]);
		}

		Packet debugPacket =
		{
			HostToUSB,
			64,
			packetBytes
		};
		//PacketStream::PrintPacket(debugPacket);

		handler->Send64(packetBytes);
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