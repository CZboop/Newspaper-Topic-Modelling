import unittest, pytest
from pathlib import Path
import sys
sys.path.append(f"{Path(__file__).parent.parent}")
import src
from src.data_processor import DataProcessor
import os
from pathlib import Path
import pandas as pd
import pandas.testing as pd_testing

class TestDataProcessor(unittest.TestCase):

    maxDiff = None

    # setup before the test suite run
    @classmethod
    def setUpClass(self):
        # create temp directory for files with test data
        self.test_dir_name = 'temp_test_files'
        self.temp_within_current_dir = f'{Path(__file__).parent}/{self.test_dir_name}'
        Path(self.temp_within_current_dir).mkdir(parents=True, exist_ok=True)
        # pass

    def setup_write_test_csv_file(self, dataframe, name):
        dataframe.to_csv(f'{self.temp_within_current_dir}/{name}')

    # def test_tests_running(self):
    #     self.assertEqual(1, 0)

    def test_select_data_files(self):
        # given - a data processor object with selector for csv files starting with test, path pointing to the temp test files directory
        data_processor = DataProcessor(f'./{self.test_dir_name}', ['headline', 'url'], selector= 'test*.csv')
        print(self.test_dir_name)
        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : ['testing', 'test of the test', 'another test', 'final test'], 'url' : ['www.test-news.co.uk/123', 'www.test-news.co.uk/321', 'www.test-news.co.uk/3141', 'www.test-news.co.uk/897']})
            self.setup_write_test_csv_file(test_dataframe, f'test_{i}.csv')
        # when - we call the select data files method of the data processor
        actual = data_processor.select_data_files()

        # then - an array of the four test files is returned, and the data processor has a new property called files
        expected = [f'./{self.test_dir_name}\\test_0.csv', f'./{self.test_dir_name}\\test_1.csv', f'./{self.test_dir_name}\\test_2.csv', f'./{self.test_dir_name}\\test_3.csv', f'./{self.test_dir_name}\\test_4.csv']
        
        self.assertEqual(actual, expected)
        self.assertTrue(hasattr(data_processor, 'files'))

# TODO: test with and without files there already?
    def test_read_and_concat_data_files(self):
        # given - a data processor object with parameters to read in dummy files with names starting with test
        data_processor = DataProcessor(f'./{self.test_dir_name}', ['headline', 'url'], selector= 'test*.csv')
        all_dfs = []
        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : ['testing', 'test of the test', 'another test', 'final test'], 'url' : ['www.test-news.co.uk/123', 'www.test-news.co.uk/321', 'www.test-news.co.uk/3141', 'www.test-news.co.uk/897'], 'source' : ['test', 'test', 'test', 'test']})
            all_dfs.append(test_dataframe)
            self.setup_write_test_csv_file(test_dataframe, f'test_{i}.csv')
            
        # when - we call the read and concat data files method
        actual = data_processor.read_and_concat_data_files()

        # then - a pandas dataframe of combined data from all the files is returned, with a new column 'source' based on the data selector/file names
        expected_df = pd.concat(all_dfs, axis=0, ignore_index=True)
        print(f'ACTUAL::::{actual}')
        print(f'EXPECTED::::{expected_df}')
        pd_testing.assert_frame_equal(actual, expected_df)
        #  - and the pandas dataframe is assigned to a class attribute 'combined_data'
        self.assertTrue(hasattr(data_processor, 'combined_data'))

    # def test_clean_text(self):
    #     pass

    # def test_remove_duplicates_and_nones(self):
    #     pass

    # def test_filter_dates(self):
    #     pass
    
    # def test_filter_topics(self):
    #     pass

    # teardown to undo temp changes after the test suite run
    # @classmethod
    # def tearDownClass(cls):
    #     pass
        # TODO: remove file and contents with appropriate exception handling

if __name__ == "__main__":
    unittest.main()