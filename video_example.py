from moviepy.editor import VideoFileClip
import time
from pupil_labs.realtime_api.simple import discover_one_device
from datetime import datetime


def play_video(video_path: str) -> None:
    clip = VideoFileClip(video_path)
    clip.preview(fullscreen=True)


def main():
    # Look for devices. Returns as soon as it has found the first device.
    print("Looking for the next best device...")
    device = discover_one_device(max_search_duration_seconds=10)
    if device is None:
        print("No device found.")
        raise SystemExit(-1)

    print(f"Starting recording")
    recording_id = device.recording_start()
    print(f"Started recording with id {recording_id}")

    time.sleep(5)  # Wait for 5 seconds to ensure recording has started

    video_file_path = "assets/Tom_and_Jerry_short.mp4"
    play_video(video_file_path)  # Start playing the video

    device.recording_stop_and_save()
    print("Recording stopped and saved")

    # device.recording_cancel()  # uncomment to cancel recording

    eye_sample = device.receive_scene_video_frame()

    dt = datetime.fromtimestamp(eye_sample.timestamp_unix_seconds)
    print(f"This scene camera image was recorded at {dt}")

    device.close()


main()
