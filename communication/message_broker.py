import json
import pika


RABBITMQ_HOST = "localhost"
RABBITMQ_PORT = 5672
RABBITMQ_USER = "archon"
RABBITMQ_PASSWORD = "archon123"

QUEUE_NAME = "archon_events"


def create_connection():
    credentials = pika.PlainCredentials(
        RABBITMQ_USER,
        RABBITMQ_PASSWORD
    )

    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials
    )

    return pika.BlockingConnection(parameters)


def publish_event(node_id, event_type, message):
    connection = create_connection()
    channel = connection.channel()

    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True
    )

    event = {
        "node_id": node_id,
        "event_type": event_type,
        "message": message
    }

    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(event)
    )

    print(f"[MESSAGE SENT] {event}")

    connection.close()


def consume_events():
    connection = create_connection()
    channel = connection.channel()

    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True
    )

    print("[MESSAGE CONSUMER] Waiting for ARCHON events...")

    def callback(ch, method, properties, body):
        event = json.loads(body)

        print("=" * 50)
        print("       ARCHON - EVENT RECEIVED")
        print("=" * 50)
        print(f"Node       : {event['node_id']}")
        print(f"Event Type : {event['event_type']}")
        print(f"Message    : {event['message']}")
        print("=" * 50)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback
    )

    channel.start_consuming()


if __name__ == "__main__":
    consume_events()
