from communication.message_broker import publish_event


if __name__ == "__main__":
    publish_event(
        node_id="ZONE_A",
        event_type="INTRUSION_DETECTED",
        message="Possible unauthorized activity detected at Zone A."
    )
