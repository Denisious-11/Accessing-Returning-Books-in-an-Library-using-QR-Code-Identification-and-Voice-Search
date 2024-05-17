import cv2
import webbrowser
cap = cv2.VideoCapture('http://192.168.29.132:8081/video')#('rtsp://192.168.29.132:8081/1')
# cap = cv2.VideoCapture(0)
# initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()


while True:
	_, img = cap.read()
	# detect and decode
	data, bbox, _ = detector.detectAndDecode(img)
	# check if there is a QRCode in the image
	if data:
		a=data
		break

	cv2.imshow("QRCODEscanner", img)
	if cv2.waitKey(1) == ord("q"):
		break

b=webbrowser.open(str(a))
cap.release()
cv2.destroyAllWindows()


# import cv2
# #print("Before URL")
# cap = cv2.VideoCapture('rtsp://admin:123456@192.168.1.216/H264?ch=1&subtype=0')
# #print("After URL")
# while True:
#     #print('About to start the Read command')
#     ret, frame = cap.read()
#     #print('About to show frame of Video.')
#     cv2.imshow("Capturing",frame)
#     #print('Running..')
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()
