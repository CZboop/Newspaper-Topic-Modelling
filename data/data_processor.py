# read concat and select data for topic modelling
import glob
import pandas as pd
import datetime
from datetime import datetime as dt

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

    def resolve_encoding_errors(self):
        # a couple seem to get weird windows encoding issue, is this just when viewing in excel?
        # but anyway goal here is to remove those issues
        pass

    def remove_duplicates_and_nones(self):
        # hard coding headline category for now
        if not hasattr(self, 'files'):
            self.read_and_concat_data_files()
        self.combined_data = self.combined_data.drop_duplicates(subset='headline').dropna()
        
    def filter_dates(self, start_date, end_date):
        # where start date is further back in time
        self.combined_data['date'] = pd.to_datetime(self.combined_data['date'], errors='coerce')
        self.data_in_range = self.combined_data.loc[(self.combined_data['date'].dt.date >= start_date) & (self.combined_data['date'].dt.date <= end_date)]
        return self.data_in_range