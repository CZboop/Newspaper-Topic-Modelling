# read concat and select data for topic modelling
import glob
import pandas as pd
import datetime
from datetime import datetime as dt
from spacy.lang.en.stop_words import STOP_WORDS

class DataProcessor:
    def __init__(self, path_to_dir, cols, selector= "*.csv", topics_to_remove = None, start_date = datetime.date(2019, 12, 1), end_date = datetime.date(2023, 1, 5)):
        # relative path to the directory storing data (assuming multiple csv files)
        self.path_to_dir = path_to_dir
        # target column(s) within resulting dataframe
        self.cols = cols 
        # selector within that directory if we only want some files, glob format
        self.selector = selector
        # optional, leaving as None will mean no topics are filtered out
        self.topics_to_remove = topics_to_remove
        # optional, default set to end of 2019 to start of 2023
        self.start_date = start_date 
        self.end_date = end_date

        self.stopwords_list = STOP_WORDS

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
            # below to get and add source from file name hard coded to the existing data files and how they're formatted
            df['source'] = file_.split("\\")[-1].split("_")[0]
            df_list.append(df)
        combined_df = pd.concat(df_list, axis=0, ignore_index=True)
        self.combined_data = combined_df
        return combined_df

    def _clean_text(self, text):
        return ' '.join([str(word) for word in str(text).lower().split() if word not in (self.stopwords_list)])

    def remove_duplicates_and_nones(self):
        # hard coding headline category for now
        if not hasattr(self, 'files'):
            self.read_and_concat_data_files()
        self.combined_data = self.combined_data.drop_duplicates(subset='headline')
        self.combined_data = self.combined_data.dropna()
        return self.combined_data
        
    def filter_dates(self):
        if not hasattr(self, 'files'):
            self.read_and_concat_data_files()
        # where start date is further back in time
        self.combined_data['date'] = pd.to_datetime(self.combined_data['date'], errors='coerce')
        self.combined_data = self.combined_data.loc[(self.combined_data['date'].dt.date >= self.start_date) & (self.combined_data['date'].dt.date <= self.end_date)]
        return self.combined_data

    # somewhat blunt tool to remove certain topics based on url, mainly intended to make daily mail dataset size manageable
    def filter_topics(self):
        if not self.topics_to_remove:
            raise Exception('No topics to remove found. Please pass these in to the DataProcessor as an array topics_to_remove')
        if not hasattr(self, 'files'):
            self.read_and_concat_data_files()
        if 'url' not in self.combined_data.columns:
            raise Exception('Filter topic method relies on having the url as column within the dataset. Try running again with url as one of the items in the \'cols\' parameter')
        for topic in self.topics_to_remove:
            self.combined_data = self.combined_data[~self.combined_data['url'].str.contains(topic)]
        return self.combined_data