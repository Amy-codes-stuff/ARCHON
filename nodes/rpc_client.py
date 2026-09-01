import grpc

from communication.proto import archon_pb2
from communication.proto import archon_pb2_grpc


def get_zone_status(node_id):
    channel = grpc.insecure_channel("localhost:5000")

    stub = archon_pb2_grpc.ArchonCoordinatorStub(channel)

    request = archon_pb2.ZoneRequest(
        node_id=node_id
    )

    response = stub.GetZoneStatus(request)

    print("=" * 50)
    print("        ARCHON - RPC RESPONSE")
    print("=" * 50)
    print(f"Node ID : {response.node_id}")
    print(f"Status  : {response.status}")
    print(f"Message : {response.message}")
    print("=" * 50)


if __name__ == "__main__":
    get_zone_status("ZONE_B")
