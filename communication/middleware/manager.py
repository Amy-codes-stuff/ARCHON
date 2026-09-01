import json
from datetime import datetime

from communication.message_broker import publish_event


class ArchonMiddleware:
    """
    Common communication interface for ARCHON nodes.

    The application layer can use this middleware
    instead of directly handling communication details.
    """

    def __init__(self, node_id):
        self.node_id = node_id

    def send_event(self, event_type, message):
        """
        Send an asynchronous event through RabbitMQ.
        """

        event = {
            "node_id": self.node_id,
            "event_type": event_type,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }

        print(f"[MIDDLEWARE] Sending event: {json.dumps(event)}")

        publish_event(
            node_id=self.node_id,
            event_type=event_type,
            message=message
        )

    def log_message(self, message):
        """
        Common middleware logging.
        """

        print(
            f"[MIDDLEWARE] "
            f"{self.node_id}: {message}"
        )
