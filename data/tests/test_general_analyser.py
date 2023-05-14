import unittest, pytest
from pathlib import Path
import sys
sys.path.append(f"{Path(__file__).parent.parent}")
import src
from src.general_analyser import GeneralAnalyser
from src.data_processor import DataProcessor
import os
import glob
from pathlib import Path
import pandas as pd
import datetime
import shutil
from itertools import chain
import plotly
import json

class TestGeneralAnalyser(unittest.TestCase):

    maxDiff = None

    # setup before the test suite run
    @classmethod
    def setUpClass(self):
        # create temp directory for files with test data
        self.test_dir_name = 'temp_test_files'
        self.temp_within_current_dir = f'{Path(__file__).parent}/{self.test_dir_name}'
        Path(self.temp_within_current_dir).mkdir(parents=True, exist_ok=True)

        # also for this class, writing to existing relative path for plots so will create that too
        self.temp_plot_path_parent = f'{self.temp_within_current_dir}/plots'
        Path(self.temp_plot_path_parent).mkdir(parents=True, exist_ok=True)

    def setup_write_test_csv_file(self, dataframe, name):
        dataframe.to_csv(f'{self.temp_within_current_dir}/{name}')

    def test_compare_ratio_of_docs_returns_correct_total_number_of_docs(self):
        # given - an instance of the undertest class, with multiple sources' data with different numbers of headlines
        headline_list_of_lists = [['testingtesting'], ['this is a test headline', 'final test'], ['testing test', 'test of the other test', 'testing testing 123', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'a different test', 'another test but not the other test'], ['testing', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'another version of a test']]
        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')
        
        undertest_class = GeneralAnalyser(data_selectors = {'test0' : {'selector': 'test0_*.csv'}, 'test1' : {'selector': 'test1_*.csv'}, 
        'test2': {'selector':'test2_*.csv'}, 'test3' : {'selector': 'test3_*.csv'}, 'test4' : {'selector': 'test4_*.csv'}}, path_to_data=f'./{self.test_dir_name}', path_to_save=f'./{self.test_dir_name}')

        # when - the compare ratio of docs method is called
        actual_all_records, actual_record_numbers, actual_record_percentages = undertest_class.compare_ratio_of_docs()

        # then - total number of records matches the total passed into the class
        expected_all_records = len(list(chain.from_iterable(headline_list_of_lists)))
        self.assertEqual(actual_all_records, expected_all_records)

    def test_compare_ratio_of_docs_returns_correct_number_of_docs_per_source(self):
        # given - an instance of the undertest class, with multiple sources' data with different numbers of headlines
        headline_list_of_lists = [['testingtesting'], ['this is a test headline', 'final test'], ['testing test', 'test of the other test', 'testing testing 123', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'a different test', 'another test but not the other test'], ['testing', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'another version of a test']]
        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')
        
        undertest_class = GeneralAnalyser(data_selectors = {'test0' : {'selector': 'test0_*.csv'}, 'test1' : {'selector': 'test1_*.csv'}, 
        'test2': {'selector':'test2_*.csv'}, 'test3' : {'selector': 'test3_*.csv'}, 'test4' : {'selector': 'test4_*.csv'}}, path_to_data=f'./{self.test_dir_name}', path_to_save=f'./{self.test_dir_name}')

        # when - the compare ratio of docs method is called
        actual_all_records, actual_record_numbers, actual_record_percentages = undertest_class.compare_ratio_of_docs()

        # then - number of records per source matches the numbers passed into the class
        expected_record_numbers = {'Test0' : 1, 'Test1' : 2, 'Test2' : 7, 'Test3' : 4, 'Test4' : 6}

        self.assertEqual(actual_record_numbers, expected_record_numbers)
    
    def test_compare_ratio_of_docs_returns_correct_percentage_of_docs_per_source(self):
        # given - an instance of the undertest class, with multiple sources' data with different numbers of headlines
        headline_list_of_lists = [['testingtesting'], ['this is a test headline', 'final test'], ['testing test', 'test of the other test', 'testing testing 123', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'a different test', 'another test but not the other test'], ['testing', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'another version of a test']]
        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')
        
        undertest_class = GeneralAnalyser(data_selectors = {'test0' : {'selector': 'test0_*.csv'}, 'test1' : {'selector': 'test1_*.csv'}, 
        'test2': {'selector':'test2_*.csv'}, 'test3' : {'selector': 'test3_*.csv'}, 'test4' : {'selector': 'test4_*.csv'}}, path_to_data=f'./{self.test_dir_name}', path_to_save=f'./{self.test_dir_name}')

        # when - the compare ratio of docs method is called
        actual_all_records, actual_record_numbers, actual_record_percentages = undertest_class.compare_ratio_of_docs()

        # then - the percentages per source returned match the numbers passed into the class
        # in total there are 20 records so %age should be x5 the number
        expected_record_percentages = {'Test0' : 5, 'Test1' : 10, 'Test2' : 35, 'Test3' : 20, 'Test4' : 30}

        self.assertEqual(actual_record_percentages, expected_record_percentages)
    
    def test_compare_ratio_of_docs_returns_percentages_that_total_100(self):
        # given - an instance of the undertest class, with multiple sources' data with different numbers of headlines
        headline_list_of_lists = [['testingtesting'], ['this is a test headline', 'final test'], ['testing test', 'test of the other test', 'testing testing 123', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'a different test', 'another test but not the other test'], ['testing', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'another version of a test']]
        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')
        
        undertest_class = GeneralAnalyser(data_selectors = {'test0' : {'selector': 'test0_*.csv'}, 'test1' : {'selector': 'test1_*.csv'}, 
        'test2': {'selector':'test2_*.csv'}, 'test3' : {'selector': 'test3_*.csv'}, 'test4' : {'selector': 'test4_*.csv'}}, path_to_data=f'./{self.test_dir_name}', path_to_save=f'./{self.test_dir_name}')

        # when - the compare ratio of docs method is called
        actual_all_records, actual_record_numbers, actual_record_percentages = undertest_class.compare_ratio_of_docs()

        # then - total percentages across sources is 100
        self.assertEqual(sum(actual_record_percentages.values()), 100)

    def test_visualise_percentages_returns_a_plotly_figure(self):
        # given - a general analyser passed some data from different sources
        headline_list_of_lists = [['testingtesting'], ['this is a test headline', 'final test'], ['testing test', 'test of the other test', 'testing testing 123', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'a different test', 'another test but not the other test'], ['testing', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'another version of a test']]
        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')
        
        undertest_class = GeneralAnalyser(data_selectors = {'test0' : {'selector': 'test0_*.csv'}, 'test1' : {'selector': 'test1_*.csv'}, 
        'test2': {'selector':'test2_*.csv'}, 'test3' : {'selector': 'test3_*.csv'}, 'test4' : {'selector': 'test4_*.csv'}}, path_to_data=f'./{self.test_dir_name}', path_to_save=f'./{self.test_dir_name}')

        # when - we pass the resulting percentages into a call to the visualise percentages method (%ages from the compare ratios method)
        actual_all_records, actual_record_numbers, actual_record_percentages = undertest_class.compare_ratio_of_docs()
        actual_pie = undertest_class.visualise_percentages(actual_record_percentages)

        # then - an instance of a plotly figure is produced
        self.assertTrue(isinstance(actual_pie, plotly.graph_objects.Figure))

    def test_visualise_percentages_returns_a_figure_with_correct_data(self):
        # given - a general analyser passed some data from different sources
        headline_list_of_lists = [['testingtesting'], ['this is a test headline', 'final test'], ['testing test', 'test of the other test', 'testing testing 123', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'a different test', 'another test but not the other test'], ['testing', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'another version of a test']]
        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')
        
        undertest_class = GeneralAnalyser(data_selectors = {'test0' : {'selector': 'test0_*.csv'}, 'test1' : {'selector': 'test1_*.csv'}, 
        'test2': {'selector':'test2_*.csv'}, 'test3' : {'selector': 'test3_*.csv'}, 'test4' : {'selector': 'test4_*.csv'}}, path_to_data=f'./{self.test_dir_name}', path_to_save=f'./{self.test_dir_name}')

        # when - we pass the resulting percentages into a call to the visualise percentages method (%ages from the compare ratios method)
        actual_all_records, actual_record_numbers, actual_record_percentages = undertest_class.compare_ratio_of_docs()
        actual_pie = undertest_class.visualise_percentages(actual_record_percentages)

        actual_pie_data = list(actual_pie['data'][0]['values'])

        # then - a plotly pie chart is produced with values that matches the percentages calculated per source
        expected_pie_data = list(actual_record_percentages.values())

        self.assertListEqual(actual_pie_data, expected_pie_data)

    def test_save_as_json_creates_expected_file(self):
        # given - an instance of the general analyser and a json friendly plotly figure created by it
        headline_list_of_lists = [['testingtesting'], ['this is a test headline', 'final test'], ['testing test', 'test of the other test', 'testing testing 123', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'a different test', 'another test but not the other test'], ['testing', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'another version of a test']]
        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')
        
        undertest_class = GeneralAnalyser(data_selectors = {'test0' : {'selector': 'test0_*.csv'}, 'test1' : {'selector': 'test1_*.csv'}, 
        'test2': {'selector':'test2_*.csv'}, 'test3' : {'selector': 'test3_*.csv'}, 'test4' : {'selector': 'test4_*.csv'}}, path_to_data=f'./{self.test_dir_name}', path_to_save=f'./{self.test_dir_name}')

        # when - we call the save as json method passing in the figure and a file name
        actual_all_records, actual_record_numbers, actual_record_percentages = undertest_class.compare_ratio_of_docs()
        actual_pie = undertest_class.visualise_percentages(actual_record_percentages)
        test_file_name = 'test_json_save'
        undertest_class.save_as_json(actual_pie, test_file_name)

        # then - a json file containing the data of the figure is save in the expected place with expected name
        test_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/{test_file_name}.json')
        self.assertTrue(test_file_path.is_file())

    def test_compare_number_of_docs_over_time_gives_correct_total_over_time(self):
        # given - data with dates passed into an instance of general analyser class
        headline_list_of_lists = [['testingtesting'], ['this is a test headline', 'final test'], ['testing test', 'test of the other test', 'testing testing 123', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'a different test', 'another test but not the other test'], ['testing', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'another version of a test']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2020, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')
        
        undertest_class = GeneralAnalyser(data_selectors = {'test0' : {'selector': 'test0_*.csv'}, 'test1' : {'selector': 'test1_*.csv'}, 
        'test2': {'selector':'test2_*.csv'}, 'test3' : {'selector': 'test3_*.csv'}, 'test4' : {'selector': 'test4_*.csv'}}, path_to_data=f'./{self.test_dir_name}', path_to_save=f'./{self.test_dir_name}')

        # when - we call the compare number of docs over time method
        actual_per_source , actual_total = undertest_class.compare_num_of_docs_over_time()

        # then - two collections are returned with the docs over time for each source and overall
        # total will be object with keys of datetime start of month with value of int how many docs in that month
        expected_total = {datetime.date(2019, 12, 1): 4, datetime.date(2020, 1, 1): 0, datetime.date(2020, 2, 1): 0, datetime.date(2020, 3, 1): 1, datetime.date(2020, 4, 1) : 2, datetime.date(2020, 5, 1) : 1, datetime.date(2020, 6, 1) : 1, datetime.date(2020, 7, 1) : 0, datetime.date(2020, 8, 1) : 1, datetime.date(2020, 9, 1) : 1, datetime.date(2020, 10, 1) : 0, datetime.date(2020, 11, 1) : 0, datetime.date(2020, 12, 1): 0, datetime.date(2021, 1, 1): 0, datetime.date(2021, 2, 1): 0, datetime.date(2021, 3, 1): 1, datetime.date(2021, 4, 1) : 1, datetime.date(2021, 5, 1) : 1, datetime.date(2021, 6, 1) : 0, datetime.date(2021, 7, 1) : 0, datetime.date(2021, 8, 1) : 0, datetime.date(2021, 9, 1) : 0, datetime.date(2021, 10, 1) : 1, datetime.date(2021, 11, 1) : 1, datetime.date(2021, 12, 1): 0, datetime.date(2022, 1, 1): 0, datetime.date(2022, 2, 1): 0, datetime.date(2022, 3, 1): 0, datetime.date(2022, 4, 1) : 0, datetime.date(2022, 5, 1) : 0, datetime.date(2022, 6, 1) : 0, datetime.date(2022, 7, 1) : 1, datetime.date(2022, 8, 1) : 0, datetime.date(2022, 9, 1) : 2, datetime.date(2022, 10, 1) : 0, datetime.date(2022, 11, 1) : 0, datetime.date(2022, 12, 1) : 0, datetime.date(2023, 1, 1) : 1}

        self.assertEqual(actual_total, expected_total)

    def test_compare_number_of_docs_over_time_gives_correct_for_each_source_over_time(self):
        # given - data with dates passed into an instance of general analyser class
        headline_list_of_lists = [['testingtesting'], ['this is a test headline', 'final test'], ['testing test', 'test of the other test', 'testing testing 123', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'a different test', 'another test but not the other test'], ['testing', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'another version of a test']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2020, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')
        
        undertest_class = GeneralAnalyser(data_selectors = {'test0' : {'selector': 'test0_*.csv'}, 'test1' : {'selector': 'test1_*.csv'}, 
        'test2': {'selector':'test2_*.csv'}, 'test3' : {'selector': 'test3_*.csv'}, 'test4' : {'selector': 'test4_*.csv'}}, path_to_data=f'./{self.test_dir_name}', path_to_save=f'./{self.test_dir_name}')

        # when - we call the compare number of docs over time method
        actual_per_source , actual_total = undertest_class.compare_num_of_docs_over_time()

        # then - two collections are returned with the docs over time for each source and overall
        # per source will be list of lists first elem datetime start of month then how many per source in order sources passed in
        expected_per_source = [
            [datetime.date(2019, 12, 1), 1, 1, 1, 0, 1], 
            [datetime.date(2020, 1, 1), 0, 0, 0, 0, 0], 
            [datetime.date(2020, 2, 1), 0, 0, 0, 0, 0], 
            [datetime.date(2020, 3, 1), 0, 0, 0, 0, 1], 
            [datetime.date(2020, 4, 1), 0, 0, 1, 1, 0], 
            [datetime.date(2020, 5, 1), 0, 0, 0, 0, 1], 
            [datetime.date(2020, 6, 1), 0, 0, 1, 0, 0], 
            [datetime.date(2020, 7, 1), 0, 0, 0, 0, 0], 
            [datetime.date(2020, 8, 1), 0, 0, 0, 0, 1], 
            [datetime.date(2020, 9, 1), 0, 0, 0, 0, 1], 
            [datetime.date(2020, 10, 1), 0, 0, 0, 0, 0], 
            [datetime.date(2020, 11, 1), 0, 0, 0, 0, 0], 
            [datetime.date(2020, 12, 1), 0, 0, 0, 0, 0], 
            [datetime.date(2021, 1, 1), 0, 0, 0, 0, 0], 
            [datetime.date(2021, 2, 1), 0, 0, 0, 0, 0], 
            [datetime.date(2021, 3, 1), 0, 0, 1, 0, 0], 
            [datetime.date(2021, 4, 1), 0, 0, 0, 1, 0], 
            [datetime.date(2021, 5, 1), 0, 0, 1, 0, 0], 
            [datetime.date(2021, 6, 1), 0, 0, 0, 0, 0], 
            [datetime.date(2021, 7, 1), 0, 0, 0, 0, 0], 
            [datetime.date(2021, 8, 1), 0, 0, 0, 0, 0], 
            [datetime.date(2021, 9, 1), 0, 0, 0, 0, 0], 
            [datetime.date(2021, 10, 1), 0, 1, 0, 0, 0], 
            [datetime.date(2021, 11, 1), 0, 0, 0, 1, 0], 
            [datetime.date(2021, 12, 1), 0, 0, 0, 0, 0], 
            [datetime.date(2022, 1, 1), 0, 0, 0, 0, 0], 
            [datetime.date(2022, 2, 1), 0, 0, 0, 0, 0], 
            [datetime.date(2022, 3, 1), 0, 0, 0, 0, 0], 
            [datetime.date(2022, 4, 1), 0, 0, 0, 0, 0], 
            [datetime.date(2022, 5, 1), 0, 0, 0, 0, 0], 
            [datetime.date(2022, 6, 1), 0, 0, 0, 0, 0], 
            [datetime.date(2022, 7, 1), 0, 0, 0, 1, 0], 
            [datetime.date(2022, 8, 1), 0, 0, 0, 0, 0], 
            [datetime.date(2022, 9, 1), 0, 0, 1, 0, 1], 
            [datetime.date(2022, 10, 1), 0, 0, 0, 0, 0], 
            [datetime.date(2022, 11, 1), 0, 0, 0, 0, 0], 
            [datetime.date(2022, 12, 1), 0, 0, 0, 0, 0], 
            [datetime.date(2023, 1, 1), 0, 0, 1, 0, 0]
        ]

        self.assertEqual(actual_per_source, expected_per_source)

    def test_visualise_number_over_time_total_creates_a_figure_with_expected_data(self):
        # given - data for multiple sources passed into an instance of the undertest class
        headline_list_of_lists = [['testingtesting'], ['this is a test headline', 'final test'], ['testing test', 'test of the other test', 'testing testing 123', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'a different test', 'another test but not the other test'], ['testing', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'another version of a test']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2020, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')
        
        undertest_class = GeneralAnalyser(data_selectors = {'test0' : {'selector': 'test0_*.csv'}, 'test1' : {'selector': 'test1_*.csv'}, 
        'test2': {'selector':'test2_*.csv'}, 'test3' : {'selector': 'test3_*.csv'}, 'test4' : {'selector': 'test4_*.csv'}}, path_to_data=f'./{self.test_dir_name}', path_to_save=f'./{self.test_dir_name}')

        # when - delete any existing plots, pass the number of docs over time for all sources combined into the visualise number over time method with 'single' flag set to true
        self.delete_temp_dir_contents()

        _ , number_of_docs_over_time_total = undertest_class.compare_num_of_docs_over_time()
        actual_fig = undertest_class.visualise_number_over_time(number_of_docs_over_time_total, single= True, source_name= "test")
        actual_fig_data = list(actual_fig["data"][0]["y"])

        # then - a graph is created with the expected data for each month
        expected_fig_data = [4, 0, 0, 1, 2, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 1]
        
        self.assertListEqual(actual_fig_data, expected_fig_data)

    def test_visualise_number_over_time_total_creates_a_plotly_figure(self):
        # given - data for multiple sources passed into an instance of the undertest class
        headline_list_of_lists = [['testingtesting'], ['this is a test headline', 'final test'], ['testing test', 'test of the other test', 'testing testing 123', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'a different test', 'another test but not the other test'], ['testing', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'another version of a test']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2020, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')
        
        undertest_class = GeneralAnalyser(data_selectors = {'test0' : {'selector': 'test0_*.csv'}, 'test1' : {'selector': 'test1_*.csv'}, 
        'test2': {'selector':'test2_*.csv'}, 'test3' : {'selector': 'test3_*.csv'}, 'test4' : {'selector': 'test4_*.csv'}}, path_to_data=f'./{self.test_dir_name}', path_to_save=f'./{self.test_dir_name}')

        # when - delete any existing plots, pass the number of docs over time for all sources combined into the visualise number over time method with 'single' flag set to true
        self.delete_temp_dir_contents()

        _ , number_of_docs_over_time_total = undertest_class.compare_num_of_docs_over_time()
        actual_fig = undertest_class.visualise_number_over_time(number_of_docs_over_time_total, single= True, source_name= "test")
        actual_fig_data = list(actual_fig["data"][0]["y"])

        # then - a graoh is created which is an instance of the plotly figure class
        expected_fig_data = [4, 0, 0, 1, 2, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 1]
        
        self.assertTrue(isinstance(actual_fig, plotly.graph_objects.Figure))

    def test_visualise_number_over_time_total_creates_the_expected_json_file(self):
        # given - data for multiple sources passed into an instance of the undertest class
        headline_list_of_lists = [['testingtesting'], ['this is a test headline', 'final test'], ['testing test', 'test of the other test', 'testing testing 123', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'a different test', 'another test but not the other test'], ['testing', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'another version of a test']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2020, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')
        
        undertest_class = GeneralAnalyser(data_selectors = {'test0' : {'selector': 'test0_*.csv'}, 'test1' : {'selector': 'test1_*.csv'}, 
        'test2': {'selector':'test2_*.csv'}, 'test3' : {'selector': 'test3_*.csv'}, 'test4' : {'selector': 'test4_*.csv'}}, path_to_data=f'./{self.test_dir_name}', path_to_save=f'./{self.test_dir_name}')

        # when - delete any existing plots, pass the number of docs over time for all sources combined into the visualise number over time method with 'single' flag set to true
        self.delete_temp_dir_contents()

        _ , number_of_docs_over_time_total = undertest_class.compare_num_of_docs_over_time()
        actual_fig = undertest_class.visualise_number_over_time(number_of_docs_over_time_total, single= True, source_name= "test")
        actual_fig_data = list(actual_fig["data"][0]["y"])

        # then - a json file is created with the expected path and name
        expected_fig_data = [4, 0, 0, 1, 2, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 1]

        test_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/articles_over_time_test.json')
        self.assertTrue(test_file_path.is_file())

    def test_visualise_number_over_time_multi_source_has_correct_data_for_each_source(self):
        # given - data for multiple sources passed into an instance of the undertest class
        headline_list_of_lists = [['testingtesting'], ['this is a test headline', 'final test'], ['testing test', 'test of the other test', 'testing testing 123', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'a different test', 'another test but not the other test'], ['testing', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'another version of a test']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2020, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')
        
        undertest_class = GeneralAnalyser(data_selectors = {'test0' : {'selector': 'test0_*.csv'}, 'test1' : {'selector': 'test1_*.csv'}, 
        'test2': {'selector':'test2_*.csv'}, 'test3' : {'selector': 'test3_*.csv'}, 'test4' : {'selector': 'test4_*.csv'}}, path_to_data=f'./{self.test_dir_name}', path_to_save=f'./{self.test_dir_name}')

        # when - delete any existing plots, then pass the number of docs over time for all sources combined into the visualise number over time method with 'single' flag set to false
        self.delete_temp_dir_contents()

        number_of_docs_over_time_sources , _ = undertest_class.compare_num_of_docs_over_time()
        actual_fig = undertest_class.visualise_number_over_time(number_of_docs_over_time_sources, single= False)

        # then - the line graph figure shows the same data passed into it, with y line for each source
        actual_fig_data_source1 = list(actual_fig["data"][0]["y"])
        actual_fig_data_source2 = list(actual_fig["data"][1]["y"])
        actual_fig_data_source3 = list(actual_fig["data"][2]["y"])
        actual_fig_data_source4 = list(actual_fig["data"][3]["y"])
        actual_fig_data_source5 = list(actual_fig["data"][4]["y"])

        expected_fig_data_source1 = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        expected_fig_data_source2 = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        expected_fig_data_source3 = [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1]
        expected_fig_data_source4 = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        expected_fig_data_source5 = [1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]

        self.assertListEqual(actual_fig_data_source1, expected_fig_data_source1)
        self.assertListEqual(actual_fig_data_source2, expected_fig_data_source2)
        self.assertListEqual(actual_fig_data_source3, expected_fig_data_source3)
        self.assertListEqual(actual_fig_data_source4, expected_fig_data_source4)
        self.assertListEqual(actual_fig_data_source5, expected_fig_data_source5)

    def test_visualise_number_over_time_multi_source_creates_plotly_plot(self):
        # given - data for multiple sources passed into an instance of the undertest class
        headline_list_of_lists = [['testingtesting'], ['this is a test headline', 'final test'], ['testing test', 'test of the other test', 'testing testing 123', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'a different test', 'another test but not the other test'], ['testing', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'another version of a test']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2020, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')
        
        undertest_class = GeneralAnalyser(data_selectors = {'test0' : {'selector': 'test0_*.csv'}, 'test1' : {'selector': 'test1_*.csv'}, 
        'test2': {'selector':'test2_*.csv'}, 'test3' : {'selector': 'test3_*.csv'}, 'test4' : {'selector': 'test4_*.csv'}}, path_to_data=f'./{self.test_dir_name}', path_to_save=f'./{self.test_dir_name}')

        # when - delete any existing plots, then pass the number of docs over time for all sources combined into the visualise number over time method with 'single' flag set to false
        self.delete_temp_dir_contents()

        number_of_docs_over_time_sources , _ = undertest_class.compare_num_of_docs_over_time()
        actual_fig = undertest_class.visualise_number_over_time(number_of_docs_over_time_sources, single= False)

        # then - the line graph created is an instance of a plotly figure
        self.assertTrue(isinstance(actual_fig, plotly.graph_objects.Figure))

    def test_visualise_number_over_time_multi_source_creates_expected_json_file(self):
        # given - data for multiple sources passed into an instance of the undertest class
        headline_list_of_lists = [['testingtesting'], ['this is a test headline', 'final test'], ['testing test', 'test of the other test', 'testing testing 123', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'a different test', 'another test but not the other test'], ['testing', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'another version of a test']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2020, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')
        
        undertest_class = GeneralAnalyser(data_selectors = {'test0' : {'selector': 'test0_*.csv'}, 'test1' : {'selector': 'test1_*.csv'}, 
        'test2': {'selector':'test2_*.csv'}, 'test3' : {'selector': 'test3_*.csv'}, 'test4' : {'selector': 'test4_*.csv'}}, path_to_data=f'./{self.test_dir_name}', path_to_save=f'./{self.test_dir_name}')

        # when - delete any existing plots, then pass the number of docs over time for all sources combined into the visualise number over time method with 'single' flag set to false
        self.delete_temp_dir_contents()

        number_of_docs_over_time_sources , _ = undertest_class.compare_num_of_docs_over_time()
        actual_fig = undertest_class.visualise_number_over_time(number_of_docs_over_time_sources, single= False)

        # then - a json file is created with the expected path and name
        test_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/articles_over_time.json')
        self.assertTrue(test_file_path.is_file())

    def test_run_creates_all_expected_files(self):
        # given - headline style data and an instance of the undertest general analyser class
        headline_list_of_lists = [['testingtesting'], ['this is a test headline', 'final test'], ['testing test', 'test of the other test', 'testing testing 123', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'a different test', 'another test but not the other test'], ['testing', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'another version of a test']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2020, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')
        
        undertest_class = GeneralAnalyser(data_selectors = {'test0' : {'selector': 'test0_*.csv'}, 'test1' : {'selector': 'test1_*.csv'}, 
        'test2': {'selector':'test2_*.csv'}, 'test3' : {'selector': 'test3_*.csv'}, 'test4' : {'selector': 'test4_*.csv'}}, path_to_data=f'./{self.test_dir_name}', path_to_save=f'./{self.test_dir_name}')

        # when - we delete any existing plot files and then call the run method
        self.delete_temp_dir_contents()
        undertest_class.run()

        # then - three json files are created with the expected path and name
        test_file_path_over_time_all = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/articles_over_time_All Sources.json')
        self.assertTrue(test_file_path_over_time_all.is_file())

        test_file_path_over_time_combined = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/articles_over_time_Combined Sources.json')
        self.assertTrue(test_file_path_over_time_combined.is_file())

        test_file_path_ratios = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/news_source_ratios.json')
        self.assertTrue(test_file_path_ratios.is_file())

    def test_run_creates_file_with_expected_data_for_individual_sources(self):
        # given - headline style data and an instance of the undertest general analyser class
        headline_list_of_lists = [['testingtesting'], ['this is a test headline', 'final test'], ['testing test', 'test of the other test', 'testing testing 123', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'a different test', 'another test but not the other test'], ['testing', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'another version of a test']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2020, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')
        
        undertest_class = GeneralAnalyser(data_selectors = {'test0' : {'selector': 'test0_*.csv'}, 'test1' : {'selector': 'test1_*.csv'}, 
        'test2': {'selector':'test2_*.csv'}, 'test3' : {'selector': 'test3_*.csv'}, 'test4' : {'selector': 'test4_*.csv'}}, path_to_data=f'./{self.test_dir_name}', path_to_save=f'./{self.test_dir_name}')

        # when - we delete any existing plot files, call the run method and load the data from the resulting all sources file
        self.delete_temp_dir_contents()
        undertest_class.run()

        test_file_path_over_time_all = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/articles_over_time_All Sources.json')
        with open(test_file_path_over_time_all) as f:
            over_time_all_data = json.load(f)

        # then - the data from each y axis line from the file has the same percentages of docs from each source as expected
        actual_fig_data_source1 = list(over_time_all_data["data"][0]["y"])
        actual_fig_data_source2 = list(over_time_all_data["data"][1]["y"])
        actual_fig_data_source3 = list(over_time_all_data["data"][2]["y"])
        actual_fig_data_source4 = list(over_time_all_data["data"][3]["y"])
        actual_fig_data_source5 = list(over_time_all_data["data"][4]["y"])

        expected_fig_data_source1 = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        expected_fig_data_source2 = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        expected_fig_data_source3 = [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1]
        expected_fig_data_source4 = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        expected_fig_data_source5 = [1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]

        self.assertListEqual(actual_fig_data_source1, expected_fig_data_source1)
        self.assertListEqual(actual_fig_data_source2, expected_fig_data_source2)
        self.assertListEqual(actual_fig_data_source3, expected_fig_data_source3)
        self.assertListEqual(actual_fig_data_source4, expected_fig_data_source4)
        self.assertListEqual(actual_fig_data_source5, expected_fig_data_source5)

    def test_run_creates_file_with_expected_data_for_combined_sources(self):
        # given - headline style data and an instance of the undertest general analyser class
        headline_list_of_lists = [['testingtesting'], ['this is a test headline', 'final test'], ['testing test', 'test of the other test', 'testing testing 123', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'a different test', 'another test but not the other test'], ['testing', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'another version of a test']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2020, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')
        
        undertest_class = GeneralAnalyser(data_selectors = {'test0' : {'selector': 'test0_*.csv'}, 'test1' : {'selector': 'test1_*.csv'}, 
        'test2': {'selector':'test2_*.csv'}, 'test3' : {'selector': 'test3_*.csv'}, 'test4' : {'selector': 'test4_*.csv'}}, path_to_data=f'./{self.test_dir_name}', path_to_save=f'./{self.test_dir_name}')

        # when - we delete any existing plot files, call the run method and load the data from the resulting combined sources file
        self.delete_temp_dir_contents()
        undertest_class.run()

        test_file_path_over_time_combined = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/articles_over_time_Combined Sources.json')
        with open(test_file_path_over_time_combined) as f:
            over_time_combined_data = json.load(f)

        # then - the data in the file matches the total over time expected
        expected_fig_data = [4, 0, 0, 1, 2, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 1]
        actual_fig_data = list(over_time_combined_data["data"][0]["y"])

        self.assertListEqual(expected_fig_data, actual_fig_data)

    def test_run_creates_file_with_expected_ratios_for_docs_per_source(self):
        # given - headline style data and an instance of the undertest general analyser class
        headline_list_of_lists = [['testingtesting'], ['this is a test headline', 'final test'], ['testing test', 'test of the other test', 'testing testing 123', 'final test but different', 'a test headline', 'another test', 'headline for purpose of test'], ['testing 123', 'test check 12', 'a different test', 'another test but not the other test'], ['testing', 'this is an example of a test headline', 'example of a test', 'final test the final one', 'test of the test', 'another version of a test']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2021, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2022, 9, 17), datetime.date(2021, 5, 26), datetime.date(2023, 1, 3), datetime.date(2020, 4, 8), datetime.date(2020, 6, 17), datetime.date(2021, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2021, 4, 8), datetime.date(2022, 7, 9), datetime.date(2020, 4, 18), datetime.date(2021, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2020, 5, 25), datetime.date(2020, 9, 8), datetime.date(2022, 9, 25), datetime.date(2020, 8, 15), datetime.date(2020, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')
        
        undertest_class = GeneralAnalyser(data_selectors = {'test0' : {'selector': 'test0_*.csv'}, 'test1' : {'selector': 'test1_*.csv'}, 
        'test2': {'selector':'test2_*.csv'}, 'test3' : {'selector': 'test3_*.csv'}, 'test4' : {'selector': 'test4_*.csv'}}, path_to_data=f'./{self.test_dir_name}', path_to_save=f'./{self.test_dir_name}')

        # when - we delete any existing plot files, call the run method and load the data from the resulting ratios file
        self.delete_temp_dir_contents()
        undertest_class.run()

        test_file_path_ratios = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/news_source_ratios.json')
        with open(test_file_path_ratios) as f:
            ratio_data = json.load(f)

        # then - the data in the file matches the total over time expected
        expected_fig_data = [5, 10, 35, 20, 30]
        actual_fig_data = list(ratio_data['data'][0]['values'])

        self.assertListEqual(expected_fig_data, actual_fig_data)
        
    # not deleting directory itself here, for between tests rather than fully in teardown
    def delete_temp_dir_contents(self):
        files_to_delete = glob.glob(f'{self.temp_plot_path_parent}/*')
        for file_ in files_to_delete:
            os.remove(file_)

    @classmethod
    def tearDownClass(self):
        try:
            shutil.rmtree(self.temp_within_current_dir)
        except OSError as error:
            print(f'An error occured while trying to delete directory: {error.filename} - {error.strerror}.')

if __name__ == "__main__":
    unittest.main()