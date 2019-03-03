#include "TrafficSetup.h"

PacketStream::PacketStream() {}

PacketStream::PacketStream(std::string path)
{
	packets = std::vector<Packet>();

	std::ifstream file("Read.txt");
	std::string str;

	std::ifstream packetStreamFile(path);
	if (packetStreamFile.is_open())
	{
		std::string line;
		while (std::getline(packetStreamFile, line))
		{
			if (line != "")
			{
				char direction = line[0];
				if (direction == 'I' || direction == 'O')
				{
					std::string dataString = line.substr(2, line.length());
					Packet packet = BuildPacket(direction, dataString);
					packets.push_back(packet);
				}
			}
		}
	}
	else
	{
		std::cout << "Error opening file " << path << std::endl;
	}

	std::cout << "PacketStream " << path << " parsed correctly" << std::endl;
}

Packet PacketStream::BuildPacket(char direction, std::string data)
{
	PacketDirection packetDirection = HostToUSB;
	if (direction == 'I')
		packetDirection = USBToHost;

	if (data.length() % 2 != 0)
	{
		std::cout << "Error. Uneven data length";
	}

	uint32_t byteArrayLength = data.length() / 2;
	std::vector<uint8_t> PacketData = std::vector<uint8_t>();
	for (uint32_t i = 0; i < byteArrayLength; i++)
	{
		int startIndex = i * 2;

		char hexChars[3];
		hexChars[0] = data[startIndex];
		hexChars[1] = data[startIndex + 1];
		hexChars[2] = '\x00';

		uint8_t byte = (uint8_t)strtol(hexChars, NULL, 16);
		PacketData.push_back(byte);
	}

	Packet result = Packet
	{
		packetDirection,
		byteArrayLength,
		PacketData
	};

	return result;
}

void PacketStream::PrintPacket(Packet packet)
{
	for (uint32_t i = 0; i < packet.PacketDataLength; i++)
	{
		uint8_t value = packet.PacketData[i];
		printf("%02x", value);
	}
	printf("\n");
}

void PacketStream::PrintAllPackets()
{
	for (Packet packet : packets)
	{
		PrintPacket(packet);
	}
}

TrafficSetup::TrafficSetup()
{
	std::string initFilePath = "Traffic_Init.txt";
	std::string exitFilePath = "Traffic_Exit.txt";

	InitStream = std::unique_ptr<PacketStream>(new PacketStream(initFilePath));
	ExitStream = std::unique_ptr<PacketStream>(new PacketStream(exitFilePath));
}

/*TrafficSetup::~TrafficSetup()
{
	delete InitStream;
	delete ExitStream;
}*/