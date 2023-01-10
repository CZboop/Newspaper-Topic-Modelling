# read concat and select data for topic modelling
import glob
import pandas as pd

class DataProcessor:
    def __init__(self, path_to_dir, cols, selector= "*"):
        # relative path to the directory storing data (assuming multiple csv files)
        self.path_to_dir = path_to_dir
        # target column(s) within resulting dataframe
        self.cols = cols 
        # selector within that directory if we only want some files, glob format
        self.selector = selector

    def select_data_files(self):
        files = glob.glob(f'{self.path_to_dir}/{self.selector}')
        self.files = files 
        return files

    def read_and_concat_data_files(self):
        if not hasattr(self, 'files'):
            self.select_data_files()
        df_list = []
        for file_ in self.files:
            df = pd.read_csv(file_, usecols = self.cols)
            df_list.append(df)
        combined_df = pd.concat(df_list, axis=0, ignore_index=True)
        self.combined_data = combined_df
        return combined_df

    