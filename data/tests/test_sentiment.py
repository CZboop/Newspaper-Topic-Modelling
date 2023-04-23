import unittest, pytest
from pathlib import Path
import sys
sys.path.append(f"{Path(__file__).parent.parent}")
import src
from src.sentiment import SentimentAnalyser
from src.data_processor import DataProcessor
import os
import glob
from pathlib import Path
import pandas as pd
import pandas.testing as pd_testing
import datetime
import shutil
import plotly

class TestSentiment(unittest.TestCase):

    maxDiff = None

    # setup before the test suite run
    @classmethod
    def setUpClass(self):
        # create temp directory for files with test data
        self.test_dir_name = 'temp_test_files'
        self.temp_within_current_dir = f'{Path(__file__).parent}/{self.test_dir_name}'
        Path(self.temp_within_current_dir).mkdir(parents=True, exist_ok=True)

    def setup_write_test_csv_file(self, dataframe, name):
        dataframe.to_csv(f'{self.temp_within_current_dir}/{name}')

    # pre-process uses methods from data processor which don't need to be tested again individually
    def test_preprocess(self):
        # given - unprocessed headline data and an instance of the undertest sentiment class
        headline_list_of_lists = [['testingtesting'], ['this is a test headline', 'final test'], ['testing test', 'test of the other test', 'testing testing 123', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'a different test', 'another test but not the other test'], ['testing', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'another version of a test']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2025, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        test_data_processor = DataProcessor(path_to_dir=f'{self.temp_within_current_dir}', cols=['headline', 'date', 'url', 'source'], selector= "*.csv")
        undertest_class = SentimentAnalyser(test_data_processor)

        # when - we call the preprocess method of the undertest class
        undertest_class._preprocess()

        # then - the data processor inside the undertest class is storing the data, which has been preprocessed
        self.assertTrue(hasattr(undertest_class.data_processor, 'combined_data'))

    def test_get_polarity_and_subjectivity(self):
        pass

    def test_get_polarity_ratio(self):
        pass

    def test_plot_polarity_ratio(self):
        pass

    def test_get_polarity_over_time(self):
        pass

    def test_plot_polarity_over_time(self):
        pass

    def test_get_subjectivity_averages(self):
        pass 

    def test_plot_subejctivity(self):
        pass

    def test_get_subjectivity_over_time(self):
        pass

    def test_plot_subjectivity_over_time(self):
        pass

    def test_save_as_json(self):
        pass

    # teardown after all tests run to delete temporary files used in tests
    @classmethod
    def tearDownClass(self):
        try:
            shutil.rmtree(self.temp_within_current_dir)
        except OSError as error:
            print(f'An error occured while trying to delete directory: {error.filename} - {error.strerror}.')

if __name__ == "__main__":
    unittest.main()