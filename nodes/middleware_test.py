from communication.middleware.manager import ArchonMiddleware


if __name__ == "__main__":

    middleware = ArchonMiddleware("ZONE_A")

    middleware.log_message(
        "ARCHON middleware initialized."
    )

    middleware.send_event(
        event_type="ARTIFACT_ALERT",
        message="Artifact movement detected in Zone A."
    )
