import pickle
import os
import copy

# DataHandler class responsible for managing the data and saving it.
class DataHandler:
    # constructor
    def __init__(self):
        # members
        self.data = {}
        self.last_time_data = {}
        self.currentData = {}
        self.currentRects = []
        self.pf = 0
        self.first_writing = True

    # The add_key function adding a new key-value pair to the current image data or a value if the key exists.
    # Input: key - string, the image name.
    # rect - list, representation of a rectangle(x,y,w,h).
    def add_key(self, key, rect):
        if key in self.currentData:
            self.currentData[key].append(rect)
        else:
            self.currentData[key] = [rect]

    # The flash_CurrentData function adds the current image data to the general data.
    def flash_CurrentData(self):
        if len(self.currentData) > 0:
            print(self.last_time_data)
            key = list(self.currentData.keys())[0]
            if key in self.data:  # in case the key already exists in the general data.
                self.data[key].extend(self.currentData[key])
            else:  # in case of a new key.
                self.data[key] = self.currentData[key]
            self.currentData.clear()
            print(self.last_time_data)

    # The data_to_pickle function saves the general data in a pickle format.
    def data_to_pickle(self):
        if len(self.data) > 0:
            self.pf = open('results.pickle', 'wb')
            pickle.dump(self.data, self.pf)

    # The current_data_to_pickle function saves the current image data in a pickle format.
    def current_data_to_pickle(self):
        if len(self.currentData) > 0:
            if self.first_writing:  # prevent from reopening the file.
                self.pf = open('results.pickle', 'wb')
                self.first_writing = False
            self.last_time_data[list(self.currentData.keys())[0]] = self.currentData[list(self.currentData.keys())[0]]
            pickle.dump(self.last_time_data, self.pf)
    # The pickle_to_data function constructs an img-rects dictionary from the pickle file.
    # return: true, if a pickle file exist and not empty or false, otherwise.
    def pickle_to_data(self):
        if os.path.exists("results.pickle"):  # checks if their is a pickle file.
            if os.path.getsize("results.pickle") > 0:  # checks that the pickle file is not empty.
                unpickled = []
                with open("results.pickle", 'rb') as f:
                    while True:
                        try:
                            unpickled.append(pickle.load(f))  # reading from the pickle file.
                        except EOFError:
                            f.close()
                            break
                    self.data = unpickled[-1]
                    self.last_time_data = copy.deepcopy(self.data)
                    return True
            else:
                return False
        else:
            return False

    # The close_file function closes the pickle file when exiting the program.
    def close_file(self):
        if self.pf != 0:
            self.pf.close()

    # The add_rect function adds a rectangle representation to the current image rectangles list.
    # Input: rect - representation of a rectangle(x,y,w,h).
    def add_rect(self, rect):
        self.currentRects.append(rect)

    # The last_rect function returns the last rectangle.
    def last_rect(self):
        return self.currentRects.pop()

    # The del_last_rect function deletes the last rectangle from the current image rectangle list.
    def del_last_rect(self):
        self.currentData[list(self.currentData.keys())[0]].pop()

    # The clear_rects function clears the current image rectangle list.
    def clear_rects(self):
        self.currentRects.clear()

    # The get_rects_size function returns the size of the current_rects list.
    def get_rects_size(self):
        return len(self.currentRects)

    # The get_data function returns the data which is an imgs-rects dictionary.
    def get_data(self):
        return self.data
