from concurrent import futures
import threading

import grpc

from communication.proto import archon_pb2
from communication.proto import archon_pb2_grpc


class ArchonCoordinator(
    archon_pb2_grpc.ArchonCoordinatorServicer
):

    def __init__(self):
        self.nodes = {}
        self.lock = threading.Lock()

    def RegisterNode(self, request, context):
        with self.lock:
            self.nodes[request.node_id] = {
                "host": request.host,
                "port": request.port
            }

        print(
            f"[REGISTRATION] {request.node_id} "
            f"registered at {request.host}:{request.port}"
        )

        return archon_pb2.NodeRegistrationResponse(
            success=True,
            message=f"{request.node_id} registered successfully"
        )

    def GetZoneStatus(self, request, context):
        with self.lock:
            is_registered = request.node_id in self.nodes

        status = "ONLINE" if is_registered else "UNKNOWN"

        print(
            f"[RPC] Status request received from "
            f"{request.node_id}"
        )

        return archon_pb2.ZoneStatus(
            node_id=request.node_id,
            status=status,
            message=f"{request.node_id} is {status}"
        )

    def print_nodes(self):
        with self.lock:
            print("\n[ACTIVE NODES]")

            if not self.nodes:
                print("No nodes registered.")

            for node_id, details in self.nodes.items():
                print(
                    f"- {node_id} "
                    f"({details['host']}:{details['port']})"
                )


def serve():
    coordinator = ArchonCoordinator()

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    archon_pb2_grpc.add_ArchonCoordinatorServicer_to_server(
        coordinator,
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

    try:
        while True:
            coordinator.print_nodes()
            threading.Event().wait(10)

    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
