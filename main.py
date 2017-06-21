import cv2

img1 = cv2.imread('img/large1stplace.PNG', 0)
cap = cv2.VideoCapture('https://video-edge-c2afa4.dfw02.hls.ttvnw.net/v1/playlist/CpcD4Nql51U5NhxUumTz3D37At7nrF78QQPgDBKdlW0kIkNpuZBaRauR45mwkbM7I3XnxwHeK9_KnYw6BLCEMk9MvfBXyD1Y7PB5iIQjBVKe0H80KHGcmVES0KEhyUbTKBffj0weF1S60t6aGHwWqfwba7WZ4XEy5Xj0hKuv6ML5VH9pRcjwF6W5ozAPi8ud3UkvEC565LCcp_OCAeDuWj7HJ__oDyUJ697QpMLaS-ruyCWQbvwii3jGBVdxkJwZQxwlmKniCd5g96Lp-oMOFWlLxeNYFTUTmTi0G8qGpd7zmDsJTse5P4C7GWX0-5KSLQYKNydgt9xP-PH7B70KZBvAIq272rxBjNcd1TRAk8GgD3HqJT24yZ2ZIZ-BvHrN8uGflb8XrJGhp8JD3BPFJqgf423eFnP94g3oB8K88X5C_1MedL5bTAQxroumhJtnK_gbB5F20IEQp_nbI0Xaj8g7J2p8FW2CyLlxWIPDKkziy3ABneucenpNYco5vfzmXO816ro4aCU_XDBSa0URt5DQGxFjcZTyXRoSEF6LGVG1xPWRARhEh5AA8e4aDMl4mq2oFY163HhT3g.m3u8')
orb = cv2.ORB_create()
kp1, des1 = orb.detectAndCompute(img1, None)

checkCount = 0

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

    if (x2 > 300 and x2 < 400) and (y2 > 280 and y2 < 350) or (x2 > 190 and x2 < 270) and (y2 > 280 and y2 < 350):
        if(x2 > 300 and x2 < 400) and (y2 > 300 and y2 < 350):
            checkCount = checkCount + 1
            if checkCount > 100:
                checkCount = 0
                print("Assuming Player 2 Won")

        if (x2 > 190 and x2 < 270) and (y2 > 280 and y2 < 350):
            checkCount = checkCount + 1
            if checkCount > 100:
                checkCount = 0
                print("Assuming Player 1 Won")
    else:
        checkCount = checkCount - 1
        if checkCount < 0:
            checkCount = 0
    img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches[:1], None, flags=2)
    cv2.imshow('frame', img3)
