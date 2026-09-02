from concurrent import futures
from datetime import datetime
import threading
import time

import grpc

from communication.proto import archon_pb2
from communication.proto import archon_pb2_grpc


HEARTBEAT_TIMEOUT = 15


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
                "port": request.port,
                "last_heartbeat": time.time(),
                "status": "ONLINE"
            }

        print(
            f"[REGISTRATION] {request.node_id} "
            f"registered at {request.host}:{request.port}"
        )

        return archon_pb2.NodeRegistrationResponse(
            success=True,
            message=f"{request.node_id} registered successfully"
        )

    def Heartbeat(self, request, context):
        with self.lock:
            if request.node_id in self.nodes:
                self.nodes[request.node_id]["last_heartbeat"] = time.time()
                self.nodes[request.node_id]["status"] = "ONLINE"

                print(
                    f"[HEARTBEAT] {request.node_id} is alive"
                )

                return archon_pb2.HeartbeatResponse(
                    acknowledged=True,
                    message="Heartbeat received"
                )

        return archon_pb2.HeartbeatResponse(
            acknowledged=False,
            message="Node not registered"
        )

    def GetZoneStatus(self, request, context):
        with self.lock:
            node = self.nodes.get(request.node_id)

            if node:
                status = node["status"]
            else:
                status = "UNKNOWN"

        return archon_pb2.ZoneStatus(
            node_id=request.node_id,
            status=status,
            message=f"{request.node_id} is {status}"
        )

    def check_node_health(self):
        while True:
            current_time = time.time()

            with self.lock:
                for node_id, node in self.nodes.items():

                    elapsed = (
                        current_time -
                        node["last_heartbeat"]
                    )

                    if elapsed > HEARTBEAT_TIMEOUT:
                        if node["status"] != "OFFLINE":
                            node["status"] = "OFFLINE"

                            print(
                                f"[FAULT DETECTED] "
                                f"{node_id} is OFFLINE"
                            )

            time.sleep(5)

    def print_nodes(self):
        with self.lock:
            print("\n[ACTIVE NODES]")

            if not self.nodes:
                print("No nodes registered.")

            for node_id, node in self.nodes.items():
                print(
                    f"- {node_id} "
                    f"({node['host']}:{node['port']}) "
                    f"[{node['status']}]"
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

    health_thread = threading.Thread(
        target=coordinator.check_node_health,
        daemon=True
    )

    health_thread.start()

    print("=" * 50)
    print("       ARCHON - COORDINATOR")
    print("=" * 50)
    print("Port   : 5000")
    print("Status : ONLINE")
    print("=" * 50)

    try:
        while True:
            coordinator.print_nodes()
            time.sleep(10)

    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
