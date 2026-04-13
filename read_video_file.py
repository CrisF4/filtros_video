# Utilizar el comando: python read_video_file.py video.mp4
import cv2
import argparse

def recolorRC(src, dst):
    """Simulate conversion from BGR to RC (red, cyan).

    The source and destination images must both be in BGR format.

    Blues and greens are replaced with cyans.

    Pseudocode:
    dst.b = dst.g = 0.5 * (src.b + src.g)
    dst.r = src.r

    """
    b, g, r = cv2.split(src)
    cv2.addWeighted(b, 0.5, g, 0.5, 0, b)
    cv2.merge((b, b, r), dst)
    
    return dst

def recolorRGV(src, dst):
    """Simulate conversion from BGR to RGV (red, green, value).

    The source and destination images must both be in BGR format.

    Blues are desaturated.

    Pseudocode:
    dst.b = min(src.b, src.g, src.r)
    dst.g = src.g
    dst.r = src.r

    """
    b, g, r = cv2.split(src)
    cv2.min(b, g, b)
    cv2.min(b, r, b)
    cv2.merge((b, g, r), dst)

    return dst

def recolorCMV(src, dst):
    """Simulate conversion from BGR to CMV (cyan, magenta, value).

    The source and destination images must both be in BGR format.

    Yellows are desaturated.

    Pseudocode:
    dst.b = max(src.b, src.g, src.r)
    dst.g = src.g
    dst.r = src.r

    """
    b, g, r = cv2.split(src)
    cv2.max(b, g, b)
    cv2.max(b, r, b)
    cv2.merge((b, g, r), dst)
    
    return dst

parser = argparse.ArgumentParser()

# We add 'video_path' argument using add_argument() including a help.
parser.add_argument("video_path", help="path to the video file")
args = parser.parse_args()

# Create a VideoCapture object. In this case, the argument is the video file name:
capture = cv2.VideoCapture(args.video_path)
 
# Check if the video is opened successfully
if capture.isOpened() is False:
    print("Error opening the video file!")
 
# Read until video is completed, or 'q' is pressed
while capture.isOpened():
    # Capture frame-by-frame from the video file
    ret, frame = capture.read()
    frame_resize = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)

    if ret is True:
        # Display the resulting frame
        frame_rgb = cv2.cvtColor(frame_resize, cv2.COLOR_BGR2RGB)
        frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
        frame_hsv = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2HSV)
        frame_rc = recolorRC(frame_resize, frame_resize.copy())
        frame_rgv = recolorRGV(frame_resize, frame_resize.copy())
        frame_cmv = recolorCMV(frame_resize, frame_resize.copy())
        cv2.imshow('Original frame from the video file', frame_resize)
        cv2.imshow('RGB frame from the video file', frame_rgb)
        cv2.imshow('HSV frame from the video file', frame_hsv)
        cv2.imshow('RC frame from the video file', frame_rc)
        cv2.imshow('RGV frame from the video file', frame_rgv)
        cv2.imshow('CMV frame from the video file', frame_cmv)

        # Convert the frame from the video file to grayscale:
        #gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the grayscale frame
        #cv2.imshow('Grayscale frame', gray_frame)
 
        # Press q on keyboard to exit the program
        if cv2.waitKey(200) & 0xFF == ord('q'):
            break
    # Break the loop
    else:
        break
 
# Release everything
capture.release()
cv2.destroyAllWindows()
