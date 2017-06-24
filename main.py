import cv2
import pyautogui
import time
import streamlink

#Get URL of stream
streams = streamlink.streams("http://twitch.tv/trophywagers")
stream = streams['480p']

#Get first-place image to compare to frame of stream
img1 = cv2.imread('img/large1stplace.PNG', 0)

#Get stream
cap = cv2.VideoCapture(stream.url)

orb = cv2.ORB_create()
kp1, des1 = orb.detectAndCompute(img1, None)

checkCount = 0
previousRequest = time.time()

def clickRequest(winner):
    global previousRequest
    if time.time() - previousRequest > 30:
        # Payouts
        if winner == 1:
            print("Player 1 Won")
        elif winner == 2:
            print("Player 2 Won")

        pyautogui.click(clicks=10, interval=0.5)
        print("clicked")
        previousRequest = time.time()

        #Pause Game and Take Bets
        #Coming Soon#

print("Program has successfully begun")

while True:
    ret, frame = cap.read()
    img2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    kp2, des2 = orb.detectAndCompute(img2, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
    try:
        matches = bf.match(des1, des2)
        matches = sorted(matches, key = lambda x:x.distance)
        (x2, y2) = kp2[matches[0].trainIdx].pt

        #Find Coordinates of match
        if (x2 > 300 and x2 < 425) and (y2 > 280 and y2 < 417) or (x2 > 190 and x2 < 270) and (y2 > 280 and y2 < 417):
            #Player 2 Coordinates
            if(x2 > 300 and x2 < 425) and (y2 > 280 and y2 < 417):
                checkCount = checkCount + 1
                if checkCount > 250:
                    clickRequest(2)
                    checkCount = 0
            #Player 1 coordinates
            if (x2 > 190 and x2 < 270) and (y2 > 280 and y2 < 417):
                checkCount = checkCount + 1
                if checkCount > 250:
                    clickRequest(1)
                    checkCount = 0
        else:
            #Reduce false-positives
            checkCount = checkCount - 3
            if checkCount < 0:
                checkCount = 0
    except:
        #Likely Assertion failure; as expected from random inputs of frames
        print("There was an error, likely due to changing game modes")

    #img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches[:1], None, flags=2)
    #cv2.imshow('frame', img3)
