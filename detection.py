from retrieval.detector import Detector

if __name__ == '__main__':	
	detector = Detector("weight/mask_rcnn_fashion.h5")

	detector.detection("2.jpg")