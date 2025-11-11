from endstone import Player
from color_plugin.src.packets import SetActorDataPacket
from bedrock_protocol.packets import MinecraftPacketIds

def sendCustomNameToPlayerForPlayer(viewver : Player, target_id : int, name: str):
    packet = SetActorDataPacket(
        target_id,
        [{'id': 4, 'type': 4, 'value': name}]
    ).serialize()
    viewver.send_packet(MinecraftPacketIds.SetActorData, packet)