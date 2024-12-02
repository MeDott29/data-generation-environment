import numpy as np
import random

class DataGenerator:
    def __init__(self, seed):
        random.seed(seed)
    
    def generate_sand_plot(self, size):
        data = np.random.rand(size, size)
        return data
    
    def generate_mnist_data(self, size):
        data = np.zeros((size, size))
        data += np.random.rand(size, size) * 0.1
        return data
    
    def data_to_image_data(self, data, size):
        img_data = (data * 255).astype(np.uint8).flatten()
        return img_data