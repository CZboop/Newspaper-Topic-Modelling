import unittest, pytest
from pathlib import Path
import sys
sys.path.append(f"{Path(__file__).parent.parent}")
import src
from src.multi_source_sentiments import MultiSourceSentiments
import datetime
import os
import glob
from pathlib import Path
import pandas as pd
import shutil

# testing the multi source sentiment analyser class
# NOTE: mostly organising the methods from the sentiment analyser class that are tested separately
class TestMultiSourceSentiments(unittest.TestCase):

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

    def test_getting_sentiment_info_for_single_source_with_source_sent_method_returns_polarity_over_time(self):
        # given - an instance of the multi source sentiment getter class and data for a news source
        headline_list_of_lists = [['testing software'], ['writing fake headlines', 'headlines produced'], ['journalism involves writing headlines as well as articles', 'unit testing', 'integration testing', 'spies are a part of software testing', 'headlines are often written by people', 'there are several popular code editors', 'code editors often have optional extensions'], ['an example of a code editor is the one being used now', 'colour schemes can help convey information', 'colour wheels are a tool used in producing colour schemes', 'some color schemes are more universal than others'], ['questions often end with a question mark in english', 'the combination of a question mark and an exclamation mark is a way of indicating shocked confusion', 'heavy use of question marks can make text seem more informal', 'musical scales can be minor or major', 'arpeggios are a musical device that produce effects similar to a chord', 'chord progressions are a central part of producing music'],['Shakespeare died on his birthday'], ['Shakespeare had seven siblings', 'Shakespeare had his own family coat of arms'], ['Shakespeare put a curse on his grave', 'Space is completely silent', 'Nobody knows how many stars are in space', 'Halleys Comet won’t orbit past Earth again until 2061', 'If two pieces of the same type of metal touch in space they will permanently bond', 'The Moon was once a piece of the Earth', 'Alan Turing is the father of modern computer science'], ['Alan Turing played a key role in winning World War II', 'Alan Turing tried out for the Olympics', 'In the UK, there is now a law named after Alan Turing', 'Alan Turing created the first computer chess program'], ['Alan Turing cracked the Enigma code that made Britain win World War II', 'Half the world is bilingual', 'Sumerian is the oldest written language dating back to 3500 BC', 'Almost all languages in the world have been influenced by another language', 'A language dies out if there is no one to speak it, or record using written variations', 'There is no official language in the US']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2019, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2019, 9, 17), datetime.date(2019, 5, 26), datetime.date(2019, 1, 3), datetime.date(2019, 4, 8), datetime.date(2019, 6, 17), datetime.date(2019, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2019, 4, 8), datetime.date(2019, 7, 9), datetime.date(2019, 4, 18), datetime.date(2019, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2019, 5, 25), datetime.date(2019, 9, 8), datetime.date(2019, 9, 25), datetime.date(2019, 8, 15), datetime.date(2019, 3, 10)],[datetime.date(2019, 12, 1)], [datetime.date(2019, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2019, 9, 17), datetime.date(2019, 5, 26), datetime.date(2019, 1, 3), datetime.date(2019, 4, 8), datetime.date(2019, 6, 17), datetime.date(2019, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2019, 4, 8), datetime.date(2019, 7, 9), datetime.date(2019, 4, 18), datetime.date(2019, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2019, 5, 25), datetime.date(2019, 9, 8), datetime.date(2019, 9, 25), datetime.date(2019, 8, 15), datetime.date(2019, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        undertest_class = MultiSourceSentiments(selectors = {'test0' : {'selector': 'test0*.csv'}, 'test1' : {'selector': 'test1*.csv'}, 'test2' : {'selector': 'test2*.csv'}, 'test3' : {'selector': 'test3*.csv'}, 'test4' : {'selector': 'test4*.csv'}}, data_path = f'{self.temp_within_current_dir}', save_path = f'{self.temp_within_current_dir}', start_date = datetime.date(2019, 1, 1), end_date = datetime.date(2019, 12, 31))

        # when - we call internal _source_sent method passing in a specific source
        polarity_over_time, polarity_ratio, subjectivity_over_time = undertest_class._source_sent(name = 'test3', selector = {'selector': 'test3*.csv'})

        expected_keys = [datetime.date(2019, 12, 31), datetime.date(2019, 11, 30), datetime.date(2019, 10, 31), datetime.date(2019, 9, 30), datetime.date(2019, 8, 31), datetime.date(2019, 7, 31), datetime.date(2019, 6, 30), datetime.date(2019, 5, 31), datetime.date(2019, 4, 30), datetime.date(2019, 3, 31), datetime.date(2019, 2, 28),  datetime.date(2019, 1, 31)]

        # then - the polarity over time is returned with an entry for every month in range
        self.assertListEqual(list(i.replace(day=1) for i in polarity_over_time.keys()) , [i.replace(day=1) for i in expected_keys])

    def test_getting_sentiment_info_for_single_source_with_source_sent_method_returns_polarity_ratio(self):
        # given - an instance of the multi source sentiment getter class and data for a news source
        headline_list_of_lists = [['testing software'], ['writing fake headlines', 'headlines produced'], ['journalism involves writing headlines as well as articles', 'unit testing', 'integration testing', 'spies are a part of software testing', 'headlines are often written by people', 'there are several popular code editors', 'code editors often have optional extensions'], ['an example of a code editor is the one being used now', 'colour schemes can help convey information', 'colour wheels are a tool used in producing colour schemes', 'some color schemes are more universal than others'], ['questions often end with a question mark in english', 'the combination of a question mark and an exclamation mark is a way of indicating shocked confusion', 'heavy use of question marks can make text seem more informal', 'musical scales can be minor or major', 'arpeggios are a musical device that produce effects similar to a chord', 'chord progressions are a central part of producing music'],['Shakespeare died on his birthday'], ['Shakespeare had seven siblings', 'Shakespeare had his own family coat of arms'], ['Shakespeare put a curse on his grave', 'Space is completely silent', 'Nobody knows how many stars are in space', 'Halleys Comet won’t orbit past Earth again until 2061', 'If two pieces of the same type of metal touch in space they will permanently bond', 'The Moon was once a piece of the Earth', 'Alan Turing is the father of modern computer science'], ['Alan Turing played a key role in winning World War II', 'Alan Turing tried out for the Olympics', 'In the UK, there is now a law named after Alan Turing', 'Alan Turing created the first computer chess program'], ['Alan Turing cracked the Enigma code that made Britain win World War II', 'Half the world is bilingual', 'Sumerian is the oldest written language dating back to 3500 BC', 'Almost all languages in the world have been influenced by another language', 'A language dies out if there is no one to speak it, or record using written variations', 'There is no official language in the US']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2019, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2019, 9, 17), datetime.date(2019, 5, 26), datetime.date(2019, 1, 3), datetime.date(2019, 4, 8), datetime.date(2019, 6, 17), datetime.date(2019, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2019, 4, 8), datetime.date(2019, 7, 9), datetime.date(2019, 4, 18), datetime.date(2019, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2019, 5, 25), datetime.date(2019, 9, 8), datetime.date(2019, 9, 25), datetime.date(2019, 8, 15), datetime.date(2019, 3, 10)],[datetime.date(2019, 12, 1)], [datetime.date(2019, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2019, 9, 17), datetime.date(2019, 5, 26), datetime.date(2019, 1, 3), datetime.date(2019, 4, 8), datetime.date(2019, 6, 17), datetime.date(2019, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2019, 4, 8), datetime.date(2019, 7, 9), datetime.date(2019, 4, 18), datetime.date(2019, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2019, 5, 25), datetime.date(2019, 9, 8), datetime.date(2019, 9, 25), datetime.date(2019, 8, 15), datetime.date(2019, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        undertest_class = MultiSourceSentiments(selectors = {'test0' : {'selector': 'test0*.csv'}, 'test1' : {'selector': 'test1*.csv'}, 'test2' : {'selector': 'test2*.csv'}, 'test3' : {'selector': 'test3*.csv'}, 'test4' : {'selector': 'test4*.csv'}}, data_path = f'{self.temp_within_current_dir}', save_path = f'{self.temp_within_current_dir}', start_date = datetime.date(2019, 1, 1), end_date = datetime.date(2019, 12, 31))

        # when - we call internal _source_sent method passing in a specific source
        polarity_over_time, polarity_ratio, subjectivity_over_time = undertest_class._source_sent(name = 'test3', selector = {'selector': 'test3*.csv'})
        expected_polarity_ratio_keys = ['positive', 'negative', 'neutral']

        # then - the polarity ratio is returned as a dict with expected keys
        self.assertListEqual(list(polarity_ratio.keys()), expected_polarity_ratio_keys)

    def test_getting_sentiment_info_for_single_source_with_source_sent_method_returns_subjectivity_over_time(self):
        # given - an instance of the multi source sentiment getter class and data for a news source
        headline_list_of_lists = [['testing software'], ['writing fake headlines', 'headlines produced'], ['journalism involves writing headlines as well as articles', 'unit testing', 'integration testing', 'spies are a part of software testing', 'headlines are often written by people', 'there are several popular code editors', 'code editors often have optional extensions'], ['an example of a code editor is the one being used now', 'colour schemes can help convey information', 'colour wheels are a tool used in producing colour schemes', 'some color schemes are more universal than others'], ['questions often end with a question mark in english', 'the combination of a question mark and an exclamation mark is a way of indicating shocked confusion', 'heavy use of question marks can make text seem more informal', 'musical scales can be minor or major', 'arpeggios are a musical device that produce effects similar to a chord', 'chord progressions are a central part of producing music'],['Shakespeare died on his birthday'], ['Shakespeare had seven siblings', 'Shakespeare had his own family coat of arms'], ['Shakespeare put a curse on his grave', 'Space is completely silent', 'Nobody knows how many stars are in space', 'Halleys Comet won’t orbit past Earth again until 2061', 'If two pieces of the same type of metal touch in space they will permanently bond', 'The Moon was once a piece of the Earth', 'Alan Turing is the father of modern computer science'], ['Alan Turing played a key role in winning World War II', 'Alan Turing tried out for the Olympics', 'In the UK, there is now a law named after Alan Turing', 'Alan Turing created the first computer chess program'], ['Alan Turing cracked the Enigma code that made Britain win World War II', 'Half the world is bilingual', 'Sumerian is the oldest written language dating back to 3500 BC', 'Almost all languages in the world have been influenced by another language', 'A language dies out if there is no one to speak it, or record using written variations', 'There is no official language in the US']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2019, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2019, 9, 17), datetime.date(2019, 5, 26), datetime.date(2019, 1, 3), datetime.date(2019, 4, 8), datetime.date(2019, 6, 17), datetime.date(2019, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2019, 4, 8), datetime.date(2019, 7, 9), datetime.date(2019, 4, 18), datetime.date(2019, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2019, 5, 25), datetime.date(2019, 9, 8), datetime.date(2019, 9, 25), datetime.date(2019, 8, 15), datetime.date(2019, 3, 10)],[datetime.date(2019, 12, 1)], [datetime.date(2019, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2019, 9, 17), datetime.date(2019, 5, 26), datetime.date(2019, 1, 3), datetime.date(2019, 4, 8), datetime.date(2019, 6, 17), datetime.date(2019, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2019, 4, 8), datetime.date(2019, 7, 9), datetime.date(2019, 4, 18), datetime.date(2019, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2019, 5, 25), datetime.date(2019, 9, 8), datetime.date(2019, 9, 25), datetime.date(2019, 8, 15), datetime.date(2019, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        undertest_class = MultiSourceSentiments(selectors = {'test0' : {'selector': 'test0*.csv'}, 'test1' : {'selector': 'test1*.csv'}, 'test2' : {'selector': 'test2*.csv'}, 'test3' : {'selector': 'test3*.csv'}, 'test4' : {'selector': 'test4*.csv'}}, data_path = f'{self.temp_within_current_dir}', save_path = f'{self.temp_within_current_dir}', start_date = datetime.date(2019, 1, 1), end_date = datetime.date(2019, 12, 31))

        # when - we call internal _source_sent method passing in a specific source
        polarity_over_time, polarity_ratio, subjectivity_over_time = undertest_class._source_sent(name = 'test3', selector = {'selector': 'test3*.csv'})

        expected_keys = [datetime.date(2019, 12, 31), datetime.date(2019, 11, 30), datetime.date(2019, 10, 31), datetime.date(2019, 9, 30), datetime.date(2019, 8, 31), datetime.date(2019, 7, 31), datetime.date(2019, 6, 30), datetime.date(2019, 5, 31), datetime.date(2019, 4, 30), datetime.date(2019, 3, 31), datetime.date(2019, 2, 28),  datetime.date(2019, 1, 31)]

        # then - subjectivity over time is returned
        print(subjectivity_over_time, expected_keys)
        self.assertListEqual(list(i.replace(day=1) for i in subjectivity_over_time.keys()) , [i.replace(day=1) for i in expected_keys])

    def test_run_method_with_multiple_sources_creates_polarity_over_time_files_for_all_sources(self):
        # given - an instance of the multi source sentiment getter class and data for multiple news sources
        headline_list_of_lists = [['testing software'], ['writing fake headlines', 'headlines produced'], ['journalism involves writing headlines as well as articles', 'unit testing', 'integration testing', 'spies are a part of software testing', 'headlines are often written by people', 'there are several popular code editors', 'code editors often have optional extensions'], ['an example of a code editor is the one being used now', 'colour schemes can help convey information', 'colour wheels are a tool used in producing colour schemes', 'some color schemes are more universal than others'], ['questions often end with a question mark in english', 'the combination of a question mark and an exclamation mark is a way of indicating shocked confusion', 'heavy use of question marks can make text seem more informal', 'musical scales can be minor or major', 'arpeggios are a musical device that produce effects similar to a chord', 'chord progressions are a central part of producing music'],['Shakespeare died on his birthday'], ['Shakespeare had seven siblings', 'Shakespeare had his own family coat of arms'], ['Shakespeare put a curse on his grave', 'Space is completely silent', 'Nobody knows how many stars are in space', 'Halleys Comet won’t orbit past Earth again until 2061', 'If two pieces of the same type of metal touch in space they will permanently bond', 'The Moon was once a piece of the Earth', 'Alan Turing is the father of modern computer science'], ['Alan Turing played a key role in winning World War II', 'Alan Turing tried out for the Olympics', 'In the UK, there is now a law named after Alan Turing', 'Alan Turing created the first computer chess program'], ['Alan Turing cracked the Enigma code that made Britain win World War II', 'Half the world is bilingual', 'Sumerian is the oldest written language dating back to 3500 BC', 'Almost all languages in the world have been influenced by another language', 'A language dies out if there is no one to speak it, or record using written variations', 'There is no official language in the US']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2019, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2019, 9, 17), datetime.date(2019, 5, 26), datetime.date(2019, 1, 3), datetime.date(2019, 4, 8), datetime.date(2019, 6, 17), datetime.date(2019, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2019, 4, 8), datetime.date(2019, 7, 9), datetime.date(2019, 4, 18), datetime.date(2019, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2019, 5, 25), datetime.date(2019, 9, 8), datetime.date(2019, 9, 25), datetime.date(2019, 8, 15), datetime.date(2019, 3, 10)],[datetime.date(2019, 12, 1)], [datetime.date(2019, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2019, 9, 17), datetime.date(2019, 5, 26), datetime.date(2019, 1, 3), datetime.date(2019, 4, 8), datetime.date(2019, 6, 17), datetime.date(2019, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2019, 4, 8), datetime.date(2019, 7, 9), datetime.date(2019, 4, 18), datetime.date(2019, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2019, 5, 25), datetime.date(2019, 9, 8), datetime.date(2019, 9, 25), datetime.date(2019, 8, 15), datetime.date(2019, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        undertest_class = MultiSourceSentiments(selectors = {'test0' : {'selector': 'test0*.csv'}, 'test1' : {'selector': 'test1*.csv'}, 'test2' : {'selector': 'test2*.csv'}, 'test3' : {'selector': 'test3*.csv'}, 'test4' : {'selector': 'test4*.csv'}}, data_path = f'{self.temp_within_current_dir}', save_path = f'{self.temp_within_current_dir}', start_date = datetime.date(2019, 1, 1), end_date = datetime.date(2019, 12, 31))

        # when - we call the run method
        undertest_class.run()

        # then - a polarity over time file is created for each source
        test0_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test0_subjectivity_over_time.json')
        test1_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test1_subjectivity_over_time.json')
        test2_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test2_subjectivity_over_time.json')
        test3_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test3_subjectivity_over_time.json')
        test4_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test4_subjectivity_over_time.json')

        self.assertTrue(test0_file_path.is_file())
        self.assertTrue(test1_file_path.is_file())
        self.assertTrue(test2_file_path.is_file())
        self.assertTrue(test3_file_path.is_file())
        self.assertTrue(test4_file_path.is_file())

    def test_run_method_with_multiple_sources_creates_polarity_ratio_files_for_all_sources(self):
        # given - an instance of the multi source sentiment getter class and data for multiple news sources
        headline_list_of_lists = [['testing software'], ['writing fake headlines', 'headlines produced'], ['journalism involves writing headlines as well as articles', 'unit testing', 'integration testing', 'spies are a part of software testing', 'headlines are often written by people', 'there are several popular code editors', 'code editors often have optional extensions'], ['an example of a code editor is the one being used now', 'colour schemes can help convey information', 'colour wheels are a tool used in producing colour schemes', 'some color schemes are more universal than others'], ['questions often end with a question mark in english', 'the combination of a question mark and an exclamation mark is a way of indicating shocked confusion', 'heavy use of question marks can make text seem more informal', 'musical scales can be minor or major', 'arpeggios are a musical device that produce effects similar to a chord', 'chord progressions are a central part of producing music'],['Shakespeare died on his birthday'], ['Shakespeare had seven siblings', 'Shakespeare had his own family coat of arms'], ['Shakespeare put a curse on his grave', 'Space is completely silent', 'Nobody knows how many stars are in space', 'Halleys Comet won’t orbit past Earth again until 2061', 'If two pieces of the same type of metal touch in space they will permanently bond', 'The Moon was once a piece of the Earth', 'Alan Turing is the father of modern computer science'], ['Alan Turing played a key role in winning World War II', 'Alan Turing tried out for the Olympics', 'In the UK, there is now a law named after Alan Turing', 'Alan Turing created the first computer chess program'], ['Alan Turing cracked the Enigma code that made Britain win World War II', 'Half the world is bilingual', 'Sumerian is the oldest written language dating back to 3500 BC', 'Almost all languages in the world have been influenced by another language', 'A language dies out if there is no one to speak it, or record using written variations', 'There is no official language in the US']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2019, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2019, 9, 17), datetime.date(2019, 5, 26), datetime.date(2019, 1, 3), datetime.date(2019, 4, 8), datetime.date(2019, 6, 17), datetime.date(2019, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2019, 4, 8), datetime.date(2019, 7, 9), datetime.date(2019, 4, 18), datetime.date(2019, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2019, 5, 25), datetime.date(2019, 9, 8), datetime.date(2019, 9, 25), datetime.date(2019, 8, 15), datetime.date(2019, 3, 10)],[datetime.date(2019, 12, 1)], [datetime.date(2019, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2019, 9, 17), datetime.date(2019, 5, 26), datetime.date(2019, 1, 3), datetime.date(2019, 4, 8), datetime.date(2019, 6, 17), datetime.date(2019, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2019, 4, 8), datetime.date(2019, 7, 9), datetime.date(2019, 4, 18), datetime.date(2019, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2019, 5, 25), datetime.date(2019, 9, 8), datetime.date(2019, 9, 25), datetime.date(2019, 8, 15), datetime.date(2019, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        undertest_class = MultiSourceSentiments(selectors = {'test0' : {'selector': 'test0*.csv'}, 'test1' : {'selector': 'test1*.csv'}, 'test2' : {'selector': 'test2*.csv'}, 'test3' : {'selector': 'test3*.csv'}, 'test4' : {'selector': 'test4*.csv'}}, data_path = f'{self.temp_within_current_dir}', save_path = f'{self.temp_within_current_dir}', start_date = datetime.date(2019, 1, 1), end_date = datetime.date(2019, 12, 31))

        # when - we call the run method
        undertest_class.run()

        # then - a polarity ratio file is created for each source
        test0_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test0_polarity_ratio.json')
        test1_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test1_polarity_ratio.json')
        test2_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test2_polarity_ratio.json')
        test3_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test3_polarity_ratio.json')
        test4_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test4_polarity_ratio.json')

        self.assertTrue(test0_file_path.is_file())
        self.assertTrue(test1_file_path.is_file())
        self.assertTrue(test2_file_path.is_file())
        self.assertTrue(test3_file_path.is_file())
        self.assertTrue(test4_file_path.is_file())

    def test_run_method_with_multiple_sources_creates_subjectivity_box_plot_files_for_all_sources(self):
        # given - an instance of the multi source sentiment getter class and data for multiple news sources
        headline_list_of_lists = [['testing software'], ['writing fake headlines', 'headlines produced'], ['journalism involves writing headlines as well as articles', 'unit testing', 'integration testing', 'spies are a part of software testing', 'headlines are often written by people', 'there are several popular code editors', 'code editors often have optional extensions'], ['an example of a code editor is the one being used now', 'colour schemes can help convey information', 'colour wheels are a tool used in producing colour schemes', 'some color schemes are more universal than others'], ['questions often end with a question mark in english', 'the combination of a question mark and an exclamation mark is a way of indicating shocked confusion', 'heavy use of question marks can make text seem more informal', 'musical scales can be minor or major', 'arpeggios are a musical device that produce effects similar to a chord', 'chord progressions are a central part of producing music'],['Shakespeare died on his birthday'], ['Shakespeare had seven siblings', 'Shakespeare had his own family coat of arms'], ['Shakespeare put a curse on his grave', 'Space is completely silent', 'Nobody knows how many stars are in space', 'Halleys Comet won’t orbit past Earth again until 2061', 'If two pieces of the same type of metal touch in space they will permanently bond', 'The Moon was once a piece of the Earth', 'Alan Turing is the father of modern computer science'], ['Alan Turing played a key role in winning World War II', 'Alan Turing tried out for the Olympics', 'In the UK, there is now a law named after Alan Turing', 'Alan Turing created the first computer chess program'], ['Alan Turing cracked the Enigma code that made Britain win World War II', 'Half the world is bilingual', 'Sumerian is the oldest written language dating back to 3500 BC', 'Almost all languages in the world have been influenced by another language', 'A language dies out if there is no one to speak it, or record using written variations', 'There is no official language in the US']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2019, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2019, 9, 17), datetime.date(2019, 5, 26), datetime.date(2019, 1, 3), datetime.date(2019, 4, 8), datetime.date(2019, 6, 17), datetime.date(2019, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2019, 4, 8), datetime.date(2019, 7, 9), datetime.date(2019, 4, 18), datetime.date(2019, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2019, 5, 25), datetime.date(2019, 9, 8), datetime.date(2019, 9, 25), datetime.date(2019, 8, 15), datetime.date(2019, 3, 10)],[datetime.date(2019, 12, 1)], [datetime.date(2019, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2019, 9, 17), datetime.date(2019, 5, 26), datetime.date(2019, 1, 3), datetime.date(2019, 4, 8), datetime.date(2019, 6, 17), datetime.date(2019, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2019, 4, 8), datetime.date(2019, 7, 9), datetime.date(2019, 4, 18), datetime.date(2019, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2019, 5, 25), datetime.date(2019, 9, 8), datetime.date(2019, 9, 25), datetime.date(2019, 8, 15), datetime.date(2019, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        undertest_class = MultiSourceSentiments(selectors = {'test0' : {'selector': 'test0*.csv'}, 'test1' : {'selector': 'test1*.csv'}, 'test2' : {'selector': 'test2*.csv'}, 'test3' : {'selector': 'test3*.csv'}, 'test4' : {'selector': 'test4*.csv'}}, data_path = f'{self.temp_within_current_dir}', save_path = f'{self.temp_within_current_dir}', start_date = datetime.date(2019, 1, 1), end_date = datetime.date(2019, 12, 31))

        # when - we call the run method
        undertest_class.run()

        # then - a subjectivity plot file is created for each source
        test0_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test0_subjectivity_box_plot.json')
        test1_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test1_subjectivity_box_plot.json')
        test2_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test2_subjectivity_box_plot.json')
        test3_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test3_subjectivity_box_plot.json')
        test4_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test4_subjectivity_box_plot.json')

        self.assertTrue(test0_file_path.is_file())
        self.assertTrue(test1_file_path.is_file())
        self.assertTrue(test2_file_path.is_file())
        self.assertTrue(test3_file_path.is_file())
        self.assertTrue(test4_file_path.is_file())

    def test_run_method_with_multiple_sources_creates_subjectivity_over_time_files_for_all_sources(self):
        # given - an instance of the multi source sentiment getter class and data for multiple news sources
        headline_list_of_lists = [['testing software'], ['writing fake headlines', 'headlines produced'], ['journalism involves writing headlines as well as articles', 'unit testing', 'integration testing', 'spies are a part of software testing', 'headlines are often written by people', 'there are several popular code editors', 'code editors often have optional extensions'], ['an example of a code editor is the one being used now', 'colour schemes can help convey information', 'colour wheels are a tool used in producing colour schemes', 'some color schemes are more universal than others'], ['questions often end with a question mark in english', 'the combination of a question mark and an exclamation mark is a way of indicating shocked confusion', 'heavy use of question marks can make text seem more informal', 'musical scales can be minor or major', 'arpeggios are a musical device that produce effects similar to a chord', 'chord progressions are a central part of producing music'],['Shakespeare died on his birthday'], ['Shakespeare had seven siblings', 'Shakespeare had his own family coat of arms'], ['Shakespeare put a curse on his grave', 'Space is completely silent', 'Nobody knows how many stars are in space', 'Halleys Comet won’t orbit past Earth again until 2061', 'If two pieces of the same type of metal touch in space they will permanently bond', 'The Moon was once a piece of the Earth', 'Alan Turing is the father of modern computer science'], ['Alan Turing played a key role in winning World War II', 'Alan Turing tried out for the Olympics', 'In the UK, there is now a law named after Alan Turing', 'Alan Turing created the first computer chess program'], ['Alan Turing cracked the Enigma code that made Britain win World War II', 'Half the world is bilingual', 'Sumerian is the oldest written language dating back to 3500 BC', 'Almost all languages in the world have been influenced by another language', 'A language dies out if there is no one to speak it, or record using written variations', 'There is no official language in the US']]

        date_list_of_lists = [[datetime.date(2019, 12, 1)], [datetime.date(2019, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2019, 9, 17), datetime.date(2019, 5, 26), datetime.date(2019, 1, 3), datetime.date(2019, 4, 8), datetime.date(2019, 6, 17), datetime.date(2019, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2019, 4, 8), datetime.date(2019, 7, 9), datetime.date(2019, 4, 18), datetime.date(2019, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2019, 5, 25), datetime.date(2019, 9, 8), datetime.date(2019, 9, 25), datetime.date(2019, 8, 15), datetime.date(2019, 3, 10)],[datetime.date(2019, 12, 1)], [datetime.date(2019, 10, 1), datetime.date(2019, 12, 3)], [datetime.date(2019, 9, 17), datetime.date(2019, 5, 26), datetime.date(2019, 1, 3), datetime.date(2019, 4, 8), datetime.date(2019, 6, 17), datetime.date(2019, 3, 20), datetime.date(2019, 12, 1)], [datetime.date(2019, 4, 8), datetime.date(2019, 7, 9), datetime.date(2019, 4, 18), datetime.date(2019, 11, 30)], [datetime.date(2019, 12, 30), datetime.date(2019, 5, 25), datetime.date(2019, 9, 8), datetime.date(2019, 9, 25), datetime.date(2019, 8, 15), datetime.date(2019, 3, 10)]]

        for i in range(5):
            test_dataframe = pd.DataFrame(data= {'headline' : headline_list_of_lists[i], 'date' : date_list_of_lists[i], 'url' : ['www.test-url.com/123'] * len(headline_list_of_lists[i]), 'source' : [f'test{i}'] * len(headline_list_of_lists[i])})
            self.setup_write_test_csv_file(test_dataframe, f'test{i}_1.csv')

        undertest_class = MultiSourceSentiments(selectors = {'test0' : {'selector': 'test0*.csv'}, 'test1' : {'selector': 'test1*.csv'}, 'test2' : {'selector': 'test2*.csv'}, 'test3' : {'selector': 'test3*.csv'}, 'test4' : {'selector': 'test4*.csv'}}, data_path = f'{self.temp_within_current_dir}', save_path = f'{self.temp_within_current_dir}', start_date = datetime.date(2019, 1, 1), end_date = datetime.date(2019, 12, 31))

        # when - we call the run method
        undertest_class.run()

        # then - a subjectivity over time file is created for each source
        test0_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test0_subjectivity_over_time.json')
        test1_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test1_subjectivity_over_time.json')
        test2_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test2_subjectivity_over_time.json')
        test3_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test3_subjectivity_over_time.json')
        test4_file_path = Path(f'{Path(__file__).parent}/{self.test_dir_name}/plots/test4_subjectivity_over_time.json')

        self.assertTrue(test0_file_path.is_file())
        self.assertTrue(test1_file_path.is_file())
        self.assertTrue(test2_file_path.is_file())
        self.assertTrue(test3_file_path.is_file())
        self.assertTrue(test4_file_path.is_file())

    # teardown after all tests run to delete temporary files used in tests
    @classmethod
    def tearDownClass(self):
        try:
            shutil.rmtree(self.temp_within_current_dir)
        except OSError as error:
            print(f'An error occured while trying to delete directory: {error.filename} - {error.strerror}.')

if __name__ == "__main__":
    unittest.main()