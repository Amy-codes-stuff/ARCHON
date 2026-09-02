import argparse
import time
import grpc

from communication.proto import archon_pb2
from communication.proto import archon_pb2_grpc


def register_with_coordinator(node_id, host, port, coordinator):
    print("[REGISTRATION] Connecting to Coordinator...")

    channel = grpc.insecure_channel(f"{coordinator}:5000")
    stub = archon_pb2_grpc.ArchonCoordinatorStub(channel)

    response = stub.RegisterNode(
        archon_pb2.NodeRegistration(
            node_id=node_id,
            host=host,
            port=port
        )
    )

    if response.success:
        print(f"[REGISTRATION] {node_id} registered successfully")
        return stub
    else:
        print(f"[REGISTRATION] Failed: {response.message}")
        return None


def send_heartbeat(stub, node_id):
    try:
        response = stub.Heartbeat(
            archon_pb2.HeartbeatRequest(
                node_id=node_id
            )
        )

        if response.acknowledged:
            print(f"[HEARTBEAT] {node_id} acknowledged")

    except grpc.RpcError as e:
        print(f"[HEARTBEAT ERROR] {node_id}: {e}")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--id", required=True)
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--coordinator", default="localhost")

    args = parser.parse_args()

    print()
    print("================================")
    print("       ARCHON ZONE NODE")
    print("================================")
    print(f"Node ID : {args.id}")
    print(f"Host    : {args.host}")
    print(f"Port    : {args.port}")
    print("Status  : ONLINE")
    print("================================")
    print()

    stub = None

    # Keep trying until Coordinator is available
    while stub is None:
        try:
            stub = register_with_coordinator(
                args.id,
                args.host,
                args.port,
                args.coordinator
            )
        except grpc.RpcError as e:
            print(f"[REGISTRATION ERROR] {e}")
            print("[REGISTRATION] Retrying in 3 seconds...")
            time.sleep(3)

    # Send heartbeat every 5 seconds
    while True:
        send_heartbeat(stub, args.id)

        print(
            f"[MONITORING] {args.id} is monitoring "
            "the archaeological site..."
        )

        time.sleep(5)


if __name__ == "__main__":
    main()