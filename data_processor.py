# read concat and select data for topic modelling
import glob

class DataProcessor:
    def __init__(self, path_to_dir, selector, cols):
        # relative path to the directory storing data (assuming multiple csv files)
        self.path_to_dir = path_to_dir
        # selector within that directory if we only want some files, glob format
        self.selector = selector
        # target column(s) within resulting dataframe
        self.cols = cols 

    def select_data_files(self):
        pass 

    def read_and_concat_data_files(self):
        pass

    