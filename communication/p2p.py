import socket
import threading


def start_peer(node_id, host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)

    print("=" * 50)
    print("          ARCHON - P2P PEER")
    print("=" * 50)
    print(f"Node   : {node_id}")
    print(f"Address: {host}:{port}")
    print("Status : ONLINE")
    print("=" * 50)
    print("[P2P] Waiting for peer connections...")

    while True:
        connection, address = server.accept()

        data = connection.recv(4096).decode()

        if data:
            print("\n[P2P MESSAGE RECEIVED]")
            print(f"From    : {address[0]}:{address[1]}")
            print(f"Message : {data}")

        connection.close()


def send_peer_message(host, port, message):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    client.sendall(message.encode())
    client.close()

    print(f"[P2P MESSAGE SENT] {message}")


if __name__ == "__main__":
    start_peer("ZONE_B", "0.0.0.0", 6002)
