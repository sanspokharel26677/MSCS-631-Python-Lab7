import cv2
import numpy as np

# Create a black image
blank_image = np.zeros((400, 600, 3), dtype=np.uint8)

# Put test text
cv2.putText(blank_image, "OpenCV Test", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)

# Show the image
cv2.imshow("Test Window", blank_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

