
from helper.stream__helper.stream_helper import StreamHelper

async def stream_camera_service(body,id):
    return await StreamHelper(body,id)