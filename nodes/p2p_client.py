from communication.p2p import send_peer_message


if __name__ == "__main__":
    send_peer_message(
        "localhost",
        6002,
        "Artifact disturbance detected at Zone A."
    )
