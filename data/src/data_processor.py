import glob
import pandas as pd
import datetime
from datetime import datetime as dt
from spacy.lang.en.stop_words import STOP_WORDS

# read concat and select data for topic modelling
class DataProcessor:
    # constructor with mix of required and optional arguments
    def __init__(self, path_to_dir, cols, selector= "*.csv", topics_to_remove = None, start_date = datetime.date(2019, 12, 1), end_date = datetime.date(2023, 1, 5)):
        self.path_to_dir = path_to_dir # relative path to the directory storing data (assuming multiple csv files)
        self.cols = cols # target column(s) within resulting dataframe
        self.selector = selector # selector within that directory if we only want some files, glob format
        self.topics_to_remove = topics_to_remove # topics to remove - optional, leaving as None will mean no topics are filtered out
        self.start_date = start_date # start and end date - optional, default set to end of 2019 to start of 2023
        self.end_date = end_date
        
        self.stopwords_list = STOP_WORDS # stop words from SpaCy to remove

    # using .selector and .path_to_dir to return all files matching selector in given directory
    def select_data_files(self):
        files = glob.glob(f'{self.path_to_dir}/{self.selector}')
        self.files = files 
        return files

    # reads data from all files selected in select_data_files(), returns single dataframe with data from all files
    def read_and_concat_data_files(self):
        # running select_data_files() if not run already, as this method depends on it
        if not hasattr(self, 'files'):
            self.select_data_files()

        # initialising list to store data from individual files
        df_list = []
        # iterating over each file found that matches selector
        for file_ in self.files:
            # creating pandas dataframe from each csv file
            df = pd.read_csv(file_, usecols = self.cols)
            # setting source column from path - first part of file name separated by underscores e.g. dir1/dir2/dir3/sourcename_date1_to_date2.csv
            df['source'] = file_.split("\\")[-1].split("_")[0]
            df_list.append(df)
        
        # combining if multiple files, returning original df if one file, raising exception if no files or error
        if len(df_list) > 1:
            combined_df = pd.concat(df_list, axis=0, ignore_index=True)
        elif len(df_list) == 1:
            combined_df = df_list[0]
        else:
            raise Exception(f'Something went wrong while trying to read data in from the {self.path_to_dir} directory using the {self.selector} selector - try checking these are correct')

        # returning combined data and storing as a property of the object
        self.combined_data = combined_df
        return combined_df

    # cleaning text by removing stopwords and lowercasing, takes in text of type string so to be used in apply on dataframe
    def _clean_text(self, text):
        return ' '.join([str(word) for word in str(text).lower().split() if word not in (self.stopwords_list)])

    # using pandas to drop duplicates and nones from headline column and updating in class prperty, requires headline column to be present
    def remove_duplicates_and_nones(self):
        if not hasattr(self, 'files'):
            self.read_and_concat_data_files()
        self.combined_data = self.combined_data.drop_duplicates(subset='headline')
        self.combined_data = self.combined_data.dropna()
        return self.combined_data
        
    # filter out dates to within range between .start_date and .end_date, where start date is further back in time/before the end date
    def filter_dates(self):
        if not hasattr(self, 'files'):
            self.read_and_concat_data_files()
        
        self.combined_data['date'] = pd.to_datetime(self.combined_data['date'], errors='coerce')
        self.combined_data = self.combined_data.loc[(self.combined_data['date'].dt.date >= self.start_date) & (self.combined_data['date'].dt.date <= self.end_date)]
        return self.combined_data

    # somewhat blunt tool to remove certain topics based on url, mainly intended to make daily mail dataset size manageable
    def filter_topics(self):
        # handling several potential errors
        if not self.topics_to_remove:
            raise Exception('No topics to remove found. Please pass these in to the DataProcessor as an array topics_to_remove')
        if not hasattr(self, 'files'):
            self.read_and_concat_data_files()
        if 'url' not in self.combined_data.columns:
            raise Exception('Filter topic method relies on having the url as column within the dataset. Try running again with url as one of the items in the \'cols\' parameter')
        
        # removing topics from data, updating object properties and returning resulting data
        for topic in self.topics_to_remove:
            self.combined_data = self.combined_data[~self.combined_data['url'].str.contains(topic)]
        return self.combined_data