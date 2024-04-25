import torch
import numpy as np
import cv2
import time
import functions as f

# loads my custom trained model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='customModel.pt')
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 640) # specify width as 640 px 350/300
cap.set(4, 480) # specift height as 480 px

timer = 0
state = False
startGame = False
scores = [0,0] # [Comp, User]

while cap.isOpened():
  # loads the web camera
  ret, frame = cap.read()
  bgImage = cv2.imread("img/bg.png") # loads the background image

  # applies the model to the camera stream and resizes/crops the stream
  results = model(frame)
  feed = np.squeeze(results.render())
  feed = cv2.resize(feed, (0,0), None, 0.625, 0.625)
  feed = feed[:, 25:375]

  # game logic
  if startGame:

    # if the state of the game is ongoing update the timer
    if state is False:
      timer = time.time() - initialTime
      cv2.putText(bgImage, str(int(timer)), (610, 505), cv2.FONT_HERSHEY_PLAIN, 6, (255,255,255), 4)

      if timer > 3.1: # stop the timer after 3 seconds have passed
        state = True
        timer = 0

        user = f.get_user_choice(str(results))
        comp = f.get_comp_choice()

        compImg = cv2.imread(f"img/{comp}.png")
        compImg = cv2.resize(compImg, (0,0), None, 0.5, 0.5)

        if len(user) != 1:
          print("ERROR:User must make a single valid choice: rock, paper, or scissors")
        else:
          result = f.find_winner(user[0], comp)

          match result:
            case -1:
              scores[1] += 1
              print("Player Win")
            case 0:
              print("Tie")
            case 1:
              scores[0] += 1
              print("Computer Win")
        startGame = False

  if state:
    cv2.putText(bgImage, "GO", (595, 490), cv2.FONT_HERSHEY_PLAIN, 4, (255,255,255), 4)

    bgImage[365:590, 205:430] = compImg

  # Display the scores
  cv2.putText(bgImage, str(scores[0]), (515, 423), cv2.FONT_HERSHEY_PLAIN, 6, (255,255,255), 4)
  cv2.putText(bgImage, str(scores[1]), (705, 423), cv2.FONT_HERSHEY_PLAIN, 6, (255,255,255), 4)

  bgImage[330:630, 790:1140] = feed # overlays the web camera feed onto the bg img

  cv2.imshow("board", bgImage)

  key = cv2.waitKey(10) & 0xFF # get the ascii value of a keypress
  if key == ord('s'): # start game if 's' key is pressedss
    startGame = True
    state = False
    initialTime = time.time() #initialize game timer for this match
  elif key == 27: # uses the 'esc' key to break out of the loop and close the program
    break

cap.release()
cv2.destroyAllWindows()