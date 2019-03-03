#include "SendPreparedTraffic.h"

SendPreparedTraffic::SendPreparedTraffic(HIDHandler *handler)
{
	//setup = TrafficSetup();
	this->handler = handler;
}

void SendPreparedTraffic::Initialize()
{
	//std::cout << "Initializing..." << std::endl;

	PreparedTrafficResults results = ExecutePacketStream(&setup.InitStream);
	size_t totalPackets = setup.InitStream->packets.size();

	//std::cout << "Initialization done. Successfully sent " << results.successes << " packets out of " << totalPackets << ". " << results.failures << " failures." << std::endl;
}

void SendPreparedTraffic::Terminate()
{
	//std::cout << "Terminating..." << std::endl;

	PreparedTrafficResults results = ExecutePacketStream(&setup.ExitStream);
	size_t totalPackets = setup.ExitStream->packets.size();

	//std::cout << "Termination done. Successfully sent " << results.successes << " packets out of " << totalPackets << ". " << results.failures << " failures." << std::endl;
}

PreparedTrafficResults SendPreparedTraffic::ExecutePacketStream(std::unique_ptr<PacketStream> *stream)
{
	uint32_t successes = 0;
	uint32_t failures = 0;

	size_t totalPackets = (*stream)->packets.size();
	for (size_t i = 0; i < totalPackets; i++)
	{
		Packet packet = (*stream)->packets[i];

		bool result = HandlePacket(packet);

		if (result)
			successes++;
		else
			failures++;
	}

	PreparedTrafficResults results =
	{
		successes,
		failures
	};

	return results;
}

bool SendPreparedTraffic::HandlePacket(Packet packet)
{
	if (packet.Direction == HostToUSB)
	{
		handler->Send64(packet.PacketData);
		return true;
	}
	else if (packet.Direction == USBToHost)
	{
		uint32_t bytesReceived;
		uint8_t *result = handler->Recv64(&bytesReceived);
		
		std::vector<uint8_t> receivedBytes = std::vector<uint8_t>();
		for (uint32_t i = 0; i < bytesReceived; i++)
		{
			uint8_t value = result[i];
			receivedBytes.push_back(value);
		}

		Packet receivedPacket =
		{
			USBToHost,
			packet.PacketDataLength,
			receivedBytes
		};

		bool packetsMatching = ComparePackets(packet, receivedPacket);

		if (!packetsMatching)
		{
			/*std::cout << "Received packet not matching expectations" << std::endl;
			std::cout << "Expected: " << std::endl;
			PacketStream::PrintPacket(packet);
			std::cout << "Received: " << std::endl;
			PacketStream::PrintPacket(receivedPacket);*/
			return false;
		}
		else
		{
			return true;
		}
	}

	return false;
}

bool SendPreparedTraffic::ComparePackets(Packet parsedPacket, Packet receivedPacket)
{
	if (parsedPacket.Direction != receivedPacket.Direction)
		return false;

	if (parsedPacket.PacketDataLength != receivedPacket.PacketDataLength)
		return false;

	for (uint32_t i = 0; i < parsedPacket.PacketDataLength; i++)
	{
		if (parsedPacket.PacketData[i] != receivedPacket.PacketData[i])
			return false;
	}

	return true;
}