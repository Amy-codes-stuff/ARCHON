import asyncio
import json

import websockets
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from av import VideoFrame


SIGNALING_URL = "ws://localhost:9000"


class ArchaeologicalCamera(VideoStreamTrack):
    """Simulated archaeological-site camera."""

    def __init__(self):
        super().__init__()
        self.frame_number = 0

    async def recv(self):
        pts, time_base = await self.next_timestamp()

        import numpy as np

        width = 640
        height = 480

        image = np.zeros((height, width, 3), dtype=np.uint8)

        x = (self.frame_number * 10) % (width - 40)
        image[200:280, x:x + 40, :] = 255

        self.frame_number += 1

        frame = VideoFrame.from_ndarray(image, format="rgb24")
        frame.pts = pts
        frame.time_base = time_base

        return frame


async def run_sender():
    peer = RTCPeerConnection()

    camera = ArchaeologicalCamera()
    peer.addTrack(camera)

    @peer.on("connectionstatechange")
    async def on_connectionstatechange():
        print(f"[WEBRTC] Connection state: {peer.connectionState}")

    async with websockets.connect(SIGNALING_URL) as signaling:

        print("[WEBRTC] Connected to signaling server.")

        offer = await peer.createOffer()
        await peer.setLocalDescription(offer)

        message = {
            "type": "offer",
            "sdp": peer.localDescription.sdp
        }

        await signaling.send(json.dumps(message))

        print("[WEBRTC] Offer sent to Zone B.")
        print("[WEBRTC] Waiting for answer...")

        while True:
            raw_message = await signaling.recv()
            message = json.loads(raw_message)

            if message["type"] == "answer":
                answer = RTCSessionDescription(
                    sdp=message["sdp"],
                    type="answer"
                )

                await peer.setRemoteDescription(answer)

                print("[WEBRTC] Answer received.")
                print("[WEBRTC] WebRTC connection established.")

                await asyncio.sleep(10)
                break

    await peer.close()
    print("[WEBRTC] Sender connection closed.")


if __name__ == "__main__":
    asyncio.run(run_sender())
