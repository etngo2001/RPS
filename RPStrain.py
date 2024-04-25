import uuid
import os
import time
import cv2

IMAGE_PATH = os.path.join('data', 'images')
labels = ['rock', 'paper', 'scissors']
quantity = 20

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

for label in labels:
  print("Collecting labels for {}".format(label))
  time.sleep(5) # 5 sec delay

  for i in range(quantity):
    print("Collecting image {}".format(i))

    ret, frame = cap.read()

    time.sleep(1) # 1 sec delay to let camera load

    img_name = os.path.join(IMAGE_PATH, label+'.'+str(uuid.uuid1())+'.jpg') # generates unique names for each image
    cv2.imwrite(img_name, frame) # saves image
    print("got it")

    time.sleep(2) # 2 sec delay

cap.release()
cv2.destroyAllWindows()