import cv2 as cv
import numpy as np
import os

# ImageHandler class responsible for reading the images from the file and mange the image order to be displayed.
class ImageHandler:
    # constructor
    # Input: img_size - int, the image size to be displayed.
    def __init__(self, img_size):
        # members
        self.path = 0
        self.img_size = img_size
        self.imgs = []
        self.idx = 0

    # The set_path function sets the path to the images dir.
    # Inputs: path - string, the path to the dir.
    def set_path(self, path):
        self.path = path

    # The init_list function reads the images from the dir to the imgs list.
    def init_list(self):
        self.imgs.clear()
        for dir, dirs, files in os.walk(os.path.join(self.path)):  # getting the files
            for file in files:
                p = os.path.join(dir, file)
                img = cv.imread(p)
                img = cv.cvtColor(img, cv.COLOR_BGR2RGB)  # changing the color representation to the normal way.
                img = cv.resize(img, (self.img_size, self.img_size))  # resizing the images.
                self.imgs.append([np.array(img), file])  # appending the image and the image name.

    # The next function returns the next image in the imgs list.
    # return: the next image-image name pair.
    def next(self):
        self.idx += 1
        if self.idx >= len(self.imgs):
            self.idx = len(self.imgs) - 1
        img = self.imgs[self.idx]
        return img

    # The prev function returns the previous image in the imgs list.
    # return: the previous image-image name pair.
    def prev(self):
        self.idx -= 1
        if self.idx <= 0:
            self.idx = 0
        img = self.imgs[self.idx]
        return img

    # The get_first_img function returns the first image in the imgs list or the last image that was saved in the
    # pickle file.
    # return: an image-image name pair.
    def get_first_img(self, DH):
        if DH.pickle_to_data():  # creating a dict from the pickle file if exist.
            data = DH.get_data()
            for i, img in enumerate(self.imgs):
                if img[1] == list(data.keys())[-1]:  # finding the last image to be saved.
                    self.idx = i
                    return img
        return self.imgs[0]

    # The get_idx function returns the idx.
    def get_idx(self):
        return self.idx

    # The get_imgs_size function returns imgs list size.
    def get_imgs_size(self):
        return len(self.imgs)

