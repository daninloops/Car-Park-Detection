import cv2
import pickle
import numpy as np


cap=cv2.VideoCapture('carPark.mp4')

with open('carParkpos','rb') as f:
    posList=pickle.load(f)

width,height=107,48

def CheckParkingSpace(frame, frame_processed):
    spot_area = width * height
    # occupancy threshold as fraction of spot area (tune between 0.1-0.25 if needed) perfect for this video 0.15
    occupancy_threshold = int(spot_area * 0.15)
    free_count = 0

    for pos in posList:
        x,y = pos
        # correct slicing: [y:y+height, x:x+width]
        crop_img = frame_processed[y:y+height, x:x+width]

        count = cv2.countNonZero(crop_img)
        cv2.putText(frame, str(count), (x, y+height-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

        if count < occupancy_threshold:
            color = (0,255,0)
            thickness = 2
            status_text = "Free"
            free_count += 1
        else:
            color = (0,0,255)
            thickness = 2
            status_text = "Occupied"

        # draw rectangle around the parking spot
        cv2.rectangle(frame, (x, y), (x + width, y + height), color, thickness)

    # show summary of free spots
    cv2.putText(frame, f"Free: {free_count}/{len(posList)}", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES)==cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgblur = cv2.GaussianBlur(gray, (3,3), 1)

    imgThreshold = cv2.adaptiveThreshold(imgblur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3,3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    CheckParkingSpace(frame, imgDilate)

    cv2.imshow("Image", frame)
    cv2.imshow("Dial", imgDilate)

    # unified Video Feed window (optional duplicate removed)
    cv2.imshow("Video Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
        
