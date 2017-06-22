import cv2
import pyautogui
import time

img1 = cv2.imread('img/large1stplace.PNG', 0)
cap = cv2.VideoCapture('https://video-edge-c2a760.dfw02.hls.ttvnw.net/v1/playlist/Cp0DhoXGetIcPF5YKaoJubASTi9O20FuY-jRmnNNmCCrNoxp5egM1063FEPtHuaQTxHH9hV12vMTb8QFg4Xf5IIURT6Q8NXJgaAE3HjitVBOf5-uCXP39wScXmsknJNM0sjpRZQ-t0UCClHDOy4zkQJhW--CQl3ZE0mc53BtSuKT-dmjvtxEF5IKtVRnwyb6M-n64OgRwdknTF_ygWEFKGz8HJQ-XTjKzAqs9VLunbYoUHjSHI8dOfFneVVa0ROzYc2mw9uz9wsTFsGmHBccdE1Fw4hCoT9P-1INQRcIZnDOBVT7GMyGFYebi1nSOpeMskjJ5zc6_s5ZCis4YP24LYPkd063g5tAh1K4GB20smo5ZI9QB1q63B560n3sD3enCF90UnOMPbKeoEU4zksL4gJs_LKRyzuitXvQpSL0xZTf4wiG3ya9oWV0QzfCqO4q92_ghpeLsT1efsUG7xyxP_Hg9GrL3jTDBdCNI_M6svbFcm1pzO7AWq_hHqwOQ615N4C5Hsd6tFBzH1r5D2s8nRfpjcaMb64pAPSL5JKPhZcSEM4IpQVXIIfUin--sfwK7EUaDIqpDWvE6eG-1F3nLw.m3u8')

orb = cv2.ORB_create()
kp1, des1 = orb.detectAndCompute(img1, None)

checkCount = 0
previousRequest = time.time()

def clickRequest():
    global previousRequest
    global checkCount
    if time.time() - previousRequest > 30:
        pyautogui.click(clicks=10, interval=0.5)
        print("clicked")
        previousRequest = time.time()

print("Program has successfully begun")

while True:
    ret, frame = cap.read()
    img2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    kp2, des2 = orb.detectAndCompute(img2, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)

    matches = bf.match(des1, des2)
    matches = sorted(matches, key = lambda x:x.distance)
    (x2, y2) = kp2[matches[0].trainIdx].pt

    if (x2 > 300 and x2 < 425) and (y2 > 280 and y2 < 417) or (x2 > 190 and x2 < 270) and (y2 > 280 and y2 < 417):
        if(x2 > 300 and x2 < 425) and (y2 > 280 and y2 < 417):
            checkCount = checkCount + 1
            if checkCount > 250:
                print("Assuming Player 2 Won")
                clickRequest()
                checkCount = 0

        if (x2 > 190 and x2 < 270) and (y2 > 280 and y2 < 417):
            checkCount = checkCount + 1
            if checkCount > 250:
                print("Assuming Player 1 Won")
                clickRequest()
                checkCount = 0
    else:
        checkCount = checkCount - 3
        if checkCount < 0:
            checkCount = 0
        #There should always be something on the screen, otherwise you'll get errors if it's completely black

#    img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches[:1], None, flags=2)
#    cv2.imshow('frame', img3)
