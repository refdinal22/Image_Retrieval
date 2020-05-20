import time
import sys
import skimage.io
import matplotlib.pyplot as plt
import tensorflow as tf
import mrcnn.model as modellib

sys.path.insert(0, "../")
from config.inference_config import InferenceConfig
graph = tf.get_default_graph()

class Detector:
    def __init__(self, model_path):
        config = InferenceConfig()  

        self.class_names = ['BG', 'top', 'long', 'bottom']
        # Using CPU
        with tf.device('/cpu:0'):
            self.model = modellib.MaskRCNN(mode="inference", config=config, model_dir="")
        
        self.model.load_weights(model_path, by_name=True)

    def detection(self, image):    	
		# Run detection
        start = time.time()
        with graph.as_default():
            detection_results = self.model.detect([image], verbose=1)
        end = time.time()

		# Visualize results
        print("Cost time: ",end-start," (s)")
        result = detection_results[0]

        return result

    def get_width(self, xy):
        width = abs(xy[1] - xy[3])
        return width

    def get_height(self, xy):
        height = abs(xy[0] - xy[2])
        return height

    def get_area(self, xy):
        width = self.get_width(xy)
        height = self.get_height(xy)
        area = width * height
        return area

    def get_biggest_box(self, xy_list):
        biggest_area = 0
        for i, xy in enumerate(xy_list):
            area = self.get_area(xy)
            if area > biggest_area:
                biggest_area = area
                biggest_xy = xy
                ix = i
        return biggest_xy, ix

    def crop_object(self, img, xy):    
        target = img[xy[0]:xy[2], xy[1]:xy[3], :]
        # Resize to 224 x 224
        target = skimage.transform.resize(target, (224, 224), preserve_range=True)
        return target

    # def show(self, image_path):
    #     print(image_path)
    #     query_image = skimage.io.imread(image_path)
    #     plt.imshow(query_image)
    #     plt.show()