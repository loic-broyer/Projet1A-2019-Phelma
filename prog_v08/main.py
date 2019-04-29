from fonctions import *
from fonctions4pointsref import *





#init

capture = cv2.VideoCapture(0)

ratio = frame.shape[1]/frame.shape[0]


#loop before the game starts
transformMat = fonctions4pointsref(capture)


#main loop


#routine core

def acqCoordinates(,arguments[i]):
	has_frame, frame = capture.read()
	correctedFrame = cv2.warpPerspective(frame,transformMat,(600,600))
	blurred = blur(correctedFrame)
	HSV = convertToHSV(blurred)

	thresholdedRed = threshold
	thresholdedGreen = threshold
	thresholdedBlue = threshold(HSV,)

	opening(thresholdedRed)
	opening(thresholdedGreen)
	opening(thresholdedBlue)
	
	lContour = []
	lContour.append(cv2.findContours(thresholdedRed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE))
	lContour.append(cv2.findContours(thresholdedGreen, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE))
	lContour.append(cv2.findContours(thresholdedBlue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE))
	
	lCenters = []
	for contour in lContour:
		lCenters.append(centroid(coutour))

	for i in range(len(lCenters)):
		if ptInZone(lCenters[i]):
			_ = lCenters.pop([i])

	return_dict[]








while 1:

