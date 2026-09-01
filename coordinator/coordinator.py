from concurrent import futures
import grpc

from communication.proto import archon_pb2
from communication.proto import archon_pb2_grpc


class ArchonCoordinator(archon_pb2_grpc.ArchonCoordinatorServicer):

    def GetZoneStatus(self, request, context):
        print(f"[RPC] Status request received from {request.node_id}")

        return archon_pb2.ZoneStatus(
            node_id=request.node_id,
            status="ONLINE",
            message=f"{request.node_id} is connected to ARCHON Coordinator"
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    archon_pb2_grpc.add_ArchonCoordinatorServicer_to_server(
        ArchonCoordinator(),
        server
    )

    server.add_insecure_port("[::]:5000")
    server.start()

    print("=" * 50)
    print("       ARCHON - COORDINATOR")
    print("=" * 50)
    print("Port   : 5000")
    print("Status : ONLINE")
    print("=" * 50)
    print("Waiting for RPC requests...")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()
