import cv2
import matplotlib.pyplot as plt
import numpy as np

# Location of image file
f = "3.0"
image_file = (
    "/home/etienne/Documents/Research/Data/2026/2026_02_07/scan_4p0_D3_F_"
    + f
    + ".jpg"
)
#
# Initialize an empty coordinate array
coordinates = []


# Mouse callback function to capture coordinates on click
def capture_coordinates(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # Capture coordinates on left mouse click
        coordinates.append((x, y))
        cv2.circle(img, (x, y), 3, (0, 0, 255), -1)  # Mark the clicked point
        cv2.imshow("image", img)  # Update the displayed image


if __name__ == "__main__":
    # Load image
    img = cv2.imread(image_file)
    # img = img[0:H_BOUND, 0:V_BOUND]

    # Create a window
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("image", capture_coordinates)

    # Capture coordinates
    while True:
        cv2.imshow("image", img)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    print(f"The number of pixels between 0 and 25 cm is {coordinates[1][1]-coordinates[0][1]}.")
