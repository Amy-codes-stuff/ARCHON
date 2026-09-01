import argparse
import time
from datetime import datetime

import grpc

from communication.proto import archon_pb2
from communication.proto import archon_pb2_grpc


def register_with_coordinator(node_id, host, port, coordinator_host):
    print("[REGISTRATION] Connecting to Coordinator...")

    channel = grpc.insecure_channel(
        f"{coordinator_host}:5000"
    )

    stub = archon_pb2_grpc.ArchonCoordinatorStub(channel)

    request = archon_pb2.NodeRegistration(
        node_id=node_id,
        host=host,
        port=port
    )

    response = stub.RegisterNode(request)

    if response.success:
        print(f"[REGISTRATION] {response.message}")
    else:
        print("[REGISTRATION] Registration failed")


def main():
    parser = argparse.ArgumentParser(
        description="ARCHON Distributed Zone Node"
    )

    parser.add_argument("--id", required=True)
    parser.add_argument("--port", required=True, type=int)

    parser.add_argument(
        "--host",
        default="localhost"
    )

    parser.add_argument(
        "--coordinator",
        default="localhost"
    )

    args = parser.parse_args()

    print("=" * 50)
    print("        ARCHON - DISTRIBUTED ZONE NODE")
    print("=" * 50)
    print(f"Node ID : {args.id}")
    print(f"Host    : {args.host}")
    print(f"Port    : {args.port}")
    print("Status  : ONLINE")
    print("=" * 50)

    register_with_coordinator(
        args.id,
        args.host,
        args.port,
        args.coordinator
    )

    try:
        while True:
            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            print(
                f"[{timestamp}] "
                f"{args.id} is monitoring the archaeological site..."
            )

            time.sleep(5)

    except KeyboardInterrupt:
        print(f"\n{args.id} shutting down...")
        print("Status: OFFLINE")


if __name__ == "__main__":
    main()
