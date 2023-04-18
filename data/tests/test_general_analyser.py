import unittest, pytest
from pathlib import Path
import sys
sys.path.append(f"{Path(__file__).parent.parent}")
import src
from src.general_analyser import GeneralAnalyser
from src.data_processor import DataProcessor
import os
from pathlib import Path
import pandas as pd
import pandas.testing as pd_testing
import datetime
import shutil
from itertools import chain

class TestGeneralAnalyser(unittest.TestCase):

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

    def test_compare_ratio_of_docs(self):
        # given - an instance of the undertest class, with multiple sources' data with different numbers of headlines
        headline_list_of_lists = [['testingtesting'], ['this is a test headline', 'final test'], ['testing test', 'test of the other test', 'testing testing 123', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'a different test', 'another test but not the other test'], ['testing', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'another version of a test']]
        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')
        
        undertest_class = GeneralAnalyser(data_selectors = {'test0' : {'selector': 'test0_*.csv'}, 'test1' : {'selector': 'test1_*.csv'}, 
        'test2': {'selector':'test2_*.csv'}, 'test3' : {'selector': 'test3_*.csv'}, 'test4' : {'selector': 'test4_*.csv'}}, path_to_dir=f'./{self.test_dir_name}')

        # when - the compare ratio of docs method is called
        actual_all_records, actual_record_numbers, actual_record_percentages = undertest_class.compare_ratio_of_docs()

        # then - total number of records matches the total passed into the class
        expected_all_records = len(list(chain.from_iterable(headline_list_of_lists)))
        # note - record numbers are returned as dict with selector in title case key and int number of records value
        expected_record_numbers = {'Test0' : 1, 'Test1' : 2, 'Test2' : 7, 'Test3' : 4, 'Test4' : 6}
        # note - expected record %ages returned as dict with same keys as above, float percentage values
        # in total there are 20 records so %age should be x5 the number
        expected_record_percentages = {'Test0' : 5, 'Test1' : 10, 'Test2' : 35, 'Test3' : 20, 'Test4' : 30}

        self.assertEqual(actual_all_records, expected_all_records)
        self.assertEqual(actual_record_numbers, expected_record_numbers)
        self.assertEqual(actual_record_percentages, expected_record_percentages)
        # checking that percentages add up to 100
        self.assertEqual(sum(actual_record_percentages.values()), 100)

    def test_visualise_percentages(self):
        pass

    # TODO: remove this from both class and test?
    def test_save_as_html(self):
        pass

    def test_save_as_json(self):
        pass

    def test_compare_number_of_docs_over_time(self):
        pass

    def test_visualise_number_over_time(self):
        pass

    def test_run(self):
        pass

    @classmethod
    def tearDownClass(self):
        try:
            shutil.rmtree(self.temp_within_current_dir)
        except OSError as error:
            print(f'An error occured while trying to delete directory: {error.filename} - {error.strerror}.')

if __name__ == "__main__":
    unittest.main()