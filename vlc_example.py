import subprocess
from pupil_labs.realtime_api.simple import discover_one_device
from datetime import datetime
import time
import tkinter as tk
from tkinter import simpledialog, messagebox


def get_user_name() -> str:
    """
    Get the user's name through a dialog box.
    :return: The user's name
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    user_name = simpledialog.askstring("Input", "Enter your name:")
    return user_name


def display_message(message: str) -> None:
    """
    Display a message to the user.
    :param message: A message to show the user
    :return: None
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo("Message", message)


def play_video_external(video_path: str, vlc_path: str):
    cmd = [vlc_path, "--no-loop", '--play-and-exit', video_path]
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def look_for_device():
    # Look for devices. Returns as soon as it has found the first device.
    print("Looking for the next best device...")
    device = discover_one_device(max_search_duration_seconds=10)
    if device is None:
        print("No device found.")
        raise SystemExit(-1)
    return device


def check_glasses(device):
    if device.receive_gaze_datum().worn is False:
        print("Please wear the glasses")
        while device.receive_gaze_datum().worn is False:
            pass
        print("Issue fixed")


def play_and_record_video(video_path: str, vlc_path: str, device):
    print("Starting in 5 seconds")
    time.sleep(5)

    print(f"Starting recording")
    recording_id = device.recording_start()
    device.send_event("start.video")
    vlc_process = play_video_external(video_path, vlc_path)

    # Wait for the VLC player process to finish (video playback to complete)
    vlc_process.communicate()
    device.recording_stop_and_save()
    print("Recording stopped and saved")

def main():
    video_path = r"assets\Tom_and_Jerry_short.mp4"
    vlc_path = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
    first_video_file_path = r"assets\Tom_and_Jerry_short.mp4"
    second_video_file_path = r"assets\Tom_and_Jerry_short.mp4"
    third_video_file_path = r"assets\Tom_and_Jerry_short.mp4"
    fourth_video_file_path = r"assets\Tom_and_Jerry_short.mp4"

    user_name = get_user_name()
    # todo save name

    device = look_for_device()
    check_glasses(device)

    # First video
    play_and_record_video(
        first_video_file_path, vlc_path, device
    )

    display_message("Press ok to start the next video")

    # Second video
    play_and_record_video(
        second_video_file_path, vlc_path, device
    )

    display_message("Press ok to start the next video")

    # Third video
    play_and_record_video(
        third_video_file_path, vlc_path, device
    )

    display_message("Press ok to start the next video")

    # Fourth video
    play_and_record_video(
        fourth_video_file_path, vlc_path, device
    )

    # device.recording_cancel()  # uncomment to cancel recording
    # eye_sample = device.receive_scene_video_frame()
    # dt = datetime.fromtimestamp(eye_sample.timestamp_unix_seconds)
    # print(f"This scene camera image was recorded at {dt}")

    device.close()


if __name__ == "__main__":
    main()
