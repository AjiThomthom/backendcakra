import httpx
from lib.db import db
from aiortc import RTCPeerConnection, RTCSessionDescription
from fastapi import HTTPException
from lib.video_track import CameraTrack
from lib.cryptographic import decryption_text


pcs = set()

async def StreamHelper(body, id):
    try:
        stream = await db.ccvtv.find_first(where={
            "cctv_id" : id
        })

        pc = RTCPeerConnection()

        @pc.on("connectionstatechange")
        async def on_connectionstatechange():
            print("Connection:", pc.connectionState)

        @pc.on("iceconnectionstatechange")
        async def on_ice():
            print("ICE:", pc.iceConnectionState)

        pcs.add(pc)


        await pc.setRemoteDescription(
            RTCSessionDescription(
                sdp=body["sdp"],
                type=body["type"]
            )
        )

        decrypted_url = decryption_text(stream.source_url)
        print(decrypted_url)
        pc.addTrack(
            CameraTrack(decrypted_url)
        )

        answer = await pc.createAnswer()

        await pc.setLocalDescription(answer)

        return {
            "sdp" : pc.localDescription.sdp,
            "type" : pc.localDescription.type
        }
    except httpx.HTTPStatusError as error:
        raise HTTPException(error)
    except httpx.RequestError as reqError:
        raise HTTPException(reqError)