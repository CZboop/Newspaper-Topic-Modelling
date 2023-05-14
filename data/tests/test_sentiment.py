import unittest, pytest
from pathlib import Path
import sys
sys.path.append(f"{Path(__file__).parent.parent}")
import src
from src.sentiment_analyser import SentimentAnalyser
from src.data_processor import DataProcessor
import os
import glob
from pathlib import Path
import pandas as pd
import datetime
import shutil
import plotly
import statistics
import plotly.express as px
import json

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

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        test_data_processor = DataProcessor(path_to_dir=f'{self.temp_within_current_dir}', cols=['headline', 'date', 'url', 'source'], selector= "*.csv")
        undertest_class = SentimentAnalyser(test_data_processor)

        # when - we call the preprocess method of the undertest class
        undertest_class._preprocess()

        # then - the data processor inside the undertest class is storing the data, which has been preprocessed
        self.assertTrue(hasattr(undertest_class.data_processor, 'combined_data'))

    def test_get_polarity_and_subjectivity_adds_polarity_column_to_main_dataframe(self):
        # given - headline data passed into a data processor in an instance of the sentiment analyser class
        headline_list_of_lists = [['testingtesting'], ['this is a test headline', 'final test'], ['testing test', 'test of the other test', 'testing testing 123', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'a different test', 'another test but not the other test'], ['testing', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'another version of a test']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        test_data_processor = DataProcessor(path_to_dir=f'{self.temp_within_current_dir}', cols=['headline', 'date', 'url', 'source'], selector= "*.csv")
        undertest_class = SentimentAnalyser(test_data_processor)

        # when - we call the get polarity and subjectivity method
        undertest_class._get_polarity_subjectivity()

        # then - the undertest sentiment analyser class has a new column called polarity
        self.assertTrue('polarity' in undertest_class.data_df.columns)

    def test_get_polarity_and_subjectivity_adds_subjectivity_column_to_main_dataframe(self):
        # given - headline data passed into a data processor in an instance of the sentiment analyser class
        headline_list_of_lists = [['testingtesting'], ['this is a test headline', 'final test'], ['testing test', 'test of the other test', 'testing testing 123', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'a different test', 'another test but not the other test'], ['testing', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'another version of a test']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        test_data_processor = DataProcessor(path_to_dir=f'{self.temp_within_current_dir}', cols=['headline', 'date', 'url', 'source'], selector= "*.csv")
        undertest_class = SentimentAnalyser(test_data_processor)

        # when - we call the get polarity and subjectivity method
        undertest_class._get_polarity_subjectivity()

        # then - the undertest sentiment analyser class has a new column called subjectivity
        self.assertTrue('subjectivity' in undertest_class.data_df.columns)

    def test_get_polarity_and_subjectivity_added_subjectivity_column_is_all_within_expected_range(self):
        # given - headline data with mixed subjectivity and polarity passed into a data processor in an instance of the sentiment analyser class
        headline_list_of_lists = [['in my opinion this is a bit like something that happened to me where i wrote a headline'], ['this is a test headline', 'final test'], ['a terrible disgusting testing test', 'i hate it', 'i love it', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'i dont know but in my opinion this might be a fake headline', 'another test but not the other test'], ['this is a great fake headline', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'this fake headline is really bad']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        test_data_processor = DataProcessor(path_to_dir=f'{self.temp_within_current_dir}', cols=['headline', 'date', 'url', 'source'], selector= "*.csv")
        undertest_class = SentimentAnalyser(test_data_processor)

        # when - we call the get polarity and subjectivity method
        undertest_class._get_polarity_subjectivity()

        # then - the created subjectivity column is all floats between 0 and 1
        actual_subjectivity_col = undertest_class.data_df['subjectivity']

        self.assertTrue(all(actual_subjectivity_col.between(0,1)))

    def test_get_polarity_and_subjectivity_added_polarity_column_is_all_within_expected_range(self):
        # given - headline data with mixed subjectivity and polarity passed into a data processor in an instance of the sentiment analyser class
        headline_list_of_lists = [['in my opinion this is a bit like something that happened to me where i wrote a headline'], ['this is a test headline', 'final test'], ['a terrible disgusting testing test', 'i hate it', 'i love it', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'i dont know but in my opinion this might be a fake headline', 'another test but not the other test'], ['this is a great fake headline', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'this fake headline is really bad']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        test_data_processor = DataProcessor(path_to_dir=f'{self.temp_within_current_dir}', cols=['headline', 'date', 'url', 'source'], selector= "*.csv")
        undertest_class = SentimentAnalyser(test_data_processor)

        # when - we call the get polarity and subjectivity method
        undertest_class._get_polarity_subjectivity()

        # then - the created polarity column is all floats between -1 and 1
        actual_polarity_col = undertest_class.data_df['polarity']

        self.assertTrue(all(actual_polarity_col.between(-1,1)))

    def test_get_polarity_ratio_gives_correct_ratio(self):
        # given - - headline data with mixed subjectivity and polarity passed into a data processor in an instance of the sentiment analyser class
        headline_list_of_lists = [['in my opinion this is a bit like something that happened to me where i wrote a headline'], ['this is a test headline', 'final test'], ['a terrible disgusting testing test', 'i hate it', 'i love it', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'i dont know but in my opinion this might be a fake headline', 'another test but not the other test'], ['this is a great fake headline', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'this fake headline is really bad i think']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        test_data_processor = DataProcessor(path_to_dir=f'{self.temp_within_current_dir}', cols=['headline', 'date', 'url', 'source'], selector= "*.csv")
        undertest_class = SentimentAnalyser(test_data_processor)

        # when - we call the get polarity subjectivity method and overwrite polarity column to set values
        undertest_class._get_polarity_subjectivity()
        polarity_col = [ 0, 0, 0, 0, 0, 0, 0, -0.5, -0.1, -0.4, -0.3, -0.2, 0.2, 0.7, 1, 0.1, 0.5, 0.88, 0.32, 0.1 ]
        undertest_class.data_df['polarity'] = polarity_col
        
        actual_ratios = undertest_class.get_polarity_ratio()

        # then - the expected percentages for each of the three categories is returned (%age will be count x 5 as there are 20 headlines)
        expected_ratios = {'positive': 40.0, 'negative': 25.0, 'neutral' : 35.0}
        self.assertDictEqual(actual_ratios, expected_ratios)

    def test_plot_polarity_ratio_saves_expected_json_file(self):
        # given - headline data with mixed subjectivity and polarity passed into a data processor in an instance of the sentiment analyser class
        headline_list_of_lists = [['in my opinion this is a bit like something that happened to me where i wrote a headline'], ['this is a test headline', 'final test'], ['a terrible disgusting testing test', 'i hate it', 'i love it', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'i dont know but in my opinion this might be a fake headline', 'another test but not the other test'], ['this is a great fake headline', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'this fake headline is really bad i think']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        test_data_processor = DataProcessor(path_to_dir=f'{self.temp_within_current_dir}', cols=['headline', 'date', 'url', 'source'], selector= "*.csv")
        undertest_class = SentimentAnalyser(test_data_processor, source_name="test", save_path=f'{self.temp_within_current_dir}')

        # when - we call the undertest plot polarity method, passing in set ratios in dict format
        expected_polarity_ratios = {'positive': 40.0, 'negative': 25.0, 'neutral' : 35.0}
        undertest_class.plot_polarity_ratio(expected_polarity_ratios)

        # then - a json file with the expected path and name is created
        test_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test_polarity_ratio.json')
        self.assertTrue(test_file_path.is_file())

    def test_plot_polarity_ratio_creates_plot_with_expected_data(self):
        # given - headline data with mixed subjectivity and polarity passed into a data processor in an instance of the sentiment analyser class
        headline_list_of_lists = [['in my opinion this is a bit like something that happened to me where i wrote a headline'], ['this is a test headline', 'final test'], ['a terrible disgusting testing test', 'i hate it', 'i love it', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'i dont know but in my opinion this might be a fake headline', 'another test but not the other test'], ['this is a great fake headline', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'this fake headline is really bad i think']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        test_data_processor = DataProcessor(path_to_dir=f'{self.temp_within_current_dir}', cols=['headline', 'date', 'url', 'source'], selector= "*.csv")
        undertest_class = SentimentAnalyser(test_data_processor, source_name="test", save_path=f'{self.temp_within_current_dir}')

        # when - we call the undertest plot polarity method, passing in set ratios in dict format
        expected_polarity_ratios_dict = {'positive': 40.0, 'negative': 25.0, 'neutral' : 35.0}
        actual_fig = undertest_class.plot_polarity_ratio(expected_polarity_ratios_dict)

        # then - the data in the figure generated matches the expected data
        expected_polarity_ratios = list(expected_polarity_ratios_dict.values())
        actual_polarity_ratios = list(actual_fig["data"][0]["values"])
        self.assertListEqual(actual_polarity_ratios, expected_polarity_ratios)

    def test_get_polarity_over_time_returns_polarity_for_each_month(self):
        # given - headline data with mixed subjectivity and polarity passed into a data processor in an instance of the sentiment analyser class
        headline_list_of_lists = [['in my opinion this is a bit like something that happened to me where i wrote a headline'], ['this is a test headline', 'final test'], ['a terrible disgusting testing test', 'i hate it', 'i love it', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'i dont know but in my opinion this might be a fake headline', 'another test but not the other test'], ['this is a great fake headline', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'this fake headline is really bad i think']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        test_data_processor = DataProcessor(path_to_dir=f'{self.temp_within_current_dir}', cols=['headline', 'date', 'url', 'source'], selector= "*.csv")
        undertest_class = SentimentAnalyser(test_data_processor, source_name="test", save_path=f'{self.temp_within_current_dir}')

        # when - we call the get polarity over time method on the undertest class
        actual_polarity_over_time = undertest_class.get_polarity_over_time()
        expected_polarity_over_time_keys = [datetime.date(2023, 1, 5), datetime.date(2022, 12, 5), datetime.date(2022, 11, 5), datetime.date(2022, 10, 5), datetime.date(2022, 9, 5), datetime.date(2022, 8, 5), datetime.date(2022, 7, 5), datetime.date(2022, 6, 5), datetime.date(2022, 5, 5), datetime.date(2022, 4, 5), datetime.date(2022, 3, 5), datetime.date(2022, 2, 5), datetime.date(2022, 1, 5), datetime.date(2021, 12, 5), datetime.date(2021, 11, 5), datetime.date(2021, 10, 5), datetime.date(2021, 9, 5), datetime.date(2021, 8, 5), datetime.date(2021, 7, 5), datetime.date(2021, 6, 5), datetime.date(2021, 5, 5), datetime.date(2021, 4, 5), datetime.date(2021, 3, 5), datetime.date(2021, 2, 5), datetime.date(2021, 1, 5), datetime.date(2020, 12, 5), datetime.date(2020, 11, 5), datetime.date(2020, 10, 5), datetime.date(2020, 9, 5), datetime.date(2020, 8, 5), datetime.date(2020, 7, 5), datetime.date(2020, 6, 5), datetime.date(2020, 5, 5), datetime.date(2020, 4, 5), datetime.date(2020, 3, 5), datetime.date(2020, 2, 5), datetime.date(2020, 1, 5), datetime.date(2019, 12, 5)]

        # then - the polarity over time is returned with a polarity value for each month
        self.assertListEqual(list(actual_polarity_over_time.keys()), expected_polarity_over_time_keys)

    def test_plot_polarity_over_time_creates_expected_json_file(self):
        # given - headline data with mixed subjectivity and polarity passed into a data processor in an instance of the sentiment analyser class
        headline_list_of_lists = [['in my opinion this is a bit like something that happened to me where i wrote a headline'], ['this is a test headline', 'final test'], ['a terrible disgusting testing test', 'i hate it', 'i love it', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'i dont know but in my opinion this might be a fake headline', 'another test but not the other test'], ['this is a great fake headline', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'this fake headline is really bad i think']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        test_data_processor = DataProcessor(path_to_dir=f'{self.temp_within_current_dir}', cols=['headline', 'date', 'url', 'source'], selector= "*.csv")
        undertest_class = SentimentAnalyser(test_data_processor, source_name="test", save_path=f'{self.temp_within_current_dir}')

        # when - we call the plot polarity over time method passing in data from get polarity over time
        polarity_over_time = undertest_class.get_polarity_over_time()
        undertest_class.plot_polarity_over_time(polarity_over_time)

        # then - a json file is created with the expected path and name
        test_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test_polarity_over_time.json')
        self.assertTrue(test_file_path.is_file())        

    def test_plot_polarity_over_time_creates_plot_with_expected_data(self):
        # given - headline data with mixed subjectivity and polarity passed into a data processor in an instance of the sentiment analyser class
        headline_list_of_lists = [['in my opinion this is a bit like something that happened to me where i wrote a headline'], ['this is a test headline', 'final test'], ['a terrible disgusting testing test', 'i hate it', 'i love it', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'i dont know but in my opinion this might be a fake headline', 'another test but not the other test'], ['this is a great fake headline', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'this fake headline is really bad i think']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        test_data_processor = DataProcessor(path_to_dir=f'{self.temp_within_current_dir}', cols=['headline', 'date', 'url', 'source'], selector= "*.csv")
        undertest_class = SentimentAnalyser(test_data_processor, source_name="test", save_path=f'{self.temp_within_current_dir}')

        # when - we call the plot polarity over time method passing in data from get polarity over time
        polarity_over_time = undertest_class.get_polarity_over_time()
        actual_fig = undertest_class.plot_polarity_over_time(polarity_over_time)

        # then - the plot returned has months as x axis
        actual_fig_months = [i.strftime('%Y-%m-%d') for i in list(actual_fig["data"][0]["x"])]
        expected_fig_months = ["2023-01-05","2022-12-05","2022-11-05","2022-10-05","2022-09-05","2022-08-05","2022-07-05","2022-06-05","2022-05-05","2022-04-05","2022-03-05","2022-02-05","2022-01-05","2021-12-05","2021-11-05","2021-10-05","2021-09-05","2021-08-05","2021-07-05","2021-06-05","2021-05-05","2021-04-05","2021-03-05","2021-02-05","2021-01-05","2020-12-05","2020-11-05","2020-10-05","2020-09-05","2020-08-05","2020-07-05","2020-06-05","2020-05-05","2020-04-05","2020-03-05","2020-02-05","2020-01-05","2019-12-05"]

        self.assertListEqual(actual_fig_months, expected_fig_months)

    def test_get_subjectivity_averages_gives_median_and_mean(self):
        # given - headline data with mixed subjectivity and polarity passed into a data processor in an instance of the sentiment analyser class
        headline_list_of_lists = [['in my opinion this is a bit like something that happened to me where i wrote a headline'], ['this is a test headline', 'final test'], ['a terrible disgusting testing test', 'i hate it', 'i love it', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'i dont know but in my opinion this might be a fake headline', 'another test but not the other test'], ['this is a great fake headline', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'this fake headline is really bad i think']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        test_data_processor = DataProcessor(path_to_dir=f'{self.temp_within_current_dir}', cols=['headline', 'date', 'url', 'source'], selector= "*.csv")
        undertest_class = SentimentAnalyser(test_data_processor, source_name="test", save_path=f'{self.temp_within_current_dir}')

        # when - we overwrite the subjectivity to set values and then call the get subjectivity info method on the undertest class
        undertest_class._get_polarity_subjectivity()
        subjectivity_data = [1, 1, 1, 1, 1, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5, 0.5, 0.5, 0.25, 0.25, 0.25, 0, 0, 0, 0]
        undertest_class.data_df['subjectivity'] = subjectivity_data

        actual_averages_dict = undertest_class.get_subjectivity_info()

        expected_mean = sum(subjectivity_data) / len(subjectivity_data)
        expected_median = statistics.median(subjectivity_data)

        # then - a dict with median and mean subjectivity is returned
        expected_averages_dict = {'mean': expected_mean, 'median': expected_median}
        self.assertDictEqual(actual_averages_dict, expected_averages_dict)

    def test_plot_subjectivity_creates_expected_json_file(self):
        # given - headline data with mixed subjectivity and polarity passed into a data processor in an instance of the sentiment analyser class
        headline_list_of_lists = [['in my opinion this is a bit like something that happened to me where i wrote a headline'], ['this is a test headline', 'final test'], ['a terrible disgusting testing test', 'i hate it', 'i love it', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'i dont know but in my opinion this might be a fake headline', 'another test but not the other test'], ['this is a great fake headline', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'this fake headline is really bad i think']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        test_data_processor = DataProcessor(path_to_dir=f'{self.temp_within_current_dir}', cols=['headline', 'date', 'url', 'source'], selector= "*.csv")
        undertest_class = SentimentAnalyser(test_data_processor, source_name="test", save_path=f'{self.temp_within_current_dir}')

        # when - we call the plot subjectivity method
        undertest_class.plot_subjectivity()

        # then - the expected json file is created
        test_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test_subjectivity_box_plot.json')
        self.assertTrue(test_file_path.is_file())
    
    def test_plot_subjectivity_returns_plotly_box_plot(self):
        # given - headline data with mixed subjectivity and polarity passed into a data processor in an instance of the sentiment analyser class
        headline_list_of_lists = [['in my opinion this is a bit like something that happened to me where i wrote a headline'], ['this is a test headline', 'final test'], ['a terrible disgusting testing test', 'i hate it', 'i love it', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'i dont know but in my opinion this might be a fake headline', 'another test but not the other test'], ['this is a great fake headline', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'this fake headline is really bad i think']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        test_data_processor = DataProcessor(path_to_dir=f'{self.temp_within_current_dir}', cols=['headline', 'date', 'url', 'source'], selector= "*.csv")
        undertest_class = SentimentAnalyser(test_data_processor, source_name="test", save_path=f'{self.temp_within_current_dir}')

        # when - we call the plot subjectivity method
        actual_box = undertest_class.plot_subjectivity()
        actual_box_type = actual_box["data"][0]["type"]

        # then - the resulting box plot is a plotly figure with type box
        self.assertEqual(actual_box_type, "box")

    def test_get_subjectivity_over_time_returns_subjectivity_for_each_month(self):
        # given - headline data with mixed subjectivity and polarity passed into a data processor in an instance of the sentiment analyser class
        headline_list_of_lists = [['in my opinion this is a bit like something that happened to me where i wrote a headline'], ['this is a test headline', 'final test'], ['a terrible disgusting testing test', 'i hate it', 'i love it', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'i dont know but in my opinion this might be a fake headline', 'another test but not the other test'], ['this is a great fake headline', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'this fake headline is really bad i think']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        test_data_processor = DataProcessor(path_to_dir=f'{self.temp_within_current_dir}', cols=['headline', 'date', 'url', 'source'], selector= "*.csv")
        undertest_class = SentimentAnalyser(test_data_processor, source_name="test", save_path=f'{self.temp_within_current_dir}')

        # when - we call the get subjectivity over time method
        actual_subjectivity_over_time_months = list(undertest_class.get_subjectivity_over_time().keys())

        # then - a collection is returned with a subjectivity value for each month in data range
        expected_subjectivity_over_time_months = [datetime.date(2023, 1, 5), datetime.date(2022, 12, 5), datetime.date(2022, 11, 5), datetime.date(2022, 10, 5), datetime.date(2022, 9, 5), datetime.date(2022, 8, 5), datetime.date(2022, 7, 5), datetime.date(2022, 6, 5), datetime.date(2022, 5, 5), datetime.date(2022, 4, 5), datetime.date(2022, 3, 5), datetime.date(2022, 2, 5), datetime.date(2022, 1, 5), datetime.date(2021, 12, 5), datetime.date(2021, 11, 5), datetime.date(2021, 10, 5), datetime.date(2021, 9, 5), datetime.date(2021, 8, 5), datetime.date(2021, 7, 5), datetime.date(2021, 6, 5), datetime.date(2021, 5, 5), datetime.date(2021, 4, 5), datetime.date(2021, 3, 5), datetime.date(2021, 2, 5), datetime.date(2021, 1, 5), datetime.date(2020, 12, 5), datetime.date(2020, 11, 5), datetime.date(2020, 10, 5), datetime.date(2020, 9, 5), datetime.date(2020, 8, 5), datetime.date(2020, 7, 5), datetime.date(2020, 6, 5), datetime.date(2020, 5, 5), datetime.date(2020, 4, 5), datetime.date(2020, 3, 5), datetime.date(2020, 2, 5), datetime.date(2020, 1, 5), datetime.date(2019, 12, 5)]

        self.assertEqual(actual_subjectivity_over_time_months, expected_subjectivity_over_time_months)

    def test_plot_subjectivity_over_time_creates_expected_json_file(self):
        # given - headline data with mixed subjectivity and polarity passed into a data processor in an instance of the sentiment analyser class
        headline_list_of_lists = [['in my opinion this is a bit like something that happened to me where i wrote a headline'], ['this is a test headline', 'final test'], ['a terrible disgusting testing test', 'i hate it', 'i love it', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'i dont know but in my opinion this might be a fake headline', 'another test but not the other test'], ['this is a great fake headline', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'this fake headline is really bad i think']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        test_data_processor = DataProcessor(path_to_dir=f'{self.temp_within_current_dir}', cols=['headline', 'date', 'url', 'source'], selector= "*.csv")
        undertest_class = SentimentAnalyser(test_data_processor, source_name="test", save_path=f'{self.temp_within_current_dir}')

        # when - we call the plot subjectivity over time method, passing in data from get subjectivity over time method
        subjectivity_over_time = undertest_class.get_subjectivity_over_time()
        undertest_class.plot_subjectivity_over_time(subjectivity_over_time)

        # then - a json file with the expected path and name is created
        test_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test_subjectivity_over_time.json')
        self.assertTrue(test_file_path.is_file())

    def test_plot_subjectivity_over_time_creates_plot_with_expected_data(self):
        # given - headline data with mixed subjectivity and polarity passed into a data processor in an instance of the sentiment analyser class
        headline_list_of_lists = [['in my opinion this is a bit like something that happened to me where i wrote a headline'], ['this is a test headline', 'final test'], ['a terrible disgusting testing test', 'i hate it', 'i love it', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'i dont know but in my opinion this might be a fake headline', 'another test but not the other test'], ['this is a great fake headline', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'this fake headline is really bad i think']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        test_data_processor = DataProcessor(path_to_dir=f'{self.temp_within_current_dir}', cols=['headline', 'date', 'url', 'source'], selector= "*.csv")
        undertest_class = SentimentAnalyser(test_data_processor, source_name="test", save_path=f'{self.temp_within_current_dir}')

        # when - we call the plot subjectivity over time method, passing in data from get subjectivity over time method
        subjectivity_over_time = undertest_class.get_subjectivity_over_time()
        actual_fig = undertest_class.plot_subjectivity_over_time(subjectivity_over_time)

        # then - the plot created has months in range as x axis
        actual_fig_months = [i.strftime('%Y-%m-%d') for i in list(actual_fig["data"][0]["x"])]
        expected_fig_months = ["2023-01-05","2022-12-05","2022-11-05","2022-10-05","2022-09-05","2022-08-05","2022-07-05","2022-06-05","2022-05-05","2022-04-05","2022-03-05","2022-02-05","2022-01-05","2021-12-05","2021-11-05","2021-10-05","2021-09-05","2021-08-05","2021-07-05","2021-06-05","2021-05-05","2021-04-05","2021-03-05","2021-02-05","2021-01-05","2020-12-05","2020-11-05","2020-10-05","2020-09-05","2020-08-05","2020-07-05","2020-06-05","2020-05-05","2020-04-05","2020-03-05","2020-02-05","2020-01-05","2019-12-05"]

        self.assertListEqual(actual_fig_months, expected_fig_months)

    def test_save_as_json_creates_expected_file(self):
        # given - an instance of the undertest sentiment analyser class and a plotly figure
        headline_list_of_lists = [['in my opinion this is a bit like something that happened to me where i wrote a headline'], ['this is a test headline', 'final test'], ['a terrible disgusting testing test', 'i hate it', 'i love it', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'i dont know but in my opinion this might be a fake headline', 'another test but not the other test'], ['this is a great fake headline', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'this fake headline is really bad i think']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        test_data_processor = DataProcessor(path_to_dir=f'{self.temp_within_current_dir}', cols=['headline', 'date', 'url', 'source'], selector= "*.csv")
        undertest_class = SentimentAnalyser(test_data_processor, source_name="test", save_path=f'{self.temp_within_current_dir}')

        test_df = pd.DataFrame({'x': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 'y': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]})
        fig = px.line(test_df, x='x', y='y', title="Test Line Graph")

        # when - we call the save as json method passing in the json data
        test_file_name = "test_json_save"
        undertest_class.save_as_json(fig, test_file_name)

        # then - a json file containing the data of the figure is save in the expected place with expected name
        test_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/{test_file_name}.json')
        self.assertTrue(test_file_path.is_file())
    
    def test_save_as_json_creates_file_with_same_x_axis_data_passed_in(self):
        # given - an instance of the undertest sentiment analyser class and a plotly figure
        headline_list_of_lists = [['in my opinion this is a bit like something that happened to me where i wrote a headline'], ['this is a test headline', 'final test'], ['a terrible disgusting testing test', 'i hate it', 'i love it', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'i dont know but in my opinion this might be a fake headline', 'another test but not the other test'], ['this is a great fake headline', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'this fake headline is really bad i think']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        test_data_processor = DataProcessor(path_to_dir=f'{self.temp_within_current_dir}', cols=['headline', 'date', 'url', 'source'], selector= "*.csv")
        undertest_class = SentimentAnalyser(test_data_processor, source_name="test", save_path=f'{self.temp_within_current_dir}')

        x_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        y_data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

        test_df = pd.DataFrame({'x': x_data, 'y': y_data})
        fig = px.line(test_df, x='x', y='y', title="Test Line Graph")

        # when - we call the save as json method passing in the json data, then load the data back in from the file
        test_file_name = "test_json_save"
        undertest_class.save_as_json(fig, test_file_name)

        test_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/{test_file_name}.json')
        with open(test_file_path) as f:
            file_data = json.load(f)

        # then - the json file created has the same data that was passed in
        actual_file_data_y = file_data["data"][0]["y"]
        expected_file_data_y = y_data

        self.assertListEqual(actual_file_data_y, expected_file_data_y)

    def test_save_as_json_creates_file_with_same_x_axis_data_passed_in(self):
        # given - an instance of the undertest sentiment analyser class and a plotly figure
        headline_list_of_lists = [['in my opinion this is a bit like something that happened to me where i wrote a headline'], ['this is a test headline', 'final test'], ['a terrible disgusting testing test', 'i hate it', 'i love it', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'i dont know but in my opinion this might be a fake headline', 'another test but not the other test'], ['this is a great fake headline', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'this fake headline is really bad i think']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2021, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        test_data_processor = DataProcessor(path_to_dir=f'{self.temp_within_current_dir}', cols=['headline', 'date', 'url', 'source'], selector= "*.csv")
        undertest_class = SentimentAnalyser(test_data_processor, source_name="test", save_path=f'{self.temp_within_current_dir}')

        x_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        y_data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

        test_df = pd.DataFrame({'x': x_data, 'y': y_data})
        fig = px.line(test_df, x='x', y='y', title="Test Line Graph")

        # when - we call the save as json method passing in the json data, then load the data back in from the file
        test_file_name = "test_json_save"
        undertest_class.save_as_json(fig, test_file_name)

        test_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/{test_file_name}.json')
        with open(test_file_path) as f:
            file_data = json.load(f)

        # then - the json file created has the same data that was passed in
        actual_file_data_x = file_data["data"][0]["x"]
        expected_file_data_x = x_data

        self.assertListEqual(actual_file_data_x, expected_file_data_x)
        
    # teardown after all tests run to delete temporary files used in tests
    @classmethod
    def tearDownClass(self):
        try:
            shutil.rmtree(self.temp_within_current_dir)
        except OSError as error:
            print(f'An error occured while trying to delete directory: {error.filename} - {error.strerror}.')

if __name__ == "__main__":
    unittest.main()