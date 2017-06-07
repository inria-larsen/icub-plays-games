import cv2

def photo():
    cap = cv2.VideoCapture(0)
    flag=True
    while(flag):
        # ambil tiap frame
        _, frame = cap.read()

        cv2.imshow('frame',frame)

        k = cv2.waitKey(5) & 0xFF
        if k != 0xFF:
            flag=False
            cv2.imwrite('frame.png',frame)
            #break
            cv2.destroyAllWindows()
            return(frame)
    return 0