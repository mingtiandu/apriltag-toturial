#!/usr/bin/env python
# coding: UTF-8

import pupil_apriltags as apriltag     # for windows
import cv2
import time, datetime, os
import numpy as np

cTime = 0
pTime = 0

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

#at_detector = apriltag.Detector(families='tag36h11 tag25h9')
at_detector = apriltag.Detector(families='tag36h11 tag25h9',
                                nthreads=1,
                                quad_decimate=1.0,
                                quad_sigma=0.0,
                                refine_edges=1,
                                decode_sharpening=0.25,
                                debug=0)


while(1):
    # obtain image
    ret, frame = cap.read()
    # detect key
    k = cv2.waitKey(1)

    if k == 27: # Esc key to stop
        break
    elif k == ord('s'): # s key to snip
        print('DEbug')
        print(datetime.datetime.now())

        cv2.imwrite('../apriltag-tutorial/'+str(1)+'.png', frame)

    # detect apriltag
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    tags = at_detector.detect(gray)
    # tags = at_detector.detect(gray, estimate_tag_pose=True,
    #                           camera_params=[color_intrin.fx, color_intrin.fy, color_intrin.ppx, color_intrin.ppy],
    #                           tag_size=tagSize)
    for tag in tags:
        cv2.circle(frame, tuple(tag.corners[0].astype(int)), 4, (255, 0, 0), 2) # left-top
        cv2.circle(frame, tuple(tag.corners[1].astype(int)), 4, (255, 0, 0), 2) # right-top
        cv2.circle(frame, tuple(tag.corners[2].astype(int)), 4, (255, 0, 0), 2) # right-bottom
        cv2.circle(frame, tuple(tag.corners[3].astype(int)), 4, (255, 0, 0), 2) # left-bottom
    # show result
    # calculate FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(frame, 'FPS: {0:.2f}'.format(fps), (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                cv2.LINE_AA)
    cv2.imshow('capture', frame)

cap.release()
cv2.destroyAllWindows()
