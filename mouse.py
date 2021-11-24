import cv2 as cv
from TrackingModule import HandTracking
from pynput.mouse import Controller, Button

handTracking = HandTracking()

cap = cv.VideoCapture(0)
mode = 'null'

mouse = Controller()
point1 = (70,70)
point2 = (454,286)

smooth = 10
preLocationX, preLocationY = 0,0
curLocationX, curLocationY = 0,0


def isClickMode(landmarks):
    check_ngon_giua = handTracking.isRaiseFinger(landmarks, 'GIUA')
    check_ngon_cai = handTracking.isRaiseFinger(landmarks, 'CAI')
    check_ngon_ut = handTracking.isRaiseFinger(landmarks, 'UT')

    if((check_ngon_giua == True)
            and (check_ngon_cai == False)
            and (check_ngon_ut == False)):
        return True

    return False

def isScrollMode(landmarks):
    check_ngon_giua = handTracking.isRaiseFinger(landmarks, 'GIUA')
    check_ngon_cai = handTracking.isRaiseFinger(landmarks, 'CAI')
    check_ngon_ut = handTracking.isRaiseFinger(landmarks, 'UT')
    check_ngon_nhan = handTracking.isRaiseFinger(landmarks, 'NHAN')

    if ((check_ngon_giua == True)
            and (check_ngon_ut == True)
            and (check_ngon_nhan == True)
            and (check_ngon_cai == False)):
        return True

    return False

def isMoveMode(landmarks):
    check_ngon_giua = handTracking.isRaiseFinger(landmarks, 'GIUA')
    check_ngon_cai = handTracking.isRaiseFinger(landmarks, 'CAI')
    check_ngon_ut = handTracking.isRaiseFinger(landmarks, 'UT')
    check_ngon_nhan = handTracking.isRaiseFinger(landmarks, 'NHAN')
    check_ngon_tro = handTracking.isRaiseFinger(landmarks, 'TRO')

    if((check_ngon_cai == True)
        and (check_ngon_tro == True)
        and (check_ngon_giua == True)
        and (check_ngon_nhan == True)
        and (check_ngon_ut == True)):
        return True

    return False

while True:
    _, frame = cap.read()

    h,w,c = frame.shape

    landmarks = handTracking.findLandMark(frame)

    if(landmarks != None):
        #Move mode
        if(isMoveMode(landmarks)):
            cv.putText(frame, "Move mouse", point1, cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv.LINE_AA)
            cv.rectangle(frame, point1, point2, (255, 255, 0), 2)
            clickPoint = ((landmarks[12].x * w), (landmarks[12].y * h))
            if (clickPoint >= point1 and clickPoint <= point2):
                curLocationX = (clickPoint[0] - point1[0])/384 * 1920
                curLocationY = (clickPoint[1] - point1[1])/216 * 1080

                mouseLocationX = preLocationX + (curLocationX - preLocationX) / smooth
                mouseLocationY = preLocationY + (curLocationY - preLocationY) / smooth

                preLocationX = mouseLocationX
                preLocationY = mouseLocationY

                mouse.position = (mouseLocationX, mouseLocationY)
        #Click mode
        elif(isClickMode(landmarks)):
            cv.putText(frame, "Mouse", point1, cv.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv.LINE_AA)
            cv.rectangle(frame, point1, point2, (255, 255, 0), 2)
            clickPoint = ((landmarks[12].x*w), (landmarks[12].y*h))
            if(clickPoint >= point1 and clickPoint <= point2):
                curLocationX = (clickPoint[0] - point1[0]) / 384 * 1920
                curLocationY = (clickPoint[1] - point1[1]) / 216 * 1080

                mouseLocationX = preLocationX + (curLocationX - preLocationX) / smooth
                mouseLocationY = preLocationY + (curLocationY - preLocationY) / smooth

                preLocationX = mouseLocationX
                preLocationY = mouseLocationY

                mouse.position = (mouseLocationX, mouseLocationY)

                if(handTracking.isRaiseFinger(landmarks, 'CHUOTTRAI') == False and handTracking.isRaiseFinger(landmarks, 'CHUOTPHAI') == True):
                    print('left mouse clicked')
                    mouse.click(Button.left, 1)
                elif (handTracking.isRaiseFinger(landmarks, 'CHUOTPHAI') == False and handTracking.isRaiseFinger(landmarks,'CHUOTTRAI') == True):
                    print('right mouse clicked')
                    mouse.click(Button.right, 1)

        #Scroll mode
        elif(isScrollMode(landmarks)):
            cv.putText(frame, "Scroll", point1, cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv.LINE_AA)
            if (handTracking.isRaiseFinger(landmarks, 'CUON') == False):
                print('mouse scroll down')
                mouse.scroll(0, -1)
            elif (handTracking.isRaiseFinger(landmarks, 'CUON') == True):
                print('mouse scroll up')
                mouse.scroll(0, 1)

    cv.imshow("tracking", frame)
    cv.waitKey(1)