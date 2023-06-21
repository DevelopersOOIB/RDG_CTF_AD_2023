from minecraft.networking.connection import Connection
from minecraft.networking.packets import clientbound, serverbound


class Minecraft:
    def __init__(self, username, password, server, port):
        self.offline = True
        self.username = username
        self.password = password
        self.server = server
        self.port = port
    
    def connect(self):
        print("Connecting in offline mode...")
        self.connection = Connection(
        self.server, self.port, username=self.username)

        def handle_join_game(join_game_packet):
            print('Connected.')

        self.connection.register_packet_listener(
            handle_join_game, clientbound.play.JoinGamePacket)

        def print_chat(chat_packet):
            print("Message (%s): %s" % (
                chat_packet.field_string('position'), chat_packet.json_data))

        self.connection.register_packet_listener(
            print_chat, clientbound.play.ChatMessagePacket)

        self.connection.connect()

    def disconnect(self):
        self.connection.disconnect()

    def respawn(self):
        print("respawning...")
        packet = serverbound.play.ClientStatusPacket()
        packet.action_id = serverbound.play.ClientStatusPacket.RESPAWN
        self.connection.write_packet(packet)

    def send_message_to_chat(self, message):
        packet = serverbound.play.ChatPacket()
        packet.message = message
        self.connection.write_packet(packet)