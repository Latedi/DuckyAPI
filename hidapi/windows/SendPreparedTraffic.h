#pragma once

#include "TrafficSetup.h"
#include "HIDHandler.h"
#include <stdio.h>

struct PreparedTrafficResults
{
	uint32_t successes;
	uint32_t failures;
};

class SendPreparedTraffic
{
private:
	TrafficSetup setup;
	HIDHandler *handler;

	bool HandlePacket(Packet packet);
	bool ComparePackets(Packet parsedPacket, Packet receivedPacket);
	PreparedTrafficResults ExecutePacketStream(std::unique_ptr<PacketStream> *stream);
public:
	SendPreparedTraffic(HIDHandler *handler);
	void Initialize();
	void Terminate();
};

