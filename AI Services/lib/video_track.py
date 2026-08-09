import cv2
from aiortc import VideoStreamTrack
import onnxruntime as ort
from ultralytics import YOLO
from av import VideoFrame

class CameraTrack(VideoStreamTrack):
    def __init__(self, rtsp):
        super().__init__()
        self.cap = cv2.VideoCapture(rtsp)
        self.model = YOLO("models/yolo11n.onnx")

    async def recv(self):
        try:
            pts, time_base = await self.next_timestamp()

            ret, frame = self.cap.read()
                
            if not ret:
                raise Exception("Frame gagal dibaca")

            results = self.model.track(
                source=frame,
                persist=True,
                tracker="bytetrack.yaml",
                imgsz=640,
                conf=0.4,
                verbose=False
            )


            annotated_frame = results[0].plot()



            video = VideoFrame.from_ndarray(
                annotated_frame,
                format="bgr24"
            )



            video.pts = pts
            video.time_base = time_base

            return video
        except Exception as e:
            print(f"[ERROR] : {e}")
            raise 