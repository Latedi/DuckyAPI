#pragma once

#include <string>
#include <vector>
#include <fstream>
#include <iostream>
#include <stdio.h>

enum PacketDirection
{
	HostToUSB,
	USBToHost
};

struct Packet
{
	PacketDirection Direction;
	uint32_t PacketDataLength;
	std::vector<uint8_t> PacketData; //Because printing byte arrays is suffering
};

class PacketStream
{
public:
	std::vector<Packet> packets;

	PacketStream();
	//~PacketStream();
	PacketStream(std::string path);
	static void PrintPacket(Packet packet);
	void PrintAllPackets();
	Packet BuildPacket(char direction, std::string data);
};

class TrafficSetup
{
public:
	std::unique_ptr<PacketStream> InitStream;
	std::unique_ptr<PacketStream> ExitStream;

	TrafficSetup();
	//~TrafficSetup();
};