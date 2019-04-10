from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import cv2
import io
import socket
import struct
import time
import pickle
import zlib

def independence_object():
	ap = argparse.ArgumentParser()
	ap.add_argument("-p", "--prototxt", required=True, help="path to Caffe 'deploy' prototxt file")
	ap.add_argument("-m", "--model", required=True, help="path to Caffe pre-trained model")
	ap.add_argument("-c", "--confidence", type=float, default=0.2, help="minimum probability to filter weak detections")
	args = vars(ap.parse_args())

	CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
			   "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
			   "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
			   "sofa", "train", "tvmonitor"]

	COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

	print("[INFO] loading model...")
	net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	time.sleep(2.0)
	fps = FPS().start()


	while True:
		frame = vs.read()
		frame = imutils.resize(frame, width=300)

		(h, w) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

		net.setInput(blob)
		detections = net.forward()

		for i in np.arange(0, detections.shape[2]):
			confidence = detections[0, 0, i, 2]

			if confidence > args["confidence"]:
				idx = int(detections[0, 0, i, 1])
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")

				persent = confidence * 100
				label = "{}: {:.2f}%".format(CLASSES[idx], persent)

				cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[idx], 2)
				y = startY - 15 if startY - 15 > 15 else startY + 15
				cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break
		fps.update()

	fps.stop()
	print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
	cv2.destroyAllWindows()
	vs.stop()

def im(host, port):
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	client_socket.connect((host,port))
	connection = client_socket.makefile('wb')

	ap = argparse.ArgumentParser()
	ap.add_argument("-p", "--prototxt", required=True, help="path to Caffe 'deploy' prototxt file")
	ap.add_argument("-m", "--model", required=True, help="path to Caffe pre-trained model")
	ap.add_argument("-c", "--confidence", type=float, default=0.2, help="minimum probability to filter weak detections")
	args = vars(ap.parse_args())

	CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
			   "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
			   "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
			   "sofa", "train", "tvmonitor"]

	COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))
	print("[INFO] loading model...")
	net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	time.sleep(2.0)
	fps = FPS().start()

	img_counter = 0
	encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
	while True:
		frame = vs.read()
		frame = imutils.resize(frame, width=300)

		(h, w) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

		net.setInput(blob)
		detections = net.forward()
		for i in np.arange(0, detections.shape[2]):

			confidence = detections[0, 0, i, 2]

			if confidence > args["confidence"]:
				idx = int(detections[0, 0, i, 1])
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")

				persent = confidence * 100
				label = "{}: {:.2f}%".format(CLASSES[idx], persent)
				if idx ==15 and persent >=90:
					result, frame = cv2.imencode('.jpg', frame, encode_param)

					data = pickle.dumps(frame, 0)
					size = len(data)
					print("{}: {}".format(img_counter, size))
					time.sleep(0.1)
					client_socket.sendall(struct.pack(">L", size) + data)
					img_counter += 1

				cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[idx], 2)
				y = startY - 15 if startY - 15 > 15 else startY + 15
				cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break
		fps.update()

	fps.stop()
	print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
	cv2.destroyAllWindows()
	vs.stop()

if __name__ == '__main__':
	host = socket.gethostname()
	port = 9999
	if bool(im(host, port)) ==True:
		im(host,port)
	else:
		time.sleep(0.5)
		independence_object()
