import cv2


def change_contrast(frame_, alpha=1.0, beta=0):
    """
    Adjust the contrast of a frame.

    :param frame_: Input frame (image)
    :param alpha: Contrast control (1.0 means no change)
    :param beta: Brightness control
    :return: Frame with adjusted contrast
    """
    adjusted_frame_ = cv2.convertScaleAbs(frame_, alpha=alpha, beta=beta)
    return adjusted_frame_


# Open a video capture object
cap = cv2.VideoCapture(
    r'C:\Maayan\First degree\fourth year\Project\run-experiment\assets\Tom_and_Jerry_short.mp4'
)

# Check if the video capture object is successfully opened
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Get the frames per second (fps) of the input video
fps = cap.get(cv2.CAP_PROP_FPS)

# Create a VideoWriter object to save the output video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You may need to adjust the codec based on your system
output_video = cv2.VideoWriter('output_video.mp4', fourcc, fps, (int(cap.get(3)), int(cap.get(4))))

# Loop through the frames of the input video
while True:
    # Read a frame from the video capture object
    ret, frame = cap.read()

    # Break the loop if the video has ended
    if not ret:
        break

    # Adjust the contrast of the frame (you can modify alpha and beta values)
    adjusted_frame = change_contrast(frame, alpha=0.5)

    # Write the adjusted frame to the output video file
    output_video.write(adjusted_frame)

# Release the video capture object and the output video writer
cap.release()
output_video.release()

print("Video processing complete. Modified video saved as 'output_video.mp4'")
