import cv2
import pickle
import os

width, height = 107, 48
base_dir = os.path.dirname(__file__)
data_file = os.path.join(base_dir, 'CarParkPos')

try:
    with open(data_file, 'rb') as f:
        posList = pickle.load(f)
except FileNotFoundError:
    posList = []

def save_positions():
    with open(data_file, 'wb') as f:
        pickle.dump(posList, f)

def mouseClick(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
        save_positions()   # save immediately after adding
    if event == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
                save_positions()
                break

cv2.namedWindow("Parking Lot")
cv2.setMouseCallback("Parking Lot", mouseClick)

while True:
    img = cv2.imread(os.path.join(base_dir, 'carParkImg.png'))
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (231, 84, 128), 2)
    cv2.imshow("Parking Lot", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        save_positions()   # extra safety on exit
        break
cv2.destroyAllWindows()
