import argparse
import time
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description="ARCHON Distributed Zone Node")
    parser.add_argument("--id", required=True, help="Unique node ID")
    parser.add_argument("--port", required=True, type=int, help="Node port")

    args = parser.parse_args()

    print("=" * 50)
    print("        ARCHON - DISTRIBUTED ZONE NODE")
    print("=" * 50)
    print(f"Node ID : {args.id}")
    print(f"Port    : {args.port}")
    print("Status  : ONLINE")
    print("=" * 50)

    try:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] {args.id} is monitoring the archaeological site...")
            time.sleep(5)

    except KeyboardInterrupt:
        print(f"\n{args.id} shutting down...")
        print("Status: OFFLINE")


if __name__ == "__main__":
    main()
