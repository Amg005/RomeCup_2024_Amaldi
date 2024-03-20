import cv2
import numpy
from math import atan2, sin, cos

class ArucoTracker():
    """
    Aruco Tracker python implementation.
    find_markers() returns: 
        - markerID;
        - x and y errors in [-1, 1] range;
        - angle in radians;
        - frame with drawn marker.
    """

    def __init__(self, aruco_numbers):
        self.aruco_numbers = aruco_numbers

        self.arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)
        self.arucoParams = cv2.aruco.DetectorParameters()

        self.Cx:int
        self.Cy:int
        self.img_h:int
        self.img_w:int
        self.top_left_corner:tuple
        self.top_right_corner:tuple
        self.bottom_left:tuple
        self.bottom_right:tuple
        self.arrow_top_coordinates:list        


        print('ArucoTracker initialized')

    def find_markers(self, frame):
        img_w = frame.shape[1]
        img_h = frame.shape[0]

        # detect ArUco markers in the input frame
        (corners, ids, _) = cv2.aruco.detectMarkers(
            frame,
            self.arucoDict,
            parameters=self.arucoParams)

        # verify *at least* one ArUco marker was detected
        if len(corners) > 0:
            self.counter = 0
            # flatten the ArUco IDs list
            ids = ids.flatten()
            # loop over the detected ArUCo corners
            for (markerCorner, markerID) in zip(corners, ids):
                if markerID in self.aruco_numbers:
                    # extract marker corners (top-left, top-right, bottom-right, bottom-left)
                    markerCorner_42 = markerCorner.reshape((4, 2))
                    (topLeft, topRight, bottomRight, bottomLeft) = markerCorner_42

                    # convert each of the (x, y)-coordinate pairs to integers
                    topRight = (int(topRight[0]), int(topRight[1]))
                    bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                    bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                    topLeft = (int(topLeft[0]), int(topLeft[1]))

                    # draw the bounding box of the ArUCo detection
                    cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
                    cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
                    cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
                    cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)

                    # compute and draw the center (x, y)-coordinates of the ArUco marker
                    cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                    cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                    cXnorm = (cX - img_w/2) / img_w * 2
                    self.Cx=cX
                    cYnorm = -(cY - img_h/2) / img_h * 2
                    self.Cy=cY
                    cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)
                    self.img_h=img_h
                    self.img_w=img_w
                    # draw the ArUco marker ID on the frame
                    cv2.putText(frame, str(markerID), (topLeft[0], topLeft[1] - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # compute angle                    
                    p_up = [(topLeft[0] + topRight[0]) / 2, (topLeft[1] + topRight[1]) / 2]
                    p_down = [(bottomLeft[0] + bottomRight[0]) / 2, (bottomLeft[1] + bottomRight[1]) / 2]
                    angle = -atan2(p_up[1] - p_down[1], p_up[0] - p_down[0])

                    # draw line from center to p_up
                    arrow_length = 0.6 * ((topLeft[0] - topRight[0]) ** 2 + (topLeft[1] - topRight[1]) ** 2) ** 0.5
                    arrow_end_x = int(cX + arrow_length * cos(angle))
                    arrow_end_y = int(cY - arrow_length * sin(angle))
                    self.arrow_top_coordinates=[arrow_end_x,arrow_end_y]
                    cv2.arrowedLine(frame, (cX, cY), (arrow_end_x, arrow_end_y), color=(255, 0, 0), thickness=2, tipLength=0.1)
                    
                    
                    
                    return markerID, (cXnorm, cYnorm), angle, frame

        return None, None, None, None