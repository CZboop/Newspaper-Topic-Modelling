import unittest, pytest
from pathlib import Path
import sys
sys.path.append(f"{Path(__file__).parent.parent}")
from data_processor import DataProcessor
import os
from pathlib import Path
import pandas as pd
import pandas.testing as pd_testing
import datetime
import shutil

# @unittest.skip('skipping for speed while still writing other new tests')
class TestDataProcessor(unittest.TestCase):

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

    def test_select_data_files(self):
        # given - a data processor object with selector for csv files starting with test, path pointing to the temp test files directory
        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : ['testing', 'test of the test', 'another test', 'final test'], 'url' : ['www.test-news.co.uk/123', 'www.test-news.co.uk/321', 'www.test-news.co.uk/3141', 'www.test-news.co.uk/897']})
            self.setup_write_test_csv_file(test_dataframe, f'test_{i}.csv')

        data_processor = DataProcessor(f'./{self.test_dir_name}', ['headline', 'url'], selector= 'test*.csv')

        # when - we call the select data files method of the data processor
        actual = data_processor.select_data_files()

        # then - an array of the five test files is returned, and the data processor has a new property called files
        expected = [f'./{self.test_dir_name}\\test_0.csv', f'./{self.test_dir_name}\\test_1.csv', f'./{self.test_dir_name}\\test_2.csv', f'./{self.test_dir_name}\\test_3.csv', f'./{self.test_dir_name}\\test_4.csv']
        
        self.assertEqual(sorted(actual), sorted(expected))
        self.assertTrue(hasattr(data_processor, 'files'))

    def test_read_and_concat_data_files(self):
        # given - a data processor object with parameters to read in dummy files with names starting with test
        all_dfs = []
        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : ['testing', 'test of the test', 'another test', 'final test'], 'url' : ['www.test-news.co.uk/123', 'www.test-news.co.uk/321', 'www.test-news.co.uk/3141', 'www.test-news.co.uk/897'], 'source' : ['test', 'test', 'test', 'test']})
            all_dfs.append(test_dataframe)
            self.setup_write_test_csv_file(test_dataframe, f'test_{i}.csv')

        data_processor = DataProcessor(f'./{self.test_dir_name}', ['headline', 'url'], selector= 'test*.csv')
        
        # when - we call the read and concat data files method
        actual = data_processor.read_and_concat_data_files()

        # then - a pandas dataframe of combined data from all the files is returned, with a new column 'source' based on the data selector/file names
        expected_df = pd.concat(all_dfs, axis=0, ignore_index=True)

        pd_testing.assert_frame_equal(actual, expected_df)
        #  - and the pandas dataframe is assigned to a class attribute 'combined_data'
        self.assertTrue(hasattr(data_processor, 'combined_data'))

    def test_clean_text_lowercases_text(self):
        # given - a data processor class and mixed case data
        data_processor = DataProcessor(f'./{self.test_dir_name}', ['headline', 'url'], selector= 'test*.csv')
        headline = 'Testing Test of The Test Another Test Final Test'

        # when - we call clean_text on the headline
        actual = data_processor._clean_text(headline)

        # then - the resulting string is the same if it is lowercased
        self.assertEqual(actual, actual.lower())

    def test_clean_text_removes_stopwords(self):
        # given - a data processor class and lowercase data with some stopwords
        data_processor = DataProcessor(f'./{self.test_dir_name}', ['headline', 'url'], selector= 'test*.csv')
        headline = 'testing test of the test and a test final test'

        # when - we call clean_text on the headline
        actual = data_processor._clean_text(headline)

        # then - the resulting string has stopwords removed
        expected = 'testing test test test final test'
        self.assertEqual(actual, expected)

    def test_remove_duplicates_and_nones_can_remove_duplicates(self):
        # given - a data processor set up with duplicate data in the headlines
        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : ['testing', 'test of the test', 'another test', 'final test'], 'url' : ['www.test-news.co.uk/123', 'www.test-news.co.uk/321', 'www.test-news.co.uk/3141', 'www.test-news.co.uk/897'], 'source' : ['test', 'test', 'test', 'test']})
            self.setup_write_test_csv_file(test_dataframe, f'test_{i}.csv')
        
        data_processor = DataProcessor(f'./{self.test_dir_name}', ['headline', 'url'], selector= 'test*.csv')

        # when - we call remove duplicates and nones, and extract the column that should have duplicates dropped
        actual = list(data_processor.remove_duplicates_and_nones()['headline'])
        expected = ['testing', 'test of the test', 'another test', 'final test']

        # then - the returned data does not have duplicates
        self.assertEqual(sorted(actual), sorted(expected))

    def test_remove_duplicates_and_nones_can_remove_nones(self):
        # given - a data processor set up with some missing data of different types (but no duplicates)
        headline_list_of_lists = [['testingtesting', '', 'another test', None], [None, 'test of the test', '', 'final test'], ['testing test', 'test of the other test', None, 'final test but different'], ['testing 123', None, 'a different test', ''], ['testing', None, None, 'final test the final one']]
        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'url' : ['www.test-news.co.uk/123', 'www.test-news.co.uk/321', 'www.test-news.co.uk/3141', 'www.test-news.co.uk/897'], 'source' : ['test', 'test', 'test', 'test']})
            self.setup_write_test_csv_file(test_dataframe, f'test_{i}.csv')
        
        data_processor = DataProcessor(f'./{self.test_dir_name}', ['headline', 'url'], selector= 'test*.csv')

        # when - we call remove duplicates and nones, and extract the column that should have duplicates removed
        actual = list(data_processor.remove_duplicates_and_nones()['headline'])
        expected = ['testingtesting', 'another test', 'test of the test', 'final test', 'testing test', 'test of the other test', 'final test but different', 'testing 123', 'a different test', 'testing','final test the final one']

        # then - the returned data is the original minus the missing data
        self.assertEqual(sorted(actual), sorted(expected))

    def test_filter_dates_removes_dates_before_start_date(self):
        # given - a data processor with start/end date parameters passed in, and data containing dates with some dates outside the start/end range
        headline_list_of_lists = [['testingtesting', 'a test of the test', 'another test', 'test headline'], ['one of the tests', 'test of the test', 'a headline', 'final test'], ['testing test', 'test of the other test', 'a headline with a value', 'final test but different'], ['testing 123', 'here is a test', 'a different test', 'there is another test'], ['testing', 'it is a test', 'it is not a test', 'final test the final one']]

        date_list_of_lists = [[ datetime.date(2019, 12, 1), datetime.date(2019, 11, 1), datetime.date(2029, 12, 1), datetime.date(2019, 12, 21)], [ datetime.date(2022, 12, 1), datetime.date(2022, 10, 1), datetime.date(2020, 5, 12), datetime.date(2021, 3, 9)], [ datetime.date(2032, 12, 1), datetime.date(2025, 8, 14), datetime.date(2122, 9, 14), datetime.date(2022, 2, 11)], [ datetime.date(2021, 7, 12), datetime.date(2021, 8, 14), datetime.date(1999, 12, 1), datetime.date(2009, 7, 12)], [ datetime.date(2020, 9, 8), datetime.date(2020, 5, 29), datetime.date(2029, 7, 23), datetime.date(2020, 1, 18)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'url' : ['www.test-news.co.uk/123', 'www.test-news.co.uk/321', 'www.test-news.co.uk/3141', 'www.test-news.co.uk/897'], 'date': date_list_of_lists[i]})
            self.setup_write_test_csv_file(test_dataframe, f'test_{i}.csv')

        start_date = datetime.date(2019, 12, 1)
        end_date = datetime.date(2022, 12, 1)

        data_processor = DataProcessor(f'./{self.test_dir_name}', ['headline', 'url', 'date'], selector= 'test*.csv', start_date= start_date, end_date= end_date)

        # when - the filter dates method is called and the date column is extracted
        actual = list(data_processor.filter_dates()['date'])

        # then - there are no dates before the start date
        actual_before_start_date = list(filter(lambda x: x < start_date, actual))

        # and there are no dates after the end date
        self.assertEqual(len(actual_before_start_date), 0)
    
    def test_filter_dates_removes_dates_after_end_date(self):
        # given - a data processor with start/end date parameters passed in, and data containing dates with some dates outside the start/end range
        headline_list_of_lists = [['testingtesting', 'a test of the test', 'another test', 'test headline'], ['one of the tests', 'test of the test', 'a headline', 'final test'], ['testing test', 'test of the other test', 'a headline with a value', 'final test but different'], ['testing 123', 'here is a test', 'a different test', 'there is another test'], ['testing', 'it is a test', 'it is not a test', 'final test the final one']]

        date_list_of_lists = [[ datetime.date(2019, 12, 1), datetime.date(2019, 11, 1), datetime.date(2029, 12, 1), datetime.date(2019, 12, 21)], [ datetime.date(2022, 12, 1), datetime.date(2022, 10, 1), datetime.date(2020, 5, 12), datetime.date(2021, 3, 9)], [ datetime.date(2032, 12, 1), datetime.date(2025, 8, 14), datetime.date(2122, 9, 14), datetime.date(2022, 2, 11)], [ datetime.date(2021, 7, 12), datetime.date(2021, 8, 14), datetime.date(1999, 12, 1), datetime.date(2009, 7, 12)], [ datetime.date(2020, 9, 8), datetime.date(2020, 5, 29), datetime.date(2029, 7, 23), datetime.date(2020, 1, 18)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'url' : ['www.test-news.co.uk/123', 'www.test-news.co.uk/321', 'www.test-news.co.uk/3141', 'www.test-news.co.uk/897'], 'date': date_list_of_lists[i]})
            self.setup_write_test_csv_file(test_dataframe, f'test_{i}.csv')

        start_date = datetime.date(2019, 12, 1)
        end_date = datetime.date(2022, 12, 1)

        data_processor = DataProcessor(f'./{self.test_dir_name}', ['headline', 'url', 'date'], selector= 'test*.csv', start_date= start_date, end_date= end_date)

        # when - the filter dates method is called and the date column is extracted
        actual = list(data_processor.filter_dates()['date'])

        # then - there are no dates before the start date
        actual_after_end_date = list(filter(lambda x: x > end_date, actual))

        # and there are no dates after the end date
        self.assertEqual(len(actual_after_end_date), 0)
    
    def test_filter_topics(self):
        # given - some data with different topics in url and a data processor object set to filter out one of the topics
        headline_list_of_lists = [['testingtesting', 'a test of the test', 'another test', 'test headline'], ['one of the tests', 'test of the test', 'a headline', 'final test'], ['testing test', 'test of the other test', 'a headline with a value', 'final test but different'], ['testing 123', 'here is a test', 'a different test', 'there is another test'], ['testing', 'it is a test', 'it is not a test', 'final test the final one']]

        url_list_of_lists = [[ 'www.test-news/science/article001', 'www.test-news/politics/article002', 'www.test-news/tech/article003', 'www.test-news/education/article004'], [ 'www.test-news/politics/article005', 'www.test-news/tech/article006', 'www.test-news/politics/article007', 'www.test-news/science/article008'], [ 'www.test-news/science/article009', 'www.test-news/politics/article010', 'www.test-news/tech/article011', 'www.test-news/politics/article012'], [ 'www.test-news/tech/article013', 'www.test-news/politics/article014', 'www.test-news/tech/article015', 'www.test-news/politics/article016'], [ 'www.test-news/tech/article017', 'www.test-news/politics/article018', 'www.test-news/science/article019', 'www.test-news/politics/article020']]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'url' : url_list_of_lists[i], 'date': [ datetime.date(2019, 12, 1), datetime.date(2019, 11, 1), datetime.date(2029, 12, 1), datetime.date(2019, 12, 21)]})
            self.setup_write_test_csv_file(test_dataframe, f'test_{i}.csv')

        data_processor = DataProcessor(f'./{self.test_dir_name}', ['headline', 'url', 'date'], selector= 'test*.csv', topics_to_remove= ['science'])

        # when - we call filter topics and extract the url column
        actual = list(data_processor.filter_topics()['url'])

        # then - resulting data no longer includes the topic that should be filtered out
        expected = ['www.test-news/politics/article002', 'www.test-news/tech/article003', 'www.test-news/education/article004','www.test-news/politics/article005', 'www.test-news/tech/article006', 'www.test-news/politics/article007', 'www.test-news/politics/article010', 'www.test-news/tech/article011', 'www.test-news/politics/article012','www.test-news/tech/article013', 'www.test-news/politics/article014', 'www.test-news/tech/article015', 'www.test-news/politics/article016','www.test-news/tech/article017', 'www.test-news/politics/article018', 'www.test-news/politics/article020']
        self.assertEqual(sorted(actual), sorted(expected))

    # teardown to undo temp changes after the test suite run - removing temporary test files and directory
    @classmethod
    def tearDownClass(self):
        try:
            shutil.rmtree(self.temp_within_current_dir)
        except OSError as error:
            print(f'An error occured while trying to delete directory: {error.filename} - {error.strerror}.')

if __name__ == "__main__":
    unittest.main()