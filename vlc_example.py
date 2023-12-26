import subprocess
from pupil_labs.realtime_api.simple import discover_one_device
from datetime import datetime
import time


def play_video_external(video_path: str):
    vlc_path = r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"
    cmd = [vlc_path, "--no-loop", '--play-and-exit', video_path]
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main():
    # Look for devices. Returns as soon as it has found the first device.
    print("Looking for the next best device...")
    device = discover_one_device(max_search_duration_seconds=10)
    if device is None:
        print("No device found.")
        raise SystemExit(-1)

    if device.receive_gaze_datum().worn is False:
        print("Please wear the glasses")
        while device.receive_gaze_datum().worn is False:
            pass
        print("issue fixed, starting in 5 seconds")
        time.sleep(5)

    print(f"Starting recording")
    recording_id = device.recording_start()
    print(f"Started recording with id {recording_id}")

    video_file_path = r"assets/Tom_and_Jerry.mp4"
    vlc_process = play_video_external(video_file_path)

    # Wait for the VLC player process to finish (video playback to complete)
    vlc_process.communicate()

    device.recording_stop_and_save()
    print("Recording stopped and saved")

    # device.recording_cancel()  # uncomment to cancel recording

    eye_sample = device.receive_scene_video_frame()

    dt = datetime.fromtimestamp(eye_sample.timestamp_unix_seconds)
    print(f"This scene camera image was recorded at {dt}")

    device.close()


main()
