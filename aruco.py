import cv2
import numpy
import math 
import serial
import time

from ArucoTracker import ArucoTracker
VELOCITà=20



def main():
    # Initialize USB camera
    cap = cv2.VideoCapture(0)   
    # Initialize ArucoTracker object
    # I numeri inseriti nella lista sono gli unici aruco che riconosce
    aruco_tracker = ArucoTracker([17])

    

    try:
        
        while True:
            
            

            # Read frame from camera
            _, frame = cap.read()

            # Find aruco markers in the frame
            markerID, errors, angle, frame_aruco = aruco_tracker.find_markers(frame)
            if markerID is not None:
                frame = frame_aruco
                
                print(f'Found aruco {markerID}')            
                print(f'Errors: {errors}')
                print(f'Coordinate del centro\nX:{aruco_tracker.Cx} Y:{aruco_tracker.Cy}')

                centro_immagine=[aruco_tracker.img_h/2,aruco_tracker.img_w/2]
                centro_aruco=[aruco_tracker.Cx, aruco_tracker.Cy]
                vettore_freccia=numpy.array([aruco_tracker.arrow_top_coordinates[0]-aruco_tracker.Cx,aruco_tracker.arrow_top_coordinates[1]-aruco_tracker.Cy])
                vettore_direzione=vettore_freccia*VELOCITà                
                vettore_direzione_ideale=numpy.array([centro_immagine[0]-centro_aruco[0],centro_immagine[1]-centro_aruco[1]])

                prodotto_scalare=numpy.dot(vettore_direzione,vettore_direzione_ideale)

                norma_vettore_direzione=numpy.linalg.norm(vettore_direzione)
                norma_vettore_direzione_ideale=numpy.linalg.norm(vettore_direzione_ideale)

                angolo_radianti=numpy.arccos(prodotto_scalare/(norma_vettore_direzione*norma_vettore_direzione_ideale))

                seno=numpy.sin(angolo_radianti)
                coseno=numpy.cos(angolo_radianti)

                print(seno,coseno,angolo_radianti)
                

            # Show frame
            cv2.imshow('Aruco Marker Detection', frame)
            
            # Exit on 'q'
            if cv2.waitKey(1) == ord('q'):
                break
    except KeyboardInterrupt:

        print('\nCtrl+C pressed')

    finally:
        # Release camera and close windows
        print('Closing...')
        cap.release()
        cv2.destroyAllWindows()
        ser.close()

if __name__ == '__main__':
    main()
